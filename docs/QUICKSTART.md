# Phase 1 Quick Start Guide

## 🚀 Get Started in 5 Steps

### Step 1: Navigate to Project Directory

**Command:**
```powershell
cd C:\Ijaj\Claude\claude-video-generation
```

### Step 2: Create Virtual Environment & Install Dependencies

**Command:**
```powershell
.\scripts\setup_venv.ps1
```

**What this does:**
- ✅ Creates `venv/` folder in your project
- ✅ Activates the virtual environment
- ✅ Installs all dependencies from `requirements.txt`
- ✅ Verifies installation automatically
- ✅ Runs setup test to confirm everything works

**Time:** ~2-3 minutes (first time only)

---

### Step 3: Activate Virtual Environment (For Future Sessions)

Once setup is complete, for any **new PowerShell session**, activate the venv:

**Command:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Verify activation:**
- You should see `(venv)` at the start of your PowerShell prompt
- Example: `(venv) C:\Ijaj\Claude\claude-video-generation>`

**Note:** You only need to do this once per PowerShell session. The setup script (Step 2) already activates it for the first time.

---

### Step 4: Set API Key (Required Each Session)

**Command:**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**To get your API key:**
1. Go to https://console.anthropic.com
2. Copy your API key from the dashboard
3. Replace `sk-ant-your-key-here` with your actual key
4. Run the command above

**Example:**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-z7x9w2k5q8m3n1p4r6t9v2y5"
```

---

### Step 5: Generate Your First Script

**Interactive Mode (Recommended):**
```powershell
python scripts/cli.py generate
```

When prompted, enter:
```
Topic: How to greet someone politely
Additional context (optional): (press Enter to skip)
```

**Direct Command Line Mode:**
```powershell
python scripts/cli.py generate --topic "How to greet someone politely"
```

---

### ✅ Verify It Worked

After running the generate command, check the output folder:
```
outputs/
└── how_to_greet_someone_politely/
    ├── script.txt
    └── script_metadata.json
```

**Success indicators:**
- ✅ Files created in `outputs/` folder
- ✅ `script.txt` contains dialogue between Sarah and Alex
- ✅ Word count between 1500-2000 words
- ✅ `script_metadata.json` has statistics

---

## 🎓 Try These Topics

**Easy (Evergreen):**
```powershell
python scripts/cli.py generate --topic "How to say hello politely"
```

**Medium (Teaching):**
```powershell
python scripts/cli.py generate --topic "Common mistakes English learners make"
```

**Hard (Specific):**
```powershell
python scripts/cli.py generate --topic "Interview tips for non-native speakers" --context "Focus on body language"
```

---

## 🔧 Additional Commands

**Validate an existing script:**
```powershell
python scripts/cli.py validate --script-path outputs/how_to_greet_someone_politely/script.txt
```

**Show help and options:**
```powershell
python scripts/cli.py generate --help
```

**Re-run the setup test:**
```powershell
python tests/test_phase_1.py
```

---

## 📁 Understanding Output Files

After generating a script, you'll find:

**script.txt** — Full dialogue script
```
Sarah : Imagine you meet someone new. How do you greet them politely?
Alex : I sometimes feel nervous when meeting new people.
Sarah : Today we learn how to greet someone in English.
...
[continues for 1500-2000 words]
```

**script_metadata.json** — Statistics
```json
{
  "topic": "How to greet someone politely",
  "word_count": 1750,
  "estimated_duration_minutes": 13.5,
  "line_count": 145,
  "generated_at": "2024-01-15T10:30:00.123456"
}
```

---

## 🐛 Troubleshooting

| Problem | Solution | Command |
|---------|----------|---------|
| `$env:ANTHROPIC_API_KEY` not found | Set your API key | `$env:ANTHROPIC_API_KEY="sk-ant-..."` |
| `(venv)` not showing in prompt | Activate virtual environment | `.\venv\Scripts\Activate.ps1` |
| "Module not found" error | Install dependencies | `pip install -r requirements.txt` |
| "Script file not created" | Check API key is valid | Verify at console.anthropic.com |
| "Word count too low" | Try adding context | `--context "Focus on this aspect"` |
| Permission denied on setup script | Allow script execution | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |

---

## 📚 Learn More

| Document | Purpose |
|----------|---------|
| `docs/PHASE_1_README.md` | Complete technical guide |
| `docs/IMPLEMENTATION_SUMMARY.md` | Architecture and design decisions |
| `docs/PLAN.md` | Full project plan and phases |
| `docs/VISUAL_STUDIO_SETUP.md` | IDE setup guide |

---

## 🎯 What's Next?

Once Phase 1 is working:
1. Generate scripts for 3-5 different topics
2. Review output quality
3. Share feedback with the team
4. Get approval to proceed to Phase 2

Phase 2 will add:
- SEO metadata generation (titles, tags, hashtags)
- Multi-agent coordination
- Parallel execution

---

**Tip:** Start with simple, evergreen topics like "How to greet someone" to see how the agent works, then try more complex scenarios.
