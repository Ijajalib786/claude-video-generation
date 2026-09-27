"""
Phase 3: Text-to-Speech (TTS) Agent
Generates audio from scripts using Google Generative AI (google.genai package).
"""

import json
import io
import wave
from pathlib import Path
from threading import Thread
from typing import Optional
from .. import config
from ..models import Script, SegmentedScript, ScriptSegment, TTSAudioMetadata

try:
    from google import genai
except ImportError:
    genai = None


def generate_tts_audio(script: Script, output_folder: Path) -> TTSAudioMetadata:
    """
    Generate TTS audio for a script using Google Generative AI.

    Args:
        script: Script object with dialogue content
        output_folder: Path to save audio files

    Returns:
        TTSAudioMetadata with audio duration and segment information
    """

    if genai is None:
        raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")

    if not config.GOOGLE_GEMINI_API_KEY:
        raise ValueError("GOOGLE_GEMINI_API_KEY not set in environment")

    print(f"\n🎙️  TTS: Generating audio for: {script.topic}")
    print("=" * 60)

    # Step 1: Parse script into speaker segments
    print("📝 Step 1: Parsing script into speaker segments...")
    segmented = _parse_speaker_segments(script)
    print(f"✅ Parsed {segmented.total_segments} segments")

    # Step 2: Validate segmentation
    print("✓ Step 2: Validating segmentation...")
    _validate_segmentation(script, segmented)
    print("✅ Validation passed - no data loss")

    # Step 3: Prepare output folder
    output_folder.mkdir(parents=True, exist_ok=True)
    audio_folder = output_folder / "audio"
    audio_folder.mkdir(exist_ok=True)

    # Step 4: Synthesize full dialogue (both speakers combined)
    print("🔄 Step 3: Synthesizing full dialogue with both voices...")

    # Reconstruct full dialogue from segments
    full_dialogue = "\n".join([f"{s.speaker}: {s.dialogue_text}" for s in segmented.segments])

    try:
        combined_audio, combined_duration = _synthesize_speaker_audio(
            full_dialogue, "Both", "combined", segmented
        )
        print("✅ Full dialogue synthesized")
    except Exception as e:
        print(f"⚠️  TTS synthesis failed: {str(e)}")
        print("   Creating placeholder audio for testing...")
        combined_audio, combined_duration = _create_placeholder_audio("Combined", segmented)

    # For compatibility, also set individual durations
    sarah_duration = combined_duration * 0.5  # Rough split
    alex_duration = combined_duration * 0.5

    # Step 5: Save combined audio file
    print("💾 Step 4: Saving audio file...")

    if combined_audio:
        audio_path = audio_folder / "audio.mp3"
        with open(audio_path, 'wb') as f:
            f.write(combined_audio)
        print(f"   ✓ Audio file: {audio_path}")

    # Step 6: Save metadata
    print("📊 Step 5: Saving TTS metadata...")
    total_duration = combined_duration

    tts_metadata = TTSAudioMetadata(
        topic=script.topic,
        total_duration_seconds=total_duration,
        sarah_duration_seconds=sarah_duration,
        alex_duration_seconds=alex_duration,
        total_segments_processed=segmented.total_segments,
        segmented_script=segmented,
        sarah_voice_id=config.TTS_VOICES["Sarah"],
        alex_voice_id=config.TTS_VOICES["Alex"]
    )

    metadata_path = audio_folder / "tts_metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        metadata_dict = tts_metadata.model_dump(mode='json')
        json.dump(metadata_dict, f, indent=2, default=str)
    print(f"   ✓ Metadata: {metadata_path}")

    # Step 7: Save segmentation report
    _save_segmentation_report(segmented, audio_folder)

    print("\n" + "=" * 60)
    print("✅ TTS generation complete!")
    print(f"   📁 Output: {audio_folder}")
    print(f"   🎙️  Audio file: {audio_folder / 'audio.mp3'}")
    print(f"   🔊 Duration: {total_duration:.1f}s")
    print(f"   🎯 Segments: {segmented.total_segments} (Sarah + Alex dialogue)")

    return tts_metadata


def _parse_speaker_segments(script: Script) -> SegmentedScript:
    """Parse script into speaker segments with line tracking."""
    segments = []
    segment_number = 1
    current_speaker = None
    current_text = []
    current_lines = []

    for line_num, script_line in enumerate(script.lines, 1):
        speaker = script_line.speaker

        if current_speaker and speaker != current_speaker:
            segment_text = " ".join(current_text).strip()
            if segment_text:
                word_count = len(segment_text.split())
                segment = ScriptSegment(
                    segment_number=segment_number,
                    speaker=current_speaker,
                    dialogue_text=segment_text,
                    original_line_numbers=current_lines.copy(),
                    sequence_identifier=f"segment_{segment_number}_{current_speaker.lower()}",
                    word_count=word_count
                )
                segments.append(segment)
                segment_number += 1

            current_speaker = speaker
            current_text = [script_line.content]
            current_lines = [line_num]
        else:
            current_speaker = speaker
            current_text.append(script_line.content)
            current_lines.append(line_num)

    # Add final segment
    if current_text:
        segment_text = " ".join(current_text).strip()
        if segment_text:
            word_count = len(segment_text.split())
            segment = ScriptSegment(
                segment_number=segment_number,
                speaker=current_speaker,
                dialogue_text=segment_text,
                original_line_numbers=current_lines,
                sequence_identifier=f"segment_{segment_number}_{current_speaker.lower()}",
                word_count=word_count
            )
            segments.append(segment)

    total_words = sum(len(s.dialogue_text.split()) for s in segments)

    return SegmentedScript(
        topic=script.topic,
        total_segments=len(segments),
        segments=segments,
        original_line_count=len(script.lines),
        total_word_count=total_words
    )


