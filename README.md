# SPEAK ENGLISH SMARTER - This is Video Generation Pipeline

An intelligent, incremental video generation pipeline for creating English learning content. Built with Claude AI and designed to teach agentic AI patterns.

## 🎯 Project Overview
Automated end-to-end pipeline that transforms topics into complete YouTube videos:

```
Topic Input → Script Generation → SEO Metadata → TTS → Images → Video Assembly → MP4
```

### Current Status (2026-09-27) - 🎉 ALL PHASES COMPLETE!
- ✅ **Phase 1:** Script Generation Agent (COMPLETE)
- ✅ **Phase 2:** SEO Metadata + Multi-Agent Coordination (COMPLETE)
- ✅ **Phase 3:** Text-to-Speech with Google Studio API (COMPLETE)
- ✅ **Phase 4:** Image Generation - Thumbnails & Video Scenes (COMPLETE)
  - Separate agents for thumbnails and video scenes
  - Flat vector illustration style matching canonical references
  - Dynamic character positioning with text space creation
- ✅ **Phase 5:** Thumbnail Text Overlay with AI-Determined Positioning (COMPLETE)
  - OpenAI Image Edit API with flexible text placement
  - Eye-catching styling for YouTube feed
  - Mobile-optimized readability
- ✅ **Phase 6:** Video Assembly with MoviePy (COMPLETE)
  - MoviePy video composition (video + audio)
  - Auto-generated SRT captions with TTS-aligned timing
  - Spectrum visualization at top-center (podcast aesthetic)
  - Interactive prompts with smart defaults

---

## 📁 Project Structure

```
claude-video-generation/
│
├── src/                           # Source code (Python package)
│   ├── __init__.py
│   ├── config.py                  # Configuration & environment
│   ├── models.py                  # Data validation (Pydantic)
│   └── agents/                    # Agent implementations
│       ├── __init__.py
│       ├── script_generation_agent.py    # Phase 1: Script generation
│       ├── seo_metadata_agent.py         # Phase 2: SEO metadata
│       ├── tts_agent.py                  # Phase 3: Text-to-speech
│       ├── thumbnail_image_agent.py      # Phase 4A: Thumbnail generation
│       ├── video_image_agent.py          # Phase 4B: Video scene generation
│       ├── edit_thumbnail_image.py       # Phase 5: Text overlay
│       └── video_assembly_agent.py       # Phase 6: Video assembly
│
├── scripts/                       # CLI and setup scripts
│   ├── cli.py                     # Main CLI interface
│   ├── setup_venv.ps1             # Virtual environment setup (PowerShell)
│   └── setup_venv.bat             # Virtual environment setup (Batch)
│
├── docs/                          # Documentation
│   ├── QUICKSTART.md              # 3-minute quick start
│   ├── PHASE_1_README.md          # Phase 1 detailed guide
│   ├── IMPLEMENTATION_SUMMARY.md  # Architecture & design
│   └── VISUAL_STUDIO_SETUP.md     # Visual Studio integration
│
├── tests/                         # Test suite
│   └── test_phase_1.py            # Setup verification
│
├── config/                        # Configuration files
│   └── .env.example               # Environment template
│
├── references/                    # Reference materials
│   ├── prompts/                   # Prompt templates
│   │   ├── Script Writer-prompt.txt
│   │   ├── Title and SEO- prompt.txt
│   │   ├── Thumbnail Image- Prompt.txt
│   │   └── Video Image- Prompt.txt
│   ├── examples/                  # Example outputs
│   │   └── Script- Say No Politely.txt
│   └── images/                    # Reference images
│       └── [4 PNG character references]
│
├── outputs/                       # Generated videos (created at runtime)
│   └── {topic_slug}/
│       ├── script.txt             # Generated script
│       ├── script_metadata.json   # Statistics
│       └── (phase 2+) seo_metadata.json
│
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

---

## 🚀 Quick Start

### 1. Setup Virtual Environment

**PowerShell (Recommended):**
```powershell
cd C:\Ijaj\Claude\claude-video-generation
.\scripts\setup_venv.ps1
```

**Or Command Prompt:**
```cmd
cd C:\Ijaj\Claude\claude-video-generation
scripts\setup_venv.bat
```

### 2. Set API Key

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

### 3. Generate First Script

```powershell
python scripts\cli.py generate
```

Enter your topic when prompted. Output saves to `outputs/{topic}/script.txt`

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `docs/QUICKSTART.md` | Get started in 3 minutes |
| `docs/PHASE_1_README.md` | Complete Phase 1 guide |
| `docs/IMPLEMENTATION_SUMMARY.md` | Architecture & decisions |
| `docs/VISUAL_STUDIO_SETUP.md` | Visual Studio integration |
| `.claude/plans/i-want-you-to-lively-gadget.md` | Project plan & requirements |

---

## 🛠️ Development

### Install Dependencies (if not using setup script)
```powershell
pip install -r requirements.txt
```

### Run CLI
```powershell
# Interactive mode
python scripts\cli.py generate

# With parameters
python scripts\cli.py generate --topic "How to greet someone"

