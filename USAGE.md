# DecoPlan LLM Usage Guide

## Quick Start

### 1. Download a Model

Using the Python script (recommended):
```bash
# Install dependencies
pip install huggingface-hub

# Download LLaVA 1.6 Mistral 7B with Q4_K_M quantization
python scripts/download_model.py llava-1.6-mistral-7b

# Or with higher quality Q5_K_M quantization
python scripts/download_model.py llava-1.6-mistral-7b --quant Q5_K_M
```

Using the bash script:
```bash
./scripts/download_model.sh llava-1.6-mistral-7b Q4_K_M
```

### 2. Run Inference

#### Text-Only Inference
```bash
./build/simple_inference \
    models/llava-v1.6-mistral-7b.Q4_K_M.gguf \
    "Describe the best furniture layout for a 3-bedroom HDB flat."
```

#### Multimodal Inference (Image + Text)
```bash
./build/multimodal_inference \
    models/llava-v1.6-mistral-7b.Q4_K_M.gguf \
    path/to/floor_plan.jpg \
    "Analyze this floor plan and suggest furniture placement for the living room."
```

## Model Selection Guide

### Recommended Models for DecoPlan

#### LLaVA 1.6 Mistral 7B (Recommended Starting Point)
- **Quantization**: Q4_K_M
- **VRAM**: ~6-8GB
- **Quality**: Good
- **Speed**: Fast
- **Use case**: Quick iterations, prototyping

```bash
python scripts/download_model.py llava-1.6-mistral-7b
```

#### LLaVA 1.6 34B (Best Quality)
- **Quantization**: Q4_K_M or Q5_K_M
- **VRAM**: ~16-20GB (Q4_K_M), ~20-24GB (Q5_K_M)
- **Quality**: Excellent
- **Speed**: Moderate
- **Use case**: Production, highest accuracy needed

```bash
python scripts/download_model.py llava-1.6-34b --quant Q5_K_M
```

#### Qwen2-VL 7B (Alternative)
- **Quantization**: Q4_K_M
- **VRAM**: ~7-9GB
- **Quality**: Good
- **Speed**: Fast
- **Use case**: Alternative architecture, good for Asian languages

```bash
python scripts/download_model.py qwen2-vl-7b
```

### Quantization Comparison

| Quantization | VRAM (7B) | VRAM (34B) | Quality | Speed |
|-------------|-----------|------------|---------|-------|
| Q4_K_M      | 6-8GB     | 16-20GB    | Good    | Fast  |
| Q5_K_M      | 8-10GB    | 20-24GB    | Better  | Medium|
| Q6_K        | 10-12GB   | 24-28GB    | High    | Slower|
| Q8_0        | 12-16GB   | 28-34GB    | Highest | Slow  |

**Recommendation**: Start with Q4_K_M, upgrade to Q5_K_M if you have extra VRAM.

## Configuration Options

### InferenceConfig Parameters

```cpp
decoplan::InferenceConfig config;
config.model_path = "models/model.gguf";
config.n_ctx = 4096;           // Context window size
config.n_gpu_layers = -1;      // -1 = all layers on GPU
config.n_predict = 512;        // Max tokens to generate
config.temperature = 0.7f;     // Randomness (0.0-2.0)
config.top_p = 0.9f;          // Nucleus sampling
config.top_k = 40;            // Top-k sampling
config.n_threads = -1;        // -1 = auto-detect
```

### Performance Tuning

#### Maximum GPU Utilization
```cpp
config.n_gpu_layers = -1;  // Offload all layers to GPU
config.n_batch = 512;      // Larger batch for faster prompt processing
```

#### Lower Memory Usage
```cpp
config.n_gpu_layers = 32;  // Only some layers on GPU
config.n_ctx = 2048;       // Smaller context window
config.use_mmap = true;    // Memory-map model file
```

#### Faster Inference
```cpp
config.temperature = 0.0f; // Greedy decoding (faster, deterministic)
config.n_batch = 512;      // Process prompt in larger batches
```

#### Higher Quality
```cpp
config.temperature = 0.8f;
config.top_p = 0.95f;
config.n_predict = 1024;   // Allow longer responses
```

## Example Prompts for Floor Planning

### Room Analysis
```cpp
"Analyze this floor plan and identify all rooms, their dimensions, and current layout."
```

### Furniture Placement
```cpp
"Given this 3-bedroom HDB floor plan, suggest optimal furniture placement for:
1. Living room
2. Master bedroom
3. Dining area

Consider traffic flow, natural lighting, and Singapore HDB regulations."
```

### Style Recommendations
```cpp
"Based on this floor plan, recommend a cohesive interior design style that would:
- Maximize space perception
- Work well with natural lighting
- Suit a young family of 4"
```

### Renovation Suggestions
```cpp
"Identify potential renovation opportunities in this floor plan to:
- Create more storage
- Improve traffic flow
- Maximize usable space"
```

## C++ API Usage

### Basic Text Generation

```cpp
#include "llm_wrapper.h"

decoplan::InferenceConfig config;
config.model_path = "models/model.gguf";
config.n_gpu_layers = -1;

decoplan::LLMWrapper llm;
llm.initialize(config);

std::string response = llm.generate("Your prompt here");
std::cout << response << std::endl;
```

### Streaming Generation

```cpp
llm.generateStreaming("Your prompt", [](const std::string& token) {
    std::cout << token << std::flush;
});
std::cout << std::endl;
```

### Multimodal Processing

```cpp
#include "multimodal_processor.h"

decoplan::MultimodalConfig config;
config.model_path = "models/llava-v1.6-mistral-7b.Q4_K_M.gguf";
config.clip_model_path = "models/mmproj-model-f16.gguf";

decoplan::MultimodalProcessor processor;
processor.initialize(config);

processor.generateFromImageStreaming(
    "floor_plan.jpg",
    "Describe this floor plan",
    [](const std::string& token) {
        std::cout << token << std::flush;
    }
);
```

## Performance Tips

1. **GPU Layers**: Use `n_gpu_layers = -1` to offload everything to GPU
2. **Batch Size**: Increase `n_batch` (e.g., 512) for faster prompt processing
3. **Context Size**: Only use what you need - smaller contexts are faster
4. **Quantization**: Q4_K_M is the sweet spot for most use cases
5. **Threading**: Let auto-detection handle CPU threads (`n_threads = -1`)

## Monitoring VRAM Usage

```bash
# NVIDIA GPUs
watch -n 1 nvidia-smi

# Monitor during inference to optimize n_gpu_layers
```

## Troubleshooting

### Out of VRAM
- Reduce `n_gpu_layers` (e.g., try 32, 24, 16)
- Use smaller quantization (Q4_K_M instead of Q5_K_M)
- Reduce `n_ctx` (e.g., 2048 instead of 4096)
- Use a smaller model (7B instead of 34B)

### Slow Inference
- Increase `n_gpu_layers` to offload more to GPU
- Check GPU utilization with `nvidia-smi`
- Reduce `temperature` for greedy decoding
- Ensure CUDA build is enabled

### Poor Quality Output
- Try higher quantization (Q5_K_M or Q6_K)
- Adjust temperature (0.7-0.9 usually works well)
- Increase `n_predict` for longer responses
- Experiment with different models

## Next Steps

- See [examples/](examples/) for more code examples
- Check [BUILD.md](BUILD.md) for build instructions
- Visit [llama.cpp](https://github.com/ggerganov/llama.cpp) for advanced features
