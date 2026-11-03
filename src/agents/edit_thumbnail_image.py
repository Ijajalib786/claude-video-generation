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
from ..models import Script, SEOMetadata, ImageMetadata


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


# ---------------------------------------------------------------------------
# Redesign pass (brief-driven). Used instead of the plain text overlay when
# config.THUMBNAIL_REDESIGN_ENABLED is True. Never raises: on any problem the
# caller falls back to the plain text overlay below.
# ---------------------------------------------------------------------------

def _default_brief(seo_metadata: SEOMetadata, topic: Optional[str]) -> Dict:
    """Safe brief used when the brief step fails."""
    return {
        "scene": "a bright, natural setting that fits the topic",
        "camera": "medium two-shot",
        "sarah_action": "talking and gesturing with an open hand",
        "alex_action": "listening with a friendly smile",
        "emotion": "warm and friendly",
        "template": "A",
        "topic_line": (topic or seo_metadata.title)[:40],
        "checklist": [],
        "bubbles": [],
        "props": [],
    }


def _clean_brief(raw, default: Dict) -> Dict:
    """Keep only valid values from the model's JSON; fill the rest from the default."""
    brief = dict(default)
    if not isinstance(raw, dict):
        return brief
    for key in ("scene", "camera", "sarah_action", "alex_action", "emotion", "topic_line"):
        value = raw.get(key)
        if isinstance(value, str) and value.strip():
            brief[key] = value.strip()
    template = str(raw.get("template", "A")).strip().upper()
    brief["template"] = template if template in config.THUMBNAIL_TEMPLATES else "A"
    for key, max_items, max_len in (("checklist", 5, 24), ("bubbles", 4, 40), ("props", 3, 30)):
        items = raw.get(key)
        if isinstance(items, list):
            cleaned = [str(x).strip() for x in items if str(x).strip() and len(str(x).strip()) <= max_len]
            brief[key] = cleaned[:max_items]
    return brief


def _get_redesign_brief(
    thumbnail_path: Path,
    seo_metadata: SEOMetadata,
    topic: Optional[str],
    context: Optional[str],
    script: Optional[Script],
) -> Dict:
    """Ask Claude (with the base thumbnail and the script) for a redesign brief."""
    default = _default_brief(seo_metadata, topic)
    try:
        from anthropic import Anthropic

        template = config.THUMBNAIL_BRIEF_PROMPT_PATH.read_text(encoding="utf-8")
        script_text = ""
        if script is not None:
            script_text = "\n".join(f"{line.speaker} : {line.content}" for line in script.lines)

        user_text = (
            template.replace("{TITLE}", seo_metadata.title)
            .replace("{HEADLINE}", seo_metadata.thumbnail_text)
            .replace("{TOPIC}", topic or seo_metadata.title)
            .replace("{CONTEXT}", context or "None")
            .replace("{SCRIPT}", script_text or "(not available)")
        )

        with open(thumbnail_path, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode()

        client = Anthropic(api_key=config.ANTHROPIC_API_KEY) if config.ANTHROPIC_API_KEY else Anthropic()
        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=1200,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
                    {"type": "text", "text": user_text},
                ],
            }],
        )
        text = next((b.text for b in response.content if hasattr(b, "text")), "")
        start, end = text.find("{"), text.rfind("}") + 1
        raw = json.loads(text[start:end]) if start >= 0 and end > start else None
        return _clean_brief(raw, default)
    except Exception as e:
        print(f"[WARN] Redesign brief failed, using the default brief: {e}")
        return default


def _build_redesign_prompt(seo_metadata: SEOMetadata, brief: Dict) -> str:
    """Fill the redesign prompt template with the brief and the exact text to draw."""
    template = config.THUMBNAIL_REDESIGN_PROMPT_PATH.read_text(encoding="utf-8")
    checklist = "\n".join(f'  - "{item}"' for item in brief["checklist"]) or "  (none)"
    bubbles = "\n".join(f'  - "{item}"' for item in brief["bubbles"]) or "  (none)"
    props = ", ".join(brief["props"]) or "only what the scene needs"
    values = {
        "{SCENE}": brief["scene"],
        "{CAMERA}": brief["camera"],
        "{SARAH_ACTION}": brief["sarah_action"],
        "{ALEX_ACTION}": brief["alex_action"],
        "{EMOTION}": brief["emotion"],
        "{PROPS}": props,
        "{LAYOUT}": config.THUMBNAIL_TEMPLATES[brief["template"]],
        "{HEADLINE}": seo_metadata.thumbnail_text,
        "{TOPIC_LINE}": brief["topic_line"],
        "{TAG}": config.THUMBNAIL_TAG_TEXT,
        "{CHECKLIST}": checklist,
        "{BUBBLES}": bubbles,
    }
    prompt = template
    for placeholder, value in values.items():
        prompt = prompt.replace(placeholder, value)
    return prompt