# Validate script
python scripts\cli.py validate --script-path outputs\topic_name\script.txt
```

### Run Tests
```powershell
python tests\test_phase_1.py
```

### Python Package Structure
```python
# Import from src package
from src.config import ANTHROPIC_API_KEY
from src.models import TopicInput, Script
from src.agents import generate_script
```

---

## 🎓 Learning Focus

This project teaches **Agentic AI patterns** incrementally:

### Phase 1: Tool Use
- Claude API integration
- Prompt engineering
- Structured output parsing
- Input validation

### Phase 2: Multi-Agent Coordination
- Agent composition
- File-based handoffs
- Parallel execution
- Data flow between agents

### Phase 3: Advanced Orchestration
- MCP (Model Context Protocol)
- Tool extensibility
- Agent specialization

### Phase 4-5: Production Patterns
- Configuration management
- Error handling & retries
- Logging & monitoring
- Batch processing

---

## 📋 Content Specifications

### Script Requirements
- **Length:** 1500-2000 words
- **Duration:** 10-15 minutes
- **Format:** Sarah (teacher) & Alex (learner) dialogue
- **Language:** Beginner-friendly English
- **Structure:** Hook → Intro → Teaching → Practice → CTA

### Quality Criteria
Scripts must meet 11 YouTube success criteria:
- High search demand
- Evergreen potential
- Beginner-friendly
- Strong CTR potential
- Practical & relatable
- And 6 more...

### Output Files (per video)
```
outputs/topic_name/
├── script.txt              # Full dialogue
├── script_metadata.json    # Statistics
└── (Phase 2+) seo_metadata.json
```

---

## 🔧 Configuration

### Environment Variables
Create `config/.env` from `config/.env.example`:
```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=...
LOG_LEVEL=INFO
```

### Settings in `src/config.py`
- Model: Claude Sonnet 3.5
- Temperature: 0.7
- Word range: 1500-2000
- Speech rate: 130 words/minute

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "venv not found" | Run `.\scripts\setup_venv.ps1` |
| "API key not set" | Run `$env:ANTHROPIC_API_KEY="..."` |
| "ModuleNotFoundError" | Activate venv: `.\venv\Scripts\Activate.ps1` |
| "Word count too low" | Add more context or rerun generation |

---

## 📊 Project Statistics

- **Source Code:** ~690 lines (Phase 1)
- **Documentation:** ~2000 lines
- **Test Coverage:** Automated verification
- **API Calls:** Claude Sonnet 3.5
- **Frameworks:** Pydantic, Click, python-dotenv

---

## 🗺️ Project Phases

### Phase 1 ✅ (COMPLETE)
- ✅ Script generation with Claude API
- ✅ Quality validation with dynamic tolerance
- ✅ CLI interface with customizable video length
- ✅ Topic-based output organization

### Phase 2 ✅ (COMPLETE)
- ✅ SEO metadata agent (title, description, hashtags, tags)
- ✅ Thumbnail text generation
- ✅ Multi-agent coordination
- ✅ Sequential execution with data handoffs

### Phase 3 ✅ (COMPLETE)
- ✅ Text-to-Speech with Google Studio API
- ✅ Multi-speaker support (Sarah & Alex)
- ✅ Parallel voice synthesis with 2 threads
- ✅ Script segmentation with line tracking

### Phase 4 ✅ (COMPLETE)
- ✅ Thumbnail Image Generation (1280×720px)
  - Scenario-aware character positioning for text space
  - Soft colors with radiant lighting
  - Ready for Phase 5 text overlay
- ✅ Video Scene Generation (1920×1088px)
  - Flat vector illustration style (matches canonical reference)
  - Professional podcast setup
  - Scenario-adaptive environments

### Phase 5 🔜 (PLANNED)
- Thumbnail text overlay using SEO metadata
- FFmpeg video assembly
- Audio + images combination
- MP4 output (1920×1080, 10-15 min)

---

## 🤝 Contributing

This is a learning project. To extend it:

1. Follow the phase-based structure
2. Add agents to `src/agents/`
3. Update models in `src/models.py`
4. Add documentation in `docs/`
5. Update tests in `tests/`

---

## 📄 License

Educational project - free to learn and modify.

---

## 🎬 Example Usage

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Set API key
$env:ANTHROPIC_API_KEY="sk-ant-..."

# Generate a script
python scripts\cli.py generate

# When prompted:
# Topic: "How to introduce yourself politely"
# Context: "Focus on professional settings"

# Output appears in: outputs\how_to_introduce_yourself_politely\script.txt
```

---

## 📞 Support

- **Setup Issues:** See `docs/VISUAL_STUDIO_SETUP.md`
- **Quick Start:** See `docs/QUICKSTART.md`
- **Full Guide:** See `docs/PHASE_1_README.md`
- **Architecture:** See `docs/IMPLEMENTATION_SUMMARY.md`

---

**Status:** Phases 1-4 Complete ✅ | Phase 5 Planned  
**Last Updated:** 2026-09-27  
**Language:** Python 3.8+  
**Platform:** Windows/Mac/Linux
