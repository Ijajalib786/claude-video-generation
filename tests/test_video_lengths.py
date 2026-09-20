#!/usr/bin/env python3
"""
Test script to validate Phase 1 works across all video lengths (8-20 minutes).
This ensures the dynamic script length feature is robust.
"""

import sys
from pathlib import Path
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import config
from src.models import TopicInput
from src.agents.script_generation_agent import generate_script

def test_video_lengths():
    """Test script generation for all supported video lengths."""

    print("\n" + "="*70)
    print("  PHASE 1: VIDEO LENGTH VALIDATION TEST")
    print("  Testing 8-20 minute range (in 2-minute increments)")
    print("="*70 + "\n")

    # Verify API key is set
    if not config.ANTHROPIC_API_KEY:
        print("❌ ERROR: ANTHROPIC_API_KEY not set in environment")
        print("   Set it with: $env:ANTHROPIC_API_KEY='your-key'")
        return False

    print("✅ API Key found\n")

    # Test lengths: 8, 10, 12, 14, 16, 18, 20 minutes
    test_lengths = [8, 10, 12, 14, 16, 18, 20]
    topic = "Learning English Through Storytelling"

    results = []
    passed = 0
    failed = 0

    for length_minutes in test_lengths:
        print(f"\n📋 Testing {length_minutes} minutes...")
        print("-" * 50)

        target_words = length_minutes * config.WORDS_PER_MINUTE
        tolerance = int(target_words * 0.35)
        min_words = max(800, target_words - tolerance)
        max_words = target_words + tolerance

        print(f"   Target: {target_words} words")
        print(f"   Range: {min_words}-{max_words} words (±35%)")

        try:
            # Generate script
            topic_input = TopicInput(
                topic=topic,
                optional_context=f"Focus on {length_minutes}-minute format",
                target_words=target_words
            )

            script = generate_script(topic_input, target_words=target_words, tolerance=tolerance)

            # Check if within range
            word_count = script.word_count
            is_valid = min_words <= word_count <= max_words
            status_icon = "✅" if is_valid else "⚠️"

            print(f"   {status_icon} Generated: {word_count} words")
            print(f"   Duration: ~{script.estimated_duration_minutes:.1f} minutes")
            print(f"   Lines: {len(script.lines)}")

            if is_valid:
                print("   ✅ PASSED - Within acceptable range")
                passed += 1
                result_status = "PASS"
            else:
                print(f"   ❌ FAILED - Outside range ({min_words}-{max_words})")
                failed += 1
                result_status = "FAIL"

            results.append({
                "length_minutes": length_minutes,
                "target_words": target_words,
                "actual_words": word_count,
                "min_acceptable": min_words,
                "max_acceptable": max_words,
                "status": result_status
            })

        except Exception as e:
            print(f"   ❌ ERROR: {str(e)[:100]}")
            failed += 1
            results.append({
                "length_minutes": length_minutes,
                "target_words": target_words,
                "error": str(e),
                "status": "ERROR"
            })

    # Summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)

    print(f"\n✅ Passed: {passed}/{len(test_lengths)}")
    print(f"❌ Failed: {failed}/{len(test_lengths)}")

    if passed == len(test_lengths):
        print("\n🎉 SUCCESS! All video lengths (8-20 min) work correctly!")
        return True
    else:
        print(f"\n⚠️  WARNING: {failed} length(s) failed. See details above.")

    # Detailed results table
    print("\n📊 DETAILED RESULTS:\n")
    print(f"{'Length':<10} {'Target':<10} {'Actual':<10} {'Range':<20} {'Status':<10}")
    print("-" * 60)

    for result in results:
        length = result["length_minutes"]
        if "error" in result:
            print(f"{length} min{'':<4} ERROR: {result['error'][:40]}")
        else:
            target = result["target_words"]
            actual = result["actual_words"]
            min_w = result["min_acceptable"]
            max_w = result["max_acceptable"]
            status = result["status"]
            print(f"{length} min{'':<4} {target:<10} {actual:<10} {min_w}-{max_w}{'':<6} {status:<10}")

    print("\n" + "="*70 + "\n")

    return failed == 0

if __name__ == "__main__":
    success = test_video_lengths()
    sys.exit(0 if success else 1)
