# CLAUDE.md - Project Instructions for Claude Code

This file contains permanent instructions for working on this project. Follow these guidelines for all sessions.

---

## 🎯 Project: SPEAK ENGLISH SMARTER - Video Generation Pipeline

**Purpose:** Build an automated, incremental video generation pipeline for English learning content.

**Input:** Topic → **Output:** Complete MP4 video (script, audio, images, metadata)

**Learning Goal:** ✅ COMPLETE - All 6 phases successfully implement Agentic AI patterns

---

## 📍 ALWAYS START HERE

### 1. Check the Plan First
**File:** `docs/PLAN.md` (or `C:\Users\ijajb\.claude\plans\i-want-you-to-lively-gadget.md`)

Read the **PHASE STATUS TRACKER** to understand:
- Which phase is currently being worked on
- What's approved vs. blocked
- What was last done

### 2. Current Project Status (2026-09-27)
```
Phase 1: ✅ COMPLETE & APPROVED
Phase 2: ✅ COMPLETE & APPROVED
Phase 3: ✅ COMPLETE & APPROVED
Phase 4: ✅ COMPLETE & APPROVED
Phase 5: ✅ COMPLETE & APPROVED (Thumbnail text overlay)
Phase 6: ✅ COMPLETE & APPROVED (Video assembly with audio)
```

**🎉 ALL PHASES COMPLETE!** Full end-to-end video generation pipeline is functional and ready for production use.

### 3. Know Your Role
- **Phase 1 (Testing):** Run scripts, verify output, get approval
- **Phase 2+ (Implementation):** Only start if previous phase approved

---

## 🚀 Quick Start (Full Pipeline)

### Setup (First Time Only)
```powershell
cd C:\Ijaj\Claude\claude-video-generation
.\scripts\setup_venv.ps1
```

### Run Full Pipeline (Phases 1-4)
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
$env:OPENAI_API_KEY="sk-your-openai-key"
$env:GOOGLE_GEMINI_API_KEY="your-google-key"
python scripts\cli.py generate
```

### Interactive Prompts
The CLI will ask for:
1. **Topic:** "Checking into a Hotel"
2. **Context (optional):** Additional details about the topic
3. **Video Length:** Desired length in minutes (8-20 min, default 12)
4. **Generate TTS audio? (Y/n):** Skip Phase 3 if not needed
5. **Generate images? (Y/n):** Skip Phase 4 if not needed
6. **Assemble final MP4 video? (y/N):** Defaults to No unless TTS enabled

### All Phases Implemented & Working (6/6 Complete)
- ✅ **Phase 1:** Topic-based script generation (Sarah & Alex dialogue)
- ✅ **Phase 2:** SEO metadata generation (title, description, hashtags, tags)
- ✅ **Phase 3:** Text-to-Speech with Google Studio API (multi-speaker)
- ✅ **Phase 4:** Image generation (thumbnails + video scenes)
  - Customizable video length (8-20 minutes)
  - Topic-based output folders with organized structure
  - Quality validation with dynamic tolerance
  - Thumbnails with character positioning for text space
  - Video scenes with flat vector illustration style
  - Metadata generation (comprehensive tracking)
- ✅ **Phase 5:** Thumbnail text overlay (AI-determined positioning)
- ✅ **Phase 6:** Video assembly (MP4 with audio + captions + spectrum visualization)

### Expected Output
```
outputs/
└── checking_into_a_hotel/
    ├── script.txt                   # Phase 1: Dialogue script
    ├── script_metadata.json         # Phase 1: Script statistics
    ├── seo_metadata.txt             # Phase 2: SEO metadata
    ├── audio/
    │   ├── audio.mp3                # Phase 3: Combined TTS audio
    │   ├── tts_metadata.json        # Phase 3: TTS metadata
    │   └── segmentation_report.txt  # Phase 3: Validation report
    ├── thumbnail.png                # Phase 4A: YouTube thumbnail (1280×720)
    ├── thumbnail_with_text.png      # Phase 5: Thumbnail with text overlay
    ├── video_scene.png              # Phase 4B: Video scene (1920×1088)
    ├── subtitle.srt                 # Phase 6: Auto-generated captions
    └── output_video.mp4             # Phase 6: Final video (1920×1080, 10-15 min)
