from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

long_instruction = """
    Babe was a professional baseball player who was known both for his prowess
     at the plate and his perceived "heart of gold." One day, Babe was
     visiting a sick boy named Jimmy in the hospital. Babe was touched by
     Jimmy's will to live despite a very poor prognosis. In a moment of 
     weakness, Babe told Jimmy that in consideration of Jimmy's courage, he
     would do anything that Jimmy asked. Jimmy's eyes momentarily gleamed as
     he asked Babe to "hit a homer for me in your next game." Babe replied,
     "Sure kid." As Babe was leaving Jimmy's hospital room, Jimmy's father,
     Joe, pulled Babe aside and told Babe, "It would mean a lot to Jimmy if
     you would hit a home run for him in your next game. The medicinal value
     of raising Jimmy's spirits would be priceless." Babe replied, "Hey man,
     we all have problems. I don't work for the Make a Wish Foundation."
     Undaunted, Joe repeated that it would really raise Jimmy's spirits if
     Babe would hit a homer, and as incentive, Joe told Babe that he would pay
     Babe $ 5,000$ if Babe did hit a home run in his next game. Babe replied,
     "You've got a deal." To raise his chances of collecting the $ 5,000$ from
     Joe, Babe took extra batting practice before his next game, and the
     practice paid off because in his next game, Babe hit two home runs.
     During a post-game interview, Babe explained, "I did it for little Jimmy,
     who is in the hospital." After showering, Babe went directly to Joe's
     house and asked Joe for $ 5,000$. Babe's contract with his ball club
     does not forbid him from accepting money from fans for good performance.
     If Joe refuses to pay and Babe brings an action against Joe for damages,
     which of the following is correct under the modern trend in contract law?
     A. Babe can recover the $ 5,000$ because the preexisting duty rule does
     not apply where the duty is owed to a third person. B. Babe can recover
     the $ 5,000$ if he can prove that the value of the home run to Jimmy is
     at least $ 5,000$. C. Babe cannot recover from Joe because Babe had a
     preexisting duty to use his best efforts to hit home runs. D. Babe cannot
     recover from Joe because, even under the modern trend, moral
     consideration is not valid."""

# Test the root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

# Test valid model inference
def test_valid_inference():
    instruction = """
    How many four-digit numbers greater than 2999 can be formed such that the
     product of the middle two digits exceeds 5?"""
    input_text = ""
    response = client.post(
        "/ask",
        json={"instruction": instruction, "input": input_text}
    )

    assert response.status_code == 200
    response_data = response.text
    assert "Reasoned Response" in response_data
    # Check if there is text after "Reasoned Response:"
    reasoned_response_part = response_data.split("Reasoned Response:")[-1].strip()
    assert len(reasoned_response_part) > 0  # Ensure that the model generated some output

# Test inference with input provided
def test_inference_with_long_instruction_and_input():
    
    input_text = "Choose A, B, C or D as your solution."
    response = client.post(
        "/ask",
        json={"instruction": long_instruction, "input": input_text}
    )

    assert response.status_code == 200
    response_data = response.text
    assert "Reasoned Response" in response_data
    # Check if there is text after "Reasoned Response:"
    reasoned_response_part = response_data.split("Reasoned Response:")[-1].strip()
    assert len(reasoned_response_part) > 0

# Test inference with missing instruction
def test_inference_missing_instruction():
    input_text = "Choose A, B, C or D as your solution."
    response = client.post(
        "/ask",
        json={"instruction": "", "input": input_text}
    )

    assert response.status_code == 422  # FastAPI will return a 422 if required fields are missing or invalid

# Test inference with a long input text
def test_inference_with_long_input():
    response = client.post(
        "/ask",
        json={"instruction": long_instruction, "input": ""}
    )

    assert response.status_code == 200
    response_data = response.text
    assert "Reasoned Response" in response_data
    # Check if there is text after "Reasoned Response:"
    reasoned_response_part = response_data.split("Reasoned Response:")[-1].strip()
    assert len(reasoned_response_part) > 0

# Test an invalid request structure
def test_invalid_request_structure():
    response = client.post(
        "/ask",
        json={"invalid_field": "test"}
    )
    assert response.status_code == 422  # FastAPI should raise a 422 error for missing required fields

# Test when model returns no tokens (edge case)
def test_empty_model_response():
    instruction = ""
    input_text = ""
    response = client.post(
        "/ask",
        json={"instruction": instruction, "input": input_text}
    )
    
    assert response.status_code == 200
    response_data = response.text
    assert "Reasoned Response" in response_data
    # Check if there is text after "Reasoned Response:"
    reasoned_response_part = response_data.split("Reasoned Response:")[-1].strip()
    assert len(reasoned_response_part) > 0
