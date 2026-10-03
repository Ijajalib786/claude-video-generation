"""
Phase 4: Thumbnail Image Generation Agent
Generates YouTube thumbnail images using OpenAI (GPT-Image-2.5-Sunburst) API.
"""

from pathlib import Path
from typing import Optional
import base64
from .. import config
from ..models import Script, SEOMetadata, ImageMetadata


def _load_canonical_references() -> dict:
    """Load canonical thumbnail reference images."""
    print("Loading canonical thumbnail references...")

    references = {
        'descriptions': [],
        'file_paths': []
    }

    if 'thumbnail' not in config.CANONICAL_REFERENCES:
        return references

    ref_paths = config.CANONICAL_REFERENCES['thumbnail']

    for ref_path in ref_paths:
        if ref_path.exists():
            references['file_paths'].append(ref_path)
            print(f"✓ Found: {ref_path.name}")
        else:
            print(f"⚠ Missing: {ref_path}")

    # Create reference descriptions
    references['descriptions'] = [
        "This is a canonical reference showing the SPEAK ENGLISH SMARTER character style.",
        "Sarah (age 24, English teacher): Oval face, warm skin tone, almond brown eyes, shoulder-length dark brown hair with side-part.",
        "Alex (age 25, English learner): Slightly rounded face, warm skin tone, brown eyes, short textured black hair.",
        "Use these reference images as the primary source of truth for character consistency.",
        "Characters must look identical across all videos - only clothing, expressions, and poses may change.",
        "Maintain the premium flat vector illustration style shown in the references."
    ]

    return references


def _get_scenario_guidance(topic: str, context: Optional[str]) -> dict:
    """Analyze topic for scenario guidance."""
    topic_lower = topic.lower()
    context_lower = (context or "").lower()

    home_keywords = ["home", "bedroom", "kitchen", "living room", "apartment", "house",
                     "casual", "relax", "morning", "evening", "family", "breakfast", "cozy", "coffee"]
    if any(kw in topic_lower or kw in context_lower for kw in home_keywords):
        return {
            "background_color": "soft beige/cream",
            "scenario": "Home/Casual scene",
            "composition_pattern": "lower-left",
            "character_positions": {
                "sarah": "lower-left area, relaxed pose",
                "alex": "lower-left area, beside Sarah"
            },
            "composition_guidance": "Position BOTH characters on the LOWER-LEFT side of frame. Leave TOP-RIGHT area completely clear and empty for text overlay. Characters should occupy left 60% of frame, leaving right 40% clear."
        }

    office_keywords = ["office", "work", "job", "interview", "business", "meeting",
                       "professional", "presentation", "corporate", "formal", "desk"]
    if any(kw in topic_lower or kw in context_lower for kw in office_keywords):
        return {
            "background_color": "soft blue/gray",
            "scenario": "Office/Professional scene",
            "composition_pattern": "right-positioned",
            "character_positions": {
                "sarah": "right-center area, professional posture",
                "alex": "right-center area, beside Sarah"
            },
            "composition_guidance": "Position BOTH characters on the RIGHT SIDE of frame. Leave LEFT SIDE completely clear and empty for text overlay. Characters should occupy right 60% of frame, leaving left 40% clear for text."
        }

    travel_keywords = ["airport", "travel", "hotel", "beach", "outdoor", "vacation",
                       "trip", "flight", "luggage", "tourism", "mountain", "forest", "cruise"]
    if any(kw in topic_lower or kw in context_lower for kw in travel_keywords):
        return {
            "background_color": "soft sky/cloud tones",
            "scenario": "Travel/Outdoor scene",
            "composition_pattern": "left-positioned",
            "character_positions": {
                "sarah": "left side, excited/adventurous pose",
                "alex": "left side beside Sarah, engaged expression"
            },
            "composition_guidance": "Position BOTH characters on the LEFT SIDE of frame. Leave RIGHT SIDE completely clear and empty for text overlay. Characters should occupy left 60% of frame, leaving right 40% clear for text."
        }

    restaurant_keywords = ["restaurant", "coffee", "cafe", "food", "dining", "party",
                           "social", "dinner", "lunch", "bar", "drink"]
    if any(kw in topic_lower or kw in context_lower for kw in restaurant_keywords):
        return {
            "background_color": "soft warm/amber tones",
            "scenario": "Restaurant/Social scene",
            "composition_pattern": "left-positioned",
            "character_positions": {
                "sarah": "left-center area, friendly/social pose",
                "alex": "left-center area beside Sarah, enjoying interaction"
            },
            "composition_guidance": "Position BOTH characters on the LEFT-CENTER of frame. Leave RIGHT SIDE completely clear and empty for text overlay. Characters should occupy left 60% of frame, leaving right 40% clear for text."
        }

    activity_keywords = ["shopping", "shop", "activity", "hobby", "gym", "sports",
                        "exercise", "game", "dance", "sport", "fitness", "hobby"]
    if any(kw in topic_lower or kw in context_lower for kw in activity_keywords):
        return {
            "background_color": "soft neutral/energetic tones",
            "scenario": "Shopping/Activity scene",
            "composition_pattern": "left-positioned",
            "character_positions": {
                "sarah": "left-center, active/engaged pose",
                "alex": "left-center beside Sarah, enthusiastic expression"
            },
            "composition_guidance": "Position BOTH characters on the LEFT-CENTER of frame. Leave RIGHT SIDE completely clear and empty for text overlay. Characters should occupy left 60% of frame, leaving right 40% clear for text."
        }

    return {
        "background_color": "soft warm tones",
        "scenario": "General conversation scene",
        "composition_pattern": "left-positioned",
        "character_positions": {
            "sarah": "left-center area",
            "alex": "left-center area beside Sarah"
        },
        "composition_guidance": "Position BOTH characters on the LEFT SIDE of frame. Leave RIGHT SIDE completely clear and empty for text overlay. Characters should occupy left 60% of frame, leaving right 40% clear for text."
    }


