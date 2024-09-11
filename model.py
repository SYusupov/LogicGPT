from llama_cpp import Llama

llm = Llama(
    model_path="./model/unsloth.Q4_K_M.gguf"
)

def model_inference(instruction: str, input: str):
    platypus_prompt = """Below is a question or task that requires logical reasoning to solve, along with additional context or information. Provide a detailed and well-reasoned response that demonstrates clear logical thinking.

    ### Question/Task:
    {}

    ### Input:
    {}

    ### Reasoned Response:
    {}"""

    input = platypus_prompt.format(
            # "What is a famous tall tower in Paris?", # instruction
            instruction,
            # "", # input
            input,
            "", # output - leave this blank for generation!
        )
    
    output = llm(input, max_tokens=100, echo=True)
    return output