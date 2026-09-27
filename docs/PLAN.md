# SPEAK ENGLISH SMARTER - Video Generation Pipeline
## Complete Multi-Phase Implementation Plan

**SOURCE OF TRUTH** — This document governs all development. Resume from this plan in future sessions.

---

## 🎯 PROJECT OVERVIEW

Build an automated, incremental video generation pipeline for English learning channel.  
**Input:** Topic → **Output:** Complete MP4 video with script, audio, images, and metadata.

### Learning Goal
Learn **Agentic AI patterns** incrementally:
- Phase 1: Claude API tool use
- Phase 2: Multi-agent coordination
- Phase 3: Advanced orchestration (MCP)
- Phase 4-5: Production patterns

---

## 📊 PHASE STATUS TRACKER

```
Phase 1: Core Script Generation Agent
  Status: ✅ READY_FOR_TESTING
  Approval: Not yet approved (awaiting testing)
  Implementation: COMPLETE (in src/agents/)
  Files: 5 Python modules + docs

Phase 2: SEO Metadata + Multi-Agent Coordination
  Status: ⏳ NOT_STARTED
  Approval: WAITING FOR PHASE 1 APPROVAL
  Implementation: PLANNED (not implemented)
  
Phase 3: Text-to-Speech + Image Generation
  Status: ⏳ NOT_STARTED
  Approval: WAITING FOR PHASE 1 APPROVAL
  Implementation: PLANNED (not implemented)
  
Phase 4: Video Assembly (FFmpeg)
  Status: ⏳ NOT_STARTED
  Approval: WAITING FOR PHASE 1 APPROVAL
  Implementation: PLANNED (not implemented)
  
Phase 5: Production Polish
  Status: ⏳ NOT_STARTED
  Approval: WAITING FOR PHASE 1 APPROVAL
  Implementation: PLANNED (not implemented)
```

**IMPORTANT:** Do not start Phase 2+ until Phase 1 is approved. This plan is the source of truth.

---

## PHASE 1: Core Agent Orchestration - READY_FOR_TESTING

### ✅ Implementation Status: COMPLETE

**What was built:**
- Python source package: `src/`
- Script generation agent: `src/agents/script_generation_agent.py`
- Data validation: `src/models.py`
- Configuration: `src/config.py`
- CLI interface: `scripts/cli.py`
- Comprehensive documentation: `docs/`
- Test verification: `tests/test_phase_1.py`

**How to run:**
```powershell
cd C:\Ijaj\Claude\claude-video-generation
.\scripts\setup_venv.ps1
$env:ANTHROPIC_API_KEY="your-key"
python scripts\cli.py generate
```

### Phase 1: Understanding & Requirements Analysis

### Current Assets
- ✓ Script Writer prompt (1500-2000 words, 10-15 min video, podcast style)
- ✓ Title & SEO prompt (YouTube optimized metadata)
- ✓ Thumbnail Image prompt (character bible + mood engine)
- ✓ Video Image prompt (long-form conversation scene)
- ✓ Reference images for character styles (4 PNG files)

### Pipeline Components Identified
1. **Script Generation** - Generate dialogue conversation script
2. **SEO Metadata** - Generate title, description, hashtags, tags
3. **Text-to-Speech** - Convert script to audio
4. **Thumbnail Generation** - Create YouTube thumbnail image
5. **Video Generation** - Combine thumbnail + audio into video
6. **Output** - Produce MP4 file

### User Preferences Confirmed

**Tools Selected:**
- **Text Generation:** Claude API + ChatGPT API
- **Text-to-Speech:** Google Studio (for multi-voice: Alex & Sarah)
- **Image Generation:** Claude API + ChatGPT API
- **Video Assembly:** FFmpeg
- **Input Method:** Interactive CLI prompts
- **Learning Path:** Incremental (tool use → multi-agent → MCP)

---

## Final Architecture

### Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INPUT (CLI)                         │
│         Topic + Voice choices + Output preferences           │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
┌──────────────────┐           ┌─────────────────────┐
│ Script Generation│           │   SEO Generation    │
│     Agent        │           │      Agent          │
│ (Claude API)     │           │  (Claude API)       │
│                  │           │                     │
│ - Conversation   │           │ - Title (65 chars)  │
│   between Alex   │           │ - Description       │
│   & Sarah        │           │ - Hashtags (15-20)  │
│ - Dialogue format│           │ - Tags (15-20)      │
└────────┬─────────┘           └──────────┬──────────┘
         │                                │
         └────────────┬───────────────────┘
                      │
        ┌─────────────▼──────────────┐
        │   Parse Script into Lines  │
        │  (Identify speaker turns)  │
        └────────────┬────────────────┘
                     │
        ┌────────────┴─────────────┐
        │                          │
        ▼                          ▼