def _build_enhanced_prompt(prompt_template: str, topic: str, context: Optional[str],
                          seo_metadata: Optional[SEOMetadata], references: dict,
                          text_position: str = "AUTO") -> str:
    """Build enhanced prompt for thumbnail generation."""
    prompt = prompt_template

    prompt = prompt.replace("[TOPIC]", topic)
    scene_context = context or "Natural conversation"
    prompt = prompt.replace("[SCENE]", scene_context)
    prompt = prompt.replace("[AUTO | LEFT | RIGHT | TOP | BOTTOM | CENTER]", text_position)

    scenario_guidance = _get_scenario_guidance(topic, context)

    composition_section = f"""
DYNAMIC CHARACTER COMPOSITION FOR THIS TOPIC:

Topic: {topic}
Detected Scenario: {scenario_guidance['scenario']}
Composition Pattern: {scenario_guidance['composition_pattern']}

CHARACTER POSITIONING:
• Sarah should be positioned in: {scenario_guidance['character_positions']['sarah']}
• Alex should be positioned in: {scenario_guidance['character_positions']['alex']}
• Overall guidance: {scenario_guidance['composition_guidance']}

TEXT SPACE POSITIONING (CRITICAL FOR THUMBNAIL TEXT OVERLAY):
• Characters must NOT fill the entire frame
• Position characters to ONE SIDE of the image to create clear empty space
• Leave the OPPOSITE SIDE completely clear and empty for text overlay
• Text space should be approximately 30-40% of the image width or height
• Characters should not extend into the text space area
"""

    background_section = f"""
CONSISTENT SOFT BACKGROUND (FOR FLEXIBLE TEXT PLACEMENT):

Topic: {topic}
Detected Scenario: {scenario_guidance['scenario']}
Background Color: {scenario_guidance['background_color']}

CRITICAL REQUIREMENTS:
• Create CONSISTENT soft background throughout ENTIRE image
• NO reserved white space or empty areas
• Background color matches scenario: {scenario_guidance['background_color']}
• Text can be placed ANYWHERE on this soft background
• Soft background ensures text readability and professional appearance
• Full frame composition with characters naturally positioned
"""

    lighting_color = scenario_guidance.get('background_color', 'soft warm')
    lighting_emphasis = f"""
LIGHTING QUALITY EMPHASIS:

Light Source: Use SOFT colored light matching this scenario
• Color: {lighting_color}
• Quality: SOFT glow, NOT bright white light
• Effect: Gentle illumination creating depth and dimension
• Blending: Light blends naturally with background

CRITICAL: NO bright white light - use soft colors only
• Soft glow on surfaces (walls, props, characters)
• Gentle shadows adding depth, not harshness
• Everything feels warmly/softly illuminated
• Light source creates radiant but soft quality
"""

    color_emphasis = """
COLOR SATURATION EMPHASIS:
• Use SOFT, MUTED tones throughout
• This image should feel CALM and INVITING
• Match the sample reference's soft color palette
• NO bright, saturated, or neon colors
• Keep all colors gentle and pleasant for educational viewing
"""

    if references and references['descriptions']:
        reference_context = "\n\nCANONICAL REFERENCE CONTEXT:\n"
        reference_context += "\n".join(f"• {desc}" for desc in references['descriptions'])
        prompt = reference_context + composition_section + background_section + lighting_emphasis + color_emphasis + "\n\n" + prompt
    else:
        prompt = composition_section + background_section + lighting_emphasis + color_emphasis + "\n\n" + prompt

    if seo_metadata:
        seo_context = f"\n\nSEO & DESIGN CONTEXT:\n"
        seo_context += f"• Video Title: {seo_metadata.title}\n"
        if seo_metadata.thumbnail_text:
            seo_context += f"• Thumbnail Headline: {seo_metadata.thumbnail_text}\n"
        seo_context += f"• Theme: {seo_metadata.description[:100]}...\n"
        prompt += seo_context

    return prompt


