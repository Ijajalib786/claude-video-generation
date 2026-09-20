# Project Structure Guide

## 📁 Complete Folder Organization

```
claude-video-generation/                    # Project root
│
├── 🐍 src/                                 # Python source package
│   ├── __init__.py                         # Package initialization
│   ├── config.py                           # Configuration & environment setup
│   │   └── Paths, API keys, model settings
│   │
│   ├── models.py                           # Data validation (Pydantic)
│   │   └── Script, ScriptLine, TopicInput, SEOMetadata, VideoOutput
│   │
│   └── agents/                             # Agent implementations
│       ├── __init__.py
│       ├── script_generation_agent.py      # Phase 1: Generate scripts from topics
│       │   └── generate_script(), _parse_script(), _validate_script_quality()
│       │
│       └── (Future agents)
│           ├── seo_metadata_agent.py       # Phase 2: Generate SEO metadata
│           ├── tts_agent.py                # Phase 3: Text-to-Speech
│           ├── image_generation_agent.py   # Phase 3: Image generation
│           └── video_assembly_agent.py     # Phase 4: FFmpeg assembly
│
├── 📜 scripts/                             # CLI and utility scripts
│   ├── cli.py                              # Main entry point (formerly main.py)
│   │   └── Commands: generate, validate
│   │
│   ├── setup_venv.ps1                      # PowerShell virtual env setup
│   └── setup_venv.bat                      # Batch virtual env setup
│
├── 📚 docs/                                # Documentation
│   ├── QUICKSTART.md                       # 3-minute quick start guide
│   ├── PHASE_1_README.md                   # Phase 1 comprehensive guide
│   ├── IMPLEMENTATION_SUMMARY.md           # Architecture & design decisions
│   └── VISUAL_STUDIO_SETUP.md              # Visual Studio integration guide
│
├── 🧪 tests/                               # Test suite
│   └── test_phase_1.py                     # Environment verification script
│
├── ⚙️ config/                              # Configuration files
│   └── .env.example                        # Environment template
│       └── Copy to .env and fill in API keys
│
├── 📖 references/                          # Reference materials
│   ├── prompts/                            # Prompt templates
│   │   ├── Script Writer-prompt.txt        # Template for script generation
│   │   ├── Title and SEO- prompt.txt       # Template for SEO metadata
│   │   ├── Thumbnail Image- Prompt.txt     # Design spec for thumbnails
│   │   └── Video Image- Prompt.txt         # Design spec for video scenes
│   │
│   ├── examples/                           # Example outputs
│   │   └── Script- Say No Politely.txt     # Example: 338-line complete script
│   │
│   └── images/                             # Reference character images
│       ├── Thumbnail_character__style_canonical_ref-1.png
│       ├── Thumbnail_character_style_canonical_ref-2.png
│       ├── Video_character_style_canonical_ref_1.png
│       └── Video_character_style_canonical_ref_2.png
│
├── 📁 outputs/                             # Generated video outputs (created at runtime)
│   └── {topic_slug}/                       # One folder per video
│       ├── script.txt                      # Generated script (Sarah & Alex dialogue)
│       ├── script_metadata.json            # Script statistics
│       │
│       └── (Phase 2+)
│           ├── seo_metadata.json           # Title, description, hashtags, tags
│           ├── thumbnail.png               # Generated thumbnail image
│           ├── video_scene.png             # Generated video scene
│           └── output_video.mp4            # Final video file
│
├── 🔒 .gitignore                           # Git ignore rules
│   └── Ignores: venv, __pycache__, outputs, .env, .idea, etc.
│
├── 📋 requirements.txt                     # Python dependencies
│   └── anthropic, openai, pydantic, click, python-dotenv
│
├── 📄 README.md                            # Main project documentation
├── 📄 PROJECT_STRUCTURE.md                 # This file
├── 📄 IMPLEMENTATION_SUMMARY.md            # (Moved to docs/)
│
└── 🧠 .claude/                             # Claude-specific files
    ├── plans/
    │   └── i-want-you-to-lively-gadget.md # Approved project plan
    │
    └── (Other Claude configuration)
```