┌──────────────────┐      ┌─────────────────┐
│   TTS Agent      │      │  Image Gen Agent│
│ (Google Studio)  │      │ (Claude/GPT API)│
│                  │      │                 │
│ - Alex voice     │      │ - Thumbnail PNG │
│ - Sarah voice    │      │ - Using style   │
│ - Combine audio  │      │   reference     │
│ - Output MP3     │      │ - Output PNG    │
└────────┬─────────┘      └────────┬────────┘
         │                         │
         │    ┌────────────────────┘
         │    │
         └────┼─────────────────────┐
              │                     │
         ┌────▼────────────────────▼──┐
         │   Video Assembly Agent     │
         │   (FFmpeg orchestrator)    │
         │                            │
         │ - Combine thumbnail + audio│
         │ - Duration calculation     │
         │ - Output MP4 (1920x1080)   │
         │ - File naming convention   │
         └────┬───────────────────────┘
              │
         ┌────▼──────────────────────────┐
         │   Output Folder (per topic)  │
         │                              │
         │ ├── script.txt               │
         │ ├── seo_metadata.json        │
         │ ├── thumbnail.png            │
         │ ├── video_scene.png          │
         │ └── output_video.mp4         │
         └──────────────────────────────┘
```

### Phase-Based Implementation (Learning Path)

**Phase 1: Core Agent Orchestration**
- Script generation agent with Claude API
  - Integrate topic quality criteria (SEO demand, evergreen, practical, CTR)
  - Use reference prompt + example script as context
  - Validate output meets beginner-friendly language requirements
- Simple error handling & state management
- Basic CLI interface
- Single-agent tool use learning
- *Goal: Understand Claude tool use & agent loops*
- **Deliverable:** Topic input → Script output (validated)

**Phase 2: Multi-Agent Coordination**
- Add SEO agent (parallel execution)
- Add TTS agent with voice management
- Implement file-based handoffs between agents
- Error handling & retry logic
- *Goal: Learn agent composition & data flow*

**Phase 3: Advanced Features**
- Image generation agent
- Video assembly orchestration
- MCP server for pipeline management
- *Goal: Learn MCP protocol & extensibility*

**Phase 4: Production Polish**
- Configuration management
- Batch processing
- Monitoring & logging
- Caching for cost optimization

---

## Technical Stack

| Component | Tool | Why This Choice |
|-----------|------|-----------------|
| **Script Generation** | Claude API | Context awareness + dialogue quality |
| **SEO Metadata** | Claude API | Consistency with script context |
| **TTS** | Google Studio | Multi-voice support, natural quality |
| **Image Generation** | Claude API + ChatGPT API | Flexibility, high quality results |
| **Video Assembly** | FFmpeg | Open-source, powerful, free |
| **CLI Framework** | Python (argparse/Click) | Simple, learner-friendly |
| **State Management** | JSON/YAML files | Transparent, debuggable |

---

## Incremental Testing Strategy

- **Phase 1 Test:** Generate script → validate output manually
- **Phase 2 Test:** Generate script + SEO metadata → check consistency
- **Phase 3 Test:** Generate audio separately → test voice quality
- **Phase 4 Test:** Combine all → produce test video
- **Phase 5 Test:** Full pipeline on 3-5 topics → iterate

---

## Key Design Decisions

1. **File-based Agent Handoffs** (Phase 1-2): JSON files between agents for transparency & debugging
   - Alternative: Direct API calls (Phase 3+)

2. **Voice Management**: Parse dialogue into speaker turns, call Google Studio API separately per voice
   - Alternative: Pre-record voice samples, mix algorithmically

3. **Image Generation**: Dynamic prompts from Claude based on script content
   - Alternative: Template-based with text overlays

4. **Video Duration**: Calculate from audio length, use silent padding if needed
   - Alternative: Fixed duration with speed adjustment

---

## Content Specifications (from Your Prompts)

### Script Requirements
- Length: 1500-2000 words (10-15 minute video)
- Style: Podcast conversation (Sarah & Alex)
- Language: Beginner-friendly English
- Format: Natural dialogue with pauses, reactions, humor
- Opening: 1-15 sec hook + channel greeting + learning objectives
- Closing: Call-to-action (Like, Comment, Subscribe)

### Topic Quality Criteria (Script Generation)
When generating scripts, topics must meet:
- **High YouTube search demand** — Popular keywords with sustained interest
- **Evergreen search potential** — Timeless content, remains relevant long-term
- **Trending or seasonally relevant** — Current/upcoming demand signals
- **Beginner-friendly** — Simple, relatable, easy to understand
- **Suitable for 10-15 min conversation** — Natural pacing, not rushed
- **Encourages watch-until-end** — Narrative flow, story elements, practice
- **Teaches everyday vocabulary** — Practical, usable in real conversations
- **Strong thumbnail potential** — Visual hooks, emotional expressions, context
- **Strong CTR potential** — Curiosity gap, benefit-driven, relatable
- **Practical & relatable** — Real-world scenarios (work, friends, daily life)
- **Platform-friendly** — Recommendations-ready, shareable, engagement-worthy

### Character Specifications
- **Sarah**: English Teacher, 24, teacher role, confident/warm/patient
- **Alex**: English Learner, 25, learner role, curious/friendly/relaxed
- Identical physical appearance across videos (only clothing/pose/expression changes)

## Success Criteria

✓ Topic input → MP4 video output (end-to-end)
✓ Both character voices in dialogue (Sarah + Alex distinct)
✓ Script matches specifications (1500-2000 words, beginner-friendly)
✓ Thumbnail follows brand guidelines (no text, character consistency)
✓ Video image preserves visual identity (16:9, podcast setup)
✓ SEO metadata includes title, description, hashtags, tags
✓ Video plays properly in standard players
✓ Reusable pipeline (no manual tweaking per video)
✓ Clear error messages for debugging
✓ All prompts and references versioned in `/references`

---

## Output Folder Structure

Each video generation creates a topic-based folder with these files:

```
outputs/
└── {topic_slug}/
    ├── script.txt              # Dialogue script (Sarah + Alex, 1500-2000 words)
    ├── seo_metadata.json       # Title, description, hashtags, tags
    ├── thumbnail.png           # YouTube thumbnail (1280×720, no text)
    ├── video_scene.png         # Long-form video scene (1920×1080)
    └── output_video.mp4        # Final video (audio + scene, 10-15 min)
