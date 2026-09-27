#!/usr/bin/env python3
"""
Debug test - Check if audio is being generated with speaker annotations.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src import config
from google import genai

print("=" * 70)
print("AUDIO GENERATION DEBUG TEST")
print("=" * 70)

client = genai.Client(api_key=config.GOOGLE_GEMINI_API_KEY)
chat = client.chats.create(model=config.TTS_MODEL)

# Test 1: Simple text without annotations
print("\n1️⃣  Test: Simple text (no annotations)...")
try:
    response = chat.send_message("Hello, this is a simple test.")
    if hasattr(response, 'parts') and response.parts:
        for part in response.parts:
            if hasattr(part, 'inline_data'):
                audio_bytes = part.inline_data.data
                print(f"   ✓ Audio generated: {len(audio_bytes)} bytes")
                with open("test_simple.wav", "wb") as f:
                    f.write(audio_bytes)
                print(f"   ✓ Saved to: test_simple.wav")
                break
    else:
        print(f"   ✗ No audio in response")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: With speaker annotations
print("\n2️⃣  Test: With speaker annotations...")
try:
    formatted_parts = [
        {
            "type": "text",
            "text": "Sarah: Hello everyone, welcome to our lesson!",
            "annotations": [{
                "type": "speech_metadata",
                "speaker": "Sarah",
                "style": "warm and patient"
            }]
        },
        {
            "type": "text",
            "text": "Alex: Thanks Sarah, I'm excited to learn!",
            "annotations": [{
                "type": "speech_metadata",
                "speaker": "Alex",
                "style": "curious and friendly"
            }]
        }
    ]

    response = chat.send_message(formatted_parts)
    if hasattr(response, 'parts') and response.parts:
        for part in response.parts:
            if hasattr(part, 'inline_data'):
                audio_bytes = part.inline_data.data
                print(f"   ✓ Audio generated: {len(audio_bytes)} bytes")
                with open("test_annotations.wav", "wb") as f:
                    f.write(audio_bytes)
                print(f"   ✓ Saved to: test_annotations.wav")
                break
    else:
        print(f"   ✗ No audio in response")
        print(f"   Response parts: {response.parts if hasattr(response, 'parts') else 'No parts'}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("✅ Debug test complete")
print("=" * 70)
print("\nCheck generated files:")
print("  - test_simple.wav (simple text)")
print("  - test_annotations.wav (with speaker annotations)")
print("\nIf files exist but are silent:")
print("  - Check file sizes")
print("  - Try playing in different audio player")
print("  - Verify Google API quota is not exhausted")
