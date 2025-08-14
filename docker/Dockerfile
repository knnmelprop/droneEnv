# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-slim AS base

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    MPLBACKEND=Agg

# Common OS deps (runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    git \
    git-lfs \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    curl \
    tini \
    # optional runtime deps for SU2 (serial usage)
    libopenmpi-dev \
    openmpi-bin \
    && rm -rf /var/lib/apt/lists/* && apt-get clean

# Optional external tools install flag
ARG INSTALL_EXTERNAL_TOOLS=false

# Optional third-party tools
ARG SU2_DOWNLOAD_URL=""
ARG AVL_DOWNLOAD_URL=""

# Separate stage to optionally install external tools (gmsh available via apt; others via URLs)
FROM base AS tools
RUN if [ "$INSTALL_EXTERNAL_TOOLS" = "true" ]; then \
      apt-get update && apt-get install -y --no-install-recommends gmsh && \
      rm -rf /var/lib/apt/lists/* && apt-get clean; \
    fi

# Install SU2 if URL provided
RUN set -eux; \
    if [ -n "$SU2_DOWNLOAD_URL" ]; then \
      mkdir -p /opt/su2 && cd /opt/su2; \
      curl -fsSL "$SU2_DOWNLOAD_URL" -o su2.tar.gz; \
      tar -xzf su2.tar.gz --strip-components=1; \
      rm -f su2.tar.gz; \
      if [ -d /opt/su2/bin ]; then ln -sf /opt/su2/bin/SU2_CFD /usr/local/bin/SU2_CFD || true; fi; \
    fi

# Install AVL if URL provided (expects a single executable named avl or similar)
RUN set -eux; \
    if [ -n "$AVL_DOWNLOAD_URL" ]; then \
      curl -fsSL "$AVL_DOWNLOAD_URL" -o /usr/local/bin/avl; \
      chmod +x /usr/local/bin/avl; \
    fi

# Final image
FROM base AS final

# Copy tools from tools stage if built
COPY --from=tools /usr/bin/gmsh /usr/bin/gmsh
COPY --from=tools /usr/lib /usr/lib
COPY --from=tools /opt/su2 /opt/su2
COPY --from=tools /usr/local/bin/avl /usr/local/bin/avl

# Create non-root user
ARG USERNAME=suave
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd --gid ${USER_GID} ${USERNAME} && \
    useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME}

WORKDIR /workspace

# Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install -r /tmp/requirements.txt

# Entrypoint and scripts
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Environment variables for external tools (can be overridden)
ENV AVL_BIN="/usr/local/bin/avl" \
    SU2_HOME="/opt/su2" \
    SU2_RUN="/opt/su2/bin" \
    SU2_BIN="/opt/su2/bin/SU2_CFD" \
    OPENVSP_BIN="" \
    GMSH_BIN="/usr/bin/gmsh" \
    JUPYTER_TOKEN="" \
    PYTHONPATH="/workspace/trunk:/workspace/student_competition" \
    PATH="/opt/su2/bin:${PATH}"

EXPOSE 8888

# Use Tini as init to handle zombies/signals
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/entrypoint.sh"]

# Default command starts Jupyter Lab; override with `bash` or `python` as needed
CMD ["jupyter"]