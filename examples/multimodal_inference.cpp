#include "multimodal_processor.h"
#include <iostream>

int main(int argc, char** argv) {
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <model_path> <image_path> [prompt]" << std::endl;
        std::cerr << "Example: " << argv[0] << " models/llava-v1.6-34b.Q4_K_M.gguf floor_plan.jpg \"Describe this floor plan\"" << std::endl;
        return 1;
    }

    std::string model_path = argv[1];
    std::string image_path = argv[2];
    std::string prompt = argc > 3 ? argv[3] : "Describe this image in detail.";

    // Configure the multimodal model
    decoplan::MultimodalConfig config;
    config.model_path = model_path;
    config.clip_model_path = "";  // Set this if using separate mmproj file
    config.n_ctx = 4096;
    config.n_gpu_layers = -1;  // Use all GPU layers
    config.n_predict = 512;
    config.temperature = 0.7f;
    config.top_p = 0.9f;
    config.top_k = 40;

    // Initialize processor
    decoplan::MultimodalProcessor processor;

    std::cout << "Initializing multimodal model..." << std::endl;
    if (!processor.initialize(config)) {
        std::cerr << "Failed to initialize model" << std::endl;
        return 1;
    }

    std::cout << "\nImage: " << image_path << std::endl;
    std::cout << "Prompt: " << prompt << std::endl;
    std::cout << "\nGenerating response (streaming)..." << std::endl;
    std::cout << "---" << std::endl;

    try {
        // Use streaming callback to print tokens as they're generated
        processor.generateFromImageStreaming(
            image_path,
            prompt,
            [](const std::string& token) {
                std::cout << token << std::flush;
            }
        );
        std::cout << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error during generation: " << e.what() << std::endl;
        return 1;
    }

    std::cout << "---" << std::endl;

    return 0;
}