```

---

## PHASE 2: SEO Metadata Agent with Thumbnail Text - READY_TO_IMPLEMENT

### Status: 🚀 READY_TO_IMPLEMENT (Phase 1 Testing Complete)

**Approval Status:** Phase 1 tested and approved. Phase 2 ready to begin.

**Phase 2 Focus:** Generate SEO metadata optimized for maximum YouTube search traffic + thumbnail text

---

### Phase 2 Architecture

```
Phase 1 Output (Script)
        │
        ▼
┌──────────────────────────────────┐
│  Script Generation Agent         │
│  (Phase 1)                       │
│                                  │
│ Input: Topic                     │
│ Output: script.txt               │
└────────┬─────────────────────────┘
         │
         │ (File handoff: script.txt)
         │
         ▼
┌──────────────────────────────────┐
│  SEO Metadata Agent (NEW)        │
│  - Modern YouTube SEO Strategy   │
│  - Trend-based optimization      │
│  - Title (65 chars)              │
│  - Description (500+ words)      │
│  - Hashtags (15-20)              │
│  - Tags (15-20)                  │
│  - Thumbnail Text                │
└────────┬─────────────────────────┘
         │
         ▼
   Output Folder ({topic}/)
   ├── script.txt
   ├── script_metadata.json
   └── seo_metadata.txt ← NEW
