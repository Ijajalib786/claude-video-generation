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
YOUTUBE SEO STRATEGY (2026) - MAXIMUM VIEWS FOCUS

1. TITLE OPTIMIZATION (≤65 chars):
   - Format: [Verb/Question] + [Benefit] + [Specificity]
   - Include long-tail keyword (topic-specific)
   - Balance searchability with clickability
   - Example: "How to Apologize Politely in English | Learn Natural Phrases"

2. DESCRIPTION OPTIMIZATION (350+ words):
   - Hook (first 150 chars): Most important keywords, compelling
   - Body: Explain what viewers will learn, educational value
   - Keywords: Sprinkle naturally (3-5 main keywords)
   - Calls-to-action: "Like", "Subscribe", "Comment"
   - Related: Suggest related topics
   - Timestamps: Major sections if applicable
   - Minimum: 350 words (aim for 350-500)

3. HASHTAGS (15-20 total):
   - 40% High-volume (#learnEnglish, #englishconversation)
   - 40% Medium-volume niche (#englishphrases, #conversationalenglish)
   - 20% Long-tail specific (#howtoapologizepolitely)
   - Avoid: Hashtags with <10K views
   - Priority: Relevance over viral potential

4. TAGS (15-20 total):
   - Main: Topic keyword phrase
   - Related: Broader learning categories
   - Specific: Long-tail variations
   - Trending: Current English learning trends (conversational English, practical English)
   - Brand: "SPEAK ENGLISH SMARTER"

5. THUMBNAIL TEXT (1 line, compelling):
   - Verb + Benefit OR Curiosity gap
   - ALL CAPS or Key words capitalized
   - Examples: "SAY NO POLITELY", "APOLOGIZE LIKE A NATIVE", "PERFECT APOLOGY?"
   - Urgent, action-oriented tone
   - Max 100 characters
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
        - title: Optimized, 65 chars max
        - description: Keyword-rich, 500+ words
        - hashtags: 15-20 trending/relevant hashtags
        - tags: 15-20 SEO tags
        - thumbnail_text: Single compelling text overlay
    """

    seo_prompt = load_seo_prompt()

    system_message = f"""You are a YouTube SEO expert optimizing titles, descriptions, hashtags, tags, and thumbnail text
for an English learning channel (SPEAK ENGLISH SMARTER).

GOAL: Maximize search traffic and views through trend-based optimization for 2026.

{SEO_STRATEGY}

SCRIPT CONTEXT:
Topic: {script.topic}
Word Count: {script.word_count}
Estimated Duration: {script.estimated_duration_minutes:.1f} minutes

SEO PROMPT GUIDE:
{seo_prompt}

Generate SEO metadata that will attract maximum views while maintaining YouTube algorithm best practices.
Focus on trending keywords in the English learning space (conversational English, practical communication, real-world scenarios).

Your output MUST be valid JSON with this exact structure:
{{
  "title": "exact title (max 65 chars)",
  "description": "full description (350+ words)",
  "hashtags": ["#hashtag1", "#hashtag2", ... 20 items total],
  "tags": ["tag1", "tag2", ... 20 items total],
  "thumbnail_text": "COMPELLING TEXT FOR THUMBNAIL"
}}

CRITICAL:
- Title must be ≤65 characters
- Description must be 350+ words (aim for 350-500)
- Hashtags must be exactly 15-20 items
- Tags must be exactly 15-20 items
- Thumbnail text must be 3-100 characters
- JSON must be properly formatted"""

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
