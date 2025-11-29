"""
LoRA fine-tuning script for vision-language models.
Supports LLaVA, Qwen2-VL, and Llama 3.2 Vision models.
"""

import os
import json
import torch
from dataclasses import dataclass, field
from typing import Optional, Dict, List
import argparse
from pathlib import Path

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    AutoModelForVision2Seq,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset, Dataset
import transformers


@dataclass
class LoRATrainingConfig:
    """Configuration for LoRA training."""

    # Model
    model_name: str = "llava-hf/llava-1.5-7b-hf"
    cache_dir: Optional[str] = None

    # LoRA parameters
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    lora_target_modules: List[str] = field(
        default_factory=lambda: ["q_proj", "k_proj", "v_proj", "o_proj"]
    )

    # Quantization
    use_4bit: bool = True
    bnb_4bit_compute_dtype: str = "float16"
    bnb_4bit_quant_type: str = "nf4"
    use_nested_quant: bool = False

    # Training
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 4
    gradient_accumulation_steps: int = 4
    learning_rate: float = 2e-4
    weight_decay: float = 0.01
    warmup_ratio: float = 0.03
    max_grad_norm: float = 0.3
    max_seq_length: int = 2048

    # Optimization
    optim: str = "paged_adamw_32bit"
    lr_scheduler_type: str = "cosine"
    logging_steps: int = 10
    save_steps: int = 100
    eval_steps: int = 100

    # Paths
    train_data: str = "datasets/Output/lora_splits/train.json"
    val_data: str = "datasets/Output/lora_splits/val.json"
    output_dir: str = "models/lora_checkpoints"

    # Misc
    seed: int = 42
    fp16: bool = False
    bf16: bool = False


