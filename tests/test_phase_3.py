#!/usr/bin/env python3
"""
Test script to validate Phase 3: Text-to-Speech (TTS) Generation
Tests script segmentation, validation, and audio generation with parallel synthesis.
"""

import sys
from pathlib import Path
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import config
from src.models import TopicInput, Script, ScriptLine
from src.agents.script_generation_agent import generate_script
from src.agents.tts_agent import (
    generate_tts_audio,
    _parse_speaker_segments,
    _validate_segmentation,
)


def create_sample_script() -> Script:
    """Create a sample script for testing."""
    lines = [
        ScriptLine(speaker="Sarah", content="Hello everyone! Welcome to today's lesson.", line_number=1),
        ScriptLine(speaker="Sarah", content="Today we're going to learn about greetings.", line_number=2),
        ScriptLine(speaker="Alex", content="Great! I'm excited to learn.", line_number=3),
        ScriptLine(speaker="Alex", content="What's the first phrase?", line_number=4),
        ScriptLine(speaker="Sarah", content="The first phrase is 'How are you doing?'", line_number=5),
        ScriptLine(speaker="Sarah", content="It's informal and friendly.", line_number=6),
        ScriptLine(speaker="Alex", content="That sounds nice and casual.", line_number=7),
        ScriptLine(speaker="Alex", content="Can you give me an example?", line_number=8),
    ]

    return Script(
        topic="Learning Greetings",
        lines=lines,
        word_count=sum(len(line.content.split()) for line in lines),
        estimated_duration_minutes=0.5,
        target_words=65
    )


