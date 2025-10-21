# Changelog

## CMake Configuration Updates

### Key Changes

#### 1. Fixed CUDA Support
- **Changed**: `LLAMA_CUBLAS` → `GGML_CUDA`
  - llama.cpp deprecated `LLAMA_CUBLAS` in favor of `GGML_CUDA`
  - Updated CMakeLists.txt to use correct option name

- **Added**: Conditional CUDA language support
  ```cmake
  if(DECOPLAN_USE_CUDA)
      project(DecoPlanLLM LANGUAGES CXX C CUDA)
  else()
      project(DecoPlanLLM LANGUAGES CXX C)
  endif()
  ```

#### 2. Fixed Include Paths
- **Updated**: Include directories to match llama.cpp structure
  ```cmake
  external/llama.cpp/include      # Main llama.h header
  external/llama.cpp/common       # Common utilities
  external/llama.cpp/ggml/include # GGML headers
  ```

#### 3. Disabled Unnecessary llama.cpp Builds
- Added flags to speed up compilation:
  ```cmake
  set(LLAMA_BUILD_TESTS OFF)
  set(LLAMA_BUILD_EXAMPLES OFF)
  set(LLAMA_BUILD_SERVER OFF)
  ```

#### 4. Static Linking Configuration
- Set `BUILD_SHARED_LIBS OFF` for easier deployment
- Produces standalone executables with all dependencies included

### Build Script Updates

Updated `build.sh` to properly pass CUDA flags:
```bash
# CUDA build
cmake .. -DDECOPLAN_USE_CUDA=ON -DGGML_CUDA=ON

# CPU-only build
cmake .. -DDECOPLAN_USE_CUDA=OFF -DGGML_CUDA=OFF
```

### New Files
- `.clang-format` - C++ code style configuration
- `QUICKSTART.md` - Quick reference guide
- `CHANGELOG.md` - This file

### Updated Files
- `CMakeLists.txt` - Fixed CUDA support and include paths
- `build.sh` - Improved CUDA flag handling
- `BUILD.md` - Enhanced troubleshooting section
- `.gitignore` - Already comprehensive (no changes needed)

## Migration Guide

If you have an existing build directory:

```bash
# Clean rebuild recommended
rm -rf build/
./build.sh
```

Or rebuild llama.cpp separately:
```bash
cd external/llama.cpp
rm -rf build/
cmake -B build -DGGML_CUDA=ON
cmake --build build -j$(nproc)
cd ../..
```

## Testing the Build

### Verify CUDA Support
```bash
# Build output should show:
# "CUDA: ON" or "GGML_CUDA: ON"

# Check if CUDA libraries are linked
ldd build/simple_inference | grep cuda
```

### Test Inference
```bash
# Download a model
python scripts/download_model.py llava-1.6-mistral-7b

# Run simple test
./build/simple_inference \
    models/llava-v1.6-mistral-7b.Q4_K_M.gguf \
    "Hello, world!"
```

## Known Issues

### WSL2 CUDA
If using WSL2, ensure you have:
1. NVIDIA drivers installed on Windows host
2. CUDA toolkit installed in WSL2
3. Environment variables set:
   ```bash
   export CUDA_PATH=/usr/local/cuda
   export PATH=/usr/local/cuda/bin:$PATH
   export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
   ```

### Apple Silicon (Metal)
For macOS with Apple Silicon, llama.cpp will automatically use Metal acceleration. No CUDA needed.

## Performance Comparison

Expected performance improvements with CUDA vs CPU:

| Model | CPU (16-core) | GPU (RTX 3090) | Speedup |
|-------|--------------|----------------|---------|
| 7B Q4 | ~8 tokens/s  | ~50-80 tokens/s| 6-10x  |
| 7B Q5 | ~6 tokens/s  | ~40-60 tokens/s| 6-10x  |
| 34B Q4| ~2 tokens/s  | ~20-30 tokens/s| 10-15x |

*Results vary based on hardware and configuration*
