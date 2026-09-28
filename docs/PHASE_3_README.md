# Phase 3: Text-to-Speech (TTS) Agent - Google Studio API

**Status:** Implementation Complete  
**Learning Goal:** Advanced orchestration, parallel processing, data integrity tracking  
**Testing:** Comprehensive segmentation and validation tests included

---

## Overview

Phase 3 adds **Text-to-Speech audio generation** using Google Studio API with multi-speaker support.

### What Phase 3 Does

Converts script dialogue into audio files:
- **Sarah Voice:** Despina (teacher, warm/patient)
- **Alex Voice:** Iapetus (learner, curious/friendly)
- **Output:** Individual audio files + combined dialogue
- **Organization:** Separate `audio/` folder per topic

### Sequential Workflow

```
Phase 1: Generate Script
    ↓ (file: script.txt)
    ↓
Phase 2: Generate SEO Metadata
    ↓ (file: seo_metadata.txt)
    ↓
Phase 3: Generate TTS Audio (NEW)
    ↓ (folder: audio/ with mp3 files)
    ↓
Phase 4+: Thumbnail/Video Assembly
```

---

## Architecture

### TTS Agent Pattern

```python
def generate_tts_audio(script: Script, output_folder: Path) -> TTSAudioMetadata:
    # Step 1: Parse script into speaker segments with line tracking
    # Step 2: Validate segmentation (no data loss)
    # Step 3: Parallel synthesis
    #   - Thread 1: Call Google Studio for Sarah
    #   - Thread 2: Call Google Studio for Alex
    # Step 4: Save audio files to audio/ folder
    # Step 5: Save metadata and reports
    # Return: TTSAudioMetadata with duration info
```

### Key Innovation: Parallel Synthesis

**Why Parallel?**
- Sarah and Alex can be synthesized simultaneously
- No dependency between voices
- Reduces total time by ~50%

**Implementation:**
```python
thread_sarah = Thread(target=synthesize_sarah)
thread_alex = Thread(target=synthesize_alex)

thread_sarah.start()
thread_alex.start()

thread_sarah.join()  # Wait for both
thread_alex.join()
```

### Script Segmentation with Line Tracking

**Purpose:** Ensure NO dialogue lines are lost during processing

**Process:**
1. Parse script into speaker turns
2. Track original line numbers for each segment
3. Generate sequence IDs: `segment_1_sarah`, `segment_2_alex`, etc.
4. Validate all original lines accounted for
5. Generate detailed segmentation report

**Example:**
```
Segment 1 (Sarah):
  Original Lines: [1, 2]
  Text: "Hello! Today we're learning..."
  Words: 45
  
Segment 2 (Alex):
  Original Lines: [3, 4]
  Text: "Great! What do we learn?"
  Words: 8
  
Segment 3 (Sarah):
  Original Lines: [5, 6]
  ...and so on...
```

---

## File Structure

### New Files Created

1. **`src/agents/tts_agent.py`** (~350 lines)
   - `generate_tts_audio()` - Main orchestrator
   - `_parse_speaker_segments()` - Script parsing
   - `_validate_segmentation()` - Data integrity check
   - `_synthesize_speaker_audio()` - Google API call
   - `_combine_audio_files()` - Simple concatenation
   - `_save_segmentation_report()` - Detailed report

2. **`tests/test_phase_3.py`** (~300 lines)
   - 6 comprehensive tests
   - Sample script generation
   - Segmentation validation
   - Error detection
   - Full pipeline readiness check

3. **`docs/PHASE_3_README.md`** (this file)
   - Phase 3 documentation
   - Usage instructions
   - Architecture details

### Updated Files

1. **`src/models.py`**
   - Added `ScriptSegment` model
   - Added `SegmentedScript` model
   - Added `TTSAudioMetadata` model
   - Updated `VideoOutput` with tts_metadata field

2. **`src/config.py`**
   - Added `GOOGLE_GEMINI_API_KEY` loading
   - Added `TTS_MODEL = "gemini-3.8-flash-tts"`
   - Added `TTS_VOICES` configuration
   - Added `TTS_PARALLEL_THREADS = 2`

3. **`scripts/cli.py`**
   - Added TTS agent import
   - Integrated TTS generation after Phase 2
   - Display TTS results in output summary
   - Updated pipeline status messaging

4. **`requirements.txt`**
   - Added `google-generativeai>=0.3.0`

5. **`config/.env.example`**
   - Added `GOOGLE_GEMINI_API_KEY` placeholder

### Output Files (per topic)

