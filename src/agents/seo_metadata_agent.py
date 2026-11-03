"""
Phase 2: SEO Metadata Agent
Generates YouTube-optimized SEO metadata with maximum search traffic focus.
Implements modern 2026 YouTube SEO strategy.
"""

import json
from pathlib import Path
from anthropic import Anthropic
from .. import config
from ..models import SEOMetadata, Script, TopicInput

client = Anthropic()

SEO_STRATEGY = """
YOUTUBE SEO NOTES (the SEO PROMPT GUIDE below has the exact formats and limits)
- Search intent first: put the main topic keyword at the start of the title and in the first sentence of the description.
- Viewers see only the first 100-150 characters of the description before "more", so make them count.
- Hashtags: 3-5 relevant ones, most relevant first. YouTube ignores all hashtags on a video that has more than 15. Put the 3 main hashtags on the last line of the description.
- Tags: 10-15 keywords; all tags joined with ", " must stay under 500 characters.
- Thumbnail text: 2-4 words, ALL CAPS, short enough to read on a phone.
- Use only details that are in the script and context. Never invent them.
"""

def load_seo_prompt():
    """Load SEO generation prompt from references."""
    if config.SEO_PROMPT_PATH.exists():
        return config.SEO_PROMPT_PATH.read_text()
    return ""

def generate_seo_metadata(script: Script, topic_input: TopicInput) -> SEOMetadata:
    """
    Generate YouTube-optimized SEO metadata with maximum search traffic focus.

    Args:
        script: Script object with dialogue content
        topic_input: Topic and context from user

    Returns:
        SEOMetadata object with:
        - title: Optimized, 70 chars or fewer
        - description: Keyword-rich, 250-400 words
        - hashtags: 3-5 relevant hashtags
        - tags: 10-15 SEO tags (500 characters or fewer in total)
        - thumbnail_text: 2-4 word text overlay
    """

    seo_prompt = load_seo_prompt()

    system_message = f"""You are a YouTube SEO expert optimizing titles, descriptions, hashtags, tags, and thumbnail text
for an English learning channel (SPEAK ENGLISH SMARTER).

GOAL: Help the right English learners find and click this video, using the keywords they actually search for.

{SEO_STRATEGY}

SCRIPT CONTEXT:
Topic: {script.topic}
Word Count: {script.word_count}
Estimated Duration: {script.estimated_duration_minutes:.1f} minutes

SEO PROMPT GUIDE:
{seo_prompt}

Follow the SEO PROMPT GUIDE above for formats and limits. Use only what is in the script and context.

Your output MUST be valid JSON with this exact structure:
{{
  "title": "exact title (70 characters or fewer)",
  "description": "full description (250-400 words)",
  "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"],
  "tags": ["tag1", "tag2", ... 10 to 15 items],
  "thumbnail_text": "2-4 WORDS"
}}

CRITICAL:
- Title must be 70 characters or fewer
- Description must be 250-400 words
- Hashtags must be 3 to 5 items
- Tags must be 10 to 15 items, and all tags joined with ", " must be 500 characters or fewer
- Thumbnail text must be 2 to 4 words (25 characters or fewer)
- JSON must be properly formatted (write line breaks inside the description as \\n)"""

    messages = [
        {
            "role": "user",
            "content": f"""Generate YouTube SEO metadata for this topic: {topic_input.topic}

Context: {topic_input.optional_context or 'No additional context provided'}

Script preview (first 500 words):
{' '.join([line.content for line in script.lines[:50]])}

Generate SEO metadata optimized for maximum search traffic and views."""
        }
    ]

    print(f"\n🔍 Generating SEO metadata for: {topic_input.topic}")
    print("⏳ Calling Claude API with SEO optimization...")

    response = client.messages.create(
        model=config.CLAUDE_MODEL,
        max_tokens=config.MAX_TOKENS,
        system=system_message,
        messages=messages
    )

    seo_text = None
    for block in response.content:
        if hasattr(block, 'text'):
            seo_text = block.text
            break

    if seo_text is None:
        raise ValueError("No text content found in API response")

    seo_metadata = _parse_seo_metadata(seo_text)
    print("✅ SEO metadata generated and validated")

    return seo_metadata

def _parse_seo_metadata(raw_response: str) -> SEOMetadata:
    """
    Parse JSON response from Claude into SEOMetadata object.
    """
    import re

    json_match = re.search(r'\{[^{}]*\}', raw_response, re.DOTALL)
    if not json_match:
        raise ValueError("No valid JSON found in API response")

    json_str = json_match.group(0)

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}")

    required_fields = ['title', 'description', 'hashtags', 'tags', 'thumbnail_text']
    missing = [f for f in required_fields if f not in data]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    return SEOMetadata(
        title=data['title'],
        description=data['description'],
        hashtags=data['hashtags'],
        tags=data['tags'],
        thumbnail_text=data['thumbnail_text']
    )

def save_seo_metadata_to_file(seo_metadata: SEOMetadata, output_folder: Path) -> Path:
    """Save SEO metadata as formatted text file."""
    output_folder.mkdir(parents=True, exist_ok=True)

    seo_path = output_folder / "seo_metadata.txt"

    with open(seo_path, 'w', encoding='utf-8') as f:
        f.write("=== YOUTUBE SEO METADATA ===\n")
        f.write(f"Generated for video optimization\n")
        f.write(f"Strategy: Trend-Based Search Optimization (2026)\n\n")

        f.write("TITLE:\n")
        f.write(f"{seo_metadata.title}\n\n")

        f.write("THUMBNAIL TEXT:\n")
        f.write(f"{seo_metadata.thumbnail_text}\n\n")

        f.write("HASHTAGS:\n")
        f.write(" ".join(seo_metadata.hashtags) + "\n\n")

        f.write("TAGS:\n")
        f.write(", ".join(seo_metadata.tags) + "\n\n")

        f.write("DESCRIPTION:\n")
        f.write(seo_metadata.description + "\n\n")

        f.write("---\n")
        f.write("Generated by SPEAK ENGLISH SMARTER SEO Agent\n")

    print(f"✅ SEO metadata saved to: {seo_path}")
    print(f"   - Title: {seo_metadata.title}")
    print(f"   - Thumbnail Text: {seo_metadata.thumbnail_text}")
    print(f"   - Hashtags: {len(seo_metadata.hashtags)} items")
    print(f"   - Tags: {len(seo_metadata.tags)} items")
    print(f"   - Description: ~{len(seo_metadata.description.split())} words")

    return seo_path
