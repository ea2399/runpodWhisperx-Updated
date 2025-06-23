#!/usr/bin/env python3
"""
Test configurations for the enhanced WhisperX MCP server.

This file demonstrates various ways to configure and test the WhisperX server
with different parameter combinations.
"""

import json
import requests
import base64
from typing import Dict, Any

# ------------------------------------------------------------------
#  Test Data and Utilities
# ------------------------------------------------------------------

def encode_audio_file(file_path: str) -> str:
    """Encode an audio file to base64 for testing."""
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode('utf-8')

def print_test_case(name: str, config: Dict[str, Any]) -> None:
    """Print a formatted test case."""
    print(f"\n{'='*60}")
    print(f"TEST CASE: {name}")
    print(f"{'='*60}")
    print(json.dumps(config, indent=2))

# ------------------------------------------------------------------
#  Test Cases
# ------------------------------------------------------------------

def basic_transcription_tests():
    """Basic transcription test cases."""
    
    # Test 1: Minimal configuration (URL)
    basic_url_config = {
        "input": {
            "audio_url": "https://example.com/audio.mp3"
        }
    }
    print_test_case("Basic URL Transcription", basic_url_config)
    
    # Test 2: Minimal configuration (Base64)
    basic_b64_config = {
        "input": {
            "audio_base_64": "UklGRiQAAABXQVZFZm10IBAAAAABAAEA..."  # Truncated for display
        }
    }
    print_test_case("Basic Base64 Transcription", basic_b64_config)
    
    # Test 3: Different models
    model_configs = [
        {"input": {"audio_url": "https://example.com/audio.mp3", "model": "tiny"}},
        {"input": {"audio_url": "https://example.com/audio.mp3", "model": "base"}},
        {"input": {"audio_url": "https://example.com/audio.mp3", "model": "small"}},
        {"input": {"audio_url": "https://example.com/audio.mp3", "model": "medium"}},
        {"input": {"audio_url": "https://example.com/audio.mp3", "model": "large-v2"}},
        {"input": {"audio_url": "https://example.com/audio.mp3", "model": "large-v3"}}
    ]
    
    for i, config in enumerate(model_configs):
        print_test_case(f"Model Test {i+1} - {config['input']['model']}", config)

def language_specific_tests():
    """Language-specific transcription tests."""
    
    languages = [
        {"language": "en", "name": "English"},
        {"language": "fr", "name": "French"},
        {"language": "de", "name": "German"},
        {"language": "es", "name": "Spanish"},
        {"language": "it", "name": "Italian"},
        {"language": "ja", "name": "Japanese"},
        {"language": "zh", "name": "Chinese"},
        {"language": "auto", "name": "Auto-detect"}
    ]
    
    for lang in languages:
        config = {
            "input": {
                "audio_url": "https://example.com/audio.mp3",
                "model": "large-v2",
                "language": lang["language"]
            }
        }
        print_test_case(f"Language Test - {lang['name']}", config)

def performance_optimization_tests():
    """Performance and memory optimization tests."""
    
    # Test 1: High-performance configuration
    high_perf_config = {
        "input": {
            "audio_url": "https://example.com/audio.mp3",
            "model": "large-v3",
            "compute_type": "float16",
            "batch_size": 32,
            "device": "cuda"
        }
    }
    print_test_case("High Performance Config", high_perf_config)
    
    # Test 2: Memory-constrained configuration
    low_memory_config = {
        "input": {
            "audio_url": "https://example.com/audio.mp3",
            "model": "small",
            "compute_type": "int8",
            "batch_size": 4,
            "device": "cuda"
        }
    }
    print_test_case("Low Memory Config", low_memory_config)
    
    # Test 3: CPU-only configuration
    cpu_config = {
        "input": {
            "audio_url": "https://example.com/audio.mp3",
            "model": "base",
            "compute_type": "int8",
            "batch_size": 2,
            "device": "cpu"
        }
    }
    print_test_case("CPU Only Config", cpu_config)

def diarization_tests():
    """Speaker diarization test cases."""
    
    # Test 1: Basic diarization
    basic_diarization = {
        "input": {
            "audio_url": "https://example.com/meeting.mp3",
            "model": "large-v2",
            "diarize": True,
            "hf_token": "your_huggingface_token_here"
        }
    }
    print_test_case("Basic Diarization", basic_diarization)
    
    # Test 2: Diarization with speaker constraints
    constrained_diarization = {
        "input": {
            "audio_url": "https://example.com/meeting.mp3",
            "model": "large-v2",
            "diarize": True,
            "min_speakers": 2,
            "max_speakers": 4,
            "hf_token": "your_huggingface_token_here"
        }
    }
    print_test_case("Constrained Diarization", constrained_diarization)
    
    # Test 3: Interview scenario (2 speakers)
    interview_config = {
        "input": {
            "audio_url": "https://example.com/interview.mp3",
            "model": "large-v2",
            "language": "en",
            "diarize": True,
            "min_speakers": 2,
            "max_speakers": 2,
            "hf_token": "your_huggingface_token_here",
            "batch_size": 16
        }
    }
    print_test_case("Interview Scenario", interview_config)