---

## 🔄 How Pieces Connect

### Entry Point
```
User runs: python scripts\cli.py generate
    ↓
Imports from src package:
    - src.config (paths, API keys)
    - src.models (validation)
    - src.agents (agents)
    ↓
Creates TopicInput (validated)
    ↓
Calls generate_script() from agents
    ↓
Claude API creates script
    ↓
Results saved to outputs/{topic}/
```

### Import Hierarchy
```
scripts/cli.py
    ↓ imports from
src/
    ├── config.py (paths, settings)
    ├── models.py (TopicInput, Script, etc.)
    └── agents/
        └── script_generation_agent.py (generate_script)
```

### Data Flow
```
Topic (string)
    ↓
TopicInput (validated by Pydantic)
    ↓
Claude API call (with system prompt from references/)
    ↓
Raw script text
    ↓
_parse_script() → Script object
    ↓
_validate_script_quality() → quality checks
    ↓
save_script_to_file() → outputs/topic/
```

---

## 📂 Directory Purposes

### `src/` — Source Code
- **Purpose:** Core Python package for the pipeline
- **Structure:** Python package with agents as submodule
- **Usage:** `from src.models import TopicInput`
- **Growth:** Add new agents to `src/agents/` for each phase

### `scripts/` — Executables
- **Purpose:** CLI and setup utilities
- **Files:** 
  - `cli.py` - Main entry point
  - `setup_venv.*` - Environment setup
- **Usage:** `python scripts\cli.py generate`

### `docs/` — Documentation
- **Purpose:** Learning guides and setup instructions
- **Files:**
  - QUICKSTART.md - 3-minute guide
  - PHASE_1_README.md - Technical deep-dive
  - VISUAL_STUDIO_SETUP.md - IDE integration
  - IMPLEMENTATION_SUMMARY.md - Architecture
- **Audience:** Developers using the pipeline

### `tests/` — Verification
- **Purpose:** Test and verify setup
- **Files:** `test_phase_1.py` - Checks environment
- **Usage:** `python tests\test_phase_1.py`

### `config/` — Configuration
- **Purpose:** Environment and settings
- **Files:** `.env.example` - Template
- **Usage:** Copy to `.env`, fill in your API keys

### `references/` — Reference Materials
- **Subdirectories:**
  - `prompts/` - Prompt templates for Claude API
  - `examples/` - Example outputs (full script)
  - `images/` - Character reference images
- **Usage:** Loaded by config.py when generating

