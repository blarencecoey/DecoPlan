# DecoPlan LLM

AI-powered interior design assistant for Singapore BTOs and HDB layouts using multimodal vision-language models.

## Overview

DecoPlan LLM is a C++ framework built on [llama.cpp](https://github.com/ggerganov/llama.cpp) that enables vision-language models to analyze floor plans and provide intelligent furniture placement, design recommendations, and space optimization suggestions tailored for Singapore HDB flats.

## Features

- **Multimodal Vision-Language Models**: Analyze floor plans using LLaVA, Qwen2-VL, or Llama 3.2 Vision
- **CUDA GPU Acceleration**: Efficient inference with CUDA support
- **GGUF Model Support**: Use quantized models (Q4_K_M, Q5_K_M, etc.) for optimal VRAM usage
- **Streaming Inference**: Real-time token-by-token generation
- **Easy C++ API**: Clean wrapper around llama.cpp for production use

## Quick Start

### 1. Build

```bash
mkdir build && cd build
cmake .. -DDECOPLAN_USE_CUDA=ON
cmake --build . -j$(nproc)
```

See [BUILD.md](BUILD.md) for detailed build instructions.

### 2. Download a Model

```bash
pip install huggingface-hub
python scripts/download_model.py llava-1.6-mistral-7b
```

### 3. Run Inference

```bash
# Analyze a floor plan image
./build/multimodal_inference \
    models/llava-v1.6-mistral-7b.Q4_K_M.gguf \
    floor_plan.jpg \
    "Suggest furniture placement for this living room"
```

## Documentation

- [BUILD.md](BUILD.md) - Build instructions and requirements
- [USAGE.md](USAGE.md) - Detailed usage guide, API documentation, and examples
- [examples/](examples/) - Example programs

## Recommended Models

| Model | VRAM (Q4_K_M) | Quality | Use Case |
|-------|---------------|---------|----------|
| LLaVA 1.6 Mistral 7B | ~6-8GB | Good | Development, prototyping |
| LLaVA 1.6 34B | ~16-20GB | Excellent | Production, best quality |
| Qwen2-VL 7B | ~7-9GB | Good | Alternative architecture |

## System Requirements

- **OS**: Linux, macOS, Windows (WSL2)
- **CPU**: x86_64 with AVX2 or ARM64
- **GPU** (Optional): NVIDIA GPU with CUDA 11.0+, or Apple Silicon (Metal)
- **RAM**: 16GB minimum, 32GB recommended
- **VRAM**: 6GB minimum for Q4_K_M quantization

## Project Structure

```
DecoPlan LLM/
├── include/              # Public headers
│   ├── llm_wrapper.h
│   └── multimodal_processor.h
├── src/                  # Implementation
│   ├── llm_wrapper.cpp
│   └── multimodal_processor.cpp
├── examples/             # Example programs
│   ├── simple_inference.cpp
│   └── multimodal_inference.cpp
├── scripts/              # Utility scripts
│   ├── download_model.py
│   └── download_model.sh
├── external/
│   └── llama.cpp/       # llama.cpp submodule
└── models/              # Downloaded models (created on first use)
```

## C++ API Example

```cpp
#include "multimodal_processor.h"

decoplan::MultimodalConfig config;
config.model_path = "models/llava-v1.6-mistral-7b.Q4_K_M.gguf";
config.n_gpu_layers = -1;  // Use all GPU layers

decoplan::MultimodalProcessor processor;
processor.initialize(config);

processor.generateFromImageStreaming(
    "floor_plan.jpg",
    "Analyze this floor plan and suggest furniture placement",
    [](const std::string& token) {
        std::cout << token << std::flush;
    }
);
```

## Performance Tips

1. Use **Q4_K_M quantization** for best quality/VRAM balance (~6-8GB)
2. Set `n_gpu_layers = -1` to offload all layers to GPU
3. Use **Q5_K_M** if you have extra VRAM for better quality
4. Monitor VRAM with `nvidia-smi` and adjust layers as needed

## Contributing

This is a university project for HDB/BTO interior design assistance. Contributions welcome!

## License

See [LICENSE](LICENSE) for details.

## Acknowledgments

- Built on [llama.cpp](https://github.com/ggerganov/llama.cpp) by Georgi Gerganov
- Models from [Hugging Face](https://huggingface.co/) community
- Inspired by Singapore HDB interior design needs
