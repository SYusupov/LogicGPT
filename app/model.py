from llama_cpp import Llama
import os

platypus_prompt = """
    Below is a question or task that requires logical reasoning to solve,
     along with additional context or information. Provide a detailed and
     well-reasoned response that demonstrates clear logical thinking.

    ### Question/Task:
    {}

    ### Input:
    {}

    ### Reasoned Response:
    {}"""

num_cores = os.cpu_count()
# n_threads = max(1, num_cores // 2)
# print('n_threads', n_threads)
# print('supports cuda: ', Llama.supports_cuda())

llm = Llama(
    model_path="/model_files/unsloth.Q4_K_M.gguf",
    use_mmap=True,
    # use_gpu=True,
    n_batch=4,
    n_threads=num_cores
)


def model_inference(instruction: str, input: str, max_tokens: int=200):

    input = platypus_prompt.format(
        instruction,
        input,
        ""  # output - leave this blank for generation!
    )

    output = llm(input, max_tokens=max_tokens, echo=True)
    return output
