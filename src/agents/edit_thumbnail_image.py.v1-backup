"""
Phase 5: Thumbnail Text Overlay Agent (ENHANCED - Hybrid Approach)
Combines:
- AI image analysis for color guidance (dynamic colors, not fixed)
- OpenAI rendering (professional quality visuals)
"""

from pathlib import Path
from typing import Optional, Dict, List, Tuple
from openai import OpenAI
from PIL import Image
import json
import base64
from .. import config
from ..models import SEOMetadata, ImageMetadata


def _build_color_analysis_prompt(thumbnail_text: str, topic: Optional[str] = None) -> str:
    """
    Build prompt for AI to analyze image colors and suggest text colors.
    Returns JSON with dominant colors and recommended text color.
    """

    prompt = f"""Analyze this YouTube thumbnail for the SPEAK ENGLISH SMARTER channel.
Text to add: "{thumbnail_text}"
{f'Topic: {topic}' if topic else ''}

ANALYZE and return JSON ONLY:
{{
  "dominant_colors": ["#HEX1", "#HEX2", "#HEX3"],
  "background_brightness": "dark|light|medium",
  "recommended_text_color": "#HEX",
  "text_position": "top_left|top_center|top_right|center_left|center|center_right|bottom_left|bottom_center|bottom_right",
  "text_style": "bold_white_shadow|bold_yellow_glow|bold_cyan_shadow|bold_orange_outline",
  "contrast_ratio": 7.5
}}

Consider:
1. Image's dominant colors for complementary text
2. Background brightness for text visibility
3. Best empty space for text placement
4. Professional styling (not garish)

Return ONLY valid JSON."""

    return prompt


def _extract_image_colors_local(image_path: Path) -> List[Tuple[int, int, int]]:
    """
    Extract dominant colors from thumbnail using PIL for analysis.
    """
    try:
        print(f"[DATA] Analyzing image colors...")

        img = Image.open(image_path)
        img_small = img.copy()
        img_small.thumbnail((100, 100))

        if img_small.mode != 'RGB':
            img_small = img_small.convert('RGB')

        pixels = list(img_small.getdata())
        color_freq = {}

        for pixel in pixels:
            pixel_tuple = tuple(pixel[:3])
            color_freq[pixel_tuple] = color_freq.get(pixel_tuple, 0) + 1

        dominant = sorted(color_freq.items(), key=lambda x: x[1], reverse=True)[:3]
        colors = [color[0] for color in dominant]

        for i, color in enumerate(colors):
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            print(f"   Color {i+1}: {hex_color}")

        return colors

    except Exception as e:
        print(f"[WARN] Color extraction failed: {str(e)}")
        return []


def _build_rendering_prompt(
    thumbnail_text: str,
    dominant_colors: List[str],
    text_color: str,
    text_position: str,
    text_style: str,
    topic: Optional[str] = None
) -> str:
    """
    Build enhanced prompt for OpenAI to render text with dynamic colors.
    """

    colors_str = ", ".join(dominant_colors[:3])

    prompt = f"""Add professional text overlay to this YouTube thumbnail for SPEAK ENGLISH SMARTER.

TEXT TO ADD: "{thumbnail_text}"
{f'TOPIC: {topic}' if topic else ''}

STYLING REQUIREMENTS:
- Text: "{thumbnail_text}"
- Position: {text_position} area of the frame
- Style: {text_style}
- Text Color: {text_color} (recommended for this image)
- Image Dominant Colors: {colors_str}

IMPORTANT:
- Make text EYE-CATCHING and READABLE on mobile (375px screens)
- Use PROFESSIONAL styling (bold, shadow, or glow effects)
- Avoid covering main characters/subjects
- Maintain brand appearance (not garish or neon)
- Use {text_color} for TEXT color (this color has good contrast on this image)
- Position text in the {text_position} area where there's available space
- Apply shadow or outline effects for depth and readability

QUALITY:
- High-quality professional rendering
- Text must be clearly readable
- Professional YouTube thumbnail appearance
- Dynamic styling (not static/plain)"""

    return prompt


def _get_color_suggestions(
    analysis: Dict,
    dominant_colors: List[Tuple[int, int, int]]
) -> Tuple[str, str, str]:
    """
    Extract color and styling suggestions from AI analysis.
    Returns: (text_color_hex, text_position, text_style)
    """

    text_color = analysis.get("recommended_text_color", "#FFFFFF")
    text_position = analysis.get("text_position", "bottom_center")
    text_style = analysis.get("text_style", "bold_white_shadow")

    return text_color, text_position, text_style


