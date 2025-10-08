#include "multimodal_processor.h"
#include "llama.h"
#include "llava.h"

#include <iostream>
#include <stdexcept>

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
    if (image_embed_) {
        llava_image_embed_free(image_embed_);
        image_embed_ = nullptr;
    }

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
    if (!clip_ctx_) {
        std::cerr << "Vision encoder not initialized" << std::endl;
        return false;
    }

    // Free previous image embed if exists
    if (image_embed_) {
        llava_image_embed_free(image_embed_);
        image_embed_ = nullptr;
    }

    // Load and encode image
    // This is model-specific - example for LLaVA
    // auto img = clip_image_load_from_file(image_path.c_str());
    // if (!img) {
    //     std::cerr << "Failed to load image: " << image_path << std::endl;
    //     return false;
    // }

    // image_embed_ = llava_image_embed_make_with_clip_img(clip_ctx_, img);
    // clip_image_free(img);

    // For now, just return true if we have a clip context
    return clip_ctx_ != nullptr;
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
