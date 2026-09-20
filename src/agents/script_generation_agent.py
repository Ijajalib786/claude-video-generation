"""
Phase 1: Script Generation Agent
Generates YouTube video scripts using Claude API based on topics.
Validates output against quality criteria.
"""

import json
import re
from pathlib import Path
from anthropic import Anthropic
from .. import config
from ..models import Script, ScriptLine, TopicInput

client = Anthropic()

TOPIC_QUALITY_CRITERIA = """
Quality criteria the script must address:
1. High YouTube search demand - Use popular keywords with sustained interest
2. Evergreen search potential - Timeless content, remains relevant long-term
3. Trending or seasonally relevant - Current/upcoming demand signals
4. Beginner-friendly - Simple, relatable, easy to understand
5. Suitable for 10-15 min conversation - Natural pacing, not rushed
6. Encourages watch-until-end - Narrative flow, story elements, practice
7. Teaches everyday vocabulary - Practical, usable in real conversations
8. Strong thumbnail potential - Visual hooks, emotional expressions, context
9. Strong CTR potential - Curiosity gap, benefit-driven, relatable
10. Practical & relatable - Real-world scenarios (work, friends, daily life)
11. Platform-friendly - Recommendations-ready, shareable, engagement-worthy
"""

def load_script_prompt():
    """Load the script writer prompt from references."""
    if config.SCRIPT_PROMPT_PATH.exists():
        return config.SCRIPT_PROMPT_PATH.read_text()
    return ""

def load_example_script():
    """Load the example script for context."""
    if config.EXAMPLE_SCRIPT_PATH.exists():
        return config.EXAMPLE_SCRIPT_PATH.read_text()
    return ""

def generate_script(topic_input: TopicInput, target_words: int = None, tolerance: int = None) -> Script:
    """
    Generate a video script using Claude API with multi-turn conversation.

    Args:
        topic_input: User topic and context
        target_words: Target word count (default from config.SCRIPT_MIN_WORDS + SCRIPT_MAX_WORDS average)
        tolerance: Allowed deviation from target words

    Phase 1 Learning: This demonstrates Claude tool use and agent loops
    with file-based state management for transparency.
    """

    # Use default target if not specified
    if target_words is None:
        target_words = (config.SCRIPT_MIN_WORDS + config.SCRIPT_MAX_WORDS) // 2

    if tolerance is None:
        tolerance = int(target_words * 0.10)

    min_words = target_words - tolerance
    max_words = target_words + tolerance

    script_prompt = load_script_prompt()
    example_script = load_example_script()

    # System message for script generation agent
    system_message = f"""You are an expert script writer for an English learning YouTube channel called "SPEAK ENGLISH SMARTER".

Your role is to write natural, engaging video scripts where Sarah (English teacher) and Alex (English learner) have conversations.

IMPORTANT QUALITY CRITERIA:
{TOPIC_QUALITY_CRITERIA}

SCRIPT WRITER PROMPT:
{script_prompt}

EXAMPLE SCRIPT FORMAT (from "Say No Politely"):
{example_script[:2000]}... [truncated for context]

Guidelines:
- Write dialogue in the exact format: "Sarah : [line]" and "Alex : [line]"
- Each speaker's line should be clear and on its own line
- **CRITICAL:** Target {target_words} words (acceptable range: {min_words}-{max_words} words)
  * Expand dialogue with natural pauses, reactions, and detailed explanations
  * Include personal anecdotes and relatable examples
  * Add practice exercises and reinforcement of key points
  * Aim for the upper end of the range to maximize learning time
- Begin with a hook (15-30 sec), channel intro, clear learning objectives
- Teach the main content with examples, then practice, then CTA
- Use simple, beginner-friendly English
- Make it natural and conversational, not robotic
- **IMPORTANT:** At this word count, you have room to be thorough - explain concepts fully, don't rush
- Include pauses, reactions, humor, and small stories to keep it engaging

After generating the script, provide a JSON block with statistics like this:
```json
{{
  "word_count": 1850,
  "estimated_duration_minutes": 12.5,
  "quality_checks": {{
    "has_hook": true,
    "has_channel_intro": true,
    "has_cta": true,
    "is_beginner_friendly": true
  }}
}}
```"""

    messages = [
        {
            "role": "user",
            "content": f"Generate a YouTube video script for this topic: {topic_input.topic}\n\nAdditional context: {topic_input.optional_context or 'None provided'}"
        }
    ]

    print(f"\n🎬 Generating script for topic: {topic_input.topic}")
    print("⏳ Calling Claude API with script generation prompt...")

    # Call Claude API
    response = client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=config.MAX_TOKENS,
        system=system_message,
        messages=messages
    )

    # Extract text from response, skipping ThinkingBlocks
    script_text = None
    for block in response.content:
        if hasattr(block, 'text'):
            script_text = block.text
            break

    if script_text is None:
        raise ValueError("No text content found in API response")

    # Parse the generated script
    script_obj = _parse_script(script_text, topic_input.topic, target_words=target_words)

    # Validate quality
    quality_issues = _validate_script_quality(script_obj)
    if quality_issues:
        print(f"⚠️  Quality warnings: {quality_issues}")
    else:
        print("✅ Script passed quality validation")

    return script_obj

