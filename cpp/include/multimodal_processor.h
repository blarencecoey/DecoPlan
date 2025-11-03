#pragma once

#include "llm_wrapper.h"
#include <string>
#include <vector>

struct clip_ctx;
struct llava_image_embed;

namespace decoplan {

struct MultimodalConfig : public InferenceConfig {
    std::string clip_model_path;  // Path to vision encoder (mmproj file)
};

class MultimodalProcessor {
public:
    MultimodalProcessor();
    ~MultimodalProcessor();

    // Delete copy constructor and assignment
    MultimodalProcessor(const MultimodalProcessor&) = delete;
    MultimodalProcessor& operator=(const MultimodalProcessor&) = delete;

    // Initialize with multimodal model
    bool initialize(const MultimodalConfig& config);

    // Clean up resources
    void cleanup();

    // Process image + text prompt
    std::string generateFromImage(
        const std::string& image_path,
        const std::string& prompt
    );

    // Streaming version
    void generateFromImageStreaming(
        const std::string& image_path,
        const std::string& prompt,
        LLMWrapper::StreamCallback callback
    );

    // Check if initialized
    bool isLoaded() const;

private:
    std::unique_ptr<LLMWrapper> llm_;
    clip_ctx* clip_ctx_;
    llava_image_embed* image_embed_;
    MultimodalConfig config_;

    bool loadImage(const std::string& image_path);
};

} // namespace decoplan
