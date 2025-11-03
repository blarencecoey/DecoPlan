#include "llm_wrapper.h"
#include "llama.h"
#include "common.h"
#include "sampling.h"

#include <thread>
#include <iostream>
#include <stdexcept>
#include <cstring>

namespace decoplan {

LLMWrapper::LLMWrapper()
    : model_(nullptr)
    , ctx_(nullptr)
    , sampler_(nullptr)
{}

LLMWrapper::~LLMWrapper() {
    cleanup();
}

bool LLMWrapper::initialize(const InferenceConfig& config) {
    config_ = config;

    // Initialize llama backend
    llama_backend_init();
    llama_numa_init(GGML_NUMA_STRATEGY_DISABLED);

    // Set up model parameters
    llama_model_params model_params = llama_model_default_params();
    model_params.n_gpu_layers = config.n_gpu_layers;
    model_params.use_mmap = config.use_mmap;
    model_params.use_mlock = config.use_mlock;

    // Load model
    std::cout << "Loading model from: " << config.model_path << std::endl;
    model_ = llama_load_model_from_file(config.model_path.c_str(), model_params);

    if (!model_) {
        std::cerr << "Failed to load model" << std::endl;
        return false;
    }

    // Set up context parameters
    llama_context_params ctx_params = llama_context_default_params();
    ctx_params.n_ctx = config.n_ctx;
    ctx_params.n_batch = config.n_batch;
    ctx_params.n_ubatch = config.n_ubatch;
    ctx_params.n_threads = config.n_threads > 0 ? config.n_threads : std::thread::hardware_concurrency();
    ctx_params.n_threads_batch = ctx_params.n_threads;

    // Create context
    ctx_ = llama_new_context_with_model(model_, ctx_params);

    if (!ctx_) {
        std::cerr << "Failed to create context" << std::endl;
        llama_free_model(model_);
        model_ = nullptr;
        return false;
    }

    // Set up sampler
    auto sparams = llama_sampler_chain_default_params();
    sampler_ = llama_sampler_chain_init(sparams);

    llama_sampler_chain_add(sampler_, llama_sampler_init_top_k(config.top_k));
    llama_sampler_chain_add(sampler_, llama_sampler_init_top_p(config.top_p, 1));
    llama_sampler_chain_add(sampler_, llama_sampler_init_temp(config.temperature));
    llama_sampler_chain_add(sampler_, llama_sampler_init_dist(config.seed));

    std::cout << "Model loaded successfully!" << std::endl;
    std::cout << "Context size: " << config.n_ctx << " tokens" << std::endl;

    return true;
}

void LLMWrapper::cleanup() {
    if (sampler_) {
        llama_sampler_free(sampler_);
        sampler_ = nullptr;
    }

    if (ctx_) {
        llama_free(ctx_);
        ctx_ = nullptr;
    }

    if (model_) {
        llama_free_model(model_);
        model_ = nullptr;
    }

    llama_backend_free();
}

std::vector<int> LLMWrapper::tokenize(const std::string& text, bool add_bos) {
    int n_tokens = text.length() + (add_bos ? 1 : 0) + 1;
    std::vector<int> tokens(n_tokens);

    auto vocab = llama_model_get_vocab(model_);

    n_tokens = llama_tokenize(
        vocab,
        text.c_str(),
        text.length(),
        tokens.data(),
        tokens.size(),
        add_bos,
        false  // special
    );

    if (n_tokens < 0) {
        tokens.resize(-n_tokens);
        n_tokens = llama_tokenize(
            vocab,
            text.c_str(),
            text.length(),
            tokens.data(),
            tokens.size(),
            add_bos,
            false
        );
    }

    tokens.resize(n_tokens);
    return tokens;
}

std::string LLMWrapper::detokenize(const std::vector<int>& tokens) {
    std::string result;
    result.reserve(tokens.size() * 4);  // Rough estimate

    auto vocab = llama_model_get_vocab(model_);

    for (int token : tokens) {
        char buf[256];
        int n = llama_token_to_piece(vocab, token, buf, sizeof(buf), 0, false);
        if (n > 0) {
            result.append(buf, n);
        }
    }

    return result;
}

std::string LLMWrapper::generate(const std::string& prompt) {
    if (!isLoaded()) {
        throw std::runtime_error("Model not loaded");
    }

    // Tokenize prompt
    auto tokens = tokenize(prompt, true);

    if (tokens.size() > (size_t)config_.n_ctx) {
        throw std::runtime_error("Prompt too long for context size");
    }

    // Create batch
    llama_batch batch = llama_batch_get_one(tokens.data(), tokens.size());

    // Decode prompt
    if (llama_decode(ctx_, batch) != 0) {
        throw std::runtime_error("Failed to decode prompt");
    }

    // Generate tokens
    std::vector<int> output_tokens;
    output_tokens.reserve(config_.n_predict);

    int n_cur = tokens.size();
    int n_decode = 0;

    auto vocab = llama_model_get_vocab(model_);

    while (n_decode < config_.n_predict) {
        // Sample next token
        int new_token_id = llama_sampler_sample(sampler_, ctx_, -1);

        // Check for EOS
        if (llama_vocab_is_eog(vocab, new_token_id)) {
            break;
        }

        output_tokens.push_back(new_token_id);

        // Prepare next batch
        batch = llama_batch_get_one(&new_token_id, 1);

        if (llama_decode(ctx_, batch) != 0) {
            std::cerr << "Failed to decode token" << std::endl;
            break;
        }

        n_decode++;
    }

    return detokenize(output_tokens);
}

void LLMWrapper::generateStreaming(const std::string& prompt, StreamCallback callback) {
    if (!isLoaded()) {
        throw std::runtime_error("Model not loaded");
    }

    // Tokenize prompt
    auto tokens = tokenize(prompt, true);

    if (tokens.size() > (size_t)config_.n_ctx) {
        throw std::runtime_error("Prompt too long for context size");
    }

    // Create batch
    llama_batch batch = llama_batch_get_one(tokens.data(), tokens.size());

    // Decode prompt
    if (llama_decode(ctx_, batch) != 0) {
        throw std::runtime_error("Failed to decode prompt");
    }

    // Generate tokens with streaming
    int n_decode = 0;

    auto vocab = llama_model_get_vocab(model_);

    while (n_decode < config_.n_predict) {
        // Sample next token
        int new_token_id = llama_sampler_sample(sampler_, ctx_, -1);

        // Check for EOS
        if (llama_vocab_is_eog(vocab, new_token_id)) {
            break;
        }

        // Detokenize and call callback
        std::vector<int> single_token = {new_token_id};
        std::string token_str = detokenize(single_token);
        callback(token_str);

        // Prepare next batch
        batch = llama_batch_get_one(&new_token_id, 1);

        if (llama_decode(ctx_, batch) != 0) {
            std::cerr << "Failed to decode token" << std::endl;
            break;
        }

        n_decode++;
    }
}

std::string LLMWrapper::getModelName() const {
    if (!model_) return "";

    char buf[256];
    llama_model_desc(model_, buf, sizeof(buf));
    return std::string(buf);
}

size_t LLMWrapper::getContextSize() const {
    if (!ctx_) return 0;
    return llama_n_ctx(ctx_);
}

} // namespace decoplan
