# WhisperX MCP Server - Enhanced

**2025 Update:** Dockerfile now targets the latest `runpod/pytorch` base image with Python 3.11 and CUDA 12.8. The required Python packages have been upgraded to modern versions.

This is an **Enhanced Docker Image** that runs the [WhisperX](https://github.com/m-bain/whisperX) repository with **comprehensive parameter configuration support** for MCP (Model Context Protocol). 

## ✨ New Features (Enhanced Version)

- 🎛️ **Configurable Parameters**: Control every aspect of WhisperX processing
- 🌍 **Language Detection**: Auto-detect or specify languages
- 👥 **Speaker Diarization**: Full support with configurable speaker counts
- ⚡ **Performance Tuning**: Optimize for your GPU memory and speed requirements
- 🎯 **Model Selection**: Choose from all WhisperX models (tiny to large-v3)
- 📝 **Advanced Alignment**: Word-level and character-level alignment options
- 🛡️ **Error Handling**: Comprehensive validation and error reporting
- 📊 **Detailed Output**: Enhanced response format with metadata

## Basic Usage

### Simple Audio Transcription
```json
{
    "input": {
        "audio_base_64": "base64 encoding of audio"
    }
}
```

### Advanced Configuration Example
```json
{
    "input": {
        "audio_url": "https://example.com/meeting.mp3",
        "model": "large-v2",
        "language": "en",
        "diarize": true,
        "min_speakers": 2,
        "max_speakers": 4,
        "hf_token": "your_huggingface_token",
        "batch_size": 16,
        "compute_type": "float16",
        "highlight_words": true
    }
}
```

## 📋 Configuration Parameters

### Audio Input (Required - Choose One)
- `audio_url` (string): Direct URL to audio file (MP3, MP4, WAV, etc.) - preferred for large files
- `audio_base_64` (string): Base64-encoded audio data - alternative to audio_url

### Core WhisperX Parameters
- `model` (string, default: "small"): WhisperX model size
  - Options: `"tiny"`, `"base"`, `"small"`, `"medium"`, `"large"`, `"large-v2"`, `"large-v3"`
- `language` (string, default: "auto"): Language code for transcription
  - Options: `"auto"`, `"en"`, `"fr"`, `"de"`, `"es"`, `"it"`, `"ja"`, `"zh"`, `"ko"`, etc.
- `compute_type` (string, default: "float16"): Computation precision
  - Options: `"float16"` (recommended), `"float32"` (highest quality), `"int8"` (fastest)
- `device` (string, default: "cuda"): Device to use
  - Options: `"cuda"`, `"cpu"`

### Performance Parameters
- `batch_size` (integer, default: 16): Batch size for inference
  - Lower values use less GPU memory but are slower
  - Recommended: 32 for 8GB VRAM, 16 for 6GB, 8 for 4GB, 4 for 2GB
- `condition_on_prev_text` (boolean, default: false): Whether to condition on previous text
- `without_timestamps` (boolean, default: true): Process without timestamps for faster batching
- `initial_prompt` (string, optional): Initial prompt to guide transcription

### Alignment Parameters
- `return_char_alignments` (boolean, default: false): Return character-level alignments
- `interpolate_method` (string, default: "nearest"): Interpolation method for alignment

### Speaker Diarization Parameters
- `diarize` (boolean, default: false): Enable speaker diarization
- `min_speakers` (integer, optional): Minimum number of speakers
- `max_speakers` (integer, optional): Maximum number of speakers
- `hf_token` (string, required for diarization): HuggingFace token for diarization models

### Output Parameters
- `highlight_words` (boolean, default: false): Highlight words in output
- `segment_resolution` (string, default: "sentence"): Segment resolution
  - Options: `"sentence"`, `"chunk"`

## 🚀 Usage Examples

### Podcast Transcription with Speaker Identification
```json
{
    "input": {
        "audio_url": "https://example.com/podcast.mp3",
        "model": "large-v2",
        "language": "en",
        "diarize": true,
        "min_speakers": 2,
        "max_speakers": 3,
        "hf_token": "your_huggingface_token",
        "batch_size": 20,
        "highlight_words": true
    }
}
```

### High-Performance Large File Processing
```json
{
    "input": {
        "audio_url": "https://example.com/long_meeting.mp3",
        "model": "large-v3",
        "compute_type": "float16",
        "batch_size": 32,
        "language": "auto"
    }
}
```

### Memory-Optimized Configuration
```json
{
    "input": {
        "audio_base_64": "UklGRiQAAABXQVZFZm10IBAAAAABAAEA...",
        "model": "small",
        "compute_type": "int8",
        "batch_size": 4,
        "device": "cuda"
    }
}
```

### Multilingual Auto-Detection
```json
{
    "input": {
        "audio_url": "https://example.com/mixed_languages.mp3",
        "model": "large-v2",
        "language": "auto",
        "batch_size": 12
    }
}
```

## 🔍 Response Format

The enhanced server returns detailed information:

```json
{
    "segments": [
        {
            "start": 0.0,
            "end": 5.2,
            "text": "Hello, this is a test.",
            "words": [
                {
                    "word": "Hello,",
                    "start": 0.0,
                    "end": 0.8,
                    "score": 0.95,
                    "speaker": "SPEAKER_00"
                }
            ],
            "speaker": "SPEAKER_00"
        }
    ],
    "language": "en",
    "config_used": {
        "model": "large-v2",
        "language": "en",
        "compute_type": "float16",
        "batch_size": 16,
        "diarize": true
    }
}
```

## 🧪 Local Testing

Test the enhanced server locally:

```bash
# Test with example audio file
python test_local_example.py

# Test different configurations
python test_configurations.py
```

## ⚡ Performance & Memory Guidelines

### GPU Memory Requirements
- **Large-v3**: ~8GB VRAM (best quality)
- **Large-v2**: ~6GB VRAM (excellent quality)
- **Medium**: ~4GB VRAM (good quality)
- **Small**: ~2GB VRAM (decent quality)
- **Base**: ~1GB VRAM (basic quality)
- **Tiny**: ~500MB VRAM (minimal quality)

### Batch Size Recommendations
- **8GB VRAM**: batch_size 16-32
- **6GB VRAM**: batch_size 8-16  
- **4GB VRAM**: batch_size 4-8
- **2GB VRAM**: batch_size 2-4

### Compute Type Impact
- **float16**: Best balance of speed and accuracy (recommended)
- **float32**: Highest accuracy, slower, more memory
- **int8**: Fastest, lowest memory, may reduce accuracy

## 🔄 Migration from Previous Version

The enhanced version is **fully backward compatible**. Your existing API calls will continue to work unchanged:

```json
// Old format still works
{
    "input": {
        "audio_base_64": "base64_data",
        "model": "small",
        "diarize": false
    }
}
```

New parameters are **optional** with sensible defaults, so you can gradually adopt new features as needed.

## 📖 Documentation

For complete parameter documentation, see `Instructions.md` in this repository.

## How to Build This Docker Image

You can replace anything that is `depot` with docker. I'm just using their service to build for amd64 platform, since I am on an arm64 platform on an M1 Mac.

Build the Image using Depot

```
depot build -t runpodwhisperx . --platform linux/amd64
```

Tag and Push it

```
docker tag runpodwhisperx:latest justinwlin/runpodwhisperx:1.0 && docker push justinwlin/runpodwhisperx:1.0
```

Or build & directly push it with depot:

```
depot build -t justinwlin/runpodwhisperx:1.0 . --platform linux/amd64 --push
```

Docker Repo:
(FYI - I don't do proper versioning control. I keep pushing over 1.0 until it is stable, and only there, do I
begin to do versioning control with 1.1, 1.2, etc.)

https://hub.docker.com/repository/docker/justinwlin/runpodwhisperx/general

Environment Variable for when working on Mac locally:

```
export DEVICE=cpu
export COMPUTE_TYPE=int8
```

## Local Testing

If you want to test locally, can just run:
`python3 main.py` It will automatically call the handler with the test_input.json

https://docs.runpod.io/docs/local-testing

This is assuming that you install requirements such as anything listed on the WHisperX repository and the runpod sdk.
## Running on Runpod

Follow these steps to deploy the container on [Runpod](https://runpod.io):

1. **Build your image**
   ```bash
   docker build -t <docker-user>/runpodwhisperx:1.0 .
   ```
2. **Push it to Docker Hub**
   ```bash
   docker push <docker-user>/runpodwhisperx:1.0
   ```
3. **Create a Serverless Endpoint**
   - Log into Runpod and open **Serverless > Create Endpoint**.
   - Enter the image name you pushed.
   - Select your GPU type and region.
   - Set optional environment variables like `DEVICE` and `COMPUTE_TYPE`.
   - Click **Create Endpoint** and copy the generated endpoint ID.
4. **Send a request**
   ```bash
   curl -X POST https://api.runpod.ai/v2/<ENDPOINT_ID>/runsync \
        -H 'Authorization: Bearer <RUNPOD_API_KEY>' \
        -H 'Content-Type: application/json' \
        -d @test_input.json
   ```
5. **View the results**
   The API will return the transcription output in JSON.

# Example Functions of me calling the runpod:

```
def send_and_auto_async_request_runpod_subtitler(base64_string, RUNPOD_API_KEY):
    """
    Automatically makes an async request to runpod and keeps checking the status until the job is completed.

    @param
    base64_string: The base64 string of the audio file
    RUNPOD_API_KEY: The API key for Runpod

    @return
    outputResponse: The response from Runpod. Structured as:
    {
        "status": "COMPLETED",
        "output": {
            "segments": [
                {
                    "start": 0.27,
                    "end": 1.632,
                    "text": " Hello world.",
                    "words": [
                        {"word": "Hello", "start": 0.27, "end": 0.61, "score": 0.862},
                        {"word": "world.", "start": 0.69, "end": 1.091, "score": 0.779},
                    ],
                },
            ...
            "words_segments": [
            {
                "start": 0.27,
                "end": 1.632,
                "text": " Hello"
            }
         ]
        }
    }
    """
    jobId = send_async_request_runpod_subtitler(
        base64_string=base64_string, RUNPOD_API_KEY=RUNPOD_API_KEY
    )
    outputResponse = get_runpod_job_status_from_id(jobId, RUNPOD_API_KEY=RUNPOD_API_KEY)
    jobStatus = outputResponse["status"]  # Will be either "IN_PROGRESS" or "COMPLETED"
    # Keep checking every minute until the job is completed
    while jobStatus == "IN_PROGRESS" or jobStatus == "IN_QUEUE":
        time.sleep(60)  # Wait for 1 minute
        outputResponse = get_runpod_job_status_from_id(
            jobId, RUNPOD_API_KEY=RUNPOD_API_KEY
        )
        print("Current output Response: ", outputResponse)
        jobStatus = outputResponse["status"]
    outputResponse = outputResponse["output"]
    return outputResponse


def send_async_request_runpod_subtitler(base64_string, RUNPOD_API_KEY):
    """
    Sends an async request to Runpod and returns the job id.

    @param
    base64_string: The base64 string of the audio file
    RUNPOD_API_KEY: The API key for Runpod

    @return
    jobId: The job id of the request
    """
    url = f"https://api.runpod.ai/v2/{SERVER_ENDPOINT}/run"

    payload = json.dumps({"input": {"audio_base_64": base64_string}})
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + RUNPOD_API_KEY,
    }

    response = requests.post(url, headers=headers, data=payload).json()
    return response["id"]


def get_runpod_job_status_from_id(id, RUNPOD_API_KEY):
    """
    Grabs a job status from Runpod using the job id.

    @param
    id: The job id of the request
    RUNPOD_API_KEY: The API key for Runpod

    @return
    outputResponse: The response from Runpod. Structured as:
    {
        "status": "COMPLETED",
        "output": [{...}...]
    }
    Or if the job is still in progress/in Queue:
    {
        "status": "IN_PROGRESS" / "IN_QUEUE
    }
    """
    url = f"https://api.runpod.ai/v2/{SERVER_ENDPOINT}/status/{id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + RUNPOD_API_KEY,
        "Cookie": "__cflb=02DiuEDmJ1gNRaog7Bucmr44gWmZj9b8Tittd5EhmroXS",
    }

    response = requests.get(url, headers=headers).json()
    print("Response from Runpod: ", response)

    if response["status"] == "IN_PROGRESS" or response["status"] == "IN_QUEUE":
        return {"status": response["status"]}
    else:
        return {
            "status": "COMPLETED",
            "output": response["output"],
        }

    return response


def send_synchronous_request_runpod_subtitler(
    base64_string: str, RUNPOD_API_KEY: str, mock: bool = False
) -> SubtitlerResponse:
    """
    Sends a synchronous request to Runpod and returns the response. Can potentially time out if the Runpod server takes too long.

    @param
    base64_string: The base64 string of the audio file
    RUNPOD_API_KEY: The API key for Runpod
    mock: If true, returns a mock response

    @return
    outputResponse: The response from Runpod. Structured as:
    {
        "segments": [
            {
                "start": 0.27,
                "end": 1.632,
                "text": " Hello world.",
                "words": [
                    {"word": "Hello", "start": 0.27, "end": 0.61, "score": 0.862},
                    {"word": "world.", "start": 0.69, "end": 1.091, "score": 0.779},
                ],
            },
        ...
        "words_segments": [
        {
            "start": 0.27,
            "end": 1.632,
            "text": " Hello"
        }
        ]
    }
    """
    if mock == True:
        return {
            "segments": [
                {
                    "start": 0.27,
                    "end": 1.632,
                    "text": " Hello world.",
                    "words": [
                        {"word": "Hello", "start": 0.27, "end": 0.61, "score": 0.862},
                        {"word": "world.", "start": 0.69, "end": 1.091, "score": 0.779},
                    ],
                },
                {
                    "start": 1.632,
                    "end": 3.055,
                    "text": "Nice to meet you.",
                    "words": [
                        {"word": "Nice", "start": 1.632, "end": 1.913, "score": 0.868},
                        {"word": "to", "start": 1.953, "end": 2.033, "score": 0.832},
                        {"word": "meet", "start": 2.093, "end": 2.274, "score": 0.788},
                        {"word": "you.", "start": 2.294, "end": 2.454, "score": 0.849},
                    ],
                },
                {
                    "start": 3.055,
                    "end": 5.1,
                    "text": "My name is John Doe.",
                    "words": [
                        {"word": "My", "start": 3.055, "end": 3.216, "score": 0.996},
                        {"word": "name", "start": 3.276, "end": 3.476, "score": 0.979},
                        {"word": "is", "start": 3.556, "end": 3.637, "score": 0.63},
                        {"word": "John", "start": 3.737, "end": 4.017, "score": 0.684},
                        {"word": "Doe.", "start": 4.057, "end": 4.358, "score": 0.531},
                    ],
                },
                {
                    "start": 5.1,
                    "end": 6.803,
                    "text": "Here's a funny story about a dog.",
                    "words": [
                        {"word": "Here's", "start": 5.1, "end": 5.4, "score": 0.619},
                        {"word": "a", "start": 5.44, "end": 5.46, "score": 0.999},
                        {"word": "funny", "start": 5.52, "end": 5.781, "score": 0.812},
                        {"word": "story", "start": 5.841, "end": 6.162, "score": 0.789},
                        {"word": "about", "start": 6.222, "end": 6.422, "score": 0.901},
                        {"word": "a", "start": 6.462, "end": 6.482, "score": 0.999},
                        {"word": "dog.", "start": 6.523, "end": 6.803, "score": 0.993},
                    ],
                },
            ]
        }

    url = f"https://api.runpod.ai/v2/{SERVER_ENDPOINT}/runsync"

    payload = json.dumps({"input": {"audio_base_64": base64_string}})
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + RUNPOD_API_KEY,
    }

    response = requests.post(url, headers=headers, data=payload).json()
    print("Response from Runpod: ", response)
    output = response["output"]
    if output == None or output == []:
        raise Exception("No output from Runpod")

    return output
```

## License

This project is licensed under the [MIT License](LICENSE).

## Troubleshooting WebSocket Connections

When deploying a chat interface alongside this server, ensure that your frontend
WebSocket URL points to the public backend host and not to `localhost`. A common
error message is `ERR_CONNECTION_REFUSED` when the code tries to connect to
`ws://localhost:8000` even though the backend runs on a different machine. Set
the appropriate environment variable (for example `VITE_WS_URL` or
`REACT_APP_WS_URL`) to the fully qualified domain of your deployment such as
`wss://your-domain.example/chat/ws`. This will allow the chat interface to
establish the WebSocket connection correctly.

