"""
Phase 4: Video Scene Image Generation Agent
Generates long-form video scene images using OpenAI (GPT-Image-2.5-Sunburst) API.
"""

from pathlib import Path
from typing import Optional
import base64
from .. import config
from ..models import Script, SEOMetadata, ImageMetadata


def _load_canonical_references() -> dict:
    """Load canonical video reference images."""
    print("Loading canonical video references...")

    references = {
        'descriptions': [],
        'file_paths': []
    }

    if 'video' not in config.CANONICAL_REFERENCES:
        return references

    ref_paths = config.CANONICAL_REFERENCES['video']

    for ref_path in ref_paths:
        if ref_path.exists():
            references['file_paths'].append(ref_path)
            print(f"✓ Found: {ref_path.name}")
        else:
            print(f"⚠ Missing: {ref_path}")

    references['descriptions'] = [
        "This is the canonical video conversation scene reference for SPEAK ENGLISH SMARTER.",
        "Core layout: Sarah seated on left, Alex on right, face-to-face podcast conversation.",
        "Maintain the professional podcast setup with microphones from the reference.",
        "Keep the warm, inviting, cinematic atmosphere shown in the reference.",
        "Transform only the environment and props to match the topic - preserve the core layout and character consistency.",
        "Both characters should maintain their canonical appearance while adapting clothing and surroundings to the topic."
    ]

    return references


def _build_enhanced_prompt(prompt_template: str, topic: str, context: Optional[str],
                          seo_metadata: Optional[SEOMetadata], references: dict) -> str:
    """Build enhanced prompt for video scene generation."""
    prompt = prompt_template

    prompt = prompt.replace("[TOPIC]", topic)
    scene_context = context or "Natural conversation"
    prompt = prompt.replace("[SCENE]", scene_context)
    prompt = prompt.replace("[AUTO | LEFT | RIGHT | TOP | BOTTOM | CENTER]", "CENTER")

    professional_emphasis = """
ILLUSTRATION STYLE (CRITICAL - MUST MATCH CANONICAL REFERENCE):

Character & Art Style
• Create in FLAT VECTOR ILLUSTRATION style, NOT photorealistic
• Characters must match canonical reference's premium illustration quality
• Use clean, modern vector art aesthetic
• Maintain consistent illustration style for both Sarah and Alex
• Both characters should look like animated/illustrated characters, not realistic people

Color & Style
• Use SOFT, MUTED tones throughout (matching canonical reference palette)
• Scene should feel WARM, INVITING, and CINEMATIC
• NO bright, saturated, or neon colors
• Keep all colors gentle and pleasant

Environment Design (CRITICAL)
• MINIMAL DECORATION - keep background CLEAN and PROFESSIONAL
• Use MAXIMUM 1-2 small plants as subtle accents only
• NO excessive plants, vines, hanging greenery, or jungle-like appearance
• Professional office/studio aesthetic (desk, shelving, modern lighting)
• Avoid clutter, overcrowding, or distracting decorative elements
• Environment should also be illustrated in flat vector style to match characters

Focus & Composition
• Characters (Sarah & Alex) are the CLEAR FOCAL POINTS
• Microphones should be visually prominent and professional
• Minimal competing visual elements
• Clean, unobstructed sightlines between hosts
• This is a PODCAST STUDIO / TALK SHOW setting

Overall Aesthetic
• Premium, professional, modern, clean
• Flat vector illustration throughout (not photorealistic)
• Minimal decoration approach (quality over quantity)
• Suitable for long viewing sessions
• Educational and professional tone
"""

    if references and references['descriptions']:
        reference_context = "\n\nCANONICAL REFERENCE CONTEXT:\n"
        reference_context += "\n".join(f"• {desc}" for desc in references['descriptions'])
        prompt = reference_context + professional_emphasis + "\n\n" + prompt
    else:
        prompt = professional_emphasis + "\n\n" + prompt

    if seo_metadata:
        seo_context = f"\n\nVIDEO CONTEXT:\n"
        seo_context += f"• Video Title: {seo_metadata.title}\n"
        seo_context += f"• Theme: {seo_metadata.description[:100]}...\n"
        prompt += seo_context

    return prompt


def generate_video_scene(script: Script, seo_metadata: Optional[SEOMetadata],
                        output_folder: Path, context: Optional[str] = None) -> Optional[ImageMetadata]:
    """Generate long-form video scene image."""

    print(f"\nGenerating video scene for: {script.topic}")
    print("=" * 60)

    try:
        from openai import OpenAI

        if not config.OPENAI_API_KEY:
            print("OpenAI API key not set")
            return None

        client = OpenAI(api_key=config.OPENAI_API_KEY)

        prompt_path = config.PROMPTS_DIR / "Video Image- Prompt.txt"
        if not prompt_path.exists():
            print(f"Video prompt not found at {prompt_path}")
            return None

        with open(prompt_path, 'r', encoding='utf-8') as f:
            video_prompt = f.read()

        references = _load_canonical_references()

        full_prompt = _build_enhanced_prompt(
            video_prompt,
            script.topic,
            context,
            seo_metadata,
            references
        )

        print("Calling OpenAI API for video scene generation...")

        response = client.images.generate(
            prompt=full_prompt,
            model=config.IMAGE_GENERATION_MODEL,
            size=config.VIDEO_SCENE_SIZE,
            n=1,
            quality="high"
        )

        output_folder.mkdir(parents=True, exist_ok=True)
        video_path = output_folder / "video_scene.png"

        if response.data and len(response.data) > 0:
            image_data = response.data[0]

            # Handle both b64_json and url responses
            if hasattr(image_data, 'b64_json') and image_data.b64_json:
                image_bytes = base64.b64decode(image_data.b64_json)
            elif hasattr(image_data, 'url') and image_data.url:
                import urllib.request
                urllib.request.urlretrieve(image_data.url, str(video_path))
                with open(video_path, 'rb') as f:
                    image_bytes = f.read()
            else:
                print("ERROR: No image data in response")
                return None

            with open(video_path, 'wb') as f:
                f.write(image_bytes)

            print(f"Video scene generated: {video_path}")
            print(f"Size: {len(image_bytes) / 1024:.1f} KB")

            metadata = ImageMetadata(
                topic=script.topic,
                image_type="video_scene",
                file_path=str(video_path),
                resolution=config.VIDEO_SCENE_SIZE,
                generation_model=config.IMAGE_GENERATION_MODEL,
                prompt_used="Video Image- Prompt.txt"
            )

            print("Video scene completed successfully")
            return metadata
        else:
            print("ERROR: No response data from API")
            return None

    except Exception as e:
        print(f"Error generating video scene: {str(e)}")
        return None