class LoRATrainer:
    """Trainer for LoRA fine-tuning."""

    def __init__(self, config: LoRATrainingConfig):
        """
        Initialize LoRA trainer.

        Args:
            config: Training configuration
        """
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        print(f"Using device: {self.device}")
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
            print(f"CUDA Version: {torch.version.cuda}")

    def load_model_and_tokenizer(self):
        """Load base model and tokenizer with quantization."""
        print(f"\nLoading model: {self.config.model_name}")

        # Quantization config
        if self.config.use_4bit:
            compute_dtype = getattr(torch, self.config.bnb_4bit_compute_dtype)
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type=self.config.bnb_4bit_quant_type,
                bnb_4bit_compute_dtype=compute_dtype,
                bnb_4bit_use_double_quant=self.config.use_nested_quant,
            )
            print("  Using 4-bit quantization")
        else:
            bnb_config = None

        # Detect model type and use appropriate class
        model_name_lower = self.config.model_name.lower()

        # Check if it's a vision-language model
        is_vision_model = any(
            keyword in model_name_lower
            for keyword in ["llava", "qwen2-vl", "llama-3.2-vision"]
        )

        if is_vision_model:
            print("  Detected vision-language model, using AutoModelForVision2Seq")
            model = AutoModelForVision2Seq.from_pretrained(
                self.config.model_name,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
                cache_dir=self.config.cache_dir,
            )
        else:
            print("  Using AutoModelForCausalLM")
            model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
                cache_dir=self.config.cache_dir,
            )

        # Prepare model for k-bit training
        if self.config.use_4bit:
            model = prepare_model_for_kbit_training(model)

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            self.config.model_name,
            trust_remote_code=True,
            cache_dir=self.config.cache_dir,
        )

        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            model.config.pad_token_id = model.config.eos_token_id

        print("  Model and tokenizer loaded successfully")
        return model, tokenizer

    def setup_lora(self, model):
        """
        Setup LoRA configuration and apply to model.

        Args:
            model: Base model

        Returns:
            Model with LoRA adapters
        """
        print("\nConfiguring LoRA...")

        lora_config = LoraConfig(
            r=self.config.lora_r,
            lora_alpha=self.config.lora_alpha,
            target_modules=self.config.lora_target_modules,
            lora_dropout=self.config.lora_dropout,
            bias="none",
            task_type="CAUSAL_LM",
        )

        model = get_peft_model(model, lora_config)

        # Print trainable parameters
        trainable_params = 0
        all_param = 0
        for _, param in model.named_parameters():
            all_param += param.numel()
            if param.requires_grad:
                trainable_params += param.numel()

        print(f"  LoRA Configuration:")
        print(f"    r={self.config.lora_r}, alpha={self.config.lora_alpha}")
        print(f"    Target modules: {self.config.lora_target_modules}")
        print(
            f"  Trainable params: {trainable_params:,} ({100 * trainable_params / all_param:.2f}%)"
        )
        print(f"  Total params: {all_param:,}")

        return model

    def load_and_prepare_dataset(self, tokenizer):
        """
        Load and prepare training/validation datasets.

        Args:
            tokenizer: Tokenizer for encoding

        Returns:
            Tuple of (train_dataset, val_dataset)
        """
        print("\nLoading datasets...")

        # Load JSON files
        with open(self.config.train_data, "r") as f:
            train_data = json.load(f)

        val_data = None
        if self.config.val_data and Path(self.config.val_data).exists():
            with open(self.config.val_data, "r") as f:
                val_data = json.load(f)

        print(f"  Training examples: {len(train_data)}")
        if val_data:
            print(f"  Validation examples: {len(val_data)}")

        # Create datasets
        train_dataset = Dataset.from_list(train_data)
        val_dataset = Dataset.from_list(val_data) if val_data else None

        # Tokenization function
        def tokenize_function(examples):
            # Handle conversation format
            if "messages" in examples:
                messages = examples["messages"]
                # Format as chat template
                text = tokenizer.apply_chat_template(
                    messages, tokenize=False, add_generation_prompt=False
                )
            # Handle Alpaca format
            elif "instruction" in examples:
                text = f"### Instruction:\n{examples['instruction']}\n\n"
                text += f"### Input:\n{examples['input']}\n\n"
                text += f"### Response:\n{examples['output']}"
            else:
                raise ValueError("Unknown data format")

            # Tokenize
            tokenized = tokenizer(
                text,
                truncation=True,
                max_length=self.config.max_seq_length,
                padding="max_length",
            )

            tokenized["labels"] = tokenized["input_ids"].copy()
            return tokenized

        # Apply tokenization
        print("  Tokenizing datasets...")
        train_dataset = train_dataset.map(
            tokenize_function,
            remove_columns=train_dataset.column_names,
            desc="Tokenizing training data",
        )

        if val_dataset:
            val_dataset = val_dataset.map(
                tokenize_function,
                remove_columns=val_dataset.column_names,
                desc="Tokenizing validation data",
            )

        return train_dataset, val_dataset

    def train(self):
        """Run the training process."""
        print("\n" + "=" * 80)
        print("Starting LoRA Fine-Tuning")
        print("=" * 80)

        # Load model and tokenizer
        model, tokenizer = self.load_model_and_tokenizer()

        # Setup LoRA
        model = self.setup_lora(model)

        # Load datasets
        train_dataset, val_dataset = self.load_and_prepare_dataset(tokenizer)

        # Training arguments
        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        training_args = TrainingArguments(
            output_dir=str(output_dir),
            num_train_epochs=self.config.num_train_epochs,
            per_device_train_batch_size=self.config.per_device_train_batch_size,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps,
            learning_rate=self.config.learning_rate,
            weight_decay=self.config.weight_decay,
            warmup_ratio=self.config.warmup_ratio,
            max_grad_norm=self.config.max_grad_norm,
            logging_steps=self.config.logging_steps,
            save_steps=self.config.save_steps,
            eval_steps=self.config.eval_steps if val_dataset else None,
            eval_strategy=(
                "steps" if val_dataset else "no"
            ),  # Changed from evaluation_strategy
            save_strategy="steps",
            load_best_model_at_end=val_dataset is not None,
            optim=self.config.optim,
            lr_scheduler_type=self.config.lr_scheduler_type,
            fp16=self.config.fp16,
            bf16=self.config.bf16,
            seed=self.config.seed,
            report_to=["tensorboard"],
            remove_unused_columns=False,
        )

        # Initialize trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
        )

        # Train
        print("\n" + "=" * 80)
        print("Training started...")
        print("=" * 80 + "\n")

        trainer.train()

        # Save final model
        final_model_path = output_dir / "final_model"
        trainer.save_model(str(final_model_path))
        tokenizer.save_pretrained(str(final_model_path))

        print("\n" + "=" * 80)
        print("Training completed!")
        print(f"Model saved to: {final_model_path}")
        print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Train LoRA adapters for DecoPlan LLM")

    # Model
    parser.add_argument("--model_name", type=str, default="llava-hf/llava-1.5-7b-hf")
    parser.add_argument("--cache_dir", type=str, default=None)

    # LoRA
    parser.add_argument("--lora_r", type=int, default=16)
    parser.add_argument("--lora_alpha", type=int, default=32)
    parser.add_argument("--lora_dropout", type=float, default=0.05)

    # Training
    parser.add_argument("--num_epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--learning_rate", type=float, default=2e-4)
    parser.add_argument("--max_seq_length", type=int, default=2048)

    # Data
    parser.add_argument(
        "--train_data", type=str, default="datasets/Output/lora_splits/train.json"
    )
    parser.add_argument(
        "--val_data", type=str, default="datasets/Output/lora_splits/val.json"
    )
    parser.add_argument("--output_dir", type=str, default="models/lora_checkpoints")

    args = parser.parse_args()

    # Create config
    config = LoRATrainingConfig(
        model_name=args.model_name,
        cache_dir=args.cache_dir,
        lora_r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        num_train_epochs=args.num_epochs,
        per_device_train_batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        max_seq_length=args.max_seq_length,
        train_data=args.train_data,
        val_data=args.val_data,
        output_dir=args.output_dir,
    )

    # Train
    trainer = LoRATrainer(config)
    trainer.train()


if __name__ == "__main__":
    main()
