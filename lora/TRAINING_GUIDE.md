# Training Optimization Guide for RTX 4500 Ada (25.8 GB VRAM)

## 🚀 Quick Start - Recommended Commands

### Option 1: MAXIMUM SPEED (Recommended) ⚡
**No quantization, full bf16 precision - 2-3x faster!**
```bash
python train_lora_optimized.py \
    --model_name llava-hf/llava-1.5-7b-hf \
    --batch_size 8 \
    --gradient_accumulation_steps 2 \
    --learning_rate 3e-4 \
    --lora_r 32 \
    --lora_alpha 64 \
    --num_epochs 3 \
    --no_quantization \
    --bf16
```
- **VRAM Usage:** ~20-22 GB
- **Speed:** ~2-3x faster than 4-bit
- **Quality:** Best (full precision)
- **Effective Batch Size:** 16

---

### Option 2: BALANCED 🎯
**8-bit quantization with large batch size**
```bash
python train_lora_optimized.py \
    --model_name llava-hf/llava-1.5-7b-hf \
    --batch_size 12 \
    --gradient_accumulation_steps 2 \
    --learning_rate 3e-4 \
    --lora_r 32 \
    --lora_alpha 64 \
    --num_epochs 3 \
    --use_8bit \
    --bf16
```
- **VRAM Usage:** ~15-18 GB
- **Speed:** ~1.5-2x faster than 4-bit
- **Quality:** Excellent
- **Effective Batch Size:** 24

---

### Option 3: MEMORY EFFICIENT 💾
**4-bit quantization with maximum batch size**
```bash
python train_lora_optimized.py \
    --model_name llava-hf/llava-1.5-7b-hf \
    --batch_size 16 \
    --gradient_accumulation_steps 1 \
    --learning_rate 2e-4 \
    --num_epochs 3 \
    --use_4bit \
    --bf16
```
- **VRAM Usage:** ~10-12 GB
- **Speed:** Baseline
- **Quality:** Good
- **Effective Batch Size:** 16

---

### Option 4: LONG CONTEXT 📄
**For processing 4096 token sequences**
```bash
python train_lora_optimized.py \
    --model_name llava-hf/llava-1.5-7b-hf \
    --batch_size 8 \
    --gradient_accumulation_steps 2 \
    --max_seq_length 4096 \
    --learning_rate 2e-4 \
    --num_epochs 3 \
    --use_4bit \
    --bf16
```
- **VRAM Usage:** ~18-20 GB
- **Speed:** Slower (longer sequences)
- **Context:** 2x longer (4096 vs 2048)

---

## 📊 Performance Comparison

| Strategy | Quantization | Batch Size | VRAM | Speed | Quality |
|----------|-------------|------------|------|-------|---------|
| **MAX SPEED** ⚡ | None | 8 | 20-22 GB | 🔥🔥🔥 | ⭐⭐⭐⭐⭐ |
| **BALANCED** 🎯 | 8-bit | 12 | 15-18 GB | 🔥🔥 | ⭐⭐⭐⭐ |
| **MEMORY EFFICIENT** 💾 | 4-bit | 16 | 10-12 GB | 🔥 | ⭐⭐⭐ |
| **LONG CONTEXT** 📄 | 4-bit | 8 | 18-20 GB | 🐌 | ⭐⭐⭐ |
| **Original** (default) | 4-bit | 4 | 5-6 GB | 🐌 | ⭐⭐⭐ |

---

## 🎛️ Key Parameters Explained

### Batch Size (`--batch_size`)
- **What it does:** Number of samples processed simultaneously
- **Your GPU:** Can handle 8-16 depending on quantization
- **Trade-off:** Higher = faster but more VRAM

### Gradient Accumulation (`--gradient_accumulation_steps`)
- **What it does:** Simulates larger batch sizes
- **Formula:** Effective batch = batch_size × accumulation_steps
- **Your GPU:** With larger batch sizes, reduce to 1-2

### LoRA Rank (`--lora_r` and `--lora_alpha`)
- **What it does:** Controls adapter capacity
- **Conservative:** r=16, alpha=32 (default)
- **Aggressive:** r=32, alpha=64 (more parameters, better quality)
- **Your GPU:** Can handle r=32 easily

### Quantization
- **`--no_quantization`**: Full precision (fastest, most VRAM)
- **`--use_8bit`**: 8-bit quantization (balanced)
- **`--use_4bit`**: 4-bit quantization (most memory efficient)

### Precision
- **`--bf16`**: Use bfloat16 (RECOMMENDED for Ada architecture)
- **`--fp16`**: Use float16 (alternative)
- **Your GPU:** Always use `--bf16` on RTX 4500 Ada

---

## 🔍 Monitoring Your Training

### Watch GPU Usage
```bash
watch -n 1 nvidia-smi
```

Look for:
- **GPU Utilization:** Should be 90-100%
- **Memory Usage:** Should be 15-22 GB (depending on config)
- **Temperature:** Should stay under 85°C

### Training Speed Benchmarks
- **Original config:** ~1-2 iterations/sec
- **Optimized config (MAX SPEED):** ~4-6 iterations/sec
- **Speedup:** 2-3x faster! 🚀

---

## ⚠️ Troubleshooting

### Out of Memory (OOM)
If you see `CUDA out of memory`:
1. Reduce `--batch_size` by 2
2. Or increase `--gradient_accumulation_steps` by 2
3. Or enable `--gradient_checkpointing` (20% slower but saves VRAM)
4. Or use `--use_8bit` or `--use_4bit`

### Training Too Slow
If GPU utilization < 80%:
1. Increase `--batch_size`
2. Reduce `--gradient_accumulation_steps`
3. Try `--no_quantization` for full speed

### Bad Results
If model quality is poor:
1. Increase `--lora_r` to 32 or 64
2. Increase `--lora_alpha` accordingly (2x the rank)
3. Try longer training: `--num_epochs 5`
4. Use full precision: `--no_quantization`

---

## 🎯 My Recommendation for You

Start with **Option 1 (MAX SPEED)**:
```bash
python train_lora_optimized.py \
    --model_name llava-hf/llava-1.5-7b-hf \
    --batch_size 8 \
    --gradient_accumulation_steps 2 \
    --learning_rate 3e-4 \
    --lora_r 32 \
    --lora_alpha 64 \
    --num_epochs 3 \
    --no_quantization \
    --bf16
```

**Why?**
- ✅ Your GPU has plenty of VRAM (25.8 GB)
- ✅ 2-3x faster training
- ✅ Better quality (no quantization loss)
- ✅ Ada architecture optimized (bf16)
- ✅ Still leaves 3-5 GB VRAM headroom

**If you get OOM**, drop to Option 2 (BALANCED) with 8-bit quantization.

---

## 📈 Expected Training Times

For a typical dataset of 1000 samples:

| Configuration | Time per Epoch | Total (3 epochs) |
|--------------|----------------|------------------|
| Original (4-bit, batch=4) | ~30-45 min | ~1.5-2 hours |
| **MAX SPEED** | ~12-15 min | **~35-45 min** |
| BALANCED | ~15-20 min | ~45-60 min |

**You'll save 1+ hour per training run!** ⚡

---

## 📝 Additional Tips

1. **Use bf16 on Ada GPUs:** RTX 4500 Ada has excellent bfloat16 support
2. **Monitor first epoch:** Watch VRAM usage and adjust if needed
3. **Effective batch size:** Keep it 16-24 for good convergence
4. **Learning rate:** Increase slightly (2e-4 → 3e-4) with larger batches
5. **Save checkpoints:** Training is faster, so save more frequently

---

## 🎓 Advanced: Further Optimizations

Once comfortable, try these for even more speed:

```bash
python train_lora_optimized.py \
    --model_name llava-hf/llava-1.5-7b-hf \
    --batch_size 8 \
    --learning_rate 3e-4 \
    --lora_r 32 \
    --lora_alpha 64 \
    --no_quantization \
    --bf16 \
    --dataloader_num_workers 4 \        # Parallel data loading
    --torch_compile                      # PyTorch 2.0+ compilation (experimental)
```

These can add another 10-20% speedup!

---

**Happy training! You have an amazing GPU - use it to its full potential! 🚀**
