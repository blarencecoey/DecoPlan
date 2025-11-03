# DecoPlan LLM - Quick Start Guide

## TL;DR

```bash
# 1. Build (with CUDA)
./build.sh

# 2. Download model (~7GB)
pip install huggingface-hub
python scripts/download_model.py llava-1.6-mistral-7b

# 3. Run inference
./build/multimodal_inference \
    models/llava-v1.6-mistral-7b.Q4_K_M.gguf \
    floor_plan.jpg \
    "Analyze this floor plan"
```

## Common Commands

### Build Options
```bash
./build.sh               # Build with CUDA
./build.sh --no-cuda     # Build CPU-only
./build.sh --debug       # Build in debug mode
./build.sh --clean       # Clean build from scratch
```

### Download Models
```bash
# Recommended starter model (6-8GB VRAM)
python scripts/download_model.py llava-1.6-mistral-7b

# Higher quality (8-10GB VRAM)
python scripts/download_model.py llava-1.6-mistral-7b --quant Q5_K_M

# Best quality, large model (16-20GB VRAM)
python scripts/download_model.py llava-1.6-34b
```

### Run Inference

**Text-only:**
```bash
./build/simple_inference \
    models/llava-v1.6-mistral-7b.Q4_K_M.gguf \
    "What makes a good living room layout?"
```

**With floor plan image:**
```bash
./build/multimodal_inference \
    models/llava-v1.6-mistral-7b.Q4_K_M.gguf \
    path/to/floorplan.jpg \
    "Suggest furniture placement for this 3-room HDB"
```

## Configuration Quick Reference

### VRAM Usage by Quantization (7B models)
- **Q4_K_M**: ~6-8GB (recommended)
- **Q5_K_M**: ~8-10GB (better quality)
- **Q6_K**: ~10-12GB (high quality)
- **Q8_0**: ~12-16GB (highest quality)

### Key Parameters

```cpp
config.n_ctx = 4096;           // Context size (higher = more memory)
config.n_gpu_layers = -1;      // -1 = all layers on GPU
config.n_predict = 512;        // Max tokens to generate
config.temperature = 0.7f;     // 0.0-2.0, higher = more creative
config.top_p = 0.9f;          // Nucleus sampling threshold
config.top_k = 40;            // Top-k sampling
```

### Performance Tips
1. Use `n_gpu_layers = -1` for maximum GPU utilization
2. Increase `n_batch` to 512+ for faster prompt processing
3. Use Q4_K_M for best speed/quality balance
4. Monitor VRAM with `watch -n1 nvidia-smi`

## Example Prompts

### Furniture Placement
```
"Analyze this 3-bedroom HDB floor plan and suggest:
1. Optimal furniture placement for the living room
2. Space-saving solutions for the bedrooms
3. Storage recommendations"
```

### Design Style
```
"Based on this floor plan, recommend an interior design style
that maximizes natural light and creates a sense of spaciousness
for a family of 4."
```

### Renovation Ideas
```
"Identify potential renovation opportunities in this BTO layout
to improve traffic flow and create more usable space."
```

## Troubleshooting

### Out of VRAM
1. Reduce `n_gpu_layers` (try 32, 24, 16)
2. Use smaller quantization (Q4_K_M instead of Q5_K_M)
3. Reduce `n_ctx` to 2048
4. Use 7B model instead of 34B

### Build Fails
```bash
# Clean rebuild
./build.sh --clean

# CPU-only build
./build.sh --no-cuda
```

### Slow Inference
1. Check GPU utilization: `nvidia-smi`
2. Ensure CUDA build: check build output for "CUDA: ON"
3. Increase `n_gpu_layers` to offload more to GPU
4. Try greedy decoding: `temperature = 0.0`

## File Locations

```
models/                    # Downloaded models
build/simple_inference     # Text-only executable
build/multimodal_inference # Vision+text executable
examples/                  # Source code examples
scripts/                   # Utility scripts
```

## Next Steps

- See [USAGE.md](USAGE.md) for detailed API documentation
- See [BUILD.md](BUILD.md) for build configuration options
- Check [examples/](examples/) for code examples