```
outputs/{topic}/
├── script.txt                 # Phase 1
├── script_metadata.json       # Phase 1
├── seo_metadata.txt           # Phase 2
└── audio/                     # Phase 3 (NEW)
    ├── sarah_audio.mp3        # Sarah voice only
    ├── alex_audio.mp3         # Alex voice only
    ├── combined_audio.mp3      # Combined dialogue
    ├── tts_metadata.json      # Metadata & segments
    └── segmentation_report.txt # Verification report
```

---

## Models & Validation

### ScriptSegment Model

```python
class ScriptSegment(BaseModel):
    segment_number: int                    # 1, 2, 3, ...
    speaker: str                           # "Sarah" or "Alex"
    dialogue_text: str                     # Full speaker turn text
    original_line_numbers: list[int]       # [1, 2] or [3]
    sequence_identifier: str               # "segment_1_sarah"
    word_count: int                        # Word count in segment
```

### SegmentedScript Model

```python
class SegmentedScript(BaseModel):
    topic: str                             # From original script
    total_segments: int                    # Total number of segments
    segments: list[ScriptSegment]          # All segments
    original_line_count: int               # Original script line count
    total_word_count: int                  # Total words across all segments
    
    @model_validator(mode='after')
    def validate_complete_segmentation(self):
        # Verify segment sequence is 1, 2, 3, ... (no gaps)
        # Verify all original lines accounted for
```

### TTSAudioMetadata Model

```python
class TTSAudioMetadata(BaseModel):
    topic: str                             # Video topic
    total_duration_seconds: float          # Full audio duration
    sarah_duration_seconds: float          # Sarah voice only
    alex_duration_seconds: float           # Alex voice only
    total_segments_processed: int          # Number of segments
    segmented_script: SegmentedScript      # Complete segmentation info
    sarah_voice_id: str = "Despina"       # Google voice name
    alex_voice_id: str = "Iapetus"        # Google voice name
    generated_at: datetime                 # Creation timestamp
```

---

## Running Phase 3

### Prerequisites

1. **Environment Setup:**
   ```powershell
   cd C:\Ijaj\Claude\claude-video-generation
   .\venv\Scripts\Activate.ps1
   ```

2. **API Keys in `config/.env`:**
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_GEMINI_API_KEY=AQ.Ab8RN6IoWcXQe9o5IFcKDWLFLv9-iglMDzBUJ4HI0XcWFRH78w
   ```

3. **Dependencies Installed:**
   ```powershell
   pip install -r requirements.txt
   ```

### Running Full Pipeline (Phases 1-3)

```powershell
python scripts\cli.py generate
```

**Prompts:**
1. Topic: Enter your video topic
2. Context (optional): Additional details
3. Video Length: 8-20 minutes (default 12)

**Output:**
- Phase 1: `script.txt` + `script_metadata.json`
- Phase 2: `seo_metadata.txt`
- Phase 3: `audio/` folder with audio files

### Running Phase 3 Tests Only

```powershell
python tests\test_phase_3.py
```

**Tests Included:**
1. ✓ Script Segmentation - Parsing into speaker turns
2. ✓ Segmentation Validation - Data loss detection
3. ✓ Speaker Balance - Both speakers present
4. ✓ Segment Sequence - Correct numbering
5. ✓ TTS Readiness - API configuration
6. ✓ Pipeline Setup - All components loaded

**Expected Output:**
```
✅ PASS: Segmentation
✅ PASS: Validation
✅ PASS: Speaker Balance
✅ PASS: Segment Sequence
✅ PASS: TTS Readiness
✅ PASS: Pipeline Setup

🎉 SUCCESS! All Phase 3 tests passed!
```

---

## Google Studio TTS API Integration

### API Call Structure

```python
# Configure Google API
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)
client = genai.Client(api_key=GOOGLE_GEMINI_API_KEY)

# Format script with speaker annotations
content = [{
    "type": "text",
    "text": "Dialogue text here",
    "annotations": [{
        "type": "speech_metadata",
        "speaker": "Sarah",
        "style": "warm and patient"
    }]
}]

# Call TTS API
response = client.models.generate_content(
    model="gemini-3.8-flash-tts",
    contents=[{"role": "user", "parts": content}],
    generation_config={
        "speech_config": {
            "mode": "conversational",
            "speakers": [
                {"speaker": "Sarah", "voice": "Despina"},
                {"speaker": "Alex", "voice": "Iapetus"}
            ]
        },
        "response_modalities": ["audio"]
    }
)