def _parse_script(raw_script: str, topic: str, target_words: int = None) -> Script:
    """
    Parse raw script text into Script object.
    Extracts dialogue lines and calculates statistics.
    """
    lines = []
    line_number = 0

    # Split into lines and parse speaker:content format
    for raw_line in raw_script.split('\n'):
        raw_line = raw_line.strip()
        if not raw_line or raw_line.startswith("```"):
            continue

        # Try to match "Sarah : content" or "Alex : content" format
        match = re.match(r"^(Sarah|Alex)\s*:\s*(.+)$", raw_line)
        if match:
            speaker, content = match.groups()
            line_number += 1
            lines.append(ScriptLine(
                speaker=speaker,
                content=content.strip(),
                line_number=line_number
            ))

    # Calculate word count
    all_content = " ".join([line.content for line in lines])
    word_count = len(all_content.split())

    # Estimate duration
    estimated_minutes = word_count / config.WORDS_PER_MINUTE

    return Script(
        topic=topic,
        lines=lines,
        word_count=word_count,
        estimated_duration_minutes=estimated_minutes,
        target_words=target_words
    )

def _validate_script_quality(script: Script) -> list[str]:
    """
    Validate script against quality criteria.
    Returns list of issues found (empty if all good).
    """
    issues = []

    # Check word count
    if script.word_count < config.SCRIPT_MIN_WORDS:
        issues.append(f"Word count too low: {script.word_count} < {config.SCRIPT_MIN_WORDS}")
    if script.word_count > config.SCRIPT_MAX_WORDS:
        issues.append(f"Word count too high: {script.word_count} > {config.SCRIPT_MAX_WORDS}")

    # Check dialogue format
    if not script.lines:
        issues.append("No dialogue lines found")

    # Check for both speakers
    speakers = set(line.speaker for line in script.lines)
    if "Sarah" not in speakers:
        issues.append("Sarah (teacher) not found in script")
    if "Alex" not in speakers:
        issues.append("Alex (learner) not found in script")

    # Check for opening hook and CTA
    first_lines = [line.content for line in script.lines[:3]]
    last_lines = [line.content for line in script.lines[-3:]]

    # Simple heuristics
    has_hook = any("imagine" in line.lower() or "how do you" in line.lower() for line in first_lines)
    has_cta = any("like" in line.lower() and "subscribe" in line.lower() for line in last_lines)

    if not has_hook:
        issues.append("Missing opening hook (should start with engaging question)")
    if not has_cta:
        issues.append("Missing call-to-action (Like, Comment, Subscribe)")

    return issues

def save_script_to_file(script: Script, output_folder: Path) -> Path:
    """Save script to text file."""
    output_folder.mkdir(parents=True, exist_ok=True)

    script_path = output_folder / "script.txt"

    with open(script_path, 'w', encoding='utf-8') as f:
        for line in script.lines:
            f.write(f"{line.speaker} : {line.content}\n")

    # Save metadata
    metadata = {
        "topic": script.topic,
        "word_count": script.word_count,
        "estimated_duration_minutes": script.estimated_duration_minutes,
        "line_count": len(script.lines),
        "generated_at": script.generated_at.isoformat()
    }

    metadata_path = output_folder / "script_metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ Script saved to: {script_path}")
    print(f"   - Lines: {len(script.lines)}")
    print(f"   - Words: {script.word_count}")
    print(f"   - Estimated duration: {script.estimated_duration_minutes:.1f} minutes")

    return script_path
