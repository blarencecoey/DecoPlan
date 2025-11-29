#!/usr/bin/env python3
"""
Test script for trained LoRA model.
Loads the fine-tuned model and runs inference.
"""

import torch
from transformers import AutoTokenizer, AutoModelForVision2Seq
from peft import PeftModel
from PIL import Image
import argparse


def load_model(base_model_name, lora_weights_path):
    """Load base model and apply LoRA weights."""
    print(f"Loading base model: {base_model_name}")

    # Load base model
    model = AutoModelForVision2Seq.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
    )

    print(f"Loading LoRA weights from: {lora_weights_path}")
    # Load LoRA weights
    model = PeftModel.from_pretrained(
        model, lora_weights_path, torch_dtype=torch.float16
    )

    # Merge LoRA weights into base model (optional, for faster inference)
    model = model.merge_and_unload()

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)

    print("✓ Model loaded successfully!")
    return model, tokenizer


def generate_response(model, tokenizer, prompt, image_path=None, max_new_tokens=256):
    """Generate a response from the model."""

    # Prepare inputs
    if image_path:
        # For vision-language models with images
        from transformers import AutoProcessor

        processor = AutoProcessor.from_pretrained(model.config._name_or_path)

        image = Image.open(image_path).convert("RGB")
        inputs = processor(text=prompt, images=image, return_tensors="pt")
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
    else:
        # Text-only
        inputs = tokenizer(prompt, return_tensors="pt")
        inputs = {k: v.to(model.device) for k, v in inputs.items()}

    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    # Decode
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Remove the prompt from response
    if response.startswith(prompt):
        response = response[len(prompt) :].strip()

    return response


def main():
    parser = argparse.ArgumentParser(description="Test trained LoRA model")
    parser.add_argument(
        "--base_model",
        type=str,
        default="llava-hf/llava-1.5-7b-hf",
        help="Base model name",
    )
    parser.add_argument(
        "--lora_weights",
        type=str,
        default="models/lora_checkpoints/final_model",
        help="Path to LoRA weights",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="What is the capital of France?",
        help="Test prompt",
    )
    parser.add_argument(
        "--image", type=str, default=None, help="Path to image (for vision models)"
    )
    parser.add_argument(
        "--max_tokens", type=int, default=256, help="Maximum tokens to generate"
    )

    args = parser.parse_args()

    print("=" * 80)
    print("LoRA Model Testing")
    print("=" * 80)

    # Load model
    model, tokenizer = load_model(args.base_model, args.lora_weights)

    # Generate response
    print(f"\nPrompt: {args.prompt}")
    if args.image:
        print(f"Image: {args.image}")
    print("\nGenerating response...\n")

    response = generate_response(
        model, tokenizer, args.prompt, args.image, args.max_tokens
    )

    print("=" * 80)
    print("RESPONSE:")
    print("=" * 80)
    print(response)
    print("=" * 80)


if __name__ == "__main__":
    main()
