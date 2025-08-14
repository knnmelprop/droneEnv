FROM mcr.microsoft.com/devcontainers/python:3.9

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

ARG INSTALL_EXTERNAL_TOOLS=false
ARG SU2_DOWNLOAD_URL=""
ARG AVL_DOWNLOAD_URL=""

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git-lfs \
    gfortran \
    liblapack-dev \
    libopenblas-dev \
    libopenmpi-dev \
    openmpi-bin \
    curl \
    tree \
    tini \
    && rm -rf /var/lib/apt/lists/* && apt-get clean

# Upgrade pip toolchain and install Python dependencies globally
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install -r /tmp/requirements.txt

# Optional SU2
RUN set -eux; \
    if [ -n "$SU2_DOWNLOAD_URL" ]; then \
      mkdir -p /opt/su2 && cd /opt/su2; \
      curl -fsSL "$SU2_DOWNLOAD_URL" -o su2.tar.gz; \
      tar -xzf su2.tar.gz --strip-components=1; \
      rm -f su2.tar.gz; \
      if [ -d /opt/su2/bin ]; then ln -sf /opt/su2/bin/SU2_CFD /usr/local/bin/SU2_CFD || true; fi; \
    fi

# Optional AVL
RUN set -eux; \
    if [ -n "$AVL_DOWNLOAD_URL" ]; then \
      curl -fsSL "$AVL_DOWNLOAD_URL" -o /usr/local/bin/avl; \
      chmod +x /usr/local/bin/avl; \
    fi

# Set up workspace
WORKDIR /workspaces

ENV SU2_HOME="/opt/su2" \
    SU2_RUN="/opt/su2/bin" \
    SU2_BIN="/opt/su2/bin/SU2_CFD" \
    AVL_BIN="/usr/local/bin/avl" \
    PATH="/opt/su2/bin:${PATH}"

EXPOSE 8888 3000 7860