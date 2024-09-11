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

## 5. API Creation
The API was implemented using FastAPI. For inference I am loading the GGUF file created in the notebook with Llamma.cpp. 

## 6. Containerization

## 7. CI/CD Pipeline with GitHub Actions
