# Quick Start Guide: Video Generation Pipeline

## ⚡ Get Started in 5 Minutes

This guide covers the complete pipeline: **Script → SEO → TTS → Images → Text Overlay → MP4 Video**

---

## Step 1: Setup (One-Time)

### Navigate to Project
```powershell
cd C:\Ijaj\Claude\claude-video-generation
```

### Create Virtual Environment
```powershell
.\scripts\setup_venv.ps1
```

**This does:**
- ✅ Creates `venv/` folder
- ✅ Installs all dependencies
- ✅ Verifies everything works

**Time:** ~2-3 minutes (first time only)

---

## Step 2: Configure API Keys (Each Session)

### Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
# You should see (venv) in your prompt
```

### Set Required API Keys

**Anthropic (Script & SEO - Required):**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-your-key"
```

**OpenAI (Images - Required for Phase 4):**
```powershell
$env:OPENAI_API_KEY = "sk-your-key"
```

**Google (TTS - Optional for Phase 3):**
```powershell
$env:GOOGLE_GEMINI_API_KEY = "your-google-key"
```

**Get API Keys:**
- Anthropic: https://console.anthropic.com
- OpenAI: https://platform.openai.com
- Google: https://ai.google.dev

---

## Step 3: Generate Video Assets

### Quick Generate (All Phases)
```powershell
python scripts/cli.py generate
```

**Interactive prompts:**
1. **Topic:** "How to introduce yourself at a party"
2. **Context (optional):** Press Enter to skip
3. **Video Length (default 12 min):** Enter 8-20, or press Enter
4. **Generate TTS audio (Y/n)?** Enter Y or N
5. **Generate images (Y/n)?** Enter Y or N
6. **Assemble final MP4 video (y/N)?** Enter y for yes, or press Enter to skip

### Example Topics
```powershell
# Easy
python scripts/cli.py generate --topic "How to say hello politely"

# Medium
python scripts/cli.py generate --topic "Common English mistakes"

# Hard
python scripts/cli.py generate --topic "Job interview tips" --context "For non-native speakers"
```

---

## Step 4: Check Output

**Success! You'll see:**
```
outputs/{topic}/
├── script.txt                 # Phase 1: Dialogue script
├── script_metadata.json       # Phase 1: Statistics
├── seo_metadata.txt           # Phase 2: Title, description, tags
├── audio/
│   └── audio.mp3            # Phase 3: TTS audio (if enabled)
├── thumbnail.png            # Phase 4: YouTube thumbnail
├── thumbnail_with_text.png  # Phase 5: Thumbnail with text (if images enabled)
├── video_scene.png          # Phase 4: Video background
├── subtitle.srt             # Phase 6: Auto-generated captions (if video enabled)
└── output_video.mp4         # Phase 6: Final MP4 video (if video enabled)
```

---

## 🎯 Common Workflows

### Minimal (Script Only)
```powershell
python scripts/cli.py generate --topic "Your topic"
# When prompted: N (skip TTS), N (skip images)
# Output: script.txt + seo_metadata.txt
```

### With Audio (No Images)
```powershell
python scripts/cli.py generate --topic "Your topic"
# When prompted: Y (generate TTS), N (skip images)
# Output: script + audio
```

### Full Pipeline (Recommended)
```powershell
python scripts/cli.py generate --topic "Your topic"
# When prompted: Y (TTS), Y (images)
# Output: Complete set of assets
```

### Custom Video Length
```powershell
python scripts/cli.py generate --topic "Your topic"
# When prompted for length: Enter 10 (for 10-minute video)
# Auto-calculates: ~1300 words target
```

---

## 📊 What Each Phase Does

| Phase | Input | Output | Optional |
|-------|-------|--------|----------|
| **1: Script** | Topic | script.txt | ❌ Required |
| **2: SEO** | Script | seo_metadata.txt | ❌ Required |
| **3: TTS** | Script | audio/audio.mp3 | ✅ Optional |
| **4: Images** | Script+SEO | thumbnail.png, video_scene.png | ✅ Optional |
| **5: Text Overlay** | Thumbnail+SEO | thumbnail_with_text.png | ✅ Auto (if Phase 4) |
| **6: Video Assembly** | Audio+Images+Script | output_video.mp4, subtitle.srt | ✅ Optional |

---

## 🔍 Understanding Output Files

### script.txt
```
Sarah : Hello! Welcome to SPEAK ENGLISH SMARTER...
Alex : Thanks for having me!
Sarah : Today we'll learn how to introduce yourself...
[continues with dialogue]
```

### seo_metadata.txt
```
Title: How to Introduce Yourself Politely | English Conversation
Description: Learn practical English phrases for introducing...
Tags: english conversation, introductions, speaking English...
```

