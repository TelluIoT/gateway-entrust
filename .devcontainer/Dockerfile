# Use a 64-bit base image compatible with ARMv8 (64-bit architecture)
FROM arm64v8/ubuntu:22.04

# Set the working directory
WORKDIR /workspace

# # Install basic dependencies (you can add more as needed)
RUN apt-get update && apt-get install -y \
    sudo \
    curl \
    wget \
    git \
    build-essential \
    libx11-xcb1 \
    libsecret-1-dev \
    libxss1 \
    libnss3 \
    libgbm1 \
    libgtk-3-0 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]

# Expose necessary ports (if applicable)
# EXPOSE 8000

# Default command
CMD ["bash"]