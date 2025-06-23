FROM runpod/pytorch:2.8.0-py3.11-cuda12.8.1-cudnn-devel-ubuntu22.04

# Set Work Directory
WORKDIR /app

# Need to redeclare it due to multi-stage build process
ARG WHISPER_MODEL=small
ARG LANG=en
ARG TORCH_HOME=/cache/torch
ARG HF_HOME=/cache/huggingface

# Environment variables
ENV TORCH_HOME=${TORCH_HOME}
ENV HF_HOME=${HF_HOME}
ENV WHISPER_MODEL=${WHISPER_MODEL}
ENV LANG=${LANG}
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/aarch64-linux-gnu/
ENV DEBIAN_FRONTEND=noninteractive

# Set Locale
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen

# Install Python dependencies, setuptools-rust, PyTorch, and download WhisperX
# Copy and install requirements
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg
    
# --- make CuDNN visible to the linker --------------------------------
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
RUN ln -sf /usr/lib/x86_64-linux-gnu/libcudnn_ops_infer.so.8 \
           /usr/local/cuda/lib64/libcudnn_ops_infer.so.8
# ---------------------------------------------------------------------

# ---- install CuDNN runtime & dev libs (brings in libcudnn_ops_infer.so.8) ----
RUN apt-get update && DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
        libcudnn8=8.9.7.* \
        libcudnn8-dev=8.9.7.*

# COPY the example.mp3 file to the container as a default testing audio file
COPY example.mp3 /app/example.mp3
COPY handler.py /app/handler.py

STOPSIGNAL SIGINT
CMD ["python", "-u", "handler.py"]
