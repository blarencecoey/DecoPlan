#include "llm_wrapper.h"
#include <iostream>

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <model_path> [prompt]" << std::endl;
        std::cerr << "Example: " << argv[0] << " models/llama-2-7b-chat.Q4_K_M.gguf \"Hello, how are you?\"" << std::endl;
        return 1;
    }

    std::string model_path = argv[1];
    std::string prompt = argc > 2 ? argv[2] : "Hello! Please tell me about yourself.";

    // Configure the model
    decoplan::InferenceConfig config;
    config.model_path = model_path;
    config.n_ctx = 4096;
    config.n_gpu_layers = -1;  // Use all GPU layers
    config.n_predict = 512;
    config.temperature = 0.7f;
    config.top_p = 0.9f;
    config.top_k = 40;

    // Initialize wrapper
    decoplan::LLMWrapper llm;

    std::cout << "Initializing model..." << std::endl;
    if (!llm.initialize(config)) {
        std::cerr << "Failed to initialize model" << std::endl;
        return 1;
    }

    std::cout << "\nModel: " << llm.getModelName() << std::endl;
    std::cout << "Context size: " << llm.getContextSize() << " tokens\n" << std::endl;

    // Generate response
    std::cout << "Prompt: " << prompt << std::endl;
    std::cout << "\nGenerating response..." << std::endl;
    std::cout << "---" << std::endl;

    try {
        std::string response = llm.generate(prompt);
        std::cout << response << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error during generation: " << e.what() << std::endl;
        return 1;
    }

    std::cout << "---" << std::endl;

    return 0;
}
