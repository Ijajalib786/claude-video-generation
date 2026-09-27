import os
from pathlib import Path
from dotenv import load_dotenv

# Project root is one level up from src/
PROJECT_ROOT = Path(__file__).parent.parent

# Load environment variables from .env file (use string path, not Path object)
env_file = str(PROJECT_ROOT / "config" / ".env")
if os.path.exists(env_file):
    load_dotenv(env_file, override=True, verbose=True)

REFERENCES_DIR = PROJECT_ROOT / "references"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
TEMP_DIR = PROJECT_ROOT / "temp"

# Create directories if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# API Keys - try .env first, then environment variables, then empty string
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip("'\"")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip("'\"")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY", "").strip("'\"")  # For Google Studio TTS

# Paths
PROMPTS_DIR = REFERENCES_DIR / "prompts"
EXAMPLES_DIR = REFERENCES_DIR / "examples"
IMAGES_DIR = REFERENCES_DIR / "images"

SCRIPT_PROMPT_PATH = PROMPTS_DIR / "Script Writer-prompt.txt"
SEO_PROMPT_PATH = PROMPTS_DIR / "Title and SEO- prompt.txt"
THUMBNAIL_PROMPT_PATH = PROMPTS_DIR / "Thumbnail Image- Prompt.txt"
VIDEO_PROMPT_PATH = PROMPTS_DIR / "Video Image- Prompt.txt"
EXAMPLE_SCRIPT_PATH = EXAMPLES_DIR / "Script- Say No Politely.txt"

# Content specs
SCRIPT_MIN_WORDS = 1500
SCRIPT_MAX_WORDS = 2000
TARGET_VIDEO_MINUTES = 12  # Average target for 10-15 min range
WORDS_PER_MINUTE = 130     # Typical English speech rate for learners

# Model settings
CLAUDE_MODEL = "claude-sonnet-5"
GPT_MODEL = "gpt-4o"
TEMPERATURE = 0.7
MAX_TOKENS = 4096

# TTS Settings (Phase 3)
TTS_MODEL = "gemini-3.8-flash-tts"
TTS_VOICES = {
    "Sarah": "Leda",    # Female voice (from official Google code)
    "Alex": "Iapetus"      # Male voice (from official Google code)
}
TTS_AUDIO_FORMAT = "mp3"  # Output format
TTS_SAMPLE_RATE = 24000  # Sample rate in Hz
TTS_PARALLEL_THREADS = 2  # Number of parallel synthesis threads (Sarah + Alex)

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
