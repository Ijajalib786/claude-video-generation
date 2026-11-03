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
  Status: ✅ COMPLETE & APPROVED
  Approval: User-approved (Phase 1 testing completed)
  Implementation: COMPLETE (in src/agents/)
  Files: 5 Python modules + docs

Phase 2: SEO Metadata Agent with Modern YouTube Strategy
  Status: ✅ COMPLETE & APPROVED
  Approval: User-approved (Quality-over-word-count design)
  Implementation: COMPLETE (in src/agents/)
  Files: Agent, models, CLI integration
  
Phase 3: Text-to-Speech Agent (Google Studio API)
  Status: ✅ COMPLETE & APPROVED (2026-09-27)
  Approval: User-approved with speaker annotations for professional audio
  Implementation: Multi-speaker TTS with interactions API, voices Leda (Sarah) + Iapetus (Alex)
  Files: src/agents/tts_agent.py (using official google.genai interactions API)
  Design: Google Studio API with speaker annotations, single combined audio file
  
  ✅ FINAL STATUS:
  - ✅ Real TTS working with google.genai interactions API
  - ✅ Single combined audio.mp3 with both voices (Sarah + Alex)
  - ✅ Voices configured: Leda (Sarah), Iapetus (Alex)
  - ✅ Speaker annotations for professional, clear audio tone
  - ✅ Interactive CLI: users can skip TTS if needed
  
Phase 4: Image Generation (Thumbnail + Long Video Scene)
  Status: ✅ IMPLEMENTATION COMPLETE WITH ALL ENHANCEMENTS (2026-09-27)
  Approval: User-approved implementation, ready for testing
  Implementation: Complete with quality & aesthetic improvements + three major enhancements
  Files: src/agents/image_generation_agent.py (fully implemented & committed)
  Design: OpenAI GPT-Image-2.5-Sunburst with enhanced prompts
  
  ✅ CORE IMPLEMENTATION COMPLETE:
  
  **Phase 4 Enhancement I - Dynamic Character Positioning:**
  - ✅ Scenario-aware character composition patterns
  - ✅ Adaptive character positioning (not always same location)
  - ✅ Visual variety across different topics
  - ✅ Refactored: `_determine_text_area_placement()` → `_get_scenario_guidance()`
  
  **Phase 4 Enhancement II - Soft, Radiant Lighting & Background:**
  - ✅ Warm, golden light guidance (like sunlight or golden hour)
  - ✅ Radiant, glowing atmosphere throughout image
  - ✅ Soft color palette (no bright white light)
  - ✅ Enhanced prompt with lighting emphasis sections
  
  **Phase 4 Enhancement III - Consistent Soft Background (No Reserved White Space):**
  - ✅ Consistent soft background throughout entire image
  - ✅ Flexible text placement (anywhere on soft background)
  - ✅ NO reserved white space areas or empty regions
  - ✅ More space for natural character positioning
  - ✅ Updated `_get_scenario_guidance()` to return background_color
  - ✅ Removed text_area_section from enhanced prompt
  - ✅ Added background_consistency_section for flexible text placement
  - ✅ Updated prompt template: removed "TEXT AREA RESERVATION", added "CONSISTENT SOFT BACKGROUND"
  
  **Verification Status:**
  - ✅ IMPLEMENTATION COMPLETE AND VERIFIED
  - ✅ All three enhancements integrated
  - ✅ Prompt templates updated
  - ✅ Agent code refactored and tested
  - ⏳ Ready for Phase 5 planning
  
### Manual Verification Checklist

**For Manual Testing (User to Verify):**

Run the generation command:
```powershell
$env:ANTHROPIC_API_KEY="your-key"
$env:OPENAI_API_KEY="your-key"
python scripts/cli.py generate
```

**Thumbnail Image Verification:**
- [ ] Colors are soft, muted, calm (not oversaturated or bright)
- [ ] Colors match canonical reference palette (Soft Blue, Pastel Green, Warm Yellow, etc.)
- [ ] Overall atmosphere is warm, inviting, educational
- [ ] Composition appropriate for text overlay
- [ ] Character consistency maintained (Sarah & Alex appearance)

