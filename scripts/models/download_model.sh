#!/bin/bash

# Script to download GGUF models from Hugging Face
# Usage: ./download_model.sh <model_name> [quantization]

set -e

MODEL_NAME=${1:-"llava-v1.6-mistral-7b"}
QUANT=${2:-"Q4_K_M"}
MODELS_DIR="models"

# Create models directory if it doesn't exist
mkdir -p "$MODELS_DIR"

echo "================================="
echo "DecoPlan Model Downloader"
echo "================================="
echo "Model: $MODEL_NAME"
echo "Quantization: $QUANT"
echo "Directory: $MODELS_DIR"
echo ""

# Function to download from Hugging Face
download_from_hf() {
    local repo=$1
    local filename=$2
    local output_path=$3

    echo "Downloading $filename from $repo..."

    if command -v huggingface-cli &> /dev/null; then
        # Use huggingface-cli if available
        huggingface-cli download "$repo" "$filename" --local-dir "$MODELS_DIR" --local-dir-use-symlinks False
    elif command -v wget &> /dev/null; then
        # Fallback to wget
        wget -O "$output_path" "https://huggingface.co/$repo/resolve/main/$filename"
    else
        echo "Error: Neither huggingface-cli nor wget found."
        echo "Please install huggingface-cli: pip install huggingface-hub[cli]"
        exit 1
    fi
}

# Download based on model name
case "$MODEL_NAME" in
    "llava-1.6-mistral-7b"|"llava-mistral")
        echo "Downloading LLaVA 1.6 Mistral 7B..."
        download_from_hf \
            "cjpais/llava-1.6-mistral-7b-gguf" \
            "llava-v1.6-mistral-7b.${QUANT}.gguf" \
            "$MODELS_DIR/llava-v1.6-mistral-7b.${QUANT}.gguf"

        # Download mmproj file for vision
        echo "Downloading vision encoder (mmproj)..."
        download_from_hf \
            "cjpais/llava-1.6-mistral-7b-gguf" \
            "mmproj-model-f16.gguf" \
            "$MODELS_DIR/mmproj-mistral-f16.gguf"
        ;;

    "llava-1.6-34b"|"llava-34b")
        echo "Downloading LLaVA 1.6 34B..."
        download_from_hf \
            "cjpais/llava-v1.6-34B-gguf" \
            "llava-v1.6-34b.${QUANT}.gguf" \
            "$MODELS_DIR/llava-v1.6-34b.${QUANT}.gguf"

        echo "Downloading vision encoder (mmproj)..."
        download_from_hf \
            "cjpais/llava-v1.6-34B-gguf" \
            "mmproj-model-f16.gguf" \
            "$MODELS_DIR/mmproj-34b-f16.gguf"
        ;;

    "qwen2-vl-7b")
        echo "Downloading Qwen2-VL 7B..."
        download_from_hf \
            "Qwen/Qwen2-VL-7B-Instruct-GGUF" \
            "qwen2-vl-7b-instruct-${QUANT}.gguf" \
            "$MODELS_DIR/qwen2-vl-7b-instruct-${QUANT}.gguf"
        ;;

    "llama-3.2-11b-vision")
        echo "Downloading Llama 3.2 11B Vision..."
        download_from_hf \
            "meta-llama/Llama-3.2-11B-Vision-Instruct-GGUF" \
            "Llama-3.2-11B-Vision-Instruct-${QUANT}.gguf" \
            "$MODELS_DIR/llama-3.2-11b-vision-${QUANT}.gguf"
        ;;

    *)
        echo "Unknown model: $MODEL_NAME"
        echo ""
        echo "Available models:"
        echo "  llava-1.6-mistral-7b  - LLaVA 1.6 Mistral 7B (recommended for starting)"
        echo "  llava-1.6-34b         - LLaVA 1.6 34B (best quality, needs 16GB+ VRAM)"
        echo "  qwen2-vl-7b           - Qwen2-VL 7B (alternative vision model)"
        echo "  llama-3.2-11b-vision  - Llama 3.2 11B Vision"
        echo ""
        echo "Available quantizations: Q4_K_M, Q5_K_M, Q6_K, Q8_0"
        exit 1
        ;;
esac

echo ""
echo "================================="
echo "Download complete!"
echo "================================="
echo ""
echo "Model files saved to: $MODELS_DIR/"
ls -lh "$MODELS_DIR/"
echo ""
echo "To use this model, run:"
echo "  ./build/multimodal_inference $MODELS_DIR/<model-file> <image-path> \"your prompt\""