def _analyze_reference_styles(reference_file_paths: list) -> dict:
    """
    Dynamically analyze canonical references to determine their character styles.

    Sends both reference images to OpenAI vision for analysis.
    Returns analysis of beard style, hair style, overall vibe, and best use cases for each reference.
    """
    from openai import OpenAI

    if not reference_file_paths or len(reference_file_paths) < 2:
        print("[WARN] Not enough references to analyze styles")
        return {}

    print("[ANALYSIS] Analyzing canonical reference styles...")

    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)

        # Encode images as base64
        encoded_images = []
        for path in reference_file_paths[:2]:  # Use first 2 references
            with open(path, 'rb') as f:
                encoded_images.append(base64.b64encode(f.read()).decode())

        analysis_prompt = """Analyze these two character reference images for SPEAK ENGLISH SMARTER.

For EACH reference image, describe:
1. Character styling (beard style, hair style, overall vibe)
2. Professional level (casual/relaxed vs professional/formal)
3. Best use cases for this style
4. Specific character traits visible

Then provide:
- Which reference is more CASUAL/RELAXED?
- Which reference is more PROFESSIONAL/FORMAL?
- Key visual differences between them?

Format your response as:
REFERENCE 0:
- Beard: [description]
- Hair: [description]
- Vibe: [professional level]
- Best for: [use cases]

REFERENCE 1:
- Beard: [description]
- Hair: [description]
- Vibe: [professional level]
- Best for: [use cases]

SUMMARY:
- Casual reference: [0 or 1]
- Professional reference: [0 or 1]
- Key differences: [description]"""

        # Send images to OpenAI for analysis
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": analysis_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_images[0]}"
                            }
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_images[1]}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )

        analysis_text = response.choices[0].message.content
        print(f"[ANALYSIS] Reference style analysis complete")
        print(f"[DEBUG] {analysis_text[:200]}...")

        return {
            'analysis': analysis_text,
            'reference_count': 2
        }

    except Exception as e:
        print(f"[ERROR] Reference style analysis failed: {str(e)}")
        return {}


def _determine_needed_style(topic: str, context: Optional[str]) -> dict:
    """
    Analyze topic and determine what character style is needed.

    Uses Claude/OpenAI to evaluate the topic and return the appropriate character style.
    Returns style needed, reasoning, and recommended traits.
    """
    from anthropic import Anthropic

    print(f"[STYLE] Determining needed character style for topic: {topic}")

    try:
        client = Anthropic(api_key=config.ANTHROPIC_API_KEY)

        analysis_prompt = f"""Analyze this YouTube English learning video topic and determine the best character styling.

Topic: {topic}
Context: {context or "No additional context"}

For this topic, determine:
1. What character style would be most appropriate? (casual/professional/adventurous/formal/friendly)
2. Why does this style fit the topic?
3. What visual traits match this style? (beard, hair, expression, formality)
4. Confidence level (high/medium/low)

Format response as:
STYLE: [style name]
REASONING: [why this style]
TRAITS: [specific visual traits]
CONFIDENCE: [high/medium/low]"""

        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": analysis_prompt}]
        )

        analysis_text = response.content[0].text
        print(f"[STYLE] Style analysis: {analysis_text.split('STYLE:')[1][:100] if 'STYLE:' in analysis_text else 'unknown'}...")

        return {
            'analysis': analysis_text,
            'topic': topic
        }

    except Exception as e:
        print(f"[ERROR] Style determination failed: {str(e)}")
        return {'analysis': 'casual', 'topic': topic}


def _match_style_to_reference(needed_style_analysis: dict, reference_styles_analysis: dict) -> dict:
    """
    Match the needed style to the best matching reference.

    Compares needed style vs each reference to find the best match.
    Returns which reference to use and confidence score.
    """
    from anthropic import Anthropic

    print(f"[MATCHING] Matching needed style to canonical references...")

    try:
        client = Anthropic(api_key=config.ANTHROPIC_API_KEY)

        matching_prompt = f"""Match the needed character style to the best canonical reference.

NEEDED STYLE:
{needed_style_analysis.get('analysis', 'casual style')}

REFERENCE ANALYSIS:
{reference_styles_analysis.get('analysis', 'Two references available')}

Task:
1. Which reference (0 or 1) best matches the needed style?
2. Score each reference 1-10 for how well it matches
3. Provide confidence level (high/medium/low)
4. Explain why this reference is the best match

Format response as:
BEST_MATCH: [0 or 1]
SCORE_0: [score]
SCORE_1: [score]
CONFIDENCE: [high/medium/low]
REASONING: [explanation]"""

        response = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": matching_prompt}]
        )

        matching_text = response.content[0].text

        # Extract best match reference
        best_match = 0
        if "BEST_MATCH:" in matching_text:
            try:
                best_match_line = matching_text.split("BEST_MATCH:")[1].split("\n")[0].strip()
                best_match = int(best_match_line[0])  # Get first character (0 or 1)
                if best_match > 1:
                    best_match = 0
            except:
                best_match = 0

        print(f"[MATCHING] Selected Reference {best_match}")
        print(f"[DEBUG] {matching_text[:150]}...")

        return {
            'best_match_index': best_match,
            'matching_analysis': matching_text,
            'confidence': 'high' if 'CONFIDENCE: high' in matching_text else 'medium'
        }

    except Exception as e:
        print(f"[ERROR] Style matching failed: {str(e)}")
        return {'best_match_index': 0, 'confidence': 'low'}


