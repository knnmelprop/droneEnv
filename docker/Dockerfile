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
    && rm -rf /var/lib/apt/lists/* && apt-get clean

# Optional external tools install flag
ARG INSTALL_EXTERNAL_TOOLS=false

# Separate stage to optionally install external tools (gmsh available via apt; others left configurable)
FROM base AS tools
RUN if [ "$INSTALL_EXTERNAL_TOOLS" = "true" ]; then \
      apt-get update && apt-get install -y --no-install-recommends gmsh && \
      rm -rf /var/lib/apt/lists/* && apt-get clean; \
    fi

# Final image
FROM base AS final

# Copy tools from tools stage if built
COPY --from=tools /usr/bin/gmsh /usr/bin/gmsh
COPY --from=tools /usr/lib /usr/lib

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
ENV AVL_BIN="" \
    SU2_BIN="" \
    OPENVSP_BIN="" \
    GMSH_BIN="/usr/bin/gmsh" \
    JUPYTER_TOKEN="" \
    PYTHONPATH="/workspace/trunk:/workspace/student_competition"

EXPOSE 8888

# Use Tini as init to handle zombies/signals
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/entrypoint.sh"]

# Default command starts Jupyter Lab; override with `bash` or `python` as needed
CMD ["jupyter"]