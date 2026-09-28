#!/usr/bin/env python3
"""
SPEAK ENGLISH SMARTER - Video Generation Pipeline
Phase 1, 2 & 3: Script Generation + SEO Metadata + Text-to-Speech

Interactive CLI for generating English learning video scripts, metadata, and audio.
"""

import click
import json
from pathlib import Path
import textwrap
import sys

# Add parent directory to path to import src package
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import config
from src.models import TopicInput
from src.agents.script_generation_agent import generate_script, save_script_to_file
from src.agents.seo_metadata_agent import generate_seo_metadata, save_seo_metadata_to_file
from src.agents.tts_agent import generate_tts_audio
from src.agents.thumbnail_image_agent import generate_thumbnail_image
from src.agents.video_image_agent import generate_video_scene
from src.agents.edit_thumbnail_image import edit_thumbnail_image
from src.agents.video_assembly_agent import generate_video

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Print project header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("=" * 60)
    print("  SPEAK ENGLISH SMARTER - Video Generation Pipeline")
    print("  Phase 1: Script Generation | Phase 2: SEO Metadata")
    print("=" * 60)
    print(f"{Colors.ENDC}")

def print_info(message):
    """Print info message."""
    print(f"{Colors.OKCYAN}ℹ️  {message}{Colors.ENDC}")

def print_success(message):
    """Print success message."""
    print(f"{Colors.OKGREEN}✅ {message}{Colors.ENDC}")

def print_warning(message):
    """Print warning message."""
    print(f"{Colors.WARNING}⚠️  {message}{Colors.ENDC}")

def print_error(message):
    """Print error message."""
    print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")

def get_video_length_input():
    """Get desired video length from user in minutes."""
    while True:
        try:
            length_str = input(f"{Colors.OKBLUE}Desired video length in minutes (default 12, range 8-20): {Colors.ENDC}").strip()

            if not length_str:
                return 12  # Default

            length = int(length_str)

            if 8 <= length <= 20:
                return length
            else:
                print_warning(f"Please enter a value between 8 and 20 minutes")
        except ValueError:
            print_warning("Please enter a valid number")

def get_skip_tts_input():
    """Ask user if they want to skip TTS generation."""
    while True:
        response = input(f"{Colors.OKBLUE}Generate TTS audio? (Y/n, default: yes): {Colors.ENDC}").strip().lower()

        if not response or response == 'y' or response == 'yes':
            return False  # Don't skip TTS
        elif response == 'n' or response == 'no':
            return True  # Skip TTS
        else:
            print_warning("Please enter 'y' or 'n'")

def get_skip_images_input():
    """Ask user if they want to skip image generation."""
    while True:
        response = input(f"{Colors.OKBLUE}Generate images (thumbnail + video scene)? (Y/n, default: yes): {Colors.ENDC}").strip().lower()

        if not response or response == 'y' or response == 'yes':
            return False  # Don't skip images
        elif response == 'n' or response == 'no':
            return True  # Skip images
        else:
            print_warning("Please enter 'y' or 'n'")

def get_skip_video_assembly_input():
    """Ask user if they want to assemble video (Phase 6)."""
    while True:
        response = input(f"{Colors.OKBLUE}Assemble final MP4 video? (y/N, default: no): {Colors.ENDC}").strip().lower()

        if not response or response == 'n' or response == 'no':
            return True  # Skip video assembly (default)
        elif response == 'y' or response == 'yes':
            return False  # Don't skip video assembly
        else:
            print_warning("Please enter 'y' or 'n'")

