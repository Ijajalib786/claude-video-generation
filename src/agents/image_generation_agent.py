"""
Phase 4: Image Generation Agent
Generates thumbnail and long-form video images using OpenAI (GPT-Image-2.5-Sunburst) API.
Uses canonical reference images for character consistency and enhanced prompts.
"""

from pathlib import Path
from typing import Optional
import base64
from .. import config
from ..models import Script, SEOMetadata, ImageMetadata


def _load_canonical_references(reference_type: str) -> dict:
    """
    Load canonical reference images and encode as base64.

    Args:
        reference_type: 'thumbnail' or 'video'

    Returns:
        dict with reference descriptions and file paths
    """
    print(f"   📸 Loading canonical {reference_type} references...")

    references = {
        'descriptions': [],
        'file_paths': []
    }

    if reference_type not in config.CANONICAL_REFERENCES:
        print(f"   ⚠️  No canonical references found for {reference_type}")
        return references

    ref_paths = config.CANONICAL_REFERENCES[reference_type]

    for ref_path in ref_paths:
        if ref_path.exists():
            references['file_paths'].append(ref_path)
            print(f"   ✓ Found: {ref_path.name}")
        else:
            print(f"   ⚠️  Missing: {ref_path}")

    # Create reference descriptions for prompt inclusion
    if reference_type == 'thumbnail':
        references['descriptions'] = [
            "This is a canonical reference showing the SPEAK ENGLISH SMARTER character style.",
            "Sarah (age 24, English teacher): Oval face, warm skin tone, almond brown eyes, shoulder-length dark brown hair with side-part.",
            "Alex (age 25, English learner): Slightly rounded face, warm skin tone, brown eyes, short textured black hair.",
            "Use these reference images as the primary source of truth for character consistency.",
            "Characters must look identical across all videos - only clothing, expressions, and poses may change.",
            "Maintain the premium flat vector illustration style shown in the references."
        ]
    elif reference_type == 'video':
        references['descriptions'] = [
            "This is the canonical video conversation scene reference for SPEAK ENGLISH SMARTER.",
            "Core layout: Sarah seated on left, Alex on right, face-to-face podcast conversation.",
            "Maintain the professional podcast setup with microphones from the reference.",
            "Keep the warm, inviting, cinematic atmosphere shown in the reference.",
            "Transform only the environment and props to match the topic - preserve the core layout and character consistency.",
            "Both characters should maintain their canonical appearance while adapting clothing and surroundings to the topic."
        ]

    return references


def _build_enhanced_prompt_video(prompt_template: str, topic: str, context: Optional[str],
                                seo_metadata: Optional[SEOMetadata], references: dict) -> str:
    """
    Build enhanced prompt for VIDEO SCENE (no text area reservation - uses full frame).

    Args:
        prompt_template: Base prompt from file
        topic: Video topic
        context: Optional topic context
        seo_metadata: SEO metadata
        references: Canonical reference descriptions

    Returns:
        Enhanced prompt ready for API call
    """
    # Start with the template
    prompt = prompt_template

    # Replace basic placeholders
    prompt = prompt.replace("[TOPIC]", topic)

    scene_context = context or "Natural conversation"
    prompt = prompt.replace("[SCENE]", scene_context)

    prompt = prompt.replace("[AUTO | LEFT | RIGHT | TOP | BOTTOM | CENTER]", "CENTER")

    # Add professional aesthetic emphasis (clean, minimal, focused on characters)
    professional_emphasis = """
PROFESSIONAL AESTHETIC EMPHASIS:

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

Focus & Composition
• Characters (Sarah & Alex) are the CLEAR FOCAL POINTS
• Microphones should be visually prominent and professional
• Minimal competing visual elements
• Clean, unobstructed sightlines between hosts
• This is a PODCAST STUDIO / TALK SHOW setting

Overall Aesthetic
• Premium, professional, modern, clean
• Minimal decoration approach (quality over quantity)
• Suitable for long viewing sessions
• Educational and professional tone
"""

    # Add canonical reference descriptions
    if references and references['descriptions']:
        reference_context = "\n\nCANONICAL REFERENCE CONTEXT:\n"
        reference_context += "\n".join(f"• {desc}" for desc in references['descriptions'])
        prompt = reference_context + professional_emphasis + "\n\n" + prompt
    else:
        prompt = professional_emphasis + "\n\n" + prompt

    # Add SEO context if available
    if seo_metadata:
        seo_context = f"\n\nVIDEO CONTEXT:\n"
        seo_context += f"• Video Title: {seo_metadata.title}\n"
        seo_context += f"• Theme: {seo_metadata.description[:100]}...\n"
        prompt += seo_context

    return prompt


def _determine_text_area_placement(topic: str, context: Optional[str]) -> dict:
    """
    Analyze topic and context to determine optimal text area placement and colors.

    Args:
        topic: Video topic
        context: Optional topic context

    Returns:
        dict with placement, percentage, and color guidance
    """
    topic_lower = topic.lower()
    context_lower = (context or "").lower()

    # Home/Casual scenarios
    home_keywords = ["home", "bedroom", "kitchen", "living room", "apartment", "house",
                     "casual", "relax", "morning", "evening", "family"]
    if any(kw in topic_lower or kw in context_lower for kw in home_keywords):
        return {
            "placement": "LEFT",
            "percentage": 40,
            "color_tone": "soft beige/cream",
            "background_blend": "warm, earthy background",
            "scenario": "Home/Casual scene"
        }

    # Office/Professional scenarios
    office_keywords = ["office", "work", "job", "interview", "business", "meeting",
                       "professional", "presentation", "corporate", "formal"]
    if any(kw in topic_lower or kw in context_lower for kw in office_keywords):
        return {
            "placement": "TOP",
            "percentage": 30,
            "color_tone": "soft blue/gray",
            "background_blend": "professional ceiling/wall area",
            "scenario": "Office/Professional scene"
        }

    # Travel/Outdoor scenarios
    travel_keywords = ["airport", "travel", "hotel", "beach", "outdoor", "vacation",
                       "trip", "flight", "luggage", "tourism", "mountain", "forest"]
    if any(kw in topic_lower or kw in context_lower for kw in travel_keywords):
        return {
            "placement": "RIGHT",
            "percentage": 35,
            "color_tone": "soft sky/cloud",
            "background_blend": "sky or outdoor background",
            "scenario": "Travel/Outdoor scene"
        }

    # Restaurant/Social scenarios
    restaurant_keywords = ["restaurant", "coffee", "cafe", "food", "dining", "party",
                           "social", "dinner", "lunch", "breakfast", "bar"]
    if any(kw in topic_lower or kw in context_lower for kw in restaurant_keywords):
        return {
            "placement": "LEFT",
            "percentage": 40,
            "color_tone": "soft warm tones",
            "background_blend": "warm, inviting background",
            "scenario": "Restaurant/Social scene"
        }

    # Shopping/Activity scenarios
    activity_keywords = ["shopping", "shop", "activity", "hobby", "gym", "sports",
                        "exercise", "game", "dance", "sport"]
    if any(kw in topic_lower or kw in context_lower for kw in activity_keywords):
        return {
            "placement": "RIGHT",
            "percentage": 35,
            "color_tone": "soft neutral",
            "background_blend": "neutral, light background",
            "scenario": "Shopping/Activity scene"
        }

    # Default: LEFT placement
    return {
        "placement": "LEFT",
        "percentage": 40,
        "color_tone": "soft warm tones",
        "background_blend": "soft, calm background",
        "scenario": "General conversation scene"
    }


def _build_enhanced_prompt(prompt_template: str, topic: str, context: Optional[str],
                          seo_metadata: Optional[SEOMetadata], references: dict,
                          text_position: str = "AUTO") -> str:
    """
    Build enhanced prompt combining template with references and topic context.

    Args:
        prompt_template: Base prompt from file
        topic: Video topic
        context: Optional topic context
        seo_metadata: SEO metadata with thumbnail_text, title, description
        references: Canonical reference descriptions
        text_position: Text placement (AUTO, LEFT, RIGHT, TOP, BOTTOM, CENTER)

    Returns:
        Enhanced prompt ready for API call
    """
    # Start with the template
    prompt = prompt_template

    # Replace basic placeholders
    prompt = prompt.replace("[TOPIC]", topic)

    scene_context = context or "Natural conversation"
    prompt = prompt.replace("[SCENE]", scene_context)

    prompt = prompt.replace("[AUTO | LEFT | RIGHT | TOP | BOTTOM | CENTER]", text_position)

    # Analyze topic for text area placement
    text_area_guidance = _determine_text_area_placement(topic, context)

    # Add text area analysis
    text_area_section = f"""
ADAPTIVE TEXT AREA ANALYSIS FOR THIS TOPIC:

Topic: {topic}
Detected Scenario: {text_area_guidance['scenario']}
Recommended Placement: {text_area_guidance['placement']} side
Reserve: {text_area_guidance['percentage']}% for text overlay
Background Tone: {text_area_guidance['color_tone']}

IMPLEMENTATION:
• Reserve {text_area_guidance['percentage']}% of {text_area_guidance['placement']} side for YouTube text
• Use {text_area_guidance['background_blend']}
• Keep this area CLEAN, UNCLUTTERED, and SOFT-COLORED
• NO characters or objects in the reserved text area
• Background should blend naturally with the scene
"""

    # Add color saturation emphasis
    color_emphasis = """
COLOR SATURATION EMPHASIS:
• Use SOFT, MUTED tones throughout
• This image should feel CALM and INVITING
• Match the sample reference's soft color palette
• NO bright, saturated, or neon colors
• Keep all colors gentle and pleasant for educational viewing
"""

    # Add canonical reference descriptions
    if references and references['descriptions']:
        reference_context = "\n\nCANONICAL REFERENCE CONTEXT:\n"
        reference_context += "\n".join(f"• {desc}" for desc in references['descriptions'])
        prompt = reference_context + text_area_section + color_emphasis + "\n\n" + prompt
    else:
        prompt = text_area_section + color_emphasis + "\n\n" + prompt

    # Add SEO context if available
    if seo_metadata:
        seo_context = f"\n\nSEO & DESIGN CONTEXT:\n"
        seo_context += f"• Video Title: {seo_metadata.title}\n"
        if seo_metadata.thumbnail_text:
            seo_context += f"• Thumbnail Headline: {seo_metadata.thumbnail_text}\n"
        seo_context += f"• Theme: {seo_metadata.description[:100]}...\n"
        prompt += seo_context

    return prompt


def generate_thumbnail_image(script: Script, seo_metadata: Optional[SEOMetadata],
                           output_folder: Path, context: Optional[str] = None) -> Optional[ImageMetadata]:
    """
    Generate YouTube thumbnail image using OpenAI API with canonical references.

    Args:
        script: Script object with dialogue content
        seo_metadata: SEO metadata with title, description, thumbnail_text
        output_folder: Path to save image files
        context: Optional context about the topic

    Returns:
        ImageMetadata with thumbnail file information
    """

    print(f"\n🎨 Thumbnail: Generating for: {script.topic}")
    print("=" * 60)

    try:
        from openai import OpenAI

        if not config.OPENAI_API_KEY:
            print(f"⚠️  OpenAI API key not set in OPENAI_API_KEY environment")
            return None

        client = OpenAI(api_key=config.OPENAI_API_KEY)

        # Load thumbnail prompt
        prompt_path = config.PROMPTS_DIR / "Thumbnail Image- Prompt.txt"
        if not prompt_path.exists():
            print(f"⚠️  Thumbnail prompt not found at {prompt_path}")
            return None

        with open(prompt_path, 'r', encoding='utf-8') as f:
            thumbnail_prompt = f.read()

        # Load canonical references
        references = _load_canonical_references('thumbnail')

        # Build enhanced prompt
        full_prompt = _build_enhanced_prompt(
            thumbnail_prompt,
            script.topic,
            context,
            seo_metadata,
            references,
            text_position="AUTO"
        )

        # Call OpenAI to generate thumbnail image with canonical references
        print("   ⏳ Calling OpenAI GPT-Image-2.5-Sunburst for thumbnail generation...")
        print(f"   📌 Using {len(references['file_paths'])} canonical reference images")

        # Open reference image files
        reference_files = []
        try:
            for ref_path in references['file_paths']:
                reference_files.append(open(ref_path, 'rb'))

            # Call API with reference images + enhanced prompt
            response = client.images.edit(
                image=reference_files,
                prompt=full_prompt,
                model=config.IMAGE_GENERATION_MODEL,
                size=config.THUMBNAIL_SIZE,
                n=1,
                quality="high"  # High quality output
            )
        finally:
            # Close all reference files
            for f in reference_files:
                f.close()

        # Create output folder
        output_folder.mkdir(parents=True, exist_ok=True)

        # Save thumbnail image
        thumbnail_path = output_folder / "thumbnail.png"

        # Decode base64 and save
        if response.data and len(response.data) > 0:
            image_base64 = response.data[0].b64_json
            if image_base64:
                image_bytes = base64.b64decode(image_base64)
                with open(thumbnail_path, 'wb') as f:
                    f.write(image_bytes)

                print(f"   ✓ Thumbnail image generated and saved")
                print(f"   📁 File: {thumbnail_path}")
                print(f"   💾 Size: {len(image_bytes) / 1024:.1f} KB")
            else:
                print(f"   ⚠️  No image data in response")
                return None
        else:
            print(f"   ⚠️  No image data in response")
            return None

        # Create metadata
        metadata = ImageMetadata(
            topic=script.topic,
            image_type="thumbnail",
            file_path=str(thumbnail_path),
            resolution=config.THUMBNAIL_SIZE,
            generation_model=config.IMAGE_GENERATION_MODEL,
            prompt_used="Thumbnail Image- Prompt.txt + Canonical References"
        )

        print(f"   ✅ Thumbnail metadata created")
        return metadata

    except Exception as e:
        error_msg = str(e)
        print(f"   ✗ Error generating thumbnail: {error_msg}")
        if "does not exist" in error_msg.lower():
            print(f"   💡 Check: OpenAI API key has access to {config.IMAGE_GENERATION_MODEL}")
        return None


