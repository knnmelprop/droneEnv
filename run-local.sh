#!/bin/bash

# SUAVE Local Development Container Runner
# This script builds and runs the SUAVE development environment locally

set -euo pipefail

echo "🚀 Setting up SUAVE Local Development Environment"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose > /dev/null 2>&1; then
    echo "❌ docker-compose is not installed. Please install it and try again."
    exit 1
fi

echo "📦 Building container..."
docker-compose build

echo "🔧 Starting container..."
docker-compose up -d

echo "⏳ Waiting for container to be ready..."
sleep 3

echo "🔍 Running SUAVE installation and verification..."
docker-compose exec suave-dev bash -c "
    set -euo pipefail
    echo 'Installing Git LFS...'
    git lfs install --force
    
    echo 'Installing SUAVE in development mode...'
    cd trunk
    python3.9 setup.py develop
    
    echo 'Verifying installation...'
    python3.9 -c \"
        import SUAVE
        import numpy, scipy, matplotlib, sklearn, plotly
        print('✅ SUAVE and all dependencies imported successfully!')
        print(f'SUAVE version: {SUAVE.__version__ if hasattr(SUAVE, \"__version__\") else \"Unknown\"}')
    \"
    
    echo 'Running student competition analysis...'
    cd /workspaces
    python3.9 student_competition/droniada_sztafeta/main.py
"

echo ""
echo "✅ SUAVE Local Environment is Ready!"
echo "====================================="
echo ""
echo "To access the container:"
echo "  docker-compose exec suave-dev bash"
echo ""
echo "To run the analysis again:"
echo "  docker-compose exec suave-dev python3.9 student_competition/droniada_sztafeta/main.py"
echo ""
echo "To stop the container:"
echo "  docker-compose down"
echo ""
echo "To view logs:"
echo "  docker-compose logs suave-dev"