```

---

### SEO Strategy for Maximum Views (2026)

**Core Strategy: Trend-Based Search Optimization**

1. **Title Optimization**
   - Format: `[Benefit/Question] | [Channel Focus]`
   - Example: `How to Apologize Politely in English | Learn Natural Phrases`
   - Include: High-intent long-tail keywords
   - Max: 65 characters (YouTube limit)
   - Priority: Searchability + Click-through rate (CTR)

2. **Description Strategy**
   - First 150 chars: Keyword-rich hook (what viewers see before "more")
   - Body: Educational value + learning points
   - Include: Timestamps, related topics, calls-to-action
   - Keywords: Sprinkled naturally (3-5 main keywords)
   - Links: Suggest related videos from your channel
   - Length: 500-1000 words (improves ranking)

3. **Hashtags Strategy** (15-20 total)
   - 5-7: High-volume popular (#learnEnglish, #englishconversation)
   - 5-7: Medium-volume niche (#englishphrasesanctuary, #conversationalenglish)
   - 3-5: Long-tail specific to topic (#howtoapologizepolitely, #englishculturelession)
   - Avoid: Hashtags with <10K views (won't help ranking)

4. **Tags Strategy** (15-20 total)
   - Main keyword: Topic itself ("apologizing in English")
   - Related: Broader category ("English learning", "English conversation")
   - Long-tail: Specific phrases ("how to apologize", "polite English phrases")
   - Trending: Current English learning trends (e.g., "conversational English", "practical English")
   - Channel brand: "SPEAK ENGLISH SMARTER" (build channel authority)

5. **Thumbnail Text Strategy**
   - One bold, eye-catching text overlay
   - Format: Action word + benefit/curiosity
   - Examples:
     - "SAY NO POLITELY" (action + benefit)
     - "APOLOGIZE LIKE A NATIVE" (benefit-driven)
     - "PERFECT APOLOGY?" (curiosity gap)
   - Font: Bold, sans-serif, high contrast
   - Position: Top or center of thumbnail
   - Size: Readable at small YouTube thumbnail scale

---

### Implementation: SEO Agent (`src/agents/seo_metadata_agent.py`)

**Function Signature:**
```python
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
```

**System Prompt for Claude:**
The SEO agent's system prompt will instruct Claude to:

```
You are a YouTube SEO expert optimizing titles, descriptions, hashtags, tags, and thumbnail text 
for an English learning channel (SPEAK ENGLISH SMARTER).

GOAL: Maximize search traffic and views through trend-based optimization.

ANALYSIS:
1. Analyze the script topic for trending keywords
2. Identify high-intent search phrases learners use
3. Balance searchability with authentic, clickable content

TITLE GENERATION (≤65 chars):
- Format: [Verb/Question] + [Benefit] + [Specificity]
- Include long-tail keyword (topic-specific)
- Make it searchable AND clickable
- Example: "How to Apologize Politely in English | Learn Natural Phrases"

DESCRIPTION GENERATION (500-1000 words):
- Hook (first 150 chars): Most important keywords, compelling
- Body: Explain what viewers will learn, educational value
- Keywords: Sprinkle naturally (target: 3-5 main keywords)
- Calls-to-action: "Like", "Subscribe", "Comment"
- Related: Suggest related topics/videos
- Timestamps: Major sections of the video
- Total: 500+ words for ranking

