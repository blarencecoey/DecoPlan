#pragma once

#include <string>
#include <vector>
#include <memory>
#include <functional>

struct llama_model;
struct llama_context;
struct gpt_params;
struct llama_sampler;

namespace decoplan {

struct InferenceConfig {
    std::string model_path;
    int n_ctx = 4096;              // Context size
    int n_gpu_layers = -1;         // -1 = all layers
    int n_batch = 512;             // Batch size for prompt processing
    int n_ubatch = 512;            // Batch size for generation
    int n_predict = 512;           // Number of tokens to predict
    float temperature = 0.7f;
    float top_p = 0.9f;
    int top_k = 40;
    int seed = -1;                 // -1 = random
    bool use_mmap = true;
    bool use_mlock = false;
    int n_threads = -1;            // -1 = auto-detect
};

class LLMWrapper {
public:
    LLMWrapper();
    ~LLMWrapper();

    // Delete copy constructor and assignment
    LLMWrapper(const LLMWrapper&) = delete;
    LLMWrapper& operator=(const LLMWrapper&) = delete;

    // Initialize the model
    bool initialize(const InferenceConfig& config);

    // Clean up resources
    void cleanup();

    // Synchronous inference
    std::string generate(const std::string& prompt);

    // Streaming inference with callback
    using StreamCallback = std::function<void(const std::string& token)>;
    void generateStreaming(const std::string& prompt, StreamCallback callback);

    // Check if model is loaded
    bool isLoaded() const { return model_ != nullptr; }

    // Get model info
    std::string getModelName() const;
    size_t getContextSize() const;

private:
    llama_model* model_;
    llama_context* ctx_;
    llama_sampler* sampler_;
    InferenceConfig config_;

    std::vector<int> tokenize(const std::string& text, bool add_bos);
    std::string detokenize(const std::vector<int>& tokens);
};

} // namespace decoplan