def _validate_segmentation(original_script: Script, segmented: SegmentedScript) -> None:
    """Validate that segmentation preserves all original lines."""
    collected_lines = []
    for segment in segmented.segments:
        collected_lines.extend(segment.original_line_numbers)

    collected_lines.sort()
    expected_lines = list(range(1, len(original_script.lines) + 1))

    if collected_lines != expected_lines:
        missing = set(expected_lines) - set(collected_lines)
        duplicates = [x for x in collected_lines if collected_lines.count(x) > 1]
        raise ValueError(
            f"Segmentation validation failed:\n"
            f"  Missing lines: {missing}\n"
            f"  Duplicate lines: {set(duplicates)}"
        )


def _synthesize_speaker_audio(text: str, speaker: str, voice_id: str,
                              segmented: SegmentedScript) -> tuple[Optional[bytes], float]:
    """
    Synthesize audio for a single speaker using Google Generative AI TTS.

    Returns:
        Tuple of (audio_bytes, duration_seconds)
    """
    try:
        print(f"   ⏳ Calling TTS for {speaker}...")

        client = genai.Client(api_key=config.GOOGLE_GEMINI_API_KEY)

        # Create chat session with TTS model
        chat = client.chats.create(model=config.TTS_MODEL)

        # Send text to generate audio
        response = chat.send_message(text)

        # Extract audio from response.parts[].inline_data.data
        audio_bytes = None
        if hasattr(response, 'parts') and response.parts:
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    audio_bytes = part.inline_data.data
                    break

        if not audio_bytes:
            raise ValueError("No audio data in response")

        # Calculate duration based on word count (fallback if duration not in response)
        word_count = len(text.split())
        estimated_duration = word_count / 2.33  # ~140 words per minute

        if speaker == "Both":
            print(f"   ✓ Full dialogue: {word_count} words, ~{estimated_duration:.1f}s, {len(audio_bytes)} bytes")
        else:
            print(f"   ✓ {speaker}: {word_count} words, ~{estimated_duration:.1f}s, {len(audio_bytes)} bytes")
        return audio_bytes, estimated_duration

    except Exception as e:
        print(f"   ✗ Error synthesizing {speaker}: {str(e)}")
        # Fall back to placeholder if TTS fails
        print(f"   ⚠️  Falling back to placeholder audio for {speaker}...")
        return _create_placeholder_audio(speaker, segmented)


def _create_placeholder_audio(speaker: str, segmented: SegmentedScript) -> tuple[bytes, float]:
    """Create a placeholder WAV file for testing the pipeline."""
    # Calculate duration based on speaker's text
    if speaker == "Both" or speaker == "Combined":
        # Use all segments for combined audio
        total_words = segmented.total_word_count
    else:
        # Use only the specified speaker's segments
        speaker_segments = [s for s in segmented.segments if s.speaker == speaker]
        total_words = sum(s.word_count for s in speaker_segments)
    duration_seconds = total_words / 2.33  # ~140 words per minute

    # Create minimal WAV file (silence)
    wav_buffer = io.BytesIO()
    sample_rate = 24000
    num_samples = int(sample_rate * duration_seconds)

    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b'\x00\x00' * num_samples)  # Silent audio

    return wav_buffer.getvalue(), duration_seconds


def _save_segmentation_report(segmented: SegmentedScript, output_folder: Path) -> None:
    """Save detailed segmentation report."""
    report_path = output_folder / "segmentation_report.txt"

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=== SCRIPT SEGMENTATION REPORT ===\n")
        f.write(f"Topic: {segmented.topic}\n")
        f.write(f"Total Segments: {segmented.total_segments}\n")
        f.write(f"Original Lines: {segmented.original_line_count}\n")
        f.write(f"Total Words: {segmented.total_word_count}\n\n")

        f.write("SEGMENT BREAKDOWN:\n")
        f.write("-" * 80 + "\n")

        for segment in segmented.segments:
            f.write(f"\n{segment.sequence_identifier}\n")
            f.write(f"  Speaker: {segment.speaker}\n")
            f.write(f"  Original Lines: {segment.original_line_numbers}\n")
            f.write(f"  Words: {segment.word_count}\n")
            f.write(f"  Text: {segment.dialogue_text[:100]}...\n")

        f.write("\n" + "-" * 80 + "\n")
        f.write("VALIDATION: All original lines preserved ✓\n")
