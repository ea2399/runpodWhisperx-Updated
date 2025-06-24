FROM runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04

# ──────────────────────────
# Basic setup
# ──────────────────────────
WORKDIR /app

ARG WHISPER_MODEL=large-v3
ARG LANG=en
ARG TORCH_HOME=/cache/torch
ARG HF_HOME=/cache/huggingface

ENV TORCH_HOME=${TORCH_HOME} \
    HF_HOME=${HF_HOME} \
    WHISPER_MODEL=${WHISPER_MODEL} \
    LANG=${LANG} \
    DEBIAN_FRONTEND=noninteractive \
    # keep CUDA libs in search path
    LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# ──────────────────────────
# Locale (optional)
# ──────────────────────────
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen

# ──────────────────────────
# Python dependencies
# ──────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ──────────────────────────
# System packages
#   – ffmpeg for audio
#   – libcudnn8 + dev headers (ensures libcudnn_ops_infer.so.8 exists)
# ──────────────────────────
RUN apt-get update && \
    apt-get install -y \
        ffmpeg \
        libcudnn8=8.9.7.* \
        libcudnn8-dev=8.9.7.* && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ──────────────────────────
# Create cache directories
# ──────────────────────────
RUN mkdir -p ${TORCH_HOME} ${HF_HOME} && \
    chmod -R 777 /cache

# ──────────────────────────
# Pre-download WhisperX models during build
# This eliminates runtime downloads and disk space issues
# ──────────────────────────
RUN echo "Starting model pre-download..." && \
    python -c "import whisperx; import os; print('Downloading large-v3 model...'); model = whisperx.load_model('large-v3', 'cpu', compute_type='int8'); del model; print('Downloading large-v2 model...'); model = whisperx.load_model('large-v2', 'cpu', compute_type='int8'); del model; print('Downloading medium model...'); model = whisperx.load_model('medium', 'cpu', compute_type='int8'); del model; print('Downloading alignment models...'); align_model, metadata = whisperx.load_align_model('en', 'cpu'); del align_model; align_model, metadata = whisperx.load_align_model('fr', 'cpu'); del align_model; align_model, metadata = whisperx.load_align_model('de', 'cpu'); del align_model; print('All models downloaded successfully!')" && \
    echo "Model pre-download completed successfully!" && \
    ls -la /cache/

# ──────────────────────────
# App code
# ──────────────────────────
COPY .env.example .env
COPY handler.py ./
COPY payloads/ ./payloads/

STOPSIGNAL SIGINT
CMD ["python", "-u", "handler.py"]