```

**Output folder naming:** Topic name converted to snake_case
- "Checking into a Hotel" → `checking_into_a_hotel/`
- "How to apologize" → `how_to_apologize/`

---

## 📁 Project Structure

```
claude-video-generation/
├── docs/
│   ├── PLAN.md                    ← READ THIS FIRST
│   ├── QUICKSTART.md              ← 3-minute setup
│   ├── PHASE_1_README.md          ← Phase 1 details
│   └── [other guides]
├── src/                           ← Python source package
│   ├── config.py                  ← Configuration
│   ├── models.py                  ← Data validation
│   └── agents/
│       ├── script_generation_agent.py      ← Phase 1: Script generation
│       ├── seo_metadata_agent.py           ← Phase 2: SEO metadata
│       ├── tts_agent.py                    ← Phase 3: Text-to-speech
│       ├── thumbnail_image_agent.py        ← Phase 4A: Thumbnail images
│       ├── video_image_agent.py            ← Phase 4B: Video scenes
│       ├── edit_thumbnail_image.py         ← Phase 5: Text overlay
│       └── video_assembly_agent.py         ← Phase 6: Video assembly
├── scripts/
│   ├── cli.py                     ← Main entry point
│   ├── setup_venv.ps1             ← Virtual env setup
│   └── setup_venv.bat
├── tests/
│   └── test_phase_1.py            ← Setup verification
├── references/                    ← Prompts & examples
│   ├── prompts/
│   ├── examples/
│   └── images/
├── outputs/                       ← Generated videos
├── requirements.txt               ← Python dependencies
├── README.md                      ← Project overview
└── CLAUDE.md                      ← This file
```

---

## 🔑 Key Files & Their Purpose

| File | Purpose | Edit? |
|------|---------|-------|
| `docs/PLAN.md` | Master plan, phase tracking | Only to update status |
| `README.md` | Project overview | Rarely |
| `src/config.py` | API keys, paths, settings | Only for config changes |
| `src/agents/*.py` | Agent implementations | For new phases |
| `scripts/cli.py` | User interface | For CLI improvements |
| `requirements.txt` | Python dependencies | When adding packages |
| `references/prompts/*.txt` | Prompt templates | User controls these |

---

## 🎯 Common Tasks

### Generate a Script (Phase 1)
```powershell
python scripts\cli.py generate
# Enter topic when prompted
# Output: outputs/{topic}/script.txt
```

### Validate a Script
```powershell
python scripts\cli.py validate --script-path outputs\topic_name\script.txt
```

### Run Tests
```powershell
python tests\test_phase_1.py
```

### Activate Virtual Environment (Required)
```powershell
.\venv\Scripts\Activate.ps1
# Should see (venv) in prompt
```

---

## 📋 Phase Guidelines (All Complete as of 2026-09-27)

### Phase 1: Script Generation ✅ COMPLETE & APPROVED
**Status:** Fully implemented and tested

**Features Implemented:**
- ✅ Interactive CLI for topic input
- ✅ Topic-based output folder structure (`outputs/{topic_name}/`)
- ✅ Customizable video length (8-20 minutes)
- ✅ Automatic word count calculation (length × 130 words/min)
- ✅ Sarah & Alex dialogue format with quality validation
- ✅ Metadata generation (word count, duration, line count)

**Current State:** Ready to generate videos

### Phase 2: SEO Metadata Agent ✅ COMPLETE & APPROVED
**Status:** Fully implemented and integrated

**Features Implemented:**
- ✅ YouTube SEO metadata generation (title, description, hashtags, tags)
- ✅ Thumbnail text generation for overlays
- ✅ Sequential integration with Phase 1
- ✅ Quality-focused design (350-500 word descriptions)

**Current State:** Automatically generates with Phase 1

### Phase 3: Text-to-Speech ✅ COMPLETE & APPROVED
**Status:** Fully implemented with Google Studio API

**Features Implemented:**
- ✅ Multi-speaker TTS (Sarah: Despina, Alex: Iapetus)
- ✅ Professional speaker annotations for tone control
- ✅ Parallel voice synthesis (2 threads)
- ✅ Script segmentation with line tracking
- ✅ Interactive CLI option to skip TTS

**Current State:** Generates audio.mp3 with both voices

### Phase 4: Image Generation ✅ COMPLETE & VERIFIED
**Status:** Fully implemented with all enhancements

**Features Implemented:**
- ✅ **Thumbnail Images (1280×720px):**
  - Scenario-aware character positioning for text space
  - Soft colors with radiant lighting
  - Ready for Phase 5 text overlay
  
- ✅ **Video Scene Images (1920×1088px):**
  - Flat vector illustration style (matches canonical reference)
  - Professional podcast setup
  - Scenario-adaptive environments

**Current State:** Generates both thumbnail.png and video_scene.png

### Phase 5: Thumbnail Text Overlay ✅ COMPLETE & APPROVED
**Status:** Fully implemented with OpenAI Image Edit API

**Features Implemented:**
- ✅ AI-determined text positioning on thumbnail images
- ✅ Flexible placement based on image content analysis
- ✅ Eye-catching text styling for YouTube feed
- ✅ Mobile-optimized readability (375px viewport)
- ✅ Separate output file: thumbnail_with_text.png

**Current State:** Generates thumbnail with text overlay

### Phase 6: Video Assembly (MoviePy) ✅ COMPLETE & APPROVED
**Status:** Fully implemented with audio + video composition

**Features Implemented:**
- ✅ MoviePy video composition (video_scene.png + audio.mp3)
- ✅ Auto-generated SRT captions with TTS-aligned timing
- ✅ Caption overlay at bottom-center with semi-transparent background
- ✅ Audio spectrum visualization (librosa analysis) at top-center
- ✅ H.264 MP4 output (1920×1080, 10-15 minutes)
- ✅ Interactive prompt: Ask user whether to generate video
- ✅ Smart defaults: Skip if TTS is disabled
- ✅ SRT caption file auto-generated with audio-aligned timing

**Current State:** Generates final MP4 video with audio + captions

---

## ⚙️ Configuration

### Environment Variables
Set before running:
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

### Settings in `src/config.py`
- Model: Claude Sonnet 3.5
- Temperature: 0.7
- Script length: 1500-2000 words
- Speech rate: 130 words/minute

---

## 🐛 Troubleshooting

### "venv not found"
```powershell
.\scripts\setup_venv.ps1
```

### "ANTHROPIC_API_KEY not set"
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-key"
```

### "ModuleNotFoundError"
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Output files empty or missing
- Check `outputs/` folder
- Verify API key is correct
- Run validation: `python scripts\cli.py validate`

---

## 📚 Documentation Guide

| Document | When to Read |
|----------|--------------|
| `docs/PLAN.md` | Always first - phase status & overview |
| `docs/QUICKSTART.md` | Quick 3-minute setup |
| `docs/PHASE_1_README.md` | Technical deep-dive on Phase 1 |
| `docs/IMPLEMENTATION_SUMMARY.md` | Architecture decisions |
| `docs/VISUAL_STUDIO_SETUP.md` | VS Code/Visual Studio setup |
| `PROJECT_STRUCTURE.md` | Folder organization |

---

## 🔄 Workflow for Each Session

### Beginning of Session
1. Read `docs/PLAN.md` → Check phase status
2. Read this file (`CLAUDE.md`) → Remember guidelines
3. Activate venv: `.\venv\Scripts\Activate.ps1`
4. Set API key: `$env:ANTHROPIC_API_KEY="..."`

### During Session
1. Work only on current phase
2. Follow phase-specific guidelines
3. Update plan status when done
4. Test thoroughly before approval

### End of Session
1. Document what was done
2. Update `docs/PLAN.md` status if changed
3. Leave notes for next session

---

## 🚫 Rules to Follow

### DO:
- ✅ **Always check `docs/PLAN.md` first** - It's your source of truth
- ✅ **Update `docs/PLAN.md` after EVERY session** - Keep status current
- ✅ **Update implementation status as phases progress** - Record what was done
- ✅ Only work on the current phase
- ✅ Test Phase 1 thoroughly before approval
- ✅ Keep prompts in `references/prompts/`
- ✅ Generate outputs to `outputs/`

### DON'T:
- ❌ Start Phase 2+ before Phase 1 is approved
- ❌ Modify prompts without user approval
- ❌ Delete or rename outputs folder
- ❌ Commit venv/ to git
- ❌ Skip tests before approval
- ❌ Assume the plan is outdated
- ❌ **Leave the plan file unchanged** - Always update it at session end

### 🔴 CRITICAL RULE: Keep docs/PLAN.md in Sync

**The plan file must ALWAYS reflect the current project state.**

Every coding session MUST end with:
1. Updated phase status in `PHASE STATUS TRACKER`
2. Detailed implementation progress logged
3. Current blockers noted
4. Next steps documented
5. Timestamp added to show when last updated

**Failure to update the plan makes it useless for future sessions.**

---

## 📝 How to Update the Plan

### CRITICAL: Keep docs/PLAN.md Updated at All Times

**This is a mandatory step in every session.** The plan file is the source of truth for project status.

### When to Update Plan Status

Update `docs/PLAN.md` whenever:
- ✅ A phase implementation is completed
- ✅ A phase is approved/blocked
- ✅ Implementation status changes
- ✅ New blockers are discovered
- ✅ Testing is in progress
- ✅ A phase is ready for the next step

### How to Update the Plan

**Step 1: Open the plan file**
```
File: docs/PLAN.md (or C:\Users\ijajb\.claude\plans\i-want-you-to-lively-gadget.md)
```

**Step 2: Find the PHASE STATUS TRACKER**
```
Look for: ## 📊 PHASE STATUS TRACKER
```

**Step 3: Update the phase status**

Example changes:
```markdown
BEFORE:
Phase 1: Core Script Generation Agent
  Status: ✅ READY_FOR_TESTING
  Approval: Not yet approved (awaiting testing)

AFTER (Testing in progress):
Phase 1: Core Script Generation Agent
  Status: ✅ TESTING_IN_PROGRESS
  Approval: Awaiting user testing & approval
  Last Update: Generated 5 test scripts, all pass validation

AFTER (Approved):
Phase 1: Core Script Generation Agent
  Status: ✅ APPROVED
  Approval: User approved - ready to start Phase 2
  
Phase 2: SEO Metadata + Multi-Agent Coordination
  Status: 🚀 READY_TO_START
  Approval: APPROVED to proceed (Phase 1 complete)
```

**Step 4: Add detailed notes**

Under each phase, include:
- What was implemented
- What was tested
- Any issues found
- Next steps

Example:
```markdown
### ✅ Implementation Status: IN_PROGRESS (Updated: 2024-01-15)

**Completed:**
- Script generation agent working
- Generated 5 test scripts successfully
- All scripts pass quality validation
- Output structure verified

**In Progress:**
- Testing with different topics
- Verifying SEO quality criteria

**Blockers:**
- None currently

**Next Steps:**
1. Generate 5 more test scripts
2. Get user approval
3. Start Phase 2 implementation
```

### Status Emoji Guide

Use these consistent status indicators:

| Status | Emoji | Meaning |
|--------|-------|---------|
| Not started | ⏳ | Phase planned but not begun |
| In progress | 🚀 | Active development/testing |
| Ready to test | 🧪 | Implementation complete, awaiting testing |
| Testing | 🔍 | Currently being tested |
| Testing complete | ✅ | Tests pass, awaiting approval |
| Approved | ✅ | User approved, proceed to next phase |
| Blocked | 🚫 | Waiting for something (blocked reason) |
| Ready to start | 🚀 | Previous phase approved, can start now |

### Commit History in Plan

Keep a running log of updates. Example:

```markdown
## Implementation Progress Log

### 2024-01-15 - Phase 1 Testing Started
- Generated test scripts for 5 topics
- All scripts pass validation
- Ready for user review

### 2024-01-16 - Phase 1 Approved
- User approved Phase 1 implementation
- Starting Phase 2 planning

### 2024-01-17 - Phase 2 Implementation Started
- Created SEO metadata agent skeleton
- Integrated with script generation
```

### Every Session Must Include

At the end of every coding session, update:

1. **Phase Status Tracker** - Current status of all phases
2. **Implementation Status** - What was done in this session
3. **Blockers** - Any issues preventing progress
4. **Next Steps** - What comes next
5. **Last Updated** - Date and time

Example session update:

```markdown
### ✅ Implementation Status: TESTING_IN_PROGRESS

**This Session (2024-01-15):**
- Generated 3 test scripts successfully
- All pass quality validation
- Verified output file structure
- Tested error handling for invalid topics

**Cumulative Progress:**
- Phase 1 implementation: 100% complete
- Phase 1 testing: 60% complete (3 of 5 test scripts done)
- Quality validation: Passing

**Blockers:**
- None

**Next Session:**
1. Generate remaining 2 test scripts
2. Request user approval
3. Plan Phase 2 implementation

**Last Updated:** 2024-01-15 14:30 UTC
```

---

## 🤝 Working with User

### Report These to User
- Phase 1 testing complete → Ready for approval
- Phase 1 approved → Ready to start Phase 2
- Any blockers or issues found
- Quality concerns with output

### Ask User Before
- Starting a new phase
- Changing reference prompts
- Modifying architecture
- Skipping tests

### Never Do Without Approval
- Modify Phase 2+ implementation
- Change prompt templates
- Delete or reorganize folders
- Force-commit changes

---

## 🔗 Cross-Session Memory

If you need to remember things across sessions:
- Save to `docs/PLAN.md` (phase status)
- Leave notes in `docs/SESSION_NOTES.md` (if created)
- Update this file if guidelines change

The plan file (`docs/PLAN.md`) is your persistent memory.

---

## 📞 Getting Help

If stuck:
1. **Read the docs:** Start with the guide for your phase
2. **Check the plan:** What phase are you on? What's next?
3. **Run tests:** `python tests/test_phase_1.py`
4. **Check setup:** Is venv activated? Is API key set?
5. **Ask user:** When in doubt, ask before proceeding

---

## ✨ Key Principles

1. **Phase-based:** Work incrementally, one phase at a time
2. **Approval-gated:** Can't proceed without user approval
3. **Plan-driven:** Always check the plan first
4. **Test-first:** Verify before declaring success
5. **Documentation:** Keep docs updated for future sessions
6. **Reversible:** Can always roll back to plan if needed

---

## 🎓 Learning Progression

Each phase teaches specific AI patterns:

- **Phase 1:** Claude API tool use & agent loops
- **Phase 2:** Multi-agent coordination & data flow
- **Phase 3:** Advanced orchestration & MCP
- **Phase 4+:** Production patterns & scaling

---

## 📅 Version History

**Last Updated:** 2024
**Status:** Active - Phase 1 ready for testing
**Next Review:** After Phase 1 approval

---

## Start of Session Checklist

- [ ] Read `docs/PLAN.md` first
- [ ] Checked phase status
- [ ] Activated virtual environment
- [ ] Set API key
- [ ] Understand what phase I'm working on
- [ ] Know what's approved vs. blocked
- [ ] Reviewed relevant documentation

## End of Session Checklist (MANDATORY)

**Before ending the session, ALWAYS do this:**

- [ ] Implementation work is complete or logged
- [ ] Tests run and results documented
- [ ] `docs/PLAN.md` opened and ready to update
- [ ] Phase status updated in PHASE STATUS TRACKER
- [ ] Implementation status details added (what was done)
- [ ] Blockers noted (if any)
- [ ] Next steps documented
- [ ] Timestamp added to show when updated
- [ ] Plan file saved

**Example status update (copy & customize):**

```markdown
### ✅ Implementation Status: [STATUS]

**This Session:**
- [What was accomplished]
- [Tests results]
- [What's ready]

**Total Progress:**
- Phase 1: [X]% complete
- Phase 2: [X]% complete

**Blockers:**
- [Any blockers or None]

**Next Steps:**
1. [First thing]
2. [Second thing]
3. [Third thing]

**Last Updated:** [DATE TIME]
```

---

## The Plan File is Your Legacy

Think of it this way:
- **You're leaving notes for future Claude sessions**
- **Future you needs to know what past you did**
- **The user needs visibility into progress**
- **The plan is the contract between sessions**

**Keep it updated. Keep it detailed. Keep it current.**

---

**You're ready to work on this project!** 🚀

Always start with the plan, follow the phase guidelines, keep the plan updated, and keep communication with the user clear.