def generate_video_scene(script: Script, seo_metadata: Optional[SEOMetadata],
                        output_folder: Path, context: Optional[str] = None) -> Optional[ImageMetadata]:
    """
    Generate long-form video scene image using OpenAI API with canonical references.

    Args:
        script: Script object with dialogue content
        seo_metadata: SEO metadata with title and context
        output_folder: Path to save image files
        context: Optional context about the topic

    Returns:
        ImageMetadata with video scene file information
    """

    print(f"\n🎬 Video Scene: Generating for: {script.topic}")
    print("=" * 60)

    try:
        from openai import OpenAI

        if not config.OPENAI_API_KEY:
            print(f"⚠️  OpenAI API key not set in OPENAI_API_KEY environment")
            return None

        client = OpenAI(api_key=config.OPENAI_API_KEY)

        # Load video scene prompt
        prompt_path = config.PROMPTS_DIR / "Video Image- Prompt.txt"
        if not prompt_path.exists():
            print(f"⚠️  Video scene prompt not found at {prompt_path}")
            return None

        with open(prompt_path, 'r', encoding='utf-8') as f:
            video_prompt = f.read()

        # Load canonical references
        references = _load_canonical_references('video')

        # Build enhanced prompt (video uses full frame, no text area reservation)
        full_prompt = _build_enhanced_prompt_video(
            video_prompt,
            script.topic,
            context,
            seo_metadata,
            references
        )

        # Call OpenAI to generate video scene image with canonical references
        print("   ⏳ Calling OpenAI GPT-Image-2.5-Sunburst for video scene generation...")
        print(f"   📌 Using {len(references['file_paths'])} canonical reference images")

        # Open reference image files
        reference_files = []
        try:
            for ref_path in references['file_paths']:
                reference_files.append(open(ref_path, 'rb'))

            # Call API with reference images + enhanced prompt
            response = client.images.edit(
                image=reference_files,
                prompt=full_prompt,
                model=config.IMAGE_GENERATION_MODEL,
                size=config.VIDEO_SCENE_SIZE,
                n=1,
                quality="high"  # High quality output
            )
        finally:
            # Close all reference files
            for f in reference_files:
                f.close()

        # Create output folder
        output_folder.mkdir(parents=True, exist_ok=True)

        # Save video scene image
        video_path = output_folder / "video_scene.png"

        # Decode base64 and save
        if response.data and len(response.data) > 0:
            image_base64 = response.data[0].b64_json
            if image_base64:
                image_bytes = base64.b64decode(image_base64)
                with open(video_path, 'wb') as f:
                    f.write(image_bytes)

                print(f"   ✓ Video scene image generated and saved")
                print(f"   📁 File: {video_path}")
                print(f"   💾 Size: {len(image_bytes) / 1024:.1f} KB")
            else:
                print(f"   ⚠️  No image data in response")
                return None
        else:
            print(f"   ⚠️  No image data in response")
            return None

        # Create metadata
        metadata = ImageMetadata(
            topic=script.topic,
            image_type="video_scene",
            file_path=str(video_path),
            resolution=config.VIDEO_SCENE_SIZE,
            generation_model=config.IMAGE_GENERATION_MODEL,
            prompt_used="Video Image- Prompt.txt + Canonical References"
        )

        print(f"   ✅ Video scene metadata created")
        return metadata

    except Exception as e:
        error_msg = str(e)
        print(f"   ✗ Error generating video scene: {error_msg}")
        if "does not exist" in error_msg.lower():
            print(f"   💡 Check: OpenAI API key has access to {config.IMAGE_GENERATION_MODEL}")
        return None