def advanced_configuration_tests():
    """Advanced configuration test cases."""
    
    # Test 1: Full-featured configuration
    full_config = {
        "input": {
            "audio_url": "https://example.com/complex_audio.mp3",
            "model": "large-v3",
            "language": "en",
            "compute_type": "float16",
            "device": "cuda",
            "batch_size": 16,
            "condition_on_prev_text": False,
            "without_timestamps": True,
            "initial_prompt": "This is a technical discussion about AI.",
            "return_char_alignments": True,
            "interpolate_method": "nearest",
            "diarize": True,
            "min_speakers": 2,
            "max_speakers": 5,
            "hf_token": "your_huggingface_token_here",
            "highlight_words": True,
            "segment_resolution": "sentence"
        }
    }
    print_test_case("Full-Featured Configuration", full_config)
    
    # Test 2: Subtitle generation optimized
    subtitle_config = {
        "input": {
            "audio_url": "https://example.com/video_audio.mp3",
            "model": "large-v2",
            "language": "en",
            "highlight_words": True,
            "max_line_width": 42,
            "max_line_count": 2,
            "segment_resolution": "sentence",
            "batch_size": 12
        }
    }
    print_test_case("Subtitle Generation", subtitle_config)
    
    # Test 3: Multilingual detection with fallback
    multilingual_config = {
        "input": {
            "audio_url": "https://example.com/mixed_language.mp3",
            "model": "large-v3",
            "language": "auto",
            "compute_type": "float16",
            "batch_size": 8,
            "condition_on_prev_text": False
        }
    }
    print_test_case("Multilingual Auto-detect", multilingual_config)

def real_world_scenarios():
    """Real-world usage scenarios."""
    
    # Scenario 1: Podcast transcription
    podcast_config = {
        "input": {
            "audio_url": "https://example.com/podcast_episode.mp3",
            "model": "large-v2",
            "language": "en",
            "diarize": True,
            "min_speakers": 2,
            "max_speakers": 3,
            "hf_token": "your_huggingface_token_here",
            "batch_size": 20,
            "highlight_words": True,
            "segment_resolution": "sentence"
        }
    }
    print_test_case("Podcast Transcription", podcast_config)
    
    # Scenario 2: Academic lecture
    lecture_config = {
        "input": {
            "audio_url": "https://example.com/lecture.mp3",
            "model": "large-v3",
            "language": "en",
            "initial_prompt": "This is an academic lecture about computer science.",
            "batch_size": 24,
            "condition_on_prev_text": True,
            "segment_resolution": "sentence"
        }
    }
    print_test_case("Academic Lecture", lecture_config)
    
    # Scenario 3: Customer service call
    customer_service_config = {
        "input": {
            "audio_url": "https://example.com/customer_call.mp3",
            "model": "large-v2",
            "language": "en",
            "diarize": True,
            "min_speakers": 2,
            "max_speakers": 2,
            "hf_token": "your_huggingface_token_here",
            "initial_prompt": "This is a customer service call.",
            "batch_size": 12
        }
    }
    print_test_case("Customer Service Call", customer_service_config)
    
    # Scenario 4: Foreign language news
    foreign_news_config = {
        "input": {
            "audio_url": "https://example.com/spanish_news.mp3",
            "model": "large-v2",
            "language": "es",
            "batch_size": 16,
            "highlight_words": True,
            "segment_resolution": "sentence"
        }
    }
    print_test_case("Foreign Language News", foreign_news_config)

def error_handling_tests():
    """Test cases for error handling."""
    
    # Test 1: Missing audio input
    no_audio_config = {
        "input": {
            "model": "large-v2"
        }
    }
    print_test_case("Missing Audio Input (Should Error)", no_audio_config)
    
    # Test 2: Invalid model
    invalid_model_config = {
        "input": {
            "audio_url": "https://example.com/audio.mp3",
            "model": "invalid-model"
        }
    }
    print_test_case("Invalid Model (Should Error)", invalid_model_config)
    
    # Test 3: Invalid batch size
    invalid_batch_config = {
        "input": {
            "audio_url": "https://example.com/audio.mp3",
            "batch_size": -1
        }
    }
    print_test_case("Invalid Batch Size (Should Error)", invalid_batch_config)

# ------------------------------------------------------------------
#  Usage Examples for Different RunPod Endpoints
# ------------------------------------------------------------------

def runpod_api_examples():
    """Examples of how to call the RunPod API with different configurations."""
    
    print(f"\n{'='*60}")
    print("RUNPOD API USAGE EXAMPLES")
    print(f"{'='*60}")
    
    # Example 1: Python requests
    python_example = """
# Python example using requests
import requests
import json

endpoint_url = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
}

# Basic transcription
data = {
    "input": {
        "audio_url": "https://example.com/audio.mp3",
        "model": "large-v2",
        "language": "en"
    }
}

response = requests.post(endpoint_url, headers=headers, json=data)
result = response.json()
print(result)
"""
    print("Python Example:")
    print(python_example)
    
    # Example 2: cURL
    curl_example = """
# cURL example
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -d '{
    "input": {
      "audio_url": "https://example.com/audio.mp3",
      "model": "large-v2",
      "diarize": true,
      "hf_token": "your_hf_token"
    }
  }'
"""
    print("cURL Example:")
    print(curl_example)

# ------------------------------------------------------------------
#  Main Test Runner
# ------------------------------------------------------------------

def main():
    """Run all test configurations."""
    print("WhisperX MCP Server - Test Configurations")
    print("=" * 60)
    
    basic_transcription_tests()
    language_specific_tests()
    performance_optimization_tests()
    diarization_tests()
    advanced_configuration_tests()
    real_world_scenarios()
    error_handling_tests()
    runpod_api_examples()
    
    print(f"\n{'='*60}")
    print("NOTES:")
    print("- Replace 'your_huggingface_token_here' with your actual HF token")
    print("- Replace example URLs with actual audio file URLs")
    print("- Adjust batch_size based on your GPU memory")
    print("- For base64 input, encode your audio file first")
    print(f"{'='*60}")

if __name__ == "__main__":
    main() 