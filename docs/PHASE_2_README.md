# Phase 2: SEO Metadata Agent - Modern YouTube Strategy

**Status:** Ready for Implementation  
**Learning Goal:** Data flow between agents, file-based handoffs  
**Testing:** Comprehensive validation for 5 diverse topics  

---

## Overview

Phase 2 adds **YouTube SEO metadata generation** with a modern 2026 strategy focused on maximizing search traffic and views.

### What Phase 2 Does

Generates optimized YouTube metadata from scripts:
- **Title** (≤65 chars) - Keyword-rich, high CTR
- **Description** (500+ words) - SEO-optimized with keywords and CTAs
- **Hashtags** (15-20) - High-volume, niche, and long-tail mix
- **Tags** (15-20) - Trending keywords and brand
- **Thumbnail Text** (≤100 chars) - Compelling overlay text

### Sequential Workflow

```
Phase 1: Generate Script
    ↓ (file: script.txt)
    ↓
Phase 2: Generate SEO Metadata
    ↓ (file: seo_metadata.txt)
    ↓
Phase 3+: TTS, Images, Video Assembly
```

---

## Architecture

### SEO Agent Pattern

Reuses Phase 1 pattern:
```python
def generate_seo_metadata(script: Script, topic_input: TopicInput) -> SEOMetadata:
    # Load SEO optimization prompt
    # Call Claude API with modern YouTube strategy
    # Parse JSON response
    # Validate metadata fields
    # Return SEOMetadata object
```

### Key Strategy: 2026 YouTube SEO

#### Title Optimization
- Format: `[Verb/Question] + [Benefit] + [Specificity]`
- Include long-tail keyword
- Max 65 characters (YouTube limit)
- Example: `"How to Apologize Politely in English | Learn Natural Phrases"`

#### Description Strategy
- First 150 chars: Hook with keywords (shown before "more")
- Body: Educational value + learning points
- Keywords: 3-5 main keywords, sprinkled naturally
- Calls-to-action: "Like", "Subscribe", "Comment"
- Length: Quality-focused (typically 350-500 words, no strict minimum)
- **Design Philosophy:** Quality and view-attraction matter more than word count

#### Hashtags Strategy (15-20)
- 40% High-volume: `#learnEnglish`, `#englishconversation`
- 40% Medium-volume niche: `#englishphrases`, `#conversationalenglish`
- 20% Long-tail specific: `#howtoapologizepolitely`
- Avoid: Hashtags with <10K views

#### Tags Strategy (15-20)
- Topic keyword phrase
- Broader learning categories
- Long-tail variations
- Trending keywords (conversational English, practical English)
- Brand: "SPEAK ENGLISH SMARTER"

#### Thumbnail Text
- One compelling text overlay
- Format: Action verb + Benefit OR Curiosity gap
- Examples: `"SAY NO POLITELY"`, `"APOLOGIZE LIKE A NATIVE"`, `"PERFECT APOLOGY?"`
- Max 100 characters
- High contrast, readable at thumbnail scale

---

## File Structure

### New Files Created

1. **`src/agents/seo_metadata_agent.py`**
   - `generate_seo_metadata()` - Main function
   - `save_seo_metadata_to_file()` - File operations
   - `_parse_seo_metadata()` - JSON parsing

2. **`tests/test_phase_2.py`**
   - Tests SEO generation for 5 topics
   - Validates all metadata fields
   - Saves sample outputs

3. **`docs/PHASE_2_README.md`** (this file)
   - Strategy guide
   - Implementation details
   - Testing instructions

### Updated Files

1. **`src/models.py`**
   - Added `thumbnail_text: str` field to SEOMetadata
   - Added validators for description (≥500 words)
   - Added validators for thumbnail_text (3-100 chars)

2. **`scripts/cli.py`**
   - Added SEO agent import
   - Integrated SEO generation after script
   - Display SEO results in CLI
   - Updated header to mention Phase 2

### Output Files (per topic)

```
outputs/{topic}/
├── script.txt              # Phase 1: Dialogue script
├── script_metadata.json    # Phase 1: Script statistics
└── seo_metadata.txt        # Phase 2: SEO metadata (NEW)
    ├── Title
    ├── Thumbnail Text
    ├── Hashtags
    ├── Tags
    └── Description
```