def generate_thumbnail_image(script: Script, seo_metadata: Optional[SEOMetadata],
                           output_folder: Path, context: Optional[str] = None) -> Optional[ImageMetadata]:
    """Generate YouTube thumbnail image with dynamic character style variation."""

    print(f"\nGenerating thumbnail for: {script.topic}")
    print("=" * 60)

    try:
        from openai import OpenAI

        if not config.OPENAI_API_KEY:
            print("OpenAI API key not set")
            return None

        client = OpenAI(api_key=config.OPENAI_API_KEY)

        prompt_path = config.PROMPTS_DIR / "Thumbnail Image- Prompt.txt"
        if not prompt_path.exists():
            print(f"Thumbnail prompt not found at {prompt_path}")
            return None

        with open(prompt_path, 'r', encoding='utf-8') as f:
            thumbnail_prompt = f.read()

        references = _load_canonical_references()

        # PHASE 1: Analyze what styles the references represent
        print("\n[PHASE 1] Analyzing canonical reference styles...")
        reference_styles = _analyze_reference_styles(references['file_paths'])

        # PHASE 2: Determine what style this topic needs
        print("\n[PHASE 2] Determining needed character style for this topic...")
        needed_style = _determine_needed_style(script.topic, context)

        # PHASE 3: Match needed style to best reference
        print("\n[PHASE 3] Matching style to best reference...")
        selected_ref = _match_style_to_reference(needed_style, reference_styles)
        best_ref_index = selected_ref.get('best_match_index', 0)

        print(f"\n[SELECTION] Using Reference {best_ref_index} for this topic")

        # Use selected reference in prompt
        if best_ref_index < len(references['file_paths']):
            selected_reference_path = references['file_paths'][best_ref_index]
            print(f"[SELECTION] Reference: {selected_reference_path.name}")

        full_prompt = _build_enhanced_prompt(
            thumbnail_prompt,
            script.topic,
            context,
            seo_metadata,
            references,
            text_position="AUTO"
        )

        # Add dynamic style guidance to prompt
        style_guidance = f"""

DYNAMIC CHARACTER STYLE SELECTION:

Topic: {script.topic}
Needed Style: {needed_style.get('analysis', 'dynamic style')[:200]}
Selected Reference: {best_ref_index}
Match Confidence: {selected_ref.get('confidence', 'medium')}

Use the selected canonical reference ({best_ref_index}) as the primary guide for character styling.
Match the character appearance shown in this reference for consistency with the topic."""

        full_prompt = style_guidance + full_prompt

        print("Calling OpenAI API for thumbnail generation...")

        response = client.images.generate(
            prompt=full_prompt,
            model=config.IMAGE_GENERATION_MODEL,
            size=config.THUMBNAIL_SIZE,
            n=1,
            quality="high"
        )

        output_folder.mkdir(parents=True, exist_ok=True)
        thumbnail_path = output_folder / "thumbnail.png"

        if response.data and len(response.data) > 0:
            image_data = response.data[0]

            # Handle both b64_json and url responses
            if hasattr(image_data, 'b64_json') and image_data.b64_json:
                image_bytes = base64.b64decode(image_data.b64_json)
            elif hasattr(image_data, 'url') and image_data.url:
                import urllib.request
                urllib.request.urlretrieve(image_data.url, str(thumbnail_path))
                with open(thumbnail_path, 'rb') as f:
                    image_bytes = f.read()
            else:
                print("ERROR: No image data in response")
                return None

            with open(thumbnail_path, 'wb') as f:
                f.write(image_bytes)

            print(f"Thumbnail generated: {thumbnail_path}")
            print(f"Size: {len(image_bytes) / 1024:.1f} KB")

            metadata = ImageMetadata(
                topic=script.topic,
                image_type="thumbnail",
                file_path=str(thumbnail_path),
                resolution=config.THUMBNAIL_SIZE,
                generation_model=config.IMAGE_GENERATION_MODEL,
                prompt_used="Thumbnail Image- Prompt.txt"
            )

            print("Thumbnail completed successfully")
            return metadata
        else:
            print("ERROR: No response data from API")
            return None

    except Exception as e:
        print(f"Error generating thumbnail: {str(e)}")
        return None