def edit_thumbnail_image(
    thumbnail_path: Path,
    seo_metadata: SEOMetadata,
    output_folder: Path,
    topic: Optional[str] = None,
    context: Optional[str] = None
) -> Optional[ImageMetadata]:
    """
    Add professional, dynamic text overlay to thumbnail.

    Hybrid approach:
    1. AI analyzes image to determine colors & positioning
    2. Enhanced prompt tells OpenAI to use those dynamic colors
    3. OpenAI renders professionally (best visual quality)

    Args:
        thumbnail_path: Path to generated thumbnail image
        seo_metadata: SEOMetadata object containing thumbnail_text
        output_folder: Output folder for edited thumbnail
        topic: Video topic (optional)
        context: Additional context (optional)

    Returns:
        ImageMetadata with updated thumbnail info, or None on error
    """

    print(f"\n{'='*60}")
    print(f"PHASE 5: Thumbnail Text Overlay (Enhanced - Dynamic Colors)")
    print(f"{'='*60}")

    try:
        # Verify inputs
        if not thumbnail_path.exists():
            print(f"[ERROR] Thumbnail not found: {thumbnail_path}")
            return None

        if not config.OPENAI_API_KEY:
            print(f"[ERROR] OPENAI_API_KEY not set")
            return None

        thumbnail_text = seo_metadata.thumbnail_text
        if not thumbnail_text:
            print(f"[WARN] No thumbnail text in SEO metadata")
            return None

        print(f"[TEXT] Adding text: '{thumbnail_text}'")

        # Step 1: Local color analysis
        print(f"\n[ANALYSIS] Analyzing image colors locally...")
        dominant_colors = _extract_image_colors_local(thumbnail_path)
        dominant_colors_hex = []
        if dominant_colors:
            dominant_colors_hex = ['#{:02x}{:02x}{:02x}'.format(*color) for color in dominant_colors]

        # Step 2: AI image analysis for positioning & color suggestions
        print(f"[ANALYSIS] Calling OpenAI for image analysis...")
        client = OpenAI(api_key=config.OPENAI_API_KEY)

        color_analysis_prompt = _build_color_analysis_prompt(thumbnail_text, topic)

        # Read image as base64 for analysis
        with open(thumbnail_path, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode()

        analysis_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_b64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": color_analysis_prompt
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        analysis_text = analysis_response.choices[0].message.content

        # Parse color analysis
        analysis = {}
        try:
            json_start = analysis_text.find('{')
            json_end = analysis_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = analysis_text[json_start:json_end]
                analysis = json.loads(json_str)
        except:
            print(f"[WARN] Could not parse color analysis, using defaults")

        text_color, text_position, text_style = _get_color_suggestions(analysis, dominant_colors)

        print(f"[ANALYSIS] Suggested color: {text_color}")
        print(f"[ANALYSIS] Position: {text_position}")
        print(f"[ANALYSIS] Style: {text_style}")

        # Step 3: Enhanced rendering prompt
        rendering_prompt = _build_rendering_prompt(
            thumbnail_text,
            dominant_colors_hex,
            text_color,
            text_position,
            text_style,
            topic
        )

        # Step 4: Call OpenAI Image Edit API with enhanced prompt
        print(f"\n[RENDER] Calling OpenAI Image Edit API with dynamic colors...")

        with open(thumbnail_path, "rb") as image_file:
            edit_response = client.images.edit(
                image=image_file,
                prompt=rendering_prompt,
                model=config.TEXT_OVERLAY_MODEL,
                size=config.TEXT_OVERLAY_SIZE,
                n=1,
                quality=config.TEXT_OVERLAY_QUALITY
            )

        if not edit_response.data or len(edit_response.data) == 0:
            print(f"[ERROR] No response from OpenAI Image Edit API")
            return None

        image_data = edit_response.data[0]

        # Step 5: Download and save edited image
        output_folder.mkdir(parents=True, exist_ok=True)

        if hasattr(image_data, 'url') and image_data.url:
            import urllib.request
            print(f"[DOWNLOAD] Getting edited image from URL...")
            edited_thumbnail_path = output_folder / "thumbnail_with_text.png"
            urllib.request.urlretrieve(image_data.url, str(edited_thumbnail_path))
            with open(edited_thumbnail_path, "rb") as f:
                image_bytes = f.read()
        elif hasattr(image_data, 'b64_json') and image_data.b64_json:
            print(f"[SAVE] Decoding base64 image...")
            image_bytes = base64.b64decode(image_data.b64_json)
            edited_thumbnail_path = output_folder / "thumbnail_with_text.png"
        else:
            print(f"[ERROR] No image data in response")
            return None

        # Save the edited thumbnail
        edited_thumbnail_path = output_folder / "thumbnail_with_text.png"
        with open(edited_thumbnail_path, "wb") as f:
            f.write(image_bytes)

        print(f"[SAVE] Text overlay saved: {edited_thumbnail_path.name}")
        print(f"       Size: {len(image_bytes) / 1024:.1f} KB")
        print(f"       Text: '{thumbnail_text}'")
        print(f"       Color: {text_color}")
        print(f"       Position: {text_position}")

        # Create metadata
        metadata = ImageMetadata(
            topic=seo_metadata.title if hasattr(seo_metadata, 'title') else "Unknown",
            image_type="thumbnail_with_text",
            file_path=str(edited_thumbnail_path),
            resolution=config.TEXT_OVERLAY_SIZE,
            generation_model="OpenAI (Enhanced with dynamic colors)",
            prompt_used="Hybrid approach: AI analysis + enhanced rendering"
        )

        print(f"\n[DONE] Text overlay completed successfully")

        return metadata

    except Exception as e:
        print(f"[ERROR] Text overlay failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
