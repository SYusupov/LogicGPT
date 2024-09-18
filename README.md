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
- I heard that LLMs do not perform well when answering logical reasoning and maths questions. I was curious if I could improve them by fine-tuning myself.
- Much preprocessing was done to the dataset to ensure a high quality, which includes:
   - pairs of sentences with similarity above 80% were removed, the similarity was computed with Sentence Transformers and using keyword search
   - questions similar to the questions in Hugging Face benchmark test sets were removed
- Change in performance across a variety of tasks can be evaluated.

### Fine-tuning Methodology
The finetuning was done using:
- Unsloth, a framework that facilitates and speeds up fine-tuning,
- SFTTrainer of HuggingFace, Supervised Fine-tuning Trainer
I used the **LoRA** approach for finetuning. The rank parameter was set at **16**. Larger values can be used to improve performance.
The finetuning is done in the notebook in [finetuning.ipynb](https://github.com/SYusupov/LogicGPT/blob/main/finetuning.ipynb) in Google Colab with the free NVIDIA T4 GPU.

## 4. Model Evaluation
To evaluate Mistral 7B before and after fine-tuning, I used the framework [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness). 

The setup for the evaluation of the **fine-tuned model** was as follows:

1. I launched the server with the model in GGUF format with [llama-cpp-python](https://github.com/abetlen/llama-cpp-python):

   ```bash
   python -m llama_cpp.server --model model/unsloth.Q4_K_M.gguf
   ```
2. Run the evaluation with lm-evaluation-harness passing the local server address of the model:
   ```bash
   lm_eval --model gguf --model_args base_url=http://localhost:8000 --tasks <task-name> --limit <number-of-questions> --log_samples --output_path '<results-output-path>'
   ```

To evaluate the original Mistral 7B **before fine-tuning**, I used Google Colab as it is faster, and the evaluation of both models is possible this way. 
The notebook is available at [evaluation/original_model_evaluation.ipynb](https://github.com/SYusupov/LogicGPT/blob/main/evaluation/original_model_evaluation.ipynb).

In particular, I evaluated both models on datasets similar to those on which the fine-tuning was done. They included science questions from the dataset [sciq]([url](https://huggingface.co/datasets/allenai/sciq)), comments generation for code from `codeXglue`, numerical calculations from `arithmetic`, reading comprehension questions from `mc_taco`, and logical reasoning questions from `logiqa`. 

The evaluation metrics were predefined by the framework, with outputs for `codeXglue` evaluated with **Smoothed BLEU-4**, and the rest of the datasets were evaluated with **Accuracy**. `codeXglue` is evaluated with Smoothed BLEU-4 because the output natural language generation so the outputs might not necessarily be the same. The metric looks at the usage of n-grams between expected and actual outputs without considering the order between them. In contrast, the other tasks are multiple-choice, like in the case of reading comprehension, or have discrete outputs like in the case of arithmetics tasks.

20 questions per programming language for `codeXglue` and 50 questions per question type for other datasets were asked from the 2 models (not the whole dataset due to time limitations). The datasets' results can be seen in the folder `evaluation`. They are visualized with the script `evaluation/visualization.ipynb`. 

<p align="center">
 <img src="images/accuracy_results.png" width="700"/>
</p>

As can be seen from the plot on accuracies, the Fine-tuned model either matches or outperforms the Original Model for many tasks. However for some of them the original had slightly (e.g. `mc_taco` and `arithmetic_2dm`) or much (e.g. `logiqa`) better performances. One explanation for that would be that training on various tasks at once affected performance on individual tasks, so there are generalization issues or there is overfitting.

<p align="center">
 <img src="images/codeXglue_results.png" width="700"/>
</p>

We can observe more significant improvements for the fine-tuned model in the code-related tasks. In every dataset, the Fine-tuned model significantly outperforms the Original model. The fine-tuning is especially good for code-to-text task in Go language, with around 5 times improvement. In contrast, the model performed worst for PHP language, though it is still much better than the original model.

## 5. API Creation
The API was implemented using FastAPI. For inference I am loading the GGUF file created in the notebook with Llamma.cpp. The GGUF file could not be loaded into this repository due to size limitations of 2GB. Therefore it is downloaded from Google Drive before running the API.

To run locally, Docker Hub credentials where the docker-image is stored, and the latest Docker-Image commit-id should be written in the file `.env`:
   ```bash
   DOCKERHUB_USERNAME=dockerhub_username
   DOCKERHUB_PASSWORD=dockerhub_password
   DOCKER_IMAGE_TAG=tag
   ```

And you should login to docker from the command prompt with `docker login`.

Also the model file should be downloaded with this command:
   ```bash
   python -m pip install gdown
   gdown 1WGmDmHXTCmIqYHL-Jla3GUgtz_yFgzk1 -O ./model_files/unsloth.Q4_K_M.gguf
   chmod -R 755 ./model_files
   ```

Then the API can be initialized with the command below. The API will be accessible at [http://localhost:8000/docs](http://localhost:8000/docs)
   ```bash
   docker compose -f compose.yaml up --build
   ```

Alternatively, the tests can be run with
   ```bash
   docker compose -f compose_test.yaml up --build
   ```

Don't forget to stop the API after you are done with `docker compose down`. 

A screenshot from the API with an output to a request can be seen in the image below.
<p align="center">
 <img src="images/app_screenshot.jpg" width="700"/>
</p>

## 6. Containerization
All the necessary packages and application deployment are included in `Dockerfile`. It is used in CI/CD Pipeline and during the location execution.

## 7. CI/CD Pipeline with GitHub Actions
The pipeline (`.github/workflows/ci.yaml`) includes all necessary steps, including linting the Python code, building the Docker image, downloading the model, starting the API, and running the tests. As can be seen from [this](https://github.com/SYusupov/LogicGPT/actions/runs/10907500609/job/30271295071) Github Actions page of one of the latest commits, all the jobs are running successfully.

In case no changes were made to Dockerfile, there is no need to build the docker-image again (takes around 10 minutes), therefore I included the option of not skipping the job `docker_build` in `.github/workflows/ci.yaml`. It can be done by:
1. setting the definition of `TO_BUILD_DOCKER` to `false` on line 17
2. setting the definition of `PREV_IMAGE_TAG` to the latest Docker image's tag on line 18, no need to change if not changed recently
3. comment line 81 (`needs: docker_build` in the job `test_api_with_model`), since we are not running `docker-build`.

Undo the above steps to rebuild and save a new Docker image.
