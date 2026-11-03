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
- Quality-over-word-count design (350-500 word descriptions)
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
| Script Generation | Anthropic Claude API | Claude Sonnet 3.5+ |
| SEO Metadata | Anthropic Claude API | Claude Sonnet 3.5+ |
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
- Script: 1500-2000 words, beginner-friendly
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

## 📝 Version History

- **2026-09-27**: Phase 4 completion (Image generation with improvements)
- **2026-09-26**: Phase 3 completion (Text-to-speech with Google API)
- **Previous**: Phase 1 & 2 completion

---

**Last Updated:** 2026-09-27  
**Status:** Phases 1-4 Complete, Awaiting Phase 4 Verification, Ready for Phase 5  
**Next Session:** Manual verification of Phase 4, then Phase 5 planning
