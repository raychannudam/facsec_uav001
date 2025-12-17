# Use a base Ubuntu image (ARM64 compatible)
FROM ubuntu:22.04

# Install dependencies and ffmpeg
RUN apt-get update && \
    apt-get install -y curl ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Download and install MediaMTX ARM64
RUN curl -L -o /tmp/mediamtx.tar.gz https://github.com/bluenviron/mediamtx/releases/download/v1.15.5/mediamtx_v1.15.5_linux_amd64.tar.gz && \
    tar -xzf /tmp/mediamtx.tar.gz -C /tmp && \
    mv /tmp/mediamtx /usr/local/bin/mediamtx && \
    chmod +x /usr/local/bin/mediamtx && \
    rm -rf /tmp/mediamtx /tmp/mediamtx.tar.gz


# Copy your MediaMTX config
COPY mediamtx.yml /config/mediamtx.yml

# Set working directory
WORKDIR /config

# Run MediaMTX
CMD ["mediamtx", "/config/mediamtx.yml"]
