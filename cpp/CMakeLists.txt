cmake_minimum_required(VERSION 3.18)

# Options (must be before project())
option(DECOPLAN_BUILD_EXAMPLES "Build example programs" ON)
option(DECOPLAN_USE_CUDA "Enable CUDA support" ON)

# Setup project languages
if(DECOPLAN_USE_CUDA)
    project(DecoPlanLLM LANGUAGES CXX C CUDA)
else()
    project(DecoPlanLLM LANGUAGES CXX C)
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)


# Configure llama.cpp options before adding subdirectory
set(BUILD_SHARED_LIBS OFF CACHE BOOL "Build shared libraries")
set(GGML_CUDA ${DECOPLAN_USE_CUDA} CACHE BOOL "Enable CUDA support in llama.cpp")

# Enable common library (required for our wrapper)
set(LLAMA_BUILD_COMMON ON CACHE BOOL "Build llama.cpp common library")

# Optional: Disable unnecessary llama.cpp examples and tools
set(LLAMA_BUILD_TESTS OFF CACHE BOOL "Disable llama.cpp tests")
set(LLAMA_BUILD_EXAMPLES OFF CACHE BOOL "Disable llama.cpp examples")
set(LLAMA_BUILD_SERVER OFF CACHE BOOL "Disable llama.cpp server")

# Add llama.cpp (now at project root)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../external/llama.cpp ${CMAKE_CURRENT_BINARY_DIR}/llama.cpp)

# DecoPlan LLM Library
add_library(decoplan_llm
    src/llm_wrapper.cpp
    src/multimodal_processor.cpp
)

target_include_directories(decoplan_llm
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/../external/llama.cpp/include
        ${CMAKE_CURRENT_SOURCE_DIR}/../external/llama.cpp/common
        ${CMAKE_CURRENT_SOURCE_DIR}/../external/llama.cpp/ggml/include
)

target_link_libraries(decoplan_llm
    PUBLIC
        llama
        common
)

# Examples
if(DECOPLAN_BUILD_EXAMPLES)
    add_executable(simple_inference examples/simple_inference.cpp)
    target_link_libraries(simple_inference PRIVATE decoplan_llm)

    add_executable(multimodal_inference examples/multimodal_inference.cpp)
    target_link_libraries(multimodal_inference PRIVATE decoplan_llm)
endif()
