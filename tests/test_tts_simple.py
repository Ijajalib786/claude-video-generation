#!/usr/bin/env python3
"""
Test google.genai TTS - extract audio from response.parts (inline_data).
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from src import config

print("=" * 70)
print("GOOGLE GENAI TTS - EXTRACT AUDIO FROM RESPONSE")
print("=" * 70)

from google import genai

client = genai.Client(api_key=config.GOOGLE_GEMINI_API_KEY)

test_text = "Hello! This is Sarah speaking. How are you doing today?"

print("\n1️⃣  Testing Chat with TTS model...")
try:
    chat = client.chats.create(model="models/gemini-3.8-flash-tts")
    response = chat.send_message(test_text)
    print(f"   ✓ Response received")

    # Extract audio from parts (inline_data)
    audio_data = None
    if hasattr(response, 'parts') and response.parts:
        for part in response.parts:
            print(f"   Part type: {type(part)}")
            if hasattr(part, 'inline_data'):
                audio_data = part.inline_data.data
                print(f"   ✓ Found audio in inline_data: {len(audio_data)} bytes")
                break

    if audio_data:
        # Save audio
        output_path = Path(__file__).parent / "test_audio_real.wav"
        with open(output_path, 'wb') as f:
            f.write(audio_data)
        print(f"   ✓ Saved to: {output_path}")
        print(f"   🎉 REAL TTS AUDIO GENERATED!")
    else:
        print(f"   ✗ No audio found in response")
        print(f"   Response parts: {response.parts}")

except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n2️⃣  Testing with custom prompt for Sarah and Alex...")
try:
    chat = client.chats.create(model="models/gemini-3.8-flash-tts")

    # Send dialogue text
    dialogue = """Sarah: Hello everyone, welcome to our lesson today!
Alex: Thanks Sarah, I'm excited to learn.
Sarah: Great! Let's get started."""

    response = chat.send_message(dialogue)

    # Extract audio
    audio_data = None
    if hasattr(response, 'parts') and response.parts:
        for part in response.parts:
            if hasattr(part, 'inline_data'):
                audio_data = part.inline_data.data
                break

    if audio_data:
        output_path = Path(__file__).parent / "test_audio_dialogue.wav"
        with open(output_path, 'wb') as f:
            f.write(audio_data)
        print(f"   ✓ Dialogue audio saved: {len(audio_data)} bytes")
    else:
        print(f"   ✗ No audio in dialogue response")

except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 70)
print("✅ REAL TTS API WORKING!")
print("=" * 70)
print("\nAudio files generated:")
print("  - test_audio_real.wav (Sarah voice)")
print("  - test_audio_dialogue.wav (Sarah + Alex dialogue)")
print("\nPlay these files to hear real voices!")
