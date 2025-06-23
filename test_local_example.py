#!/usr/bin/env python3
"""
Test the enhanced WhisperX MCP server using the local example.mp3 file.

This script demonstrates how to test the server with various configurations
using the provided example audio file.
"""

import base64
import json
from handler import handler

def encode_local_audio(file_path: str) -> str:
    """Encode the local audio file to base64."""
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode('utf-8')

def test_local_audio():
    """Test configurations using the local example.mp3 file."""
    
    # Encode the example audio file
    try:
        audio_b64 = encode_local_audio("example.mp3")
        print("✅ Successfully encoded example.mp3 to base64")
    except FileNotFoundError:
        print("❌ example.mp3 not found. Make sure you're running this from the project root.")
        return
    
    # Test configurations
    test_cases = [
        {
            "name": "Basic Transcription",
            "config": {
                "input": {
                    "audio_base_64": audio_b64,
                    "model": "small"
                }
            }
        },
        {
            "name": "Large Model with Language Detection",
            "config": {
                "input": {
                    "audio_base_64": audio_b64,
                    "model": "large-v2",
                    "language": "auto",
                    "batch_size": 8
                }
            }
        },
        {
            "name": "High Quality with Alignment",
            "config": {
                "input": {
                    "audio_base_64": audio_b64,
                    "model": "medium",
                    "language": "en",
                    "return_char_alignments": True,
                    "batch_size": 12
                }
            }
        },
        {
            "name": "Memory Optimized",
            "config": {
                "input": {
                    "audio_base_64": audio_b64,
                    "model": "base",
                    "compute_type": "int8",
                    "batch_size": 4
                }
            }
        }
    ]
    
    # Run tests
    for test_case in test_cases:
        print(f"\n{'='*50}")
        print(f"🧪 Testing: {test_case['name']}")
        print(f"{'='*50}")
        
        try:
            # Run the handler
            result = handler(test_case['config'])
            
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print("✅ Success!")
                
                # Print summary
                segments = result.get('segments', [])
                print(f"📊 Segments found: {len(segments)}")
                
                if segments:
                    print(f"🌐 Detected language: {result.get('language', 'unknown')}")
                    print(f"⚙️  Configuration used:")
                    config_used = result.get('config_used', {})
                    for key, value in config_used.items():
                        print(f"   - {key}: {value}")
                    
                    # Show first few segments
                    print(f"📝 First segment(s):")
                    for i, segment in enumerate(segments[:2]):
                        start = segment.get('start', 0)
                        end = segment.get('end', 0)
                        text = segment.get('text', '').strip()
                        speaker = segment.get('speaker', 'N/A')
                        print(f"   [{start:.2f}s - {end:.2f}s] {speaker}: {text}")
                
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")

def test_with_diarization():
    """Test with speaker diarization (requires HF token)."""
    print(f"\n{'='*50}")
    print("🎯 Diarization Test (Requires HF Token)")
    print(f"{'='*50}")
    
    hf_token = input("Enter your HuggingFace token (or press Enter to skip): ").strip()
    
    if not hf_token:
        print("⏭️  Skipping diarization test (no HF token provided)")
        return
    
    try:
        audio_b64 = encode_local_audio("example.mp3")
        
        diarization_config = {
            "input": {
                "audio_base_64": audio_b64,
                "model": "medium",
                "language": "en",
                "diarize": True,
                "hf_token": hf_token,
                "batch_size": 8
            }
        }
        
        print("🔄 Running diarization test...")
        result = handler(diarization_config)
        
        if "error" in result:
            print(f"❌ Diarization failed: {result['error']}")
        else:
            print("✅ Diarization successful!")
            segments = result.get('segments', [])
            speakers = set()
            
            for segment in segments:
                if 'speaker' in segment:
                    speakers.add(segment['speaker'])
            
            print(f"👥 Speakers detected: {len(speakers)} ({', '.join(speakers)})")
            
            # Show segments with speakers
            for i, segment in enumerate(segments[:3]):
                start = segment.get('start', 0)
                end = segment.get('end', 0)
                text = segment.get('text', '').strip()
                speaker = segment.get('speaker', 'Unknown')
                print(f"   [{start:.2f}s - {end:.2f}s] {speaker}: {text}")
    
    except Exception as e:
        print(f"❌ Diarization test failed: {str(e)}")

def show_available_options():
    """Show all available configuration options."""
    print(f"\n{'='*60}")
    print("📋 AVAILABLE CONFIGURATION OPTIONS")
    print(f"{'='*60}")
    
    options = {
        "Audio Input (required - choose one)": [
            "audio_url - URL to audio file",
            "audio_base_64 - Base64 encoded audio data"
        ],
        "Core Parameters": [
            "model - tiny, base, small, medium, large, large-v2, large-v3",
            "language - auto, en, fr, de, es, it, ja, zh, etc.",
            "compute_type - float16, float32, int8",
            "device - cuda, cpu"
        ],
        "Performance": [
            "batch_size - integer (1-64, default: 16)",
            "condition_on_prev_text - true/false",
            "without_timestamps - true/false",
            "initial_prompt - string"
        ],
        "Alignment": [
            "return_char_alignments - true/false",
            "interpolate_method - nearest, linear"
        ],
        "Diarization": [
            "diarize - true/false",
            "min_speakers - integer",
            "max_speakers - integer", 
            "hf_token - HuggingFace token (required for diarization)"
        ],
        "Output": [
            "highlight_words - true/false",
            "segment_resolution - sentence, chunk"
        ]
    }
    
    for category, items in options.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  • {item}")

def main():
    """Main test runner."""
    print("🎵 WhisperX Enhanced MCP Server - Local Testing")
    print("=" * 60)
    
    show_available_options()
    
    print(f"\n{'='*60}")
    print("🚀 RUNNING TESTS")
    print(f"{'='*60}")
    
    # Run basic tests
    test_local_audio()
    
    # Optional diarization test
    test_with_diarization()
    
    print(f"\n{'='*60}")
    print("✨ TESTING COMPLETE")
    print("💡 Tip: You can now deploy this to RunPod and use the same configurations!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main() 