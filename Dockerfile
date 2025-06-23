FROM runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04

# ──────────────────────────
# Basic setup
# ──────────────────────────
WORKDIR /app

ARG WHISPER_MODEL=small
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
# App code
# ──────────────────────────
COPY .env.example .env
COPY handler.py ./
COPY payloads/ ./payloads/

STOPSIGNAL SIGINT
CMD ["python", "-u", "handler.py"]