---

## Models & Validation

### SEOMetadata Model

```python
class SEOMetadata(BaseModel):
    title: str                  # ≤65 chars
    description: str            # ≥500 words
    hashtags: list[str]         # exactly 15-20
    tags: list[str]             # exactly 15-20
    thumbnail_text: str         # 3-100 chars
```

### Validation Rules

| Field | Rule | Example |
|-------|------|---------|
| title | ≤65 chars | "How to Apologize Politely in English" (44 chars) |
| description | Quality-focused, substantive | ~350-500 words of high-quality content |
| hashtags | 15-20 items | ["#learnEnglish", "#englishphrases", ...] |
| tags | 15-20 items | ["learn English", "english conversation", ...] |
| thumbnail_text | 3-100 chars | "SAY NO POLITELY" (15 chars) |

---

## Running Phase 2

### Interactive CLI (Recommended)

```powershell
cd C:\Ijaj\Claude\claude-video-generation
.\venv\Scripts\Activate.ps1
$env:ANTHROPIC_API_KEY="your-key"
python scripts\cli.py generate
```

**Prompts:**
1. Topic: Enter your video topic
2. Context (optional): Additional details
3. Video Length: Minutes (8-20, default 12)

**Output:**
- Phase 1: `script.txt` + `script_metadata.json`
- Phase 2: `seo_metadata.txt` ✨ NEW

### Testing Phase 2

```powershell
python tests\test_phase_2.py
```

Tests 5 diverse topics:
- ✓ Generates valid SEO metadata
- ✓ Validates all fields
- ✓ Checks title length (≤65 chars)
- ✓ Checks description length (≥500 words)
- ✓ Validates hashtags count (15-20)
- ✓ Validates tags count (15-20)
- ✓ Validates thumbnail text (3-100 chars)

---

## Implementation Details

### Claude API Integration

**Model:** `claude-sonnet-5`  
**Max Tokens:** 4096  
**Temperature:** 0.7 (default)

### System Prompt Strategy

The SEO agent uses an enhanced system prompt that:
1. Explains modern 2026 YouTube SEO strategy
2. Breaks down title, description, hashtags, tags optimization
3. Specifies exact requirements (character limits, word counts)
4. Requests JSON output with specific format
5. Emphasizes trending keywords in English learning space

### JSON Parsing

Response parsing:
- Extract text from `response.content` blocks
- Find JSON object using regex: `\{[^{}]*\}`
- Parse JSON with `json.loads()`
- Validate all required fields present
- Create SEOMetadata object with validation

### Error Handling

**Catches:**
- API failures → Raise with message
- Invalid JSON → Show parsing error
- Validation errors → Show which field failed
- Missing fields → List missing required fields

**Displays:**
- Clear error messages to user
- Option to retry or skip SEO generation
- Continues to next phase if SEO fails

---

## Output Format: seo_metadata.txt

**Human-readable format (NOT JSON):**

```
=== YOUTUBE SEO METADATA ===
Generated for video optimization
Strategy: Trend-Based Search Optimization (2026)

TITLE:
How to Apologize Politely in English | Learn Natural Phrases

THUMBNAIL TEXT:
SAY NO POLITELY

HASHTAGS:
#learnEnglish #englishconversation #englishphrases ... [20 total]

TAGS:
learn english, english conversation, how to apologize, ... [20 total]

DESCRIPTION:
[500-1000+ word optimized description with keywords and CTAs]

---
Generated by SPEAK ENGLISH SMARTER SEO Agent
```

---

## Testing Strategy

### Test Cases

**1. Basic Generation**
- Input: Topic + Context
- Expected: seo_metadata.txt created
- Verify: File exists and has all sections

**2. Data Validation**
- Title: ≤65 chars
- Description: ≥500 words
- Hashtags: 15-20 items
- Tags: 15-20 items
- Thumbnail: 3-100 chars
- Error: Raises ValueError if invalid

**3. Consistency Check**
- Title relates to topic
- Description summarizes script
- Hashtags match keywords
- Tags include trending English learning keywords