### thumbnail.png
- 1280×720 pixels (YouTube thumbnail)
- Soft colors, Sarah & Alex
- Ready for text overlay

### video_scene.png
- 1920×1088 pixels (video background)
- Podcast setup (Sarah LEFT, Alex RIGHT)
- Matches topic environment

### audio/audio.mp3
- Professional TTS with two voices
- Sarah (teacher), Alex (learner)
- Ready for video sync

### thumbnail_with_text.png
- Phase 5 output (if images enabled)
- Same as thumbnail.png but with text overlay
- Text from SEO metadata (eye-catching summary)
- Ready for YouTube upload

### subtitle.srt
- Phase 6 output (if video enabled)
- Auto-generated captions in SRT format
- Timing aligned with actual audio playback
- Ready for video player embedding

### output_video.mp4
- Phase 6 output (if video enabled)
- Final MP4 video (1920×1080, H.264 codec)
- Duration matches audio length (10-15 minutes)
- Includes audio + captions + spectrum visualization
- Ready for YouTube upload

---

## 🐛 Troubleshooting

| Error | Fix |
|-------|-----|
| `ANTHROPIC_API_KEY not set` | `$env:ANTHROPIC_API_KEY = "sk-ant-..."` |
| `OPENAI_API_KEY not set` | `$env:OPENAI_API_KEY = "sk-..."` |
| `(venv) not showing` | `.\venv\Scripts\Activate.ps1` |
| "No module named openai" | `pip install openai` |
| "Script validation failed" | Try adding context: `--context "more details"` |

---

## ⚙️ Advanced Options

### Validate Existing Script
```powershell
python scripts/cli.py validate --script-path outputs/your_topic/script.txt
```

### Run Setup Test
```powershell
python tests/test_phase_1.py
```

### Show Help
```powershell
python scripts/cli.py generate --help
```

---

## 📚 Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **QUICKSTART.md** | This file - 5-min overview | 5 min |
| **IMPLEMENTATION_SUMMARY.md** | Complete phases 1-6 overview | 15 min |
| **PHASE_1_README.md** | Script generation deep dive | 15 min |
| **PHASE_2_README.md** | SEO metadata details | 15 min |
| **PHASE_3_README.md** | Text-to-speech details | 15 min |
| **PLAN.md** | Master implementation plan | 20 min |
| **CLAUDE.md** | Project guidelines & instructions | 10 min |

---

## ✅ Success Checklist

After running `python scripts/cli.py generate`:

- [ ] Files created in `outputs/{topic}/`
- [ ] `script.txt` contains Sarah-Alex dialogue
- [ ] Script is 1500-2000 words (or ±35% of target)
- [ ] `seo_metadata.txt` has title, description, tags
- [ ] (If TTS enabled) `audio/audio.mp3` exists (~5-15 MB)
- [ ] (If images enabled) `thumbnail.png` exists
- [ ] (If images enabled) `video_scene.png` exists

---

## 🚀 Tips for Best Results

1. **Use Specific Topics**
   - ❌ "English lessons"
   - ✅ "How to apologize politely in English"

2. **Add Context for Complex Topics**
   ```powershell
   --context "Focus on business situations"
   ```

3. **Test with Different Lengths**
   ```powershell
   # Try 8, 12, 15 minutes to see variations
   ```

4. **Review Quality**
   - Check script reads naturally
   - Verify SEO metadata is engaging
   - Listen to TTS audio for clarity
   - View images for style consistency

---

## 🎓 Next Steps

### After First Success
1. ✅ Generate 3-5 scripts on different topics
2. ✅ Review output quality
3. ✅ Verify colors and style in images (Phase 4)
4. ✅ Check TTS audio clarity (Phase 3)

### When Ready for Phase 5
- Combine images + audio into final video
- Add text overlays to thumbnails
- Output ready-to-upload MP4

---

## 💡 Example Session

```powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Set API keys
$env:ANTHROPIC_API_KEY = "sk-ant-..."
$env:OPENAI_API_KEY = "sk-..."

# Generate assets
python scripts/cli.py generate

# When prompted:
# Topic: How to make small talk at parties
# Context: English learners, social situations
# Length: 12 (default)
# TTS: Y
# Images: Y

# Wait for completion...

# Check outputs/how_to_make_small_talk_at_parties/
```

---

## 🆘 Need Help?

1. **Check API Keys:** Verify they're valid on their respective platforms
2. **Read Docs:** See IMPLEMENTATION_SUMMARY.md for architecture
3. **Run Tests:** `python tests/test_phase_1.py`
4. **Check Status:** Look at `docs/PLAN.md` for current phase status

---

**Version:** Phase 1-4 Complete  
**Last Updated:** 2026-09-27  
**Status:** Ready to use - All phases functional