def _save_edit_response(edit_response, target: Path) -> bool:
    """Save an images.edit response (b64 or url) to target. Returns True on success."""
    if not edit_response.data:
        return False
    image_data = edit_response.data[0]
    if hasattr(image_data, "b64_json") and image_data.b64_json:
        target.write_bytes(base64.b64decode(image_data.b64_json))
        return True
    if hasattr(image_data, "url") and image_data.url:
        import urllib.request
        urllib.request.urlretrieve(image_data.url, str(target))
        return True
    return False


def _redesign_thumbnail(
    thumbnail_path: Path,
    seo_metadata: SEOMetadata,
    output_folder: Path,
    topic: Optional[str],
    context: Optional[str],
    script: Optional[Script],
) -> Optional[ImageMetadata]:
    """Brief step + redesign edit. Returns None on any failure (caller falls back)."""
    try:
        print(f"[BRIEF] Planning the redesign (scene, poses, text) ...")
        brief = _get_redesign_brief(thumbnail_path, seo_metadata, topic, context, script)
        output_folder.mkdir(parents=True, exist_ok=True)
        (output_folder / "thumbnail_brief.json").write_text(json.dumps(brief, indent=2), encoding="utf-8")
        print(f"[BRIEF] Scene: {brief['scene']} | Template {brief['template']}")

        prompt = _build_redesign_prompt(seo_metadata, brief)
        client = OpenAI(api_key=config.OPENAI_API_KEY)

        saved = []
        for n in range(1, config.THUMBNAIL_REDESIGN_VARIANTS + 1):
            print(f"[RENDER] Redesign pass {n}/{config.THUMBNAIL_REDESIGN_VARIANTS} ...")
            files = [open(thumbnail_path, "rb")]
            files += [open(p, "rb") for p in config.THUMBNAIL_IDENTITY_REFS if Path(p).exists()]
            try:
                edit_response = client.images.edit(
                    image=files[0] if len(files) == 1 else files,
                    prompt=prompt,
                    model=config.TEXT_OVERLAY_MODEL,
                    size=config.TEXT_OVERLAY_SIZE,
                    n=1,
                    quality=config.TEXT_OVERLAY_QUALITY,
                )
            finally:
                for f in files:
                    f.close()
            target = output_folder / ("thumbnail_with_text.png" if n == 1 else f"thumbnail_with_text_v{n}.png")
            if _save_edit_response(edit_response, target):
                saved.append(target)
                print(f"[SAVE] {target.name} ({target.stat().st_size / 1024:.1f} KB)")

        if not saved:
            return None
        return ImageMetadata(
            topic=seo_metadata.title,
            image_type="thumbnail_with_text",
            file_path=str(saved[0]),
            resolution=config.TEXT_OVERLAY_SIZE,
            generation_model=config.TEXT_OVERLAY_MODEL,
            prompt_used="Thumbnail Redesign- Prompt.txt + brief"
        )
    except Exception as e:
        print(f"[WARN] Redesign pass failed: {e}")
        return None


def edit_thumbnail_image(
    thumbnail_path: Path,
    seo_metadata: SEOMetadata,
    output_folder: Path,
    topic: Optional[str] = None,
    context: Optional[str] = None,
    script: Optional[Script] = None
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

        # Redesign pass (brief-driven); falls back to the plain text overlay below if it fails
        if config.THUMBNAIL_REDESIGN_ENABLED:
            redesigned = _redesign_thumbnail(thumbnail_path, seo_metadata, output_folder, topic, context, script)
            if redesigned:
                print(f"\n[DONE] Thumbnail redesign completed successfully")
                return redesigned
            print(f"[WARN] Redesign unavailable, falling back to the plain text overlay")

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
