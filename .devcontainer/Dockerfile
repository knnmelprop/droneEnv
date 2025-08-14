FROM mcr.microsoft.com/devcontainers/python:3.9

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

ARG INSTALL_EXTERNAL_TOOLS=false
ARG SU2_DOWNLOAD_URL=""
ARG SU2_SHA256=""
ARG AVL_DOWNLOAD_URL=""

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git-lfs \
    gfortran \
    gcc \
    g++ \
    make \
    liblapack-dev \
    libopenblas-dev \
    libopenmpi-dev \
    openmpi-bin \
    libx11-dev \
    curl \
    tree \
    tini \
    unzip \
    && rm -rf /var/lib/apt/lists/* && apt-get clean

# Upgrade pip toolchain and install Python dependencies globally
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install -r /tmp/requirements.txt

# Optional SU2
RUN set -eux; \
    if [ -n "$SU2_DOWNLOAD_URL" ]; then \
      mkdir -p /opt/su2 && cd /opt/su2; \
      curl -fsSL "$SU2_DOWNLOAD_URL" -o su2.zip; \
      if [ -n "$SU2_SHA256" ]; then echo "$SU2_SHA256  su2.zip" | sha256sum -c -; fi; \
      unzip -q su2.zip; \
      rm -f su2.zip; \
      if [ -d /opt/su2/bin ]; then ln -sf /opt/su2/bin/SU2_CFD /usr/local/bin/SU2_CFD || true; fi; \
    fi

# Optional AVL
RUN set -eux; \
    if [ -n "$AVL_DOWNLOAD_URL" ]; then \
      case "$AVL_DOWNLOAD_URL" in \
        *.tgz|*.tar.gz) \
          mkdir -p /opt/avl-src && cd /opt/avl-src; \
          curl -fsSL "$AVL_DOWNLOAD_URL" -o avl.tgz; \
          topdir=$(tar -tzf avl.tgz | head -1 | cut -f1 -d/); \
          tar -xzf avl.tgz; \
          rm -f avl.tgz; \
          cd "$topdir"; \
          make; \
          install -m 0755 avl /usr/local/bin/avl; \
          ;; \
        *) \
          curl -fsSL "$AVL_DOWNLOAD_URL" -o /usr/local/bin/avl; \
          chmod +x /usr/local/bin/avl; \
          ;; \
      esac; \
    fi

# Set up workspace
WORKDIR /workspaces

ENV SU2_HOME="/opt/su2" \
    SU2_RUN="/opt/su2/bin" \
    SU2_BIN="/opt/su2/bin/SU2_CFD" \
    AVL_BIN="/usr/local/bin/avl" \
    PATH="/opt/su2/bin:${PATH}"

EXPOSE 8888 3000 7860