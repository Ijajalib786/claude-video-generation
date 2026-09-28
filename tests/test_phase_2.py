#!/usr/bin/env python3
"""
Test script to validate Phase 2: SEO Metadata Generation
Generates SEO metadata for multiple topics and validates optimization.
"""

import sys
from pathlib import Path
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import config
from src.models import TopicInput
from src.agents.script_generation_agent import generate_script
from src.agents.seo_metadata_agent import generate_seo_metadata, save_seo_metadata_to_file

def test_seo_generation():
    """Test SEO metadata generation for multiple topics."""

    print("\n" + "="*70)
    print("  PHASE 2: SEO METADATA GENERATION TEST")
    print("  Testing Modern YouTube SEO Strategy (2026)")
    print("="*70 + "\n")

    # Verify API key is set
    if not config.ANTHROPIC_API_KEY:
        print("❌ ERROR: ANTHROPIC_API_KEY not set in environment")
        print("   Set it with: $env:ANTHROPIC_API_KEY='your-key'")
        return False

    print("✅ API Key found\n")

    # Test topics
    test_topics = [
        "How to Apologize Politely in English",
        "Making Small Talk at Parties",
        "Job Interview English Tips",
        "Casual English Slang",
        "Business Email Writing"
    ]

    results = []
    passed = 0
    failed = 0

    for topic in test_topics:
        print(f"\n📋 Testing: {topic}")
        print("-" * 50)

        try:
            # Generate script
            topic_input = TopicInput(
                topic=topic,
                optional_context=f"Focus on {topic.lower()}",
                target_words=1560  # 12 minutes
            )

            print("   1️⃣  Generating script...")
            script = generate_script(topic_input, target_words=1560, tolerance=None)

            # Generate SEO metadata
            print("   2️⃣  Generating SEO metadata...")
            seo_metadata = generate_seo_metadata(script, topic_input)

            # Validate
            print("   3️⃣  Validating metadata...")

            validations = {
                "Title length": len(seo_metadata.title) <= 65,
                "Title content": len(seo_metadata.title) > 0,
                "Description substantive": len(seo_metadata.description) > 100,
                "Description quality": len(seo_metadata.description) > 0,
                "Hashtags count": len(seo_metadata.hashtags) == 20,
                "Hashtags format": all(h.startswith('#') for h in seo_metadata.hashtags),
                "Tags count": len(seo_metadata.tags) == 20,
                "Tags content": all(len(t) > 0 for t in seo_metadata.tags),
                "Thumbnail text length": 3 <= len(seo_metadata.thumbnail_text) <= 100,
                "Thumbnail text content": len(seo_metadata.thumbnail_text) > 0,
            }

            all_valid = all(validations.values())

            # Display validation results
            for check, result in validations.items():
                status = "✓" if result else "✗"
                print(f"      {status} {check}")

            if all_valid:
                print("   ✅ PASSED - All validations passed")
                passed += 1
                status = "PASS"

                # Save to file for verification
                output_folder = config.OUTPUT_DIR / f"test_{topic.lower().replace(' ', '_')[:20]}"
                save_seo_metadata_to_file(seo_metadata, output_folder)
            else:
                print("   ❌ FAILED - Some validations failed")
                failed += 1
                status = "FAIL"

            results.append({
                "topic": topic,
                "title": seo_metadata.title,
                "title_chars": len(seo_metadata.title),
                "description_words": len(seo_metadata.description.split()),
                "hashtags": len(seo_metadata.hashtags),
                "tags": len(seo_metadata.tags),
                "thumbnail_text": seo_metadata.thumbnail_text,
                "thumbnail_chars": len(seo_metadata.thumbnail_text),
                "status": status
            })

        except Exception as e:
            print(f"   ❌ ERROR: {str(e)[:100]}")
            failed += 1
            results.append({
                "topic": topic,
                "error": str(e),
                "status": "ERROR"
            })

    # Summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)

    print(f"\n✅ Passed: {passed}/{len(test_topics)}")
    print(f"❌ Failed: {failed}/{len(test_topics)}")

    if passed == len(test_topics):
        print("\n🎉 SUCCESS! All topics generated valid SEO metadata!")
    else:
        print(f"\n⚠️  WARNING: {failed} topic(s) failed validation")

    # Detailed results
    print("\n📊 DETAILED RESULTS:\n")
    print(f"{'Topic':<30} {'Title Length':<15} {'Desc Words':<12} {'Status':<10}")
    print("-" * 67)

    for result in results:
        topic = result["topic"][:27]
        if "error" in result:
            print(f"{topic:<30} ERROR")
        else:
            title_len = result["title_chars"]
            desc_words = result["description_words"]
            status = result["status"]
            print(f"{topic:<30} {title_len:<15} {desc_words:<12} {status:<10}")

    # Sample results display
    if results and "title" in results[0]:
        print("\n📌 SAMPLE RESULTS (First Topic):")
        first = results[0]
        print(f"\nTitle: {first['title']}")
        print(f"Thumbnail Text: {first['thumbnail_text']}")
        print(f"Hashtags: {', '.join(['#hashtag' for _ in range(5)])} ... ({first['hashtags']} total)")
        print(f"Tags: {', '.join(['tag' for _ in range(5)])} ... ({first['tags']} total)")

    print("\n" + "="*70 + "\n")

    return failed == 0

if __name__ == "__main__":
    success = test_seo_generation()
    sys.exit(0 if success else 1)