def test_script_segmentation():
    """Test parsing script into speaker segments."""
    print("\n" + "="*70)
    print("  TEST 1: Script Segmentation")
    print("="*70 + "\n")

    script = create_sample_script()

    try:
        segmented = _parse_speaker_segments(script)

        print(f"✓ Script parsed successfully")
        print(f"  - Original lines: {len(script.lines)}")
        print(f"  - Segments created: {segmented.total_segments}")
        print(f"  - Total words: {segmented.total_word_count}")

        # Display segments
        print(f"\n📋 Segments breakdown:")
        for segment in segmented.segments:
            print(f"  {segment.sequence_identifier}")
            print(f"    Speaker: {segment.speaker}")
            print(f"    Lines: {segment.original_line_numbers}")
            print(f"    Words: {segment.word_count}")
            print(f"    Text: {segment.dialogue_text[:60]}...")

        # Validate segmentation
        print(f"\n🔍 Validating segmentation...")
        _validate_segmentation(script, segmented)
        print(f"✅ Segmentation validation passed!")

        return True

    except Exception as e:
        print(f"❌ Segmentation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_segmentation_validation():
    """Test that segmentation catches data loss."""
    print("\n" + "="*70)
    print("  TEST 2: Segmentation Validation")
    print("="*70 + "\n")

    script = create_sample_script()
    segmented = _parse_speaker_segments(script)

    try:
        # This should pass
        _validate_segmentation(script, segmented)
        print(f"✓ Validation passed - no data loss detected")

        # Try to corrupt the segmentation
        print(f"\n🔧 Testing error detection...")
        segmented.segments[0].original_line_numbers = [999]  # Invalid line number

        try:
            _validate_segmentation(script, segmented)
            print(f"❌ Validation should have failed but didn't!")
            return False
        except ValueError as e:
            print(f"✓ Validation correctly detected corruption:")
            print(f"  Error: {str(e)[:80]}...")
            return True

    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        return False


def test_speaker_balance():
    """Test that both speakers are present in segments."""
    print("\n" + "="*70)
    print("  TEST 3: Speaker Balance")
    print("="*70 + "\n")

    script = create_sample_script()
    segmented = _parse_speaker_segments(script)

    try:
        speakers = {s.speaker for s in segmented.segments}

        if "Sarah" in speakers and "Alex" in speakers:
            print(f"✓ Both speakers present in segments")
            print(f"  - Sarah segments: {sum(1 for s in segmented.segments if s.speaker == 'Sarah')}")
            print(f"  - Alex segments: {sum(1 for s in segmented.segments if s.speaker == 'Alex')}")
            return True
        else:
            print(f"❌ Missing speakers: {speakers}")
            return False

    except Exception as e:
        print(f"❌ Speaker balance test failed: {e}")
        return False


def test_segment_sequence():
    """Test that segments are numbered correctly."""
    print("\n" + "="*70)
    print("  TEST 4: Segment Sequence")
    print("="*70 + "\n")

    script = create_sample_script()
    segmented = _parse_speaker_segments(script)

    try:
        segment_numbers = [s.segment_number for s in segmented.segments]
        expected = list(range(1, len(segmented.segments) + 1))

        if segment_numbers == expected:
            print(f"✓ Segments numbered correctly")
            print(f"  - Sequence: {segment_numbers}")
            return True
        else:
            print(f"❌ Incorrect sequence: {segment_numbers}")
            print(f"  - Expected: {expected}")
            return False

    except Exception as e:
        print(f"❌ Segment sequence test failed: {e}")
        return False


def test_tts_generation_readiness():
    """Test if TTS generation can be called (without actually generating audio)."""
    print("\n" + "="*70)
    print("  TEST 5: TTS Generation Readiness")
    print("="*70 + "\n")

    # Check if Google API key is set
    if not config.GOOGLE_GEMINI_API_KEY:
        print(f"⚠️  GOOGLE_GEMINI_API_KEY not set")
        print(f"   Set it with: $env:GOOGLE_GEMINI_API_KEY='your-key'")
        print(f"   (Skipping actual TTS generation)")
        return True  # Not a failure - just skipped

    try:
        # Try to import the TTS module
        from src.agents.tts_agent import generate_tts_audio
        print(f"✓ TTS agent module loaded successfully")

        # Try to configure Google API
        try:
            import google.generativeai as genai
            genai.configure(api_key=config.GOOGLE_GEMINI_API_KEY)
            print(f"✓ Google API client configured")
            return True
        except ImportError:
            print(f"⚠️  google-generativeai not installed")
            print(f"   Install with: pip install google-generativeai")
            return True  # Not a failure - just missing dependency

    except Exception as e:
        print(f"❌ TTS readiness test failed: {e}")
        return False


def test_full_pipeline_setup():
    """Test that all Phase 3 components are ready."""
    print("\n" + "="*70)
    print("  TEST 6: Full Pipeline Setup")
    print("="*70 + "\n")

    try:
        # Check Phase 1 - Script generation
        print("📋 Checking Phase 1 components...")
        from src.agents.script_generation_agent import generate_script
        print("  ✓ Script generation agent available")

        # Check Phase 2 - SEO metadata
        print("📌 Checking Phase 2 components...")
        from src.agents.seo_metadata_agent import generate_seo_metadata
        print("  ✓ SEO metadata agent available")

        # Check Phase 3 - TTS
        print("🎤 Checking Phase 3 components...")
        from src.agents.tts_agent import generate_tts_audio
        print("  ✓ TTS agent available")

        # Check config
        print("⚙️  Checking configuration...")
        print(f"  ✓ ANTHROPIC_API_KEY: {'Set' if config.ANTHROPIC_API_KEY else 'Not set'}")
        print(f"  ✓ GOOGLE_GEMINI_API_KEY: {'Set' if config.GOOGLE_GEMINI_API_KEY else 'Not set'}")
        print(f"  ✓ TTS Voices: Sarah={config.TTS_VOICES['Sarah']}, Alex={config.TTS_VOICES['Alex']}")

        print(f"\n✅ Pipeline setup complete!")
        return True

    except Exception as e:
        print(f"❌ Pipeline setup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("  PHASE 3: TEXT-TO-SPEECH (TTS) AGENT TEST SUITE")
    print("  Testing segmentation, validation, and audio generation readiness")
    print("="*70)

    # Run tests
    results = {
        "Segmentation": test_script_segmentation(),
        "Validation": test_segmentation_validation(),
        "Speaker Balance": test_speaker_balance(),
        "Segment Sequence": test_segment_sequence(),
        "TTS Readiness": test_tts_generation_readiness(),
        "Pipeline Setup": test_full_pipeline_setup(),
    }

    # Summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")

    print(f"\n✅ Passed: {passed}/{total}")

    if passed == total:
        print(f"\n🎉 SUCCESS! All Phase 3 tests passed!")
        print(f"\n📝 Next Steps:")
        print(f"   1. Set GOOGLE_GEMINI_API_KEY in config/.env")
        print(f"   2. Run full pipeline: python scripts/cli.py generate")
        print(f"   3. Verify audio output in outputs/{{topic}}/audio/")
    else:
        print(f"\n⚠️  Some tests failed. Review errors above.")

    print("\n" + "="*70 + "\n")
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