### `outputs/` — Results
- **Purpose:** Storage for generated videos
- **Structure:** One folder per topic
- **Contents:** Scripts, metadata, images, videos
- **Ignored by:** `.gitignore` (don't commit generated files)

---

## 🔍 File Purposes Quick Reference

| File | Purpose | Edited By |
|------|---------|-----------|
| `src/config.py` | Paths, API keys, settings | Developer |
| `src/models.py` | Data validation schemas | Developer |
| `src/agents/script_generation_agent.py` | Script generation logic | Developer |
| `scripts/cli.py` | User-facing commands | Developer |
| `config/.env` | Your API keys | You (from .env.example) |
| `references/prompts/*.txt` | Prompt templates | Project owner (me) |
| `requirements.txt` | Python dependencies | Developer |
| `.gitignore` | Git ignore rules | Developer |
| `README.md` | Project overview | Developer |
| `docs/*.md` | Setup & learning guides | Developer |
| `outputs/*/` | Generated videos | Automated |

---

## 📦 Package Import Patterns

### From CLI (scripts/cli.py)
```python
# Path: C:\Ijaj\Claude\claude-video-generation\scripts\cli.py
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import config
from src.models import TopicInput
from src.agents import generate_script
```

### From Tests (tests/test_phase_1.py)
```python
# Path: C:\Ijaj\Claude\claude-video-generation\tests\test_phase_1.py
from src.config import ANTHROPIC_API_KEY
from src.models import Script
```

### From Agents (src/agents/script_generation_agent.py)
```python
# Same directory, can import siblings
from .. import config  # Go up to src/, then import
from ..models import Script, ScriptLine
```

---

## 🚀 How to Add New Phases

### Phase 2: SEO Metadata Agent

```
1. Create src/agents/seo_metadata_agent.py
   - Function: generate_seo_metadata(script) → SEOMetadata
   - Uses: Claude API + references/prompts/Title and SEO- prompt.txt
   
2. Update src/agents/__init__.py
   - Add: from .seo_metadata_agent import generate_seo_metadata
   
3. Update scripts/cli.py
   - Add: Call seo_metadata_agent after script_generation_agent
   
4. Update docs/PHASE_2_README.md
   - Document new agent
```

### Phase 3: TTS Agent

```
1. Create src/agents/tts_agent.py
   - Function: generate_tts(script) → AudioFile
   - Uses: Google Studio API + separate voices for Sarah/Alex
   
2. Create src/agents/image_generation_agent.py
   - Function: generate_images(script) → (thumbnail.png, video_scene.png)
   - Uses: Claude/ChatGPT API + references/images/
```

### Phase 4: Video Assembly

```
1. Create src/agents/video_assembly_agent.py
   - Function: assemble_video(audio, images) → mp4
   - Uses: FFmpeg (add to requirements.txt)
```

---

## 🗂️ File Naming Conventions

- **Python files:** `snake_case.py` (script_generation_agent.py)
- **Folders:** `lowercase` (agents, scripts, docs, tests)
- **Documentation:** `SCREAMING_SNAKE_CASE.md` (QUICKSTART.md)
- **Output folders:** `snake_case` from topic (how_to_greet_someone)
- **Config files:** `.env`, `requirements.txt`

---

## 📊 Statistics

- **Total files:** ~20
- **Python modules:** 5 (config, models, 3 agents)
- **Documentation:** 4 guides
- **Tests:** 1 verification script
- **Lines of code:** ~690 (Phase 1)
- **Storage:** ~100KB (code only, excluding venv)

---

## 🔐 What Gets Ignored

Files NOT tracked in git (see `.gitignore`):
- `venv/` — Virtual environment (created locally)
- `.env` — API keys (created locally from template)
- `outputs/` — Generated videos (created at runtime)
- `__pycache__/` — Python cache (created automatically)
- `.idea/`, `.vscode/` — IDE settings (personal preferences)

---

## 🔄 Typical Workflow

```
1. Clone/download project
2. Run: scripts\setup_venv.ps1
   - Creates venv/
   - Installs dependencies
3. Copy: config/.env.example → .env
   - Add your API key
4. Run: python scripts\cli.py generate
   - Creates outputs/{topic}/
5. Check: outputs/{topic}/script.txt
6. Ready for Phase 2!
```

---

## 💡 Best Practices

1. **Don't modify references/** — These are templates for agents
2. **Add to docs/** when documenting new phases
3. **Keep src/ clean** — One agent = one file
4. **Test locally** before committing
5. **Update .gitignore** if adding new directories
6. **Keep README.md current** with project status

---

## 🎓 Learning the Structure

- **Quick overview:** Start with README.md
- **For setup:** See docs/QUICKSTART.md
- **For architecture:** See docs/IMPLEMENTATION_SUMMARY.md
- **For deep dive:** See docs/PHASE_1_README.md
- **For Visual Studio:** See docs/VISUAL_STUDIO_SETUP.md

---

**This organization enables:**
✅ Clean separation of concerns  
✅ Easy to extend for new phases  
✅ Professional Python package structure  
✅ Simple to navigate and understand  
✅ Ready for collaboration  
✅ Test and verify easily  

---

Created: 2024 | Language: Python 3.8+ | Framework: Pydantic, Click
