"""
Optimized LoRA training configuration for NVIDIA RTX 4500 Ada (25.8 GB VRAM)
This configuration maximizes GPU utilization for faster training.
"""

# =============================================================================
# MEMORY OPTIMIZATION STRATEGIES
# =============================================================================

# Strategy 1: MAXIMUM SPEED (Full GPU Utilization)
# - No quantization (full bf16/fp16)
# - Large batch size
# - Best quality, fastest training
STRATEGY_MAX_SPEED = {
    # Quantization - DISABLED for max speed
    "use_4bit": False,
    "use_8bit": False,
    
    # Training parameters - OPTIMIZED for 25.8GB
    "per_device_train_batch_size": 8,      # Up from 4
    "gradient_accumulation_steps": 2,       # Down from 4 (effective batch = 16)
    "max_seq_length": 2048,                 # Standard
    
    # Precision - Use bf16 for Ada architecture
    "bf16": True,                           # Better than fp16 on Ada
    "fp16": False,
    
    # LoRA parameters - More parameters for better quality
    "lora_r": 32,                           # Up from 16
    "lora_alpha": 64,                       # Up from 32
    "lora_dropout": 0.05,
    
    # Learning rate - Adjust for larger batch
    "learning_rate": 3e-4,                  # Slightly higher
    
    # Estimated VRAM usage: ~20-22 GB
    # Training speed: ~2-3x faster than 4-bit
}

# Strategy 2: BALANCED (Good Speed + Memory Efficiency)
# - 8-bit quantization
# - Larger batch than default
STRATEGY_BALANCED = {
    # Quantization - 8-bit compromise
    "use_4bit": False,
    "use_8bit": True,
    
    # Training parameters
    "per_device_train_batch_size": 12,      # Up from 4
    "gradient_accumulation_steps": 2,       # Effective batch = 24
    "max_seq_length": 2048,
    
    # Precision
    "bf16": True,
    "fp16": False,
    
    # LoRA parameters
    "lora_r": 32,
    "lora_alpha": 64,
    "lora_dropout": 0.05,
    
    # Learning rate
    "learning_rate": 3e-4,
    
    # Estimated VRAM usage: ~15-18 GB
    # Training speed: ~1.5-2x faster than 4-bit
}

# Strategy 3: MEMORY EFFICIENT (Original, but optimized)
# - 4-bit quantization
# - Maximum batch size possible with 4-bit
STRATEGY_MEMORY_EFFICIENT = {
    # Quantization - 4-bit
    "use_4bit": True,
    "bnb_4bit_compute_dtype": "bfloat16",   # Changed from float16
    "bnb_4bit_quant_type": "nf4",
    "use_nested_quant": True,               # Enable for extra compression
    
    # Training parameters - Can push higher with your VRAM
    "per_device_train_batch_size": 16,      # Up from 4
    "gradient_accumulation_steps": 1,       # Effective batch = 16
    "max_seq_length": 2048,
    
    # Precision
    "bf16": True,
    "fp16": False,
    
    # LoRA parameters
    "lora_r": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    
    # Learning rate
    "learning_rate": 2e-4,
    
    # Estimated VRAM usage: ~10-12 GB
    # Training speed: Baseline
}

# Strategy 4: MAXIMUM BATCH SIZE (Longest sequences)
# - For processing longer context
STRATEGY_LONG_CONTEXT = {
    # Quantization
    "use_4bit": True,
    "bnb_4bit_compute_dtype": "bfloat16",
    "bnb_4bit_quant_type": "nf4",
    "use_nested_quant": True,
    
    # Training parameters - Longer sequences
    "per_device_train_batch_size": 8,
    "gradient_accumulation_steps": 2,
    "max_seq_length": 4096,                 # 2x longer!
    
    # Precision
    "bf16": True,
    "fp16": False,
    
    # LoRA parameters
    "lora_r": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    
    # Learning rate
    "learning_rate": 2e-4,
    
    # Estimated VRAM usage: ~18-20 GB
}

# =============================================================================
# RECOMMENDED CONFIGURATION FOR YOUR GPU
# =============================================================================

# 🎯 RECOMMENDED: Start with Strategy 1 (MAX SPEED) for best results
RECOMMENDED_CONFIG = STRATEGY_MAX_SPEED

# Alternative: If you run into OOM, use Strategy 2 (BALANCED)
# Alternative: If training very long sequences, use Strategy 4

# =============================================================================
# ADDITIONAL OPTIMIZATIONS
# =============================================================================

ADDITIONAL_OPTIMIZATIONS = {
    # Gradient checkpointing - Saves memory at cost of ~20% speed
    "gradient_checkpointing": False,  # You have enough VRAM, keep False
    
    # Mixed precision training - Already using bf16
    "tf32": True,  # Enable TensorFloat-32 for Ada architecture (free speedup!)
    
    # DataLoader workers - Parallel data loading
    "dataloader_num_workers": 4,  # Adjust based on CPU cores
    "dataloader_pin_memory": True,  # Faster CPU->GPU transfer
    
    # Optimizer - Ada architecture optimizations
    "optim": "adamw_torch_fused",  # Faster than paged_adamw on Ada
    
    # Compilation - PyTorch 2.0+ feature
    "torch_compile": False,  # Set True for ~20% speedup (experimental)
    
    # Logging
    "logging_steps": 5,  # More frequent logging
    "logging_first_step": True,
}

# =============================================================================
# TRAINING COMMAND EXAMPLES
# =============================================================================

COMMAND_EXAMPLES = """
# MAX SPEED (Recommended - No quantization, full bf16)
python train_lora.py \\
    --model_name llava-hf/llava-1.5-7b-hf \\
    --batch_size 8 \\
    --learning_rate 3e-4 \\
    --lora_r 32 \\
    --lora_alpha 64 \\
    --num_epochs 3 \\
    --no_quantization \\
    --bf16

# BALANCED (8-bit quantization)
python train_lora.py \\
    --model_name llava-hf/llava-1.5-7b-hf \\
    --batch_size 12 \\
    --learning_rate 3e-4 \\
    --lora_r 32 \\
    --lora_alpha 64 \\
    --num_epochs 3 \\
    --use_8bit \\
    --bf16

# MEMORY EFFICIENT (4-bit, but higher batch size)
python train_lora.py \\
    --model_name llava-hf/llava-1.5-7b-hf \\
    --batch_size 16 \\
    --learning_rate 2e-4 \\
    --num_epochs 3 \\
    --use_4bit \\
    --bf16

# LONG CONTEXT (4096 tokens)
python train_lora.py \\
    --model_name llava-hf/llava-1.5-7b-hf \\
    --batch_size 8 \\
    --max_seq_length 4096 \\
    --learning_rate 2e-4 \\
    --num_epochs 3 \\
    --use_4bit \\
    --bf16
"""

print(__doc__)
print("\n" + "="*80)
print("RECOMMENDED CONFIGURATION FOR RTX 4500 ADA (25.8 GB)")
print("="*80)
print("\nStrategy: MAX SPEED (No Quantization)")
for key, value in RECOMMENDED_CONFIG.items():
    print(f"  {key}: {value}")

print("\n" + "="*80)
print("ADDITIONAL OPTIMIZATIONS")
print("="*80)
for key, value in ADDITIONAL_OPTIMIZATIONS.items():
    print(f"  {key}: {value}")

print("\n" + "="*80)
print("COMMAND EXAMPLES")
print("="*80)
print(COMMAND_EXAMPLES)
