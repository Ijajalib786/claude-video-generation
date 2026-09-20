#!/usr/bin/env python3
"""
Quick test to verify Phase 1 setup is working.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import config to load .env file
try:
    import src.config
except Exception as e:
    print(f"⚠️  Warning: Could not import config: {e}")

def check_environment():
    """Check if environment is properly configured."""
    print("🔍 Checking environment setup...\n")

    # Get project root (tests is one level down)
    project_root = Path(__file__).parent.parent

    checks = {
        "src/config.py exists": (project_root / "src" / "config.py").exists(),
        "src/models.py exists": (project_root / "src" / "models.py").exists(),
        "src/agents/script_generation_agent.py exists": (project_root / "src" / "agents" / "script_generation_agent.py").exists(),
        "scripts/cli.py exists": (project_root / "scripts" / "cli.py").exists(),
        "requirements.txt exists": (project_root / "requirements.txt").exists(),
    }

    all_good = True
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")
        all_good = all_good and result

    print()

    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        print(f"✅ ANTHROPIC_API_KEY is set (length: {len(api_key)})")
    else:
        print("❌ ANTHROPIC_API_KEY not found in environment")
        print("   ℹ️  Set it with: $env:ANTHROPIC_API_KEY='your-key'")
        all_good = False

    # Check imports
    print("\n🔍 Checking Python imports...\n")
    try:
        import anthropic
        print(f"✅ anthropic {anthropic.__version__}")
    except ImportError:
        print("❌ anthropic not installed")
        all_good = False

    try:
        import click
        print(f"✅ click")
    except ImportError:
        print("❌ click not installed")
        all_good = False

    try:
        import pydantic
        print(f"✅ pydantic")
    except ImportError:
        print("❌ pydantic not installed")
        all_good = False

    # Check references
    print("\n🔍 Checking reference files...\n")
    ref_dir = project_root / "references"
    if ref_dir.exists():
        print(f"✅ references/ directory exists")

        # Check prompt files
        prompts_dir = ref_dir / "prompts"
        prompt_files = [
            "Script Writer-prompt.txt",
            "Title and SEO- prompt.txt",
            "Thumbnail Image- Prompt.txt",
            "Video Image- Prompt.txt"
        ]
        for filename in prompt_files:
            file_path = prompts_dir / filename
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"✅ prompts/{filename} ({size} bytes)")
            else:
                print(f"⚠️  prompts/{filename} (missing)")

        # Check example script
        example_file = ref_dir / "examples" / "Script- Say No Politely.txt"
        if example_file.exists():
            size = example_file.stat().st_size
            print(f"✅ examples/Script- Say No Politely.txt ({size} bytes)")
        else:
            print(f"⚠️  examples/Script- Say No Politely.txt (missing)")

        # Check reference images
        images_dir = ref_dir / "images"
        if images_dir.exists():
            image_files = list(images_dir.glob("*.png"))
            print(f"✅ images/ ({len(image_files)} PNG files)")
        else:
            print(f"⚠️  images/ directory (missing)")
    else:
        print("❌ references/ directory not found")
        all_good = False

    # Summary
    print("\n" + "=" * 50)
    if all_good:
        print("✅ Phase 1 Setup: ALL CHECKS PASSED")
        print("\n🚀 Ready to generate scripts!")
        print("\nTry running:")
        print("  python scripts/cli.py generate")
        return 0
    else:
        print("❌ Phase 1 Setup: SOME CHECKS FAILED")
        print("\nPlease fix the issues above before generating scripts.")
        return 1

if __name__ == "__main__":
    sys.exit(check_environment())
