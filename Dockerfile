FROM runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04

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
    LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH \
    TRANSFORMERS_NO_TORCHVISION_IMPORTS=1

# ──────────────────────────
# Locale (optional)
# ──────────────────────────
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen

# ──────────────────────────
# Python dependencies
# ──────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y -qq torchvision || true

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
RUN python - <<'PY'
import sys, types
from importlib.machinery import ModuleSpec

# Stub out torchvision to satisfy all dependencies (transformers, torchmetrics)
print("Creating a fake torchvision package to bypass import checks...")

# --- Create the fake package and submodules ---
torchvision_pkg = types.ModuleType('torchvision', 'Fake torchvision package')
torchvision_pkg.__path__ = [] # Essential for a package

models_mod = types.ModuleType('torchvision.models')
class _resnet50: pass
class _VGG16_Weights: pass
def _vgg16(): pass
models_mod.resnet50 = _resnet50
models_mod.VGG16_Weights = _VGG16_Weights
models_mod.vgg16 = _vgg16

transforms_mod = types.ModuleType('torchvision.transforms')
class _InterpolationMode: pass
transforms_mod.InterpolationMode = _InterpolationMode

torchvision_pkg.models = models_mod
torchvision_pkg.transforms = transforms_mod

# --- Inject all modules into sys.modules ---
sys.modules['torchvision'] = torchvision_pkg
sys.modules['torchvision.models'] = models_mod
sys.modules['torchvision.transforms'] = transforms_mod

# --- Add __spec__ to satisfy modern import machinery ---
try:
    torchvision_pkg.__spec__ = ModuleSpec(name='torchvision', loader=None, is_package=True)
    models_mod.__spec__ = ModuleSpec(name='torchvision.models', loader=None)
    transforms_mod.__spec__ = ModuleSpec(name='torchvision.transforms', loader=None)
except Exception:
    pass # For older python versions

print("Fake torchvision package created and injected.")

import whisperx
print('Downloading large-v3 model...')
model = whisperx.load_model('large-v3', 'cpu', compute_type='int8')
del model
print('Downloading English alignment model...')
align_model, metadata = whisperx.load_align_model('en', 'cpu')
del align_model
print('Models downloaded successfully!')
PY
RUN ls -la /cache/

# ──────────────────────────
# App code
# ──────────────────────────
COPY .env.example .env
COPY handler.py ./
COPY payloads/ ./payloads/

STOPSIGNAL SIGINT
CMD ["python", "-u", "handler.py"]