@click.command()
@click.option('--topic', prompt=False, default=None, help='Video topic')
@click.option('--context', prompt=False, default=None, help='Additional context for the topic')
@click.option('--output', type=click.Path(), default=None, help='Custom output directory')
def main(topic, context, output):
    """
    Generate video scripts for SPEAK ENGLISH SMARTER channel.

    Interactive mode if no --topic provided.
    """

    print_header()

    # Validate API key
    if not config.ANTHROPIC_API_KEY:
        print_error("ANTHROPIC_API_KEY not set in environment")
        print_info("Set your API key: export ANTHROPIC_API_KEY='your-key'")
        return

    # Get topic from user if not provided
    if not topic:
        print_info("Enter your video topic below")
        print("Examples: 'How to apologize politely', 'Making small talk at parties'")
        topic = input(f"{Colors.OKBLUE}Topic: {Colors.ENDC}").strip()

    if not topic:
        print_error("No topic provided")
        return

    # Get optional context
    if not context:
        context_input = input(f"{Colors.OKBLUE}Additional context (optional, press Enter to skip): {Colors.ENDC}").strip()
        context = context_input if context_input else None

    # Get desired video length
    video_length_minutes = get_video_length_input()
    target_words = video_length_minutes * config.WORDS_PER_MINUTE
    # Note: Actual tolerance is ±35% to account for natural variation in script generation
    print_success(f"Target: {video_length_minutes} minutes (~{target_words} words)")

    # Ask if user wants TTS
    skip_tts = get_skip_tts_input()
    if skip_tts:
        print_info("TTS generation will be skipped")
    else:
        print_info("TTS audio will be generated")

    # Ask if user wants images (Phase 4)
    skip_images = get_skip_images_input()
    if skip_images:
        print_info("Image generation will be skipped")
    else:
        print_info("Images (thumbnail + video scene) will be generated")

    # Ask if user wants video assembly (Phase 6)
    # Note: Only ask if TTS will be generated (can't make video without audio)
    skip_video_assembly = True  # Default: skip
    if not skip_tts:
        skip_video_assembly = get_skip_video_assembly_input()
        if skip_video_assembly:
            print_info("Video assembly will be skipped")
        else:
            print_info("Final MP4 video will be assembled")
    else:
        print_info("Video assembly will be skipped (TTS is disabled)")

    # Create topic input
    try:
        topic_input = TopicInput(
            topic=topic,
            optional_context=context,
            target_words=target_words
        )
        print_success(f"Topic validated: {topic_input.topic}")
    except Exception as e:
        print_error(f"Invalid input: {e}")
        return

    # Generate script
    try:
        script = generate_script(topic_input, target_words=target_words, tolerance=None)

        # Determine output folder
        if output:
            output_folder = Path(output)
        else:
            # Create slug from topic - remove invalid filename characters
            import re
            slug = topic.lower()
            # Remove invalid Windows filename characters: ? ! / \ : * " < > |
            slug = re.sub(r'[?!\/\\:*"<>|]', '', slug)
            # Replace spaces with underscores
            slug = slug.replace(" ", "_")
            # Limit length
            slug = slug[:50]
            output_folder = config.OUTPUT_DIR / slug

        # Save script
        script_path = save_script_to_file(script, output_folder)

        # Generate SEO metadata (Phase 2)
        seo_path = None
        seo_metadata = None
        tts_metadata = None
        try:
            seo_metadata = generate_seo_metadata(script, topic_input)
            seo_path = save_seo_metadata_to_file(seo_metadata, output_folder)

            # Display SEO summary
            print(f"\n{Colors.BOLD}{Colors.OKGREEN}=== SEO Metadata Generated ==={Colors.ENDC}")
            print(f"📌 Title: {seo_metadata.title}")
            print(f"🎯 Thumbnail Text: {seo_metadata.thumbnail_text}")
            print(f"#️⃣  Hashtags: {' '.join(seo_metadata.hashtags[:5])} ... (+15 more)")
            print(f"🏷️  Tags: {', '.join(seo_metadata.tags[:5])} ... (+15 more)")
            print(f"📄 Description: {seo_metadata.description[:150]}...")
        except Exception as e:
            print_warning(f"SEO generation skipped: {e}")
            seo_path = None

        # Generate TTS audio (Phase 3)
        try:
            if skip_tts:
                print_info("TTS generation skipped by user (--skip-tts flag)")
            elif config.GOOGLE_GEMINI_API_KEY:
                print(f"\n{Colors.BOLD}{Colors.OKBLUE}Starting Phase 3: Text-to-Speech Generation...{Colors.ENDC}")
                tts_metadata = generate_tts_audio(script, output_folder)

                # Display TTS summary
                print(f"\n{Colors.BOLD}{Colors.OKGREEN}=== TTS Audio Generated ==={Colors.ENDC}")
                print(f"🔊 Total Duration: {tts_metadata.total_duration_seconds:.1f}s")
                print(f"   - Sarah: {tts_metadata.sarah_duration_seconds:.1f}s")
                print(f"   - Alex: {tts_metadata.alex_duration_seconds:.1f}s")
                print(f"🎯 Segments: {tts_metadata.total_segments_processed}")
                print(f"📁 Audio folder: {output_folder / 'audio'}")
            else:
                print_warning("GOOGLE_GEMINI_API_KEY not set - TTS skipped")
                print_info("To enable TTS: Set GOOGLE_GEMINI_API_KEY in config/.env")
        except Exception as e:
            print_warning(f"TTS generation skipped: {e}")
            tts_metadata = None

        # Generate images (Phase 4)
        thumbnail_metadata = None
        video_scene_metadata = None

        if skip_images:
            print_info("Image generation skipped by user")
        elif config.OPENAI_API_KEY:
            try:
                print(f"\n{Colors.BOLD}{Colors.OKBLUE}Starting Phase 4: Image Generation...{Colors.ENDC}")

                # Generate thumbnail with context
                thumbnail_metadata = generate_thumbnail_image(script, seo_metadata if seo_metadata else None, output_folder, context=context)

                # Generate video scene with context
                video_scene_metadata = generate_video_scene(script, seo_metadata if seo_metadata else None, output_folder, context=context)

                if thumbnail_metadata or video_scene_metadata:
                    print(f"\n{Colors.BOLD}{Colors.OKGREEN}=== Images Generated ==={Colors.ENDC}")
                    if thumbnail_metadata:
                        print(f"🖼️  Thumbnail: {output_folder / 'thumbnail.png'}")
                    if video_scene_metadata:
                        print(f"🎬 Video Scene: {output_folder / 'video_scene.png'}")

            except Exception as e:
                print_warning(f"Image generation error: {e}")
        else:
            print_warning("OPENAI_API_KEY not set - Image generation skipped")
            print_info("To enable images: Set OPENAI_API_KEY in config/.env")

        # Add text overlay to thumbnail (Phase 5)
        edited_thumbnail_metadata = None

        if thumbnail_metadata and seo_metadata and config.TEXT_OVERLAY_ENABLED:
            try:
                print(f"\n{Colors.BOLD}{Colors.OKBLUE}Starting Phase 5: Thumbnail Text Overlay...{Colors.ENDC}")

                thumbnail_path = output_folder / "thumbnail.png"
                edited_thumbnail_metadata = edit_thumbnail_image(
                    thumbnail_path,
                    seo_metadata,
                    output_folder,
                    topic=topic,
                    context=context
                )

                if edited_thumbnail_metadata:
                    print(f"\n{Colors.BOLD}{Colors.OKGREEN}=== Thumbnail Text Overlay Complete ==={Colors.ENDC}")
                    print(f"📝 Text added: '{seo_metadata.thumbnail_text}'")
                    print(f"🖼️  Edited Thumbnail: {thumbnail_path}")

            except Exception as e:
                print_warning(f"Thumbnail text overlay error: {e}")
        elif thumbnail_metadata and not seo_metadata:
            print_info("Text overlay skipped: No SEO metadata available")
        elif not thumbnail_metadata:
            print_info("Text overlay skipped: No thumbnail generated")

        # Generate video (Phase 6)
        video_path = None
        if not skip_video_assembly and config.VIDEO_ASSEMBLY_ENABLED and tts_metadata and video_scene_metadata:
            try:
                print(f"\n{Colors.BOLD}{Colors.OKBLUE}Starting Phase 6: Video Assembly...{Colors.ENDC}")

                video_path = generate_video(
                    output_folder,
                    script_path,
                    output_folder / "audio" / "audio.mp3",
                    output_folder / "video_scene.png",
                    tts_metadata,
                    seo_metadata if seo_metadata else None
                )

                if video_path:
                    print(f"\n{Colors.BOLD}{Colors.OKGREEN}=== Video Assembly Complete ==={Colors.ENDC}")
                    print(f"🎬 Final video: {video_path}")
                else:
                    print_warning("Video assembly completed with warnings")

            except Exception as e:
                print_warning(f"Video assembly skipped: {e}")
                video_path = None
        elif skip_video_assembly:
            print_info("Phase 6: Video assembly skipped by user")
        elif not config.VIDEO_ASSEMBLY_ENABLED:
            print_info("Phase 6: Video assembly disabled in config")
        elif not tts_metadata:
            print_info("Phase 6: Video assembly requires TTS audio (Phase 3)")
        elif not video_scene_metadata:
            print_info("Phase 6: Video assembly requires video scene (Phase 4)")

        # Display complete summary
        print(f"\n{Colors.BOLD}{Colors.OKGREEN}=== Generation Complete ==={Colors.ENDC}")
        print(f"📁 Output folder: {output_folder}")
        print(f"📝 Files created:")
        print(f"   ✓ script.txt")
        print(f"   ✓ script_metadata.json")
        if seo_path:
            print(f"   ✓ seo_metadata.txt")
        if tts_metadata:
            print(f"   ✓ audio/audio.mp3")
            print(f"   ✓ audio/tts_metadata.json")
        if thumbnail_metadata:
            print(f"   ✓ thumbnail.png (Phase 4 - no text)")
        if edited_thumbnail_metadata:
            print(f"   ✓ thumbnail_with_text.png (Phase 5 - with text overlay)")
        if video_scene_metadata:
            print(f"   ✓ video_scene.png")
        if video_path:
            print(f"   ✓ output_video.mp4 (Phase 6 - final video)")
            print(f"   ✓ subtitle.srt (Phase 6 - captions)")

        print(f"\n📊 Script Statistics:")
        print(f"   - Lines: {len(script.lines)}")
        print(f"   - Words: {script.word_count}")
        print(f"   - Duration: ~{script.estimated_duration_minutes:.1f} minutes")
        print(f"   - Characters: Sarah (teacher) & Alex (learner)")

        # Next steps
        print(f"\n{Colors.BOLD}Pipeline Status:{Colors.ENDC}")
        print("✅ Phase 1: Script Generation - Complete")
        print("✅ Phase 2: SEO Metadata - Complete" if seo_path else "⏳ Phase 2: SEO Metadata - Skipped")
        print("✅ Phase 3: Text-to-Speech - Complete" if tts_metadata else "⏳ Phase 3: Text-to-Speech - Skipped")
        print("✅ Phase 4: Image Generation - Complete" if (thumbnail_metadata or video_scene_metadata) else "⏳ Phase 4: Image Generation - Skipped")
        print("✅ Phase 5: Text Overlay - Complete" if edited_thumbnail_metadata else ("⏳ Phase 5: Text Overlay - Skipped" if thumbnail_metadata else "⏳ Phase 5: Text Overlay - Not available"))
        print("✅ Phase 6: Video Assembly - Complete" if video_path else "⏳ Phase 6: Video Assembly - Skipped")

        return script

    except Exception as e:
        print_error(f"Script generation failed: {e}")
        import traceback
        traceback.print_exc()
        return

@click.command()
@click.option('--script-path', type=click.Path(exists=True), required=True, help='Path to script file')
def validate_script(script_path):
    """Validate an existing script against quality criteria."""
    print_header()
    print_info(f"Validating script: {script_path}")

    # Load script
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        from script_generation_agent import _parse_script, _validate_script_quality
        script = _parse_script(content, "Validation")
        issues = _validate_script_quality(script)

        print(f"Script Statistics:")
        print(f"  - Lines: {len(script.lines)}")
        print(f"  - Words: {script.word_count}")
        print(f"  - Duration: ~{script.estimated_duration_minutes:.1f} minutes")

        if issues:
            print_warning("Quality issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print_success("Script passes all quality checks!")

    except Exception as e:
        print_error(f"Validation failed: {e}")

@click.group()
def cli():
    """SPEAK ENGLISH SMARTER Pipeline CLI"""
    pass

cli.add_command(main, name="generate")
cli.add_command(validate_script, name="validate")

if __name__ == '__main__':
    cli()
