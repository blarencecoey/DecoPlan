# Building DecoPlan LLM

## Prerequisites

### Required
- CMake 3.18 or higher
- C++17 compatible compiler (GCC 8+, Clang 7+, MSVC 2019+)
- Git

### Optional (Recommended)
- CUDA Toolkit 11.0+ (for GPU acceleration)
- cuBLAS (included with CUDA)

## Build Instructions

### 1. Clone and Setup

The repository should already have llama.cpp cloned in `external/llama.cpp`.

If you need to update llama.cpp:
```bash
cd external/llama.cpp
git pull
cd ../..
```

### 2. Build with CMake

#### CPU Only
```bash
mkdir build
cd build
cmake .. -DDECOPLAN_USE_CUDA=OFF
cmake --build . -j$(nproc)
```

#### With CUDA (Recommended)
```bash
mkdir build
cd build
cmake .. -DDECOPLAN_USE_CUDA=ON
cmake --build . -j$(nproc)
```

#### Build Options
- `DECOPLAN_USE_CUDA`: Enable CUDA support (default: ON)
- `DECOPLAN_BUILD_EXAMPLES`: Build example programs (default: ON)

### 3. Verify Build

After building, you should see:
```
build/
├── libdecoplan_llm.a
├── simple_inference
└── multimodal_inference
```

## Platform-Specific Notes

### Linux
```bash
# Install dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install build-essential cmake git

# For CUDA support
# Install CUDA from: https://developer.nvidia.com/cuda-downloads
```

### macOS
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install CMake
brew install cmake

# Metal acceleration is automatically enabled on Apple Silicon
```

### Windows (WSL)
The project should work in WSL2. Follow the Linux instructions above.

For native Windows builds, use Visual Studio 2019+ or MinGW.

## Troubleshooting

### CMake can't find CUDA
```bash
export CUDA_PATH=/usr/local/cuda
cmake .. -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc
```

### Linking errors
Make sure llama.cpp built successfully:
```bash
cd external/llama.cpp
cmake -B build
cmake --build build -j$(nproc)
```

### Out of memory during compilation
Reduce parallel jobs:
```bash
cmake --build . -j2
```

## Next Steps

After building, see [USAGE.md](USAGE.md) for how to download models and run inference.
