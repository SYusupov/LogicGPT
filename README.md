# LogicGPT
 
## 1. Model Selection
I chose to use the pre-trained LLM Mistral 7B, because of the following reasons:
- It can be quantized while still having a good performance, in terms of remembering a conversation, applying a context
- It can be run with GPU on most commercial computers, although in this project we are running the final inference on CPU
- It has a faster and better inference because of using a novel attention mechanism called Grouped Query Attention, increased attention heads, having a larger context length, and using a Key-Value cache.

## 2. Quantization
The quantization was performed to do the inference quickly on my local machine without a GPU. In particular, I used "q4_k_m". It is medium-sized and has a balanced quality. The quantization is done in `finetuning.ipynb`.

## 3. Model Fine-Tuning
### Dataset
For fine-tuning, I used the [Open-Platypus](https://huggingface.co/datasets/garage-bAInd/Open-Platypus) dataset. It consists of questions on Math, Science, reading comprehension, coding, and Logic.
The dataset was chosen because:
- I heard that LLMs do not show good performance for logical reasoning and maths questions. I was curious if I can improve them by finetuning myself.
- Much preprocessing was done to ensure a high-quality, which include:
   - pairs of sentences with similarity above 80% were removed, the similarity was computed with Sentence Transformers and using keyword search
   - questions similar to the questions in Hugging Face benchmark test sets were removed

### Fine-tuning Methodology
The finetuning was done using:
- Unsloth, a framework that facilitates and speeds up fine-tuning,
- SFTTrainer of HuggingFace, Supervised Fine-tuning Trainer
I used LoRA approach for finetuning. 
The finetuning is done in the notebook in `finetuning.ipynb` in Google Colab with the free NVIDIA T4 GPU.

## 4. Model Evaluation
To evaluate Mistral 7B before and after fine-tuning, I used the framework [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness). The setup for the evaluation of the **fine-tuned model** was as follows:

1. I launched the server with the model in GGUF format with [llama-cpp-python](https://github.com/abetlen/llama-cpp-python):

   ```bash
   python -m llama_cpp.server --model model/unsloth.Q4_K_M.gguf
   ```
2. Run the evaluation with lm-evaluation-harness by passing the local server address of the model:
   ```bash
   lm_eval --model gguf --model_args base_url=http://localhost:8000 --tasks arithmetic --limit 10 --log_samples --output_path 'finetuned_eval_arithmetic_results'
   ```

To evaluate the original Mistral 7B before fine-tuning, I used Google Colab as it is faster, and the evaluation of both models is possible this way. The notebook is available at `evaluation/original_model_evaluation.ipynb`.

## 5. API Creation
The API was implemented using FastAPI. For inference I am loading the GGUF file created in the notebook with Llamma.cpp. 

## 6. Containerization

## 7. CI/CD Pipeline with GitHub Actions
