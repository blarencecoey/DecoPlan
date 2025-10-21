#!/bin/bash

# Quick build script for DecoPlan LLM

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=================================${NC}"
echo -e "${BLUE}DecoPlan LLM Build Script${NC}"
echo -e "${BLUE}=================================${NC}"
echo ""

# Parse arguments
USE_CUDA=ON
BUILD_TYPE=Release
CLEAN_BUILD=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --no-cuda)
            USE_CUDA=OFF
            shift
            ;;
        --debug)
            BUILD_TYPE=Debug
            shift
            ;;
        --clean)
            CLEAN_BUILD=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--no-cuda] [--debug] [--clean]"
            exit 1
            ;;
    esac
done

# Clean build directory if requested
if [ "$CLEAN_BUILD" = true ]; then
    echo -e "${BLUE}Cleaning build directory...${NC}"
    rm -rf build
fi

# Create build directory
mkdir -p build
cd build

# Configure
echo -e "${BLUE}Configuring CMake...${NC}"
echo "  CUDA Support: $USE_CUDA"
echo "  Build Type: $BUILD_TYPE"
echo ""

# Enable CUDA language only if CUDA is requested
if [ "$USE_CUDA" = "ON" ]; then
    cmake .. \
        -DCMAKE_BUILD_TYPE=$BUILD_TYPE \
        -DDECOPLAN_USE_CUDA=ON \
        -DDECOPLAN_BUILD_EXAMPLES=ON \
        -DGGML_CUDA=ON
else
    cmake .. \
        -DCMAKE_BUILD_TYPE=$BUILD_TYPE \
        -DDECOPLAN_USE_CUDA=OFF \
        -DDECOPLAN_BUILD_EXAMPLES=ON \
        -DGGML_CUDA=OFF
fi

# Build
echo ""
echo -e "${BLUE}Building...${NC}"

# Detect number of cores
if [[ "$OSTYPE" == "darwin"* ]]; then
    CORES=$(sysctl -n hw.ncpu)
else
    CORES=$(nproc)
fi

cmake --build . -j$CORES

# Check build status
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}=================================${NC}"
    echo -e "${GREEN}Build successful!${NC}"
    echo -e "${GREEN}=================================${NC}"
    echo ""
    echo "Built executables:"
    ls -lh simple_inference multimodal_inference 2>/dev/null || ls -lh *.exe 2>/dev/null
    echo ""
    echo "Next steps:"
    echo "  1. Download a model:"
    echo "     python ../scripts/download_model.py llava-1.6-mistral-7b"
    echo ""
    echo "  2. Run inference:"
    echo "     ./multimodal_inference ../models/llava-v1.6-mistral-7b.Q4_K_M.gguf image.jpg \"your prompt\""
    echo ""
else
    echo ""
    echo -e "${RED}Build failed!${NC}"
    exit 1
fi
