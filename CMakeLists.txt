cmake_minimum_required(VERSION 3.18)
project(DecoPlanLLM LANGUAGES CXX C)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Options
option(DECOPLAN_BUILD_EXAMPLES "Build example programs" ON)
option(DECOPLAN_USE_CUDA "Enable CUDA support" ON)

# Add llama.cpp
set(LLAMA_CUBLAS ${DECOPLAN_USE_CUDA} CACHE BOOL "Enable CUDA support in llama.cpp")
add_subdirectory(external/llama.cpp)

# DecoPlan LLM Library
add_library(decoplan_llm
    src/llm_wrapper.cpp
    src/multimodal_processor.cpp
)

target_include_directories(decoplan_llm
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/external/llama.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/external/llama.cpp/common
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