**4. Multiple Topics**
- Test 5 different topics
- All pass validation
- Quality consistent across topics

### Test Command

```powershell
python tests\test_phase_2.py
```

### Expected Output

```
PHASE 2: SEO METADATA GENERATION TEST
Testing Modern YouTube SEO Strategy (2026)
===============================================

✅ Passed: 5/5
🎉 SUCCESS! All topics generated valid SEO metadata!
```

---

## Trending Keywords (2026)

SEO agent focuses on current trends:
- **Conversational English** (practical, real-world)
- **Practical Communication** (business, social, daily)
- **Natural Phrasing** (authentic pronunciation, listening)
- **Real-World Scenarios** (workplace, friends, travel)
- **Confidence in Speaking** (fluency, accent reduction)

Avoids:
- Academic grammar focus
- Complex technical terms
- Non-practical content

---

## Integration with CLI

### Before Phase 2
```
User Input (Topic, Context, Length)
    ↓
Phase 1: Generate Script
    ↓
Display Results → Done
```

### After Phase 2
```
User Input (Topic, Context, Length)
    ↓
Phase 1: Generate Script
    ↓
Phase 2: Generate SEO Metadata (NEW)
    ↓
Display Full Results → Done
```

### CLI Output Example

```
=== Generation Complete ===
📁 Output folder: outputs/how_to_apologize_politely/
📝 Files created:
   ✓ script.txt
   ✓ script_metadata.json
   ✓ seo_metadata.txt (NEW)

📊 Script Statistics:
   - Lines: 287
   - Words: 1456
   - Duration: ~11.2 minutes
   - Characters: Sarah (teacher) & Alex (learner)

📌 SEO Metadata:
   Title: How to Apologize Politely in English | Learn Natural Phrases
   Thumbnail Text: SAY NO POLITELY
   Hashtags: #learnEnglish #englishconversation ... (+15 more)
   Tags: learn english, english conversation, ... (+15 more)
   Description: In this video, you'll learn ... (750 words)
```

---

## Completion Checklist

- ✅ Updated `src/models.py` with thumbnail_text field
- ✅ Created `src/agents/seo_metadata_agent.py`
- ✅ Updated `scripts/cli.py` with Phase 2 integration
- ✅ Created `tests/test_phase_2.py`
- ✅ Created `docs/PHASE_2_README.md`
- ⏳ Test Phase 2 with 5+ topics
- ⏳ Verify output files and quality
- ⏳ Get user approval for Phase 3

---

## Next Phase: Phase 3

After Phase 2 approval:
- **TTS Agent:** Convert script dialogue to audio (Sarah + Alex voices)
- **Image Generation Agent:** Create thumbnail.png and video_scene.png
- Keep same sequential workflow pattern

---

## Learning Outcomes

✅ **Agent Data Flow:** Script output → SEO input  
✅ **File-based Handoffs:** script.txt → seo_metadata.txt  
✅ **Sequential Orchestration:** Generate → Process → Save  
✅ **API Integration:** Claude generates diverse metadata types  
✅ **Validation Patterns:** Multiple field types with different constraints  
✅ **YouTube SEO:** Real-world application of optimization strategy  

---

## Troubleshooting

**"Description word count too low"**
- Claude generated fewer than 500 words
- SEO agent will retry or show error
- Manually expand description if needed

**"Hashtags not 15-20 items"**
- Parser couldn't extract exactly 20 hashtags
- Check JSON format in Claude response
- Agent shows detailed error message

**"Thumbnail text > 100 characters"**
- Make text more concise
- Agent shows validation error
- Example: "SAY NO POLITELY" (15 chars) ✓

**API Rate Limits**
- Reduce test frequency
- Wait between requests
- Check Anthropic API status

---

## References

- **Model:** `src/models.py` - SEOMetadata class
- **Agent:** `src/agents/seo_metadata_agent.py` - Implementation
- **CLI:** `scripts/cli.py` - Integration point
- **Tests:** `tests/test_phase_2.py` - Validation
- **Plan:** `docs/PLAN.md` - Master plan

---

**Phase 2: Complete! Ready for testing and Phase 3.** 🎯
