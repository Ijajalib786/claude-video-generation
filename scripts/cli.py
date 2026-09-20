#!/usr/bin/env python3
"""
SPEAK ENGLISH SMARTER - Video Generation Pipeline
Phase 1: Script Generation Agent

Interactive CLI for generating English learning video scripts.
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
    print("  Phase 1: Script Generation Agent")
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
            # Create slug from topic
            slug = topic.lower().replace(" ", "_")[:30]
            output_folder = config.OUTPUT_DIR / slug

        # Save script
        script_path = save_script_to_file(script, output_folder)

        # Display summary
        print(f"\n{Colors.BOLD}{Colors.OKGREEN}=== Script Generation Complete ==={Colors.ENDC}")
        print(f"📁 Output folder: {output_folder}")
        print(f"📝 Script file: {script_path.name}")
        print(f"📊 Statistics:")
        print(f"   - Lines: {len(script.lines)}")
        print(f"   - Words: {script.word_count}")
        print(f"   - Duration: ~{script.estimated_duration_minutes:.1f} minutes")
        print(f"   - Characters: Sarah (teacher) & Alex (learner)")

        # Next steps
        print(f"\n{Colors.BOLD}Next Steps:{Colors.ENDC}")
        print("✨ Phase 1 Complete: Script Generation")
        print("📋 Phase 2: Add SEO metadata generation (coming next)")
        print("🎤 Phase 3: Add Text-to-Speech conversion")
        print("🖼️  Phase 4: Add thumbnail generation")
        print("🎬 Phase 5: Add video assembly (FFmpeg)")

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
