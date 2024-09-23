import requests

# Replace FastAPI's TestClient with actual HTTP calls to the running Ollama server
ollama_url = "http://localhost:11434/api/generate"

# Long instruction (Babe Ruth example) to be used in testing
long_instruction = '''Babe was a baseball player known for his prowess at the plate and 
his "heart of gold." One day, he visited a sick boy Jimmy in the hospital. 
Touched by Jimmy's courage despite a poor prognosis, Babe told Jimmy 
he would do anything Jimmy asked. Jimmy asked Babe to 'hit a homer for me 
in your next game.' Babe replied, 'Sure.' As he left, Jimmy's father, 
Joe, pulled Babe aside, saying, "It would mean a lot to Jimmy if you 
hit a home run in your next game. The medicinal value of raising Jimmy's 
spirits would be priceless." Babe replied, "We all have problems. I don't 
work for the Make a Wish Foundation." Joe insisted it would help 
Jimmy and offered Babe $5,000 if he hit a home run. Babe agreed. Babe 
practiced extra before the next game and hit two home runs. During a post-game 
interview, Babe said, "I did it for little Jimmy." Afterward, Babe 
went to Joe's house to ask for the $5,000. Babe's contract with his ball 
club does not forbid accepting money from fans for good performance. If Joe 
refuses to pay and Babe sues for damages, which of the following is 
correct under modern contract law?
A. Babe can recover the $5,000 because the preexisting duty rule does 
not apply where the duty is owed to a third person.
B. Babe can recover the $5,000 if he proves the value of the home run 
to Jimmy is at least $5,000.
C. Babe cannot recover because he had a preexisting duty to use his 
best efforts to hit home runs.
D. Babe cannot recover because moral consideration is not valid.'''

def generate_request(payload):
    """Helper function to interact with Ollama model."""
    response = requests.post(ollama_url, json=payload)
    return response

def test_inference_with_long_instruction_and_input():
    """Test inference with long instruction and additional input."""
    input_text = "Choose A, B, C, or D as your solution."
    payload = {
        "model": "mistral",  # Assuming your Ollama model name is mistral
        "prompt": f"### Question/Task:\n{long_instruction}\n### Input:\n{input_text}\n### Reasoned Response:"
    }
    response = generate_request(payload)

    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    assert len(response_data["response"]) > 0

def test_inference_with_long_instruction_no_input():
    """Test inference with long instruction but no additional input."""
    payload = {
        "model": "mistral",
        "prompt": f"### Question/Task:\n{long_instruction}\n### Input:\n\n### Reasoned Response:"
    }
    response = generate_request(payload)

    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    assert len(response_data["response"]) > 0

def test_empty_instruction():
    """Test inference with an empty instruction."""
    input_text = "Choose A, B, C, or D as your solution."
    payload = {
        "model": "mistral",
        "prompt": f"### Question/Task:\n\n### Input:\n{input_text}\n### Reasoned Response:"
    }
    response = generate_request(payload)

    # Expecting an error or empty response if no instruction is provided
    assert response.status_code == 200
    response_data = response.json()
    assert "error" in response_data or len(response_data["response"]) == 0

def test_invalid_request_structure():
    """Test inference with invalid request structure."""
    payload = {
        "invalid_field": "test"  # Sending invalid structure
    }
    response = generate_request(payload)

    assert response.status_code == 400  # Expecting a 400 Bad Request

def test_empty_model_response():
    """Test when the model returns no tokens (edge case)."""
    payload = {
        "model": "mistral",
        "prompt": f"### Question/Task:\n\n### Input:\n\n### Reasoned Response:"
    }
    response = generate_request(payload)

    # Expecting an empty response
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    assert len(response_data["response"]) == 0  # Empty response expected

def test_valid_inference():
    """Test valid inference with an example question."""
    instruction = """
    How many four-digit numbers greater than 2999 can be formed such that the
    product of the middle two digits exceeds 5?"""
    payload = {
        "model": "mistral",
        "prompt": f"### Question/Task:\n{instruction}\n### Input:\n\n### Reasoned Response:"
    }
    response = generate_request(payload)

    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    assert len(response_data["response"]) > 0

