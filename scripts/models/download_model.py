#!/usr/bin/env python3
"""
Python script to download GGUF models from Hugging Face.
Requires: pip install huggingface-hub
"""

import argparse
import os
from pathlib import Path

try:
    from huggingface_hub import hf_hub_download
except ImportError:
    print("Error: huggingface-hub not installed")
    print("Please install: pip install huggingface-hub")
    exit(1)

MODELS_CONFIG = {
    "llava-1.6-mistral-7b": {
        "repo": "cjpais/llava-1.6-mistral-7b-gguf",
        "files": [
            "llava-v1.6-mistral-7b.{quant}.gguf",
            "mmproj-model-f16.gguf"
        ],
        "description": "LLaVA 1.6 Mistral 7B - Good balance of quality and speed"
    },
    "llava-1.6-34b": {
        "repo": "cjpais/llava-v1.6-34B-gguf",
        "files": [
            "llava-v1.6-34b.{quant}.gguf",
            "mmproj-model-f16.gguf"
        ],
        "description": "LLaVA 1.6 34B - Best quality, requires 16GB+ VRAM"
    },
    "qwen2-vl-7b": {
        "repo": "Qwen/Qwen2-VL-7B-Instruct-GGUF",
        "files": [
            "qwen2-vl-7b-instruct-{quant}.gguf"
        ],
        "description": "Qwen2-VL 7B - Alternative vision model"
    }
}

QUANTIZATIONS = ["Q4_K_M", "Q5_K_M", "Q6_K", "Q8_0"]

def download_model(model_name: str, quant: str, models_dir: str):
    """Download a model and its associated files."""

    if model_name not in MODELS_CONFIG:
        print(f"Error: Unknown model '{model_name}'")
        print("\nAvailable models:")
        for name, config in MODELS_CONFIG.items():
            print(f"  {name:25s} - {config['description']}")
        return False

    config = MODELS_CONFIG[model_name]
    models_path = Path(models_dir)
    models_path.mkdir(parents=True, exist_ok=True)

    print("=" * 50)
    print("DecoPlan Model Downloader")
    print("=" * 50)
    print(f"Model: {model_name}")
    print(f"Quantization: {quant}")
    print(f"Repository: {config['repo']}")
    print(f"Output directory: {models_path.absolute()}")
    print()

    for file_template in config['files']:
        filename = file_template.format(quant=quant)

        print(f"Downloading {filename}...")

        try:
            downloaded_path = hf_hub_download(
                repo_id=config['repo'],
                filename=filename,
                local_dir=models_dir,
                local_dir_use_symlinks=False
            )

            # Get file size
            size_mb = os.path.getsize(downloaded_path) / (1024 * 1024)
            print(f"  ✓ Downloaded: {downloaded_path} ({size_mb:.1f} MB)")

        except Exception as e:
            print(f"  ✗ Error downloading {filename}: {e}")
            return False

    print()
    print("=" * 50)
    print("Download complete!")
    print("=" * 50)
    print()
    print("Downloaded files:")
    for file in sorted(models_path.glob("*")):
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"  {file.name} ({size_mb:.1f} MB)")

    print()
    print("To use this model, run:")
    print(f"  ./build/multimodal_inference {models_path}/<model-file> <image-path> \"your prompt\"")

    return True

def main():
    parser = argparse.ArgumentParser(
        description="Download GGUF models for DecoPlan LLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available models:
  llava-1.6-mistral-7b  - LLaVA 1.6 Mistral 7B (recommended)
  llava-1.6-34b         - LLaVA 1.6 34B (best quality)
  qwen2-vl-7b           - Qwen2-VL 7B (alternative)

Quantization options: Q4_K_M (default), Q5_K_M, Q6_K, Q8_0
  Q4_K_M: ~6-8GB VRAM, good quality
  Q5_K_M: ~8-10GB VRAM, better quality
  Q6_K:   ~10-12GB VRAM, high quality
  Q8_0:   ~12-16GB VRAM, highest quality

Examples:
  python download_model.py llava-1.6-mistral-7b
  python download_model.py llava-1.6-34b --quant Q5_K_M
  python download_model.py qwen2-vl-7b --models-dir /path/to/models
        """
    )

    parser.add_argument(
        "model",
        choices=list(MODELS_CONFIG.keys()),
        help="Model to download"
    )

    parser.add_argument(
        "--quant", "-q",
        default="Q4_K_M",
        choices=QUANTIZATIONS,
        help="Quantization level (default: Q4_K_M)"
    )

    parser.add_argument(
        "--models-dir", "-d",
        default="models",
        help="Directory to save models (default: models)"
    )

    args = parser.parse_args()

    success = download_model(args.model, args.quant, args.models_dir)
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
