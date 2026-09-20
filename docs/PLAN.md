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

## PHASE 2: SEO Metadata + Multi-Agent Coordination - NOT_STARTED

### Status: BLOCKED - Waiting for Phase 1 Approval

**Do not start until:** Phase 1 passes testing and receives explicit approval.

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