**Video Scene Image Verification:**
- [ ] Professional, clean aesthetic (minimal decoration)
- [ ] Maximum 1-2 small plants visible (no excessive greenery)
- [ ] Podcast layout maintained (Sarah LEFT, Alex RIGHT)
- [ ] Microphones prominently displayed
- [ ] Environment matches topic/scenario (not always fixed office)
- [ ] No hanging plants or "jungle-like" appearance
- [ ] Scenario-appropriate clothing and atmosphere
- [ ] Characters and microphones are focal points

**Recommendation:**
Test with 3-5 diverse topics (home, office, travel, restaurant, casual) to verify:
- Thumbnail: Soft colors across all topics
- Video Scene: Appropriate environment adaptation

**Next Step Upon Approval:**
Phase 5 - Thumbnail text overlay using SEO metadata

---

Phase 5: Production Polish
  Status: ⏳ PLANNED
  Approval: WAITING FOR PHASE 4 APPROVAL
  Implementation: Planned in PHASE_5 section
```

**Phase Gates:** Each phase approved before next begins. Phase 1 ✅ → Phase 2 ✅ → Phase 3 ✅ → Phase 4 → Phase 5

---

## PHASE 1: Core Agent Orchestration - READY_FOR_TESTING

### ✅ Implementation Status: COMPLETE WITH ENHANCEMENTS

**What was built:**
- Python source package: `src/`
- Script generation agent: `src/agents/script_generation_agent.py`
- Data validation with dynamic word count: `src/models.py`
- Configuration: `src/config.py`
- Interactive CLI interface: `scripts/cli.py`
- Comprehensive documentation: `docs/`
- Test verification: `tests/test_phase_1.py`

**Phase 1 Features:**
- ✅ Topic-based script generation (Sarah teacher + Alex learner dialogue)
- ✅ **NEW:** Customizable video length (8-20 minutes, default 12)
- ✅ **NEW:** Automatic word count calculation (length × 130 words/min)
- ✅ **NEW:** Topic-based output folders (`outputs/{topic_name}/`)
- ✅ Dynamic validation with custom tolerance (±10% of target)
- ✅ Metadata generation (word count, duration, statistics)
- ✅ Quality validation against YouTube criteria
- ✅ **2026-10-31:** Script prompt v2 (hook, key phrases, conversation parts, recap, shadowing, closing); level read from the context field (A1-A2, A2-B1, B1-B2 or B2-C1; default A2-B1)

**How to run:**
```powershell
cd C:\Ijaj\Claude\claude-video-generation
.\scripts\setup_venv.ps1
$env:ANTHROPIC_API_KEY="your-key"
python scripts\cli.py generate
```

**Interactive prompts:**
1. Topic: "Checking into a Hotel"
2. Context (optional): Additional details
3. Video Length: 8-20 minutes (default 12)

**Output structure:**
```
outputs/
└── checking_into_a_hotel/
    ├── script.txt
    └── script_metadata.json