# Audio is in response.audio.data
audio_bytes = response.audio.data
```

### Voice Configuration

| Speaker | Google Voice | Personality |
|---------|-------------|-------------|
| Sarah | Despina | Female teacher (warm, patient) |
| Alex | Iapetus | Male learner (curious, friendly) |

### Parallel Synthesis Benefit

**Sequential (Old):**
```
Synthesize Sarah: 4.5s
Synthesize Alex:  4.5s
Total:           9s
```

**Parallel (New):**
```
Thread 1 (Sarah): 4.5s ┐
Thread 2 (Alex):  4.5s ├─ Total: ~4.5s
```

---

## Output Format: Segmentation Report

**Location:** `outputs/{topic}/audio/segmentation_report.txt`

**Content:**
```
=== SCRIPT SEGMENTATION REPORT ===
Topic: How to Apologize Politely
Total Segments: 12
Original Lines: 287
Total Words: 1456

SEGMENT BREAKDOWN:
────────────────────────────────────────────
segment_1_sarah
  Speaker: Sarah
  Original Lines: [1, 2, 3]
  Words: 45
  Text: "Hello everyone! Welcome to today's lesson..."

segment_2_alex
  Speaker: Alex
  Original Lines: [4, 5]
  Words: 12
  Text: "Great! What will we learn today?"

...

────────────────────────────────────────────
VALIDATION: All original lines preserved ✓
```

---

## Testing Strategy

### Unit Tests

1. **Segmentation Test**
   - Parse script correctly
   - Handle speaker alternation
   - Track line numbers accurately

2. **Validation Test**
   - Detect missing lines
   - Detect duplicated lines
   - Detect gaps in sequence

3. **Speaker Balance Test**
   - Both Sarah and Alex present
   - Correct segment count
   - Proper text content

### Integration Tests

1. **Pipeline Setup**
   - All components loadable
   - Google API configurable
   - Dependencies installed

2. **Error Handling**
   - Missing API key → clear error
   - Invalid script → validation error
   - API failure → graceful handling

### Manual Testing Checklist

- [ ] Run `python tests/test_phase_3.py` - All tests pass
- [ ] Run `python scripts/cli.py generate` - Full pipeline works
- [ ] Check `outputs/{topic}/audio/` folder exists
- [ ] Verify `sarah_audio.mp3` plays (audio quality)
- [ ] Verify `alex_audio.mp3` plays (distinct voice)
- [ ] Check `combined_audio.mp3` has both voices
- [ ] Review `tts_metadata.json` has correct segments
- [ ] Check `segmentation_report.txt` shows no data loss
- [ ] Verify duration matches script length (~{minutes})

---

## Troubleshooting

### "GOOGLE_GEMINI_API_KEY not set"

**Solution:**
```powershell
$env:GOOGLE_GEMINI_API_KEY="your-actual-key"
# OR add to config/.env:
# GOOGLE_GEMINI_API_KEY=AQ.your-key
```

### "google-generativeai not installed"

**Solution:**
```powershell
pip install google-generativeai>=0.3.0
```

### "Segmentation validation failed"

**Cause:** Lines were lost or duplicated during parsing

**Debug:**
1. Check `audio/segmentation_report.txt` for details
2. Look for "Missing lines" or "Duplicate lines" message
3. Verify original script has expected line count

### "TTS synthesis failed"

**Causes:**
- Invalid API key
- API rate limit exceeded
- Network connectivity issue
- Malformed speaker text

**Debug:**
1. Verify API key is correct
2. Check Google API quota
3. Test network connectivity
4. Review script formatting

---

## Completion Checklist

- ✅ `src/agents/tts_agent.py` created
- ✅ `tests/test_phase_3.py` created
- ✅ `src/models.py` updated with TTS models
- ✅ `src/config.py` updated with TTS config
- ✅ `scripts/cli.py` updated with Phase 3 integration
- ✅ `requirements.txt` updated with google-generativeai
- ✅ `config/.env.example` updated with Google API key
- ✅ Parallel synthesis implemented (2 threads)
- ✅ Script segmentation with line tracking complete
- ✅ Comprehensive validation and error handling
- ⏳ Testing: Ready for Phase 3 validation tests
- ⏳ User approval: Waiting for testing results

---

## Next Phase: Phase 4

After Phase 3 approval:
- **Video Assembly:** Combine audio + images using FFmpeg
- **Output:** Complete MP4 video ready for YouTube

---

## Learning Outcomes

✅ **Parallel Processing:** Multi-threaded TTS synthesis  
✅ **Data Integrity:** Line tracking prevents data loss  
✅ **External API Integration:** Google Studio API usage  
✅ **Complex Orchestration:** Multi-step pipeline with validation  
✅ **Error Handling:** Graceful failure and detailed reporting  
✅ **File Organization:** Structured output folder management  

---

**Phase 3: Complete!** 🎤

Ready for testing and integration with Phase 4.
