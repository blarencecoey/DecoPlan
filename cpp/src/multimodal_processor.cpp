#include "multimodal_processor.h"
#include "llama.h"

#include <iostream>
#include <stdexcept>
#include <fstream>

// Note: Full multimodal support requires llama.cpp's MTMD (multimodal) tools
// For now, this is a simplified text-only implementation
// TODO: Integrate with llama.cpp/tools/mtmd for vision support

namespace decoplan {

MultimodalProcessor::MultimodalProcessor()
    : llm_(nullptr)
    , clip_ctx_(nullptr)
    , image_embed_(nullptr)
{}

MultimodalProcessor::~MultimodalProcessor() {
    cleanup();
}

bool MultimodalProcessor::initialize(const MultimodalConfig& config) {
    config_ = config;

    // Initialize the LLM wrapper
    llm_ = std::make_unique<LLMWrapper>();

    InferenceConfig llm_config;
    llm_config.model_path = config.model_path;
    llm_config.n_ctx = config.n_ctx;
    llm_config.n_gpu_layers = config.n_gpu_layers;
    llm_config.n_batch = config.n_batch;
    llm_config.n_ubatch = config.n_ubatch;
    llm_config.n_predict = config.n_predict;
    llm_config.temperature = config.temperature;
    llm_config.top_p = config.top_p;
    llm_config.top_k = config.top_k;
    llm_config.seed = config.seed;
    llm_config.n_threads = config.n_threads;

    if (!llm_->initialize(llm_config)) {
        std::cerr << "Failed to initialize LLM" << std::endl;
        return false;
    }

    // Load CLIP model for vision encoding
    if (!config.clip_model_path.empty()) {
        std::cout << "Loading vision encoder from: " << config.clip_model_path << std::endl;

        // Note: You'll need to implement this based on the specific multimodal model
        // For LLaVA, this would load the mmproj file
        // This is a placeholder - actual implementation depends on llama.cpp's multimodal API

        // clip_ctx_ = clip_model_load(config.clip_model_path.c_str(), /* verbosity */ 1);

        if (!clip_ctx_) {
            std::cerr << "Note: Vision encoder not loaded. Text-only mode." << std::endl;
            // Don't fail - allow text-only usage
        } else {
            std::cout << "Vision encoder loaded successfully!" << std::endl;
        }
    }

    return true;
}

void MultimodalProcessor::cleanup() {
    // TODO: Free image_embed_ when MTMD integration is complete
    if (image_embed_) {
        // llava_image_embed_free(image_embed_);
        image_embed_ = nullptr;
    }

    // TODO: Free clip_ctx_ when MTMD integration is complete
    if (clip_ctx_) {
        // clip_free(clip_ctx_);
        clip_ctx_ = nullptr;
    }

    if (llm_) {
        llm_->cleanup();
        llm_.reset();
    }
}

bool MultimodalProcessor::loadImage(const std::string& image_path) {
    // TODO: Implement image loading with llama.cpp MTMD tools
    // For now, just verify the image file exists

    std::ifstream file(image_path, std::ios::binary);
    if (!file.good()) {
        std::cerr << "Image file not found: " << image_path << std::endl;
        return false;
    }

    // TODO: When MTMD is integrated:
    // 1. Load image using clip_image_u8_init() and load from file
    // 2. Preprocess with clip_image_preprocess()
    // 3. Encode with clip_image_batch_encode()
    // 4. Store embeddings for use in generation

    std::cout << "Note: Image loading placeholder - full vision support coming soon" << std::endl;
    std::cout << "Image file verified: " << image_path << std::endl;

    return true;
}

std::string MultimodalProcessor::generateFromImage(
    const std::string& image_path,
    const std::string& prompt
) {
    if (!isLoaded()) {
        throw std::runtime_error("Multimodal processor not initialized");
    }

    // Load and encode the image
    if (clip_ctx_ && !loadImage(image_path)) {
        throw std::runtime_error("Failed to load image: " + image_path);
    }

    // For multimodal models, you would typically:
    // 1. Encode the image using CLIP/vision encoder
    // 2. Construct a prompt with image embeddings
    // 3. Generate text conditioned on both image and text

    // This is a simplified version - actual implementation depends on the model
    std::string full_prompt;
    if (clip_ctx_) {
        // Format for LLaVA-style models
        full_prompt = "USER: <image>\n" + prompt + "\nASSISTANT: ";
    } else {
        // Text-only fallback
        full_prompt = prompt;
    }

    return llm_->generate(full_prompt);
}

void MultimodalProcessor::generateFromImageStreaming(
    const std::string& image_path,
    const std::string& prompt,
    LLMWrapper::StreamCallback callback
) {
    if (!isLoaded()) {
        throw std::runtime_error("Multimodal processor not initialized");
    }

    // Load and encode the image
    if (clip_ctx_ && !loadImage(image_path)) {
        throw std::runtime_error("Failed to load image: " + image_path);
    }

    // Construct prompt
    std::string full_prompt;
    if (clip_ctx_) {
        full_prompt = "USER: <image>\n" + prompt + "\nASSISTANT: ";
    } else {
        full_prompt = prompt;
    }

    llm_->generateStreaming(full_prompt, callback);
}

bool MultimodalProcessor::isLoaded() const {
    return llm_ && llm_->isLoaded();
}

} // namespace decoplan
