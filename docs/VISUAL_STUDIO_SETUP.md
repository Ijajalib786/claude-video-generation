# Visual Studio Setup Guide - Virtual Environment & Phase 1

This guide walks you through setting up the Python virtual environment in Visual Studio and running Phase 1.

## Option 1: Automated Setup (Recommended) ⚡

### Step 1: Run Setup Script

**PowerShell (Recommended):**
```powershell
cd C:\Ijaj\Claude\claude-video-generation
.\setup_venv.ps1
```

**Command Prompt (Alternative):**
```cmd
cd C:\Ijaj\Claude\claude-video-generation
setup_venv.bat
```

The script will:
- ✅ Create virtual environment (`venv` folder)
- ✅ Activate it automatically
- ✅ Install all dependencies
- ✅ Verify installation
- ✅ Run setup tests

**That's it!** Skip to "Configure Visual Studio" below.

---

## Option 2: Manual Setup

### Step 1: Open Project in Visual Studio

1. File → Open → Folder
2. Navigate to: `C:\Ijaj\Claude\claude-video-generation`
3. Click "Select Folder"

### Step 2: Create Virtual Environment

1. Open **Terminal** in Visual Studio (View → Terminal or Ctrl + `)
2. Run:
```powershell
python -m venv venv
```

### Step 3: Activate Virtual Environment

In the same terminal:
```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Verify Setup

```powershell
python test_phase_1.py
```

Look for: ✅ Phase 1 Setup: ALL CHECKS PASSED

---

## Configure Visual Studio 🔧

### Step 1: Open Python Environments

1. **View** menu
2. → **Other Windows**
3. → **Python Environments**

A panel appears on the right showing available Python interpreters.

### Step 2: Select Virtual Environment

1. Look for `venv` in the list
2. You should see something like:
   ```
   venv (Local) C:\Ijaj\Claude\claude-video-generation\venv\Scripts\python.exe
   ```

### Step 3: Set as Default

1. **Right-click** on `venv`
2. Select **"Set as Default"**

Now your virtual environment is the default for this project.

### Step 4: Verify in Terminal

Close and reopen the terminal. It should show:
```
(venv) PS C:\Ijaj\Claude\claude-video-generation>
```

If not, manually activate:
```powershell
.\venv\Scripts\Activate.ps1
```

---

## Run Phase 1 in Visual Studio 🚀

### Option A: Run via Terminal (Recommended)

1. **View** → **Terminal** (or Ctrl + `)
2. Make sure `(venv)` is shown in prompt
3. Run:
```powershell
python main.py generate
```
4. Enter topic when prompted

### Option B: Run via Python Debug Console

1. **View** → **Python Debug Console**
2. Paste and run:
```python
from models import TopicInput
from script_generation_agent import generate_script, save_script_to_file
from pathlib import Path
import config

topic = TopicInput(topic="How to greet someone politely")
script = generate_script(topic)
save_script_to_file(script, config.OUTPUT_DIR / "test_topic")
```

### Option C: Debug with Breakpoints

1. Open `main.py`
2. Click line number to set breakpoint
3. **Debug** → **Start Debugging** (F5)
4. Terminal opens, enter your topic

---

## First Script Generation 📝

### Quick Test (2 minutes)

Terminal commands:
```powershell
# Make sure venv is active (should show (venv) in prompt)
python main.py generate

# When prompted:
# Topic: How to introduce yourself
# Context: (press Enter)
```

### Expected Output

```
🎬 Generating script for topic: How to introduce yourself
⏳ Calling Claude API with script generation prompt...
✅ Script passed quality validation

=== Script Generation Complete ===
📁 Output folder: outputs\how_to_introduce_yourself
📝 Script file: script.txt
📊 Statistics:
   - Lines: 145
   - Words: 1750
   - Duration: ~13.5 minutes
```

### Find Your Script

In Visual Studio **Solution Explorer**:
1. Navigate to: `outputs/how_to_introduce_yourself/`
2. Open `script.txt` to view the script

---

## Set API Key 🔑

Your script generation requires the Anthropic API key.

### Method 1: Environment Variable (Recommended)

**In PowerShell Terminal:**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"
```

**To persist for future sessions**, add to your PowerShell profile:
```powershell
# Open profile
notepad $PROFILE

# Add this line
$env:ANTHROPIC_API_KEY="sk-ant-your-key"

# Save and reload
. $PROFILE
```

### Method 2: .env File

1. Create `.env` in project root (copy from `.env.example`)
2. Edit `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```
3. Restart Visual Studio

### Method 3: Hardcode (Not Recommended)

Only for testing - edit `config.py`:
```python
ANTHROPIC_API_KEY = "sk-ant-your-key"  # Remove after testing!
```

---

## Troubleshooting 🐛

### "venv not found"
**Solution:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### "(venv) doesn't show in terminal"
**Solution:** Manually activate:
```powershell
.\venv\Scripts\Activate.ps1
```

### "ModuleNotFoundError: No module named 'anthropic'"
**Solution:** Make sure venv is activated (look for `(venv)` in prompt), then:
```powershell
pip install -r requirements.txt
```

### "ANTHROPIC_API_KEY not set"
**Solution:** Set your API key:
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

### "Connection error when generating script"
**Solution:** 
- Check internet connection
- Verify API key is valid at https://console.anthropic.com
- Wait a moment and retry

---

## Python Debugging Features in VS 🔍

### Set Breakpoints
1. Click on line number in code
2. A red dot appears
3. Run with F5
4. Execution pauses at breakpoint

### Step Through Code
- F10 = Step over (next line)
- F11 = Step into (enter function)
- Shift+F11 = Step out (exit function)
- Ctrl+F5 = Continue execution

### Watch Variables
1. Open Debug → Windows → Watch
2. Type variable name to watch

---

## Project Structure in VS

```
📁 claude-video-generation/
├── 📁 venv/                    ← Virtual environment (hidden by default)
├── 📁 references/              ← Reference prompts & images
├── 📁 outputs/                 ← Generated scripts go here
│   └── 📁 topic_name/
│       ├── script.txt          ← Your generated script
│       └── script_metadata.json ← Statistics
├── main.py                     ← CLI entry point
├── script_generation_agent.py  ← Core agent
├── models.py                   ← Data validation
├── config.py                   ← Configuration
├── setup_venv.ps1              ← Setup script
├── setup_venv.bat              ← Setup script (batch)
├── QUICKSTART.md               ← 3-minute guide
└── PHASE_1_README.md           ← Complete guide
```

---

## Next Steps 📋

1. ✅ Virtual environment set up
2. ✅ Dependencies installed
3. ✅ API key configured
4. ✅ Phase 1 working
5. 🔜 **Generate scripts!**
   ```powershell
   python main.py generate
   ```
6. 🔜 Try different topics
7. 🔜 Ready for Phase 2 (SEO agent)

---

## Keyboard Shortcuts (VS)

| Shortcut | Action |
|----------|--------|
| Ctrl + ` | Open/close terminal |
| F5 | Start debugging |
| F10 | Step over |
| F11 | Step into |
| Ctrl+F5 | Run without debugging |
| Ctrl+Shift+` | New terminal |

---

## Resources

- **Anthropic API Docs:** https://docs.anthropic.com
- **Python Virtual Envs:** https://docs.python.org/3/tutorial/venv.html
- **Visual Studio Python:** https://learn.microsoft.com/en-us/visualstudio/python/

---

**All set!** Your virtual environment is ready. Start generating scripts with:
```powershell
python main.py generate
```

Questions? Check `QUICKSTART.md` or `PHASE_1_README.md`.