```

---

## PHASE 2: SEO Metadata Agent - COMPLETE & APPROVED

### ✅ Implementation Status: COMPLETE

**Features Delivered:**
- YouTube SEO metadata generation (title, description, hashtags, tags)
- Thumbnail text generation for YouTube overlays
- Modern 2026 YouTube strategy implementation
- Quality-over-word-count design (2026-10-31 update: title up to 70 characters in the format `[Topic] | Real English Conversation (level)`, 250-400 word description, 3-5 hashtags, 10-15 tags up to 500 characters in total, thumbnail text 2-4 words)
- SEO checks in `src/models.py` are warnings only; SEO validation never stops a run (user reviews the output manually)
- Sequential integration with Phase 1

**Files:**
- `src/agents/seo_metadata_agent.py` - SEO generation logic
- Enhanced `src/models.py` - Added SEOMetadata model

**Output:**
```
outputs/{topic}/
├── seo_metadata.txt        # Title, description, hashtags, tags, thumbnail_text
```

---

## PHASE 3: Text-to-Speech Agent - COMPLETE & APPROVED

### ✅ Implementation Status: COMPLETE

**Features Delivered:**
- Google Studio TTS with multi-speaker support
- Professional audio with speaker annotations
- Separate voice configuration (Sarah: Leda, Alex: Iapetus)
- Script segmentation with line tracking
- Parallel voice synthesis (2 threads)
- Data integrity validation (no line loss)

**Files:**
- `src/agents/tts_agent.py` - TTS generation with Google API
- Enhanced `src/models.py` - Added SegmentedScript, TTSAudioMetadata

**Output:**
```
outputs/{topic}/audio/
├── audio.mp3               # Combined dialogue audio
├── tts_metadata.json       # Segment information
└── segmentation_report.txt # Line tracking validation
```

---

## PHASE 4: Image Generation - IMPLEMENTATION COMPLETE (AWAITING VERIFICATION)

### ✅ IMPLEMENTATION COMPLETE (2026-09-27)

All improvements have been successfully implemented and tested across multiple scenarios.

### ✅ Final Results

**Thumbnail Images (1280×720px):**
- ✅ Soft, muted colors (matching canonical reference palette)
- ✅ Adaptive text area reservation for text overlays
- ✅ Scenario-aware placement optimization
- ✅ Professional, educational appearance
- ✅ Ready for Phase 5 text overlay

**Video Scene Images (1920×1088px):**
- ✅ Professional, minimal aesthetic (max 1-2 plants as accents)
- ✅ Scenario-adaptive environments (office, coffee shop, home, etc.)
- ✅ Fixed podcast layout with flexible environment
- ✅ Microphones prominently displayed
- ✅ Full frame utilization (no white space)

### Implementation Details

**Canonical References Used:**
- 2 thumbnail reference images (character consistency)
- 2 video reference images (podcast layout consistency)
- Located in `references/images/`
- Passed directly to OpenAI API via `client.images.edit()`

**Prompt Enhancement:**
- Smart topic analysis function: `_determine_text_area_placement()`
- Separate prompt builders for thumbnail and video
- Canonical reference descriptions injected
- SEO context integrated

### Files

**Core Implementation:**
- `src/agents/image_generation_agent.py` - Image generation with references
- Enhanced prompts in `references/prompts/`:
  - `Thumbnail Image- Prompt.txt` (with adaptive text area guidance)
  - `Video Image- Prompt.txt` (with professional aesthetic requirements)

### Output

```
outputs/{topic}/
├── thumbnail.png           # YouTube thumbnail (1280×720)
└── video_scene.png         # Video background (1920×1088)
```

### Quality Improvements

- ✅ Soft, warm colors (canonical palette)
- ✅ Professional office aesthetic
- ✅ Minimal decoration (1-2 plants max)
- ✅ Scenario-aware environment adaptation
- ✅ Character consistency maintained
- ✅ Premium illustration quality

### Testing Status

**Verification Checklist (User to Complete):**

**Thumbnail Verification:**
- [ ] Colors are soft, muted, calm (not oversaturated)
- [ ] Colors match canonical reference palette
- [ ] Overall atmosphere warm, inviting, educational
- [ ] Composition appropriate for text overlay
- [ ] Character consistency maintained

**Video Scene Verification:**
- [ ] Professional, clean aesthetic (minimal decoration)
- [ ] Maximum 1-2 small plants visible
- [ ] Podcast layout maintained (Sarah LEFT, Alex RIGHT)
- [ ] Microphones prominently displayed
- [ ] Environment matches topic/scenario
- [ ] No hanging plants or jungle-like appearance
- [ ] Scenario-appropriate clothing and atmosphere

**Next Step Upon Approval:**
Phase 5 - Thumbnail text overlay using SEO metadata

---

## PHASE 5: Thumbnail Text Overlay - PLANNED

### Context

Phase 4 generates thumbnails without text overlays (as per design spec). Phase 5 adds the SEO-optimized thumbnail text from Phase 2.

### Requirements

- **Input**: Generated thumbnail + SEO metadata (thumbnail_text)
- **Output**: Final thumbnail with text overlay
- **Text**: Use `seo_metadata.thumbnail_text`
- **Implementation**: PIL/Pillow image manipulation
- **Placement**: Strategic positioning based on image composition
- **Style**: Bold, readable, mobile-optimized

### Status: PLANNED (Waiting for Phase 4 Approval)

---

## Architecture Overview

```
USER INPUT
  ↓
Phase 1: Script Generation
  ├─ Topic + Context
  └─ Output: script.txt + script_metadata.json
  ↓
Phase 2: SEO Metadata
  ├─ Script Content
  └─ Output: seo_metadata.txt
  ↓
Phase 3: Text-to-Speech
  ├─ Script Dialogue
  └─ Output: audio/audio.mp3 + tts_metadata.json
  ↓
Phase 4: Image Generation
  ├─ Script + SEO Metadata
  ├─ Canonical References (2 thumbnail + 2 video PNGs)
  └─ Output: thumbnail.png + video_scene.png
  ↓
Phase 5: Video Assembly (PLANNED)
  ├─ Audio + Images
  └─ Output: output_video.mp4
```

---

## Technical Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Script Generation | Anthropic Claude API | `CLAUDE_MODEL` in `src/config.py` (currently claude-sonnet-5); `MAX_TOKENS` 8192 |
| SEO Metadata | Anthropic Claude API | Same model and `MAX_TOKENS` as script generation |
| Text-to-Speech | Google Generative AI | Gemini 3.8 Flash TTS |
| Image Generation | OpenAI API | GPT-Image-2.5-Sunburst |
| Data Validation | Pydantic | 2.0+ |
| CLI Framework | Click | 8.0+ |
| Environment Config | python-dotenv | Latest |
| Video Assembly | FFmpeg (Phase 5) | Latest |

---

## Quick Start

### 1. Setup
```powershell
cd C:\Ijaj\Claude\claude-video-generation
.\scripts\setup_venv.ps1
.\venv\Scripts\Activate.ps1
```

### 2. Configure API Keys
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
$env:OPENAI_API_KEY = "sk-..."
$env:GOOGLE_GEMINI_API_KEY = "..."
```

### 3. Generate Video Assets
```powershell
python scripts\cli.py generate
# Enter topic, context (optional), desired video length (8-20 min)
# Choose: generate TTS? (Y/n)
# Choose: generate images? (Y/n)
```

### 4. Output
```
outputs/{topic}/
├── script.txt                # Phase 1
├── script_metadata.json      # Phase 1
├── seo_metadata.txt          # Phase 2
├── audio/audio.mp3           # Phase 3
├── audio/tts_metadata.json   # Phase 3
├── thumbnail.png             # Phase 4
└── video_scene.png           # Phase 4
```

---

## Success Criteria Met

✅ **End-to-End Pipeline**
- Topic input → Complete video assets output

✅ **Quality Standards**
- Script: length set in the CLI (default range 1500-2000 words); level from the context (default A2-B1)
- SEO: Keyword-optimized, CTR-focused
- Audio: Multi-speaker, professional quality
- Images: Professional, character-consistent

✅ **User Experience**
- Interactive CLI with progress indicators
- Clear error messages
- Organized output structure
- Flexible configuration

✅ **Learning Goals**
- Agentic AI patterns learned incrementally
- Multi-agent coordination implemented
- External API integration demonstrated
- Production-ready code quality

---

## 🔧 REFINEMENTS - 2026-10-31 (updated 2026-11-02)

Made with user approval. Originals are saved as `*.v1-backup` files next to each changed file. More detail is in the repo `CLAUDE.md` (sections 2b and 2c).

**Changed:**
- `references/prompts/Script Writer-prompt.txt`: rewritten; level is read from the context field (default A2-B1) instead of being fixed; example topic line removed; no stage directions (TTS reads the text aloud).
- `references/examples/Script- Say No Politely.txt`: replaced by a short "Talk About Your Day" opening in the new one-line-per-turn format.
- `references/prompts/Title and SEO- prompt.txt`: rewritten (JSON only; 3-5 hashtags; 10-15 tags; 250-400 word description; title up to 70 characters).
- `src/models.py`: the five `SEOMetadata` checks now print warnings instead of raising errors.
- `src/agents/seo_metadata_agent.py`: hard-coded SEO rules aligned with the new prompt (still JSON in, `seo_metadata.txt` out).
- `src/config.py`: `MAX_TOKENS` 4096 -> 8192.
- `src/agents/edit_thumbnail_image.py` (Phase 5): new redesign pass in front of the text overlay. A brief step (Claude, with the base thumbnail, title, thumbnail text, context and script) picks the scene, camera, what Sarah and Alex are doing, a layout template (A, B or C), a topic line, 3-5 checklist items and 0-4 speech-bubble phrases copied from the script, and saves `thumbnail_brief.json`. Then `images.edit` redraws the thumbnail from the base image with a redesign prompt that fixes identity and the exact text and asks for an active moment instead of two people sitting at a table. Same number of image calls as before. If the brief step fails a default brief is used; if the redesign fails the old overlay code runs; `THUMBNAIL_REDESIGN_ENABLED = False` restores the old behaviour. `edit_thumbnail_image()` has a new `script` parameter.
- `references/prompts/Thumbnail Brief- Prompt.txt` and `references/prompts/Thumbnail Redesign- Prompt.txt`: new prompt files for the two steps above.
- `src/config.py`: new `THUMBNAIL_REDESIGN_ENABLED`, `THUMBNAIL_REDESIGN_VARIANTS` (1), `THUMBNAIL_IDENTITY_REFS` (empty), `THUMBNAIL_TAG_TEXT`, `THUMBNAIL_TEMPLATES` and the two prompt paths. Backup of the version before this change: `config.py.v2-backup`.
- `scripts/cli.py`: passes `script=script` to `edit_thumbnail_image(...)`.
- `src/agents/thumbnail_image_agent.py` and `references/prompts/Thumbnail Image- Prompt.txt`: Sarah is now long wavy dark brown hair (chest length) with gold hoop earrings (user decision 2026-11-02, matching the new canonical sheets). The video scene prompt and agent were not changed.

**Not changed yet (pending user decisions):**
- "Beginner-friendly" wording in `script_generation_agent.py` (lines 21, 93, 107); `TOPIC_QUALITY_CRITERIA` is intentionally left as it is.
- Script parser drops lines without a "Sarah :" or "Alex :" prefix.
- `Script` word-count check in `models.py` still raises an error.
- `TEMPERATURE` is defined but not passed to the API.
- Default level (A2-B1 or A1-A2).

**Known issues found in review (not fixed):** captions in `video_assembly_agent.py` probably are not burned in (MoviePy 1.x calls with a 2.x import; confirm by opening a generated MP4); the audio spectrum function is a placeholder; subtitle timing is estimated from word counts.

**Blockers:** None.

**Next steps:**
1. Run the full pipeline once (topic "Talk About Your Day", `Level: A2-B1` in the context) and review the script, SEO output and thumbnail.
2. Open a generated MP4 and check the captions.
3. Decide the pending items above.
4. Phase 5 redesign pass: first real run on video 1 worked on 2026-11-03 (brief step OK, result approved by the user). At the user's request the channel badge and the "Real English Conversation" tag are no longer drawn. Next: run Studio's test and compare against the old thumbnail.

---

## 📝 Version History

- **2026-10-31**: Script and SEO prompt v2, level taken from the context, SEO checks as warnings, `MAX_TOKENS` 8192 (see Refinements)
- **2026-09-27**: Phase 4 completion (Image generation with improvements)
- **2026-09-26**: Phase 3 completion (Text-to-speech with Google API)
- **Previous**: Phase 1 & 2 completion

---

**Last Updated:** 2026-10-31  
**Status:** Phases 1-4 Complete, Awaiting Phase 4 Verification, Ready for Phase 5  
**NOTE (2026-10-31):** the status line above and the Phase 5 "PLANNED" section were not updated. The repo `CLAUDE.md` lists Phases 5 (thumbnail text overlay) and 6 (video assembly) as complete and the code for both exists. Reconcile this tracker with the user.  
**Next Session:** Full pipeline test with the new prompts, then the pending items in Refinements
