"""
Phase 5: Thumbnail Text Overlay Agent
Adds SEO-optimized text overlay to generated thumbnails using OpenAI Image Edit API.
Text positioning, styling, and colors are intelligently determined by OpenAI based on image content.
"""

from pathlib import Path
from typing import Optional
from openai import OpenAI
from .. import config
from ..models import SEOMetadata, ImageMetadata


def _build_flexible_prompt(
    thumbnail_text: str,
    topic: Optional[str] = None,
    context: Optional[str] = None
) -> str:
    """
    Build an intelligent, image-aware prompt for OpenAI text overlay.

    Lets OpenAI analyze the thumbnail image and determine:
    - Best text positioning (based on character/subject positions)
    - Best text styling (bold, effects, etc.)
    - Best text color (for maximum mobile readability)
    - Best font size (for impact and legibility)

    Args:
        thumbnail_text: Text to add (from SEO metadata)
        topic: Video topic (optional, for context)
        context: Additional context (optional)

    Returns:
        Flexible prompt string that guides OpenAI's analysis and optimization
    """

    # Build context information
    context_info = ""
    if topic:
        context_info += f"\nVideo Topic: {topic}\n"
    if context:
        context_info += f"Additional Context: {context}\n"

    # Main flexible prompt with priority hierarchy
    prompt = f"""This is a YouTube thumbnail for the SPEAK ENGLISH SMARTER English learning channel.
Add the following text to this thumbnail: "{thumbnail_text}"{context_info}

ANALYSIS FIRST - Study this thumbnail image:
- Identify where the main characters/subjects are positioned
- Locate empty/clear spaces available for text overlay
- Analyze the image composition (scenario type: home, office, travel, etc.)
- Determine the natural positioning based on where space exists

PRIMARY GOAL - Make text EYE-CATCHING and ATTENTION-GRABBING:
- Use bold, impactful styling that captures attention in YouTube feed
- Apply high contrast colors (not subtle - make it POP)
- Position text in the best available space found above
- Strong visual weight so viewers notice it immediately when scrolling

CONSTRAINT - Must be READABLE on mobile (375px phone screens):
- Font size must be large enough for small screens
- Use clear, crisp letters - no overly fancy fonts
- Ensure high contrast ratio for legibility
- Test: A viewer scrolling YouTube on a phone should clearly read this text

REQUIREMENT - Maintain professional SPEAK ENGLISH SMARTER brand appearance:
- Don't use garish or neon colors - keep professional tone
- Position text to avoid covering main characters/subjects
- Text should enhance the thumbnail, not clash with design
- Use available space intelligently based on actual image layout

OPTIMIZATION - For YouTube platform:
- Avoid positioning text at outer edges (YouTube UI elements near ~30px margins)
- Position text in the safe area specific to THIS thumbnail's composition
- Consider YouTube's compressed thumbnail display format

DECISION: Based on your analysis above, determine and apply the optimal:
✓ Text position (top, bottom, left, right, center - based on where space exists)
✓ Text color (best contrast for mobile visibility)
✓ Text style (bold, shadow, outline - whatever optimizes impact)
✓ Text size (auto-scaled for readability and impact at 375px width)

Execute: Add the text "{thumbnail_text}" with your optimized positioning and styling."""

    return prompt


def edit_thumbnail_image(
    thumbnail_path: Path,
    seo_metadata: SEOMetadata,
    output_folder: Path,
    topic: Optional[str] = None,
    context: Optional[str] = None
) -> Optional[ImageMetadata]:
    """
    Add SEO-optimized text overlay to generated thumbnail.

    Uses OpenAI's image edit API with intelligent prompting to add text that:
    - Grabs attention in YouTube feed
    - Is readable on mobile (375px)
    - Maintains professional appearance
    - Avoids covering main subjects

    Args:
        thumbnail_path: Path to generated thumbnail image
        seo_metadata: SEOMetadata object containing thumbnail_text
        output_folder: Output folder for edited thumbnail
        topic: Video topic (optional, for context)
        context: Additional context (optional)

    Returns:
        ImageMetadata with updated thumbnail info, or None on error
    """

    print(f"\nAdding text overlay to thumbnail...")
    print("=" * 60)

    try:
        # Verify thumbnail exists
        if not thumbnail_path.exists():
            print(f"ERROR: Thumbnail not found at {thumbnail_path}")
            return None

        # Get OpenAI API key
        if not config.OPENAI_API_KEY:
            print("ERROR: OPENAI_API_KEY not set")
            return None

        # Initialize OpenAI client
        client = OpenAI(api_key=config.OPENAI_API_KEY)

        # Extract text from SEO metadata
        thumbnail_text = seo_metadata.thumbnail_text
        if not thumbnail_text:
            print("WARNING: No thumbnail text in SEO metadata")
            return None

        print(f"Text to add: '{thumbnail_text}'")

        # Build intelligent, flexible prompt
        edit_prompt = _build_flexible_prompt(thumbnail_text, topic, context)

        print("Calling OpenAI Image Edit API...")
        print(f"Strategy: Let AI analyze image and determine optimal positioning...")

        # Call OpenAI Image Edit API
        # Note: No mask needed - we let OpenAI analyze the image
        with open(thumbnail_path, "rb") as image_file:
            response = client.images.edit(
                image=image_file,
                prompt=edit_prompt,
                model=config.TEXT_OVERLAY_MODEL,
                size=config.TEXT_OVERLAY_SIZE,
                n=1,
                quality=config.TEXT_OVERLAY_QUALITY
            )

        # Extract edited image from response
        if not response.data or len(response.data) == 0:
            print("ERROR: No response data from OpenAI API")
            return None

        image_data = response.data[0]

        # Handle both URL and base64 responses
        if hasattr(image_data, 'url') and image_data.url:
            import urllib.request
            print(f"Downloading edited image from URL...")
            edited_thumbnail_path = output_folder / "thumbnail_with_text.png"
            urllib.request.urlretrieve(image_data.url, str(edited_thumbnail_path))
            with open(edited_thumbnail_path, "rb") as f:
                image_bytes = f.read()
        elif hasattr(image_data, 'b64_json') and image_data.b64_json:
            import base64
            image_bytes = base64.b64decode(image_data.b64_json)
            edited_thumbnail_path = output_folder / "thumbnail_with_text.png"
        else:
            print("ERROR: No image data in response")
            return None

        # Save edited thumbnail with new name (preserve original thumbnail.png)
        output_folder.mkdir(parents=True, exist_ok=True)
        edited_thumbnail_path = output_folder / "thumbnail_with_text.png"
        with open(edited_thumbnail_path, "wb") as f:
            f.write(image_bytes)

        print(f"✓ Edited thumbnail saved: {edited_thumbnail_path}")
        print(f"  Size: {len(image_bytes) / 1024:.1f} KB")
        print(f"  Text added: '{thumbnail_text}'")
        print(f"  Positioning: AI-determined (image-aware, mobile-optimized)")
        print(f"  Original preserved: {output_folder / 'thumbnail.png'}")

        # Create metadata
        metadata = ImageMetadata(
            topic=seo_metadata.title if hasattr(seo_metadata, 'title') else "Unknown",
            image_type="thumbnail_with_text",
            file_path=str(edited_thumbnail_path),
            resolution=config.TEXT_OVERLAY_SIZE,
            generation_model=config.TEXT_OVERLAY_MODEL,
            prompt_used="Flexible image-aware text overlay prompt"
        )

        print("✓ Text overlay completed successfully")
        return metadata

    except Exception as e:
        print(f"ERROR: Text overlay failed - {str(e)}")
        import traceback
        traceback.print_exc()
        return None