HASHTAGS (15-20):
- 40% High-volume (#learnEnglish, #englishconversation)
- 40% Medium-volume niche (#englishphrases, #englishcultureesson)
- 20% Long-tail specific (#howtoapologizepolitely)
- Avoid: Hashtags with <10K views
- Priority: Relevance over virality

TAGS (15-20):
- Main: Topic keyword phrase
- Related: Broader learning categories
- Specific: Long-tail variations
- Trending: Current English learning trends
- Brand: "SPEAK ENGLISH SMARTER"

THUMBNAIL TEXT (One line):
- Verb + Benefit OR Curiosity gap
- ALL CAPS or Key words capitalized
- Examples: "SAY NO POLITELY", "APOLOGIZE LIKE NATIVE", "PERFECT APOLOGY?"
- Compelling, readable, urgent tone

TRENDING FOCUS (2026):
- Prioritize: Conversational English, practical communication
- Include: Real-world scenarios (work, social, daily life)
- Avoid: Academic, complex grammar focus
- Emphasis: Confidence in speaking, natural phrasing
```

---

### SEOMetadata Model Update

**Update `src/models.py`:**

```python
class SEOMetadata(BaseModel):
    """YouTube SEO metadata for a video."""
    title: str                          # ≤65 chars
    description: str                    # 500+ words
    hashtags: list[str]                 # 15-20 items
    tags: list[str]                     # 15-20 items
    thumbnail_text: str                 # One compelling line (NEW)
    
    @validator("title")
    def validate_title_length(cls, v):
        if len(v) > 65:
            raise ValueError(f"Title must be 65 characters or less, got {len(v)}")
        return v
    
    @validator("description")
    def validate_description_length(cls, v):
        if len(v) < 500:
            raise ValueError(f"Description should be 500+ words, got ~{len(v.split())}")
        return v
    
    @validator("thumbnail_text")
    def validate_thumbnail_text(cls, v):
        if not v or len(v) < 3:
            raise ValueError("Thumbnail text must be provided and meaningful")
        if len(v) > 100:
            raise ValueError(f"Thumbnail text should be concise (≤100 chars), got {len(v)}")
        return v
```

---

### Output Format: seo_metadata.txt

**File: `outputs/{topic}/seo_metadata.txt`**

```
=== YOUTUBE SEO METADATA ===
GENERATED FOR: [Topic Name]
OPTIMIZED FOR: Maximum Search Traffic & Views

TITLE:
[Title - up to 65 characters]

THUMBNAIL TEXT:
[Single compelling text overlay for thumbnail]

HASHTAGS:
[#hashtag1] [#hashtag2] [#hashtag3] ... [#hashtag20]

TAGS:
[tag1], [tag2], [tag3], ... [tag20]

DESCRIPTION:
[500-1000 word description with keywords, structure, and CTAs]

---
Generated by SPEAK ENGLISH SMARTER SEO Agent
Strategy: Trend-Based Search Optimization (2026)
```

---

### Implementation Tasks

#### Task 1: Create SEO Agent (`src/agents/seo_metadata_agent.py`)

**Functions to implement:**

```python
def load_seo_prompt():
    """Load SEO generation prompt with modern strategy."""
    
def generate_seo_metadata(script: Script, topic_input: TopicInput) -> SEOMetadata:
    """Generate SEO metadata optimized for maximum views."""
    # Call Claude API with enhanced SEO prompt
    # Parse title, description, hashtags, tags, thumbnail_text
    # Validate all fields
    # Return SEOMetadata object
    
def save_seo_metadata_to_file(seo_metadata: SEOMetadata, output_folder: Path) -> Path:
    """Save SEO metadata as formatted text file."""
    # Format metadata as above
    # Save to seo_metadata.txt
    # Return file path
```

---

#### Task 2: Update CLI Integration (`scripts/cli.py`)

**Sequential workflow:**

```python
# 1. Generate script (Phase 1)
script = generate_script(topic_input, target_words=target_words, tolerance=None)
script_path = save_script_to_file(script, output_folder)

# 2. Generate SEO metadata (Phase 2) - NEW
seo_metadata = generate_seo_metadata(script, topic_input)
seo_path = save_seo_metadata_to_file(seo_metadata, output_folder)

# 3. Display results
print(f"\n=== SEO Metadata Generated ===")
print(f"Title: {seo_metadata.title}")
print(f"Thumbnail Text: {seo_metadata.thumbnail_text}")
print(f"Hashtags: {' '.join(seo_metadata.hashtags[:5])}...")
print(f"Tags: {', '.join(seo_metadata.tags[:5])}...")
print(f"Description: {seo_metadata.description[:200]}...")
```

---

#### Task 3: Output Folder Structure

```
outputs/
└── {topic_slug}/
    ├── script.txt              # Phase 1: Dialogue script
    ├── script_metadata.json    # Phase 1: Script stats
    └── seo_metadata.txt        # Phase 2: SEO (NEW)
                                 ├── Title
                                 ├── Thumbnail Text
                                 ├── Hashtags
                                 ├── Tags
                                 └── Description
```

---

### Testing Strategy for Phase 2

**Test Script: `tests/test_phase_2.py`**

```python
def test_seo_generation():
    """Test SEO metadata generation for multiple topics."""
    topics = [
        "How to Apologize Politely",
        "Making Small Talk at Parties",
        "Job Interview English Tips",
        "Casual English Slang",
        "Business Email Writing"
    ]
    
    for topic in topics:
        # Generate script
        script = generate_script(topic)
        
        # Generate SEO
        seo = generate_seo_metadata(script, topic)
        
        # Validate
        assert len(seo.title) <= 65
        assert len(seo.description) >= 500
        assert len(seo.hashtags) == 20
        assert len(seo.tags) == 20
        assert len(seo.thumbnail_text) > 0
        assert len(seo.thumbnail_text) <= 100
        
        # Save and verify file
        path = save_seo_metadata_to_file(seo, output_folder)
        assert path.exists()
```

**Success Criteria:**
- ✅ All 5 topics generate valid SEO metadata
- ✅ Validation passes: title ≤65, description ≥500 words, hashtags=20, tags=20
- ✅ Thumbnail text is compelling and concise (≤100 chars)
- ✅ Files created: script.txt + seo_metadata.txt
- ✅ SEO content is optimized for search traffic
- ✅ No API errors

---

### Phase 2 Completion Checklist

- [ ] Updated `src/models.py` with thumbnail_text field in SEOMetadata
- [ ] Created `src/agents/seo_metadata_agent.py` with modern SEO strategy
- [ ] Implemented `generate_seo_metadata()` function
- [ ] Implemented `save_seo_metadata_to_file()` function
- [ ] Updated `scripts/cli.py` with Phase 2 integration
- [ ] Tested: Generate script + SEO for 5 diverse topics
- [ ] All validation passes (title, description, hashtags, tags, thumbnail_text)
- [ ] SEO metadata is trend-focused and search-optimized
- [ ] Created `tests/test_phase_2.py` for comprehensive testing
- [ ] Created `docs/PHASE_2_README.md` with SEO strategy guide
- [ ] Updated `CLAUDE.md` with Phase 2 status
- [ ] Output files verified: script.txt + seo_metadata.txt
- [ ] Ready for Phase 2 approval

---

### Key Learning Outcomes for Phase 2

✅ **Data Flow Between Agents:** Script output → SEO input  
✅ **File-based Handoffs:** script.txt used by SEO agent  
✅ **Sequential Workflow:** Generate → Process → Save  
✅ **API Integration:** Claude generates diverse metadata types  
✅ **Validation Patterns:** Multiple field types with different constraints  
✅ **YouTube SEO Best Practices:** Real-world application of optimization  

---

### Next Phase (Phase 3)

After Phase 2 approval:
- **Phase 3:** TTS Agent + Image Generation Agent
- Generate audio with distinct voices (Sarah & Alex)
- Generate thumbnail.png and video_scene.png images
- Keep same sequential workflow pattern

---

## PHASE 3: Text-to-Speech + Image Generation - NOT_STARTED

### Status: BLOCKED - Waiting for Phase 1 Approval

**Do not start until:** Phase 1 passes testing and Phase 2 receives approval.

---

## PHASE 4: Video Assembly (FFmpeg) - NOT_STARTED

### Status: BLOCKED - Waiting for Phase 1 Approval

**Do not start until:** Phase 1 passes testing, Phases 2-3 receive approval.

---

## PHASE 5: Production Polish - NOT_STARTED

### Status: BLOCKED - Waiting for Phase 1 Approval

**Do not start until:** Phase 1 passes testing, all other phases approved.

---

## RESUMPTION INSTRUCTIONS FOR FUTURE SESSIONS

### When returning to this project:

1. **Check Phase Status:** Look at the `PHASE STATUS TRACKER` at the top of this file
2. **Read This Plan:** It's the source of truth for what's been done
3. **Check Phase 1:** 
   - If `READY_FOR_TESTING`: Run tests, get approval, then move to Phase 2
   - If already approved: Proceed to Phase 2
4. **Never Start Unapproved Phases:** Only work on the next phase if previous phases approved
5. **Update Status:** When a phase is approved/completed, update the status tracker above

### Critical Files:
- **Implementation:** `src/` directory (Python package)
- **CLI:** `scripts/cli.py`
- **Documentation:** `docs/` directory
- **Tests:** `tests/test_phase_1.py`
- **Plan:** This file

### Session Checkpoints:
- Phase 1 testing → Approval (user decision)
- Phase 2 planning → Implementation → Approval
- Phase 3 planning → Implementation → Approval
- Phase 4 planning → Implementation → Approval
- Phase 5 planning → Implementation → Deployment

---

## Status: Ready for Phase 1 Testing

**Next Action:** Test Phase 1 implementation
- Run: `python scripts\cli.py generate`
- Test: Generate scripts for 3-5 topics
- Verify: Output quality, file structure, error handling
- Then: Submit for user approval
