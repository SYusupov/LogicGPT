from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

long_instruction = ''\
    'Babe was a baseball player known for his prowess at the plate and '\
    'his '\
    '"heart of gold." One day, he visited a sick boy Jimmy in the hospital. '\
    "Touched by Jimmy's courage despite a poor prognosis, Babe told Jimmy "\
    "he "\
    "would do anything Jimmy asked. Jimmy asked Babe to 'hit a homer for me "\
    "in your next game.' Babe replied, 'Sure.' As he left, Jimmy's father, "\
    'Joe, pulled Babe aside, saying, "It would mean a lot to Jimmy if you '\
    'hit'\
    " a home run in your next game. The medicinal value of raising Jimmy's "\
    'spirits would be priceless." Babe replied, "We all have problems. I '\
    'dont'\
    ' work for the Make a Wish Foundation." Joe insisted it would help '\
    'Jimmy '\
    'and offered Babe $5,000 if he hit a home run. Babe agreed. Babe '\
    'practiced'\
    'extra before the next game and hit two home runs. During a post-game '\
    'interview, Babe said, "I did it for little Jimmy." Afterward, Babe '\
    'went '\
    "to Joe's house to ask for the $5,000. Babe's contract with his ball "\
    "club "\
    "does not forbid accepting money from fans for good performance. If Joe "\
    'refuses to pay and Babe sues for damages, which of the following is '\
    'correct under modern contract law?'\
    'A. Babe can recover the $5,000 because the preexisting duty rule does '\
    'not apply where the duty is owed to a third person.'\
    'B. Babe can recover the $5,000 if he proves the value of the home run '\
    'to Jimmy is at least $5,000.'\
    'C. Babe cannot recover because he had a preexisting duty to use his '\
    'best'\
    'efforts to hit home runs.'\
    'D. Babe cannot recover because moral consideration is not valid.'\



def test_read_root():
    # Test the root endpoint
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_valid_inference():
    # Test valid model inference
    instruction = """
    How many four-digit numbers greater than 2999 can be formed such that the
     product of the middle two digits exceeds 5?"""
    response = client.post(
        "/ask",
        params={"instruction": instruction}
    )

    assert response.status_code == 200
    response_data = response.text
    assert "Reasoned Response" in response_data
    # Check if there is text after "Reasoned Response:"
    reasoned_response_part = response_data.split(
        "Reasoned Response:")[-1].strip()
    # Ensure that the model generated some output
    assert len(reasoned_response_part) > 0


def test_inference_with_long_instruction_and_input():
    # Test inference with input provided

    input_text = "Choose A, B, C or D as your solution."
    response = client.post(
        "/ask",
        params={"instruction": long_instruction, "input": input_text}
    )

    assert response.status_code == 200
    response_data = response.text
    assert "Reasoned Response" in response_data
    # Check if there is text after "Reasoned Response:"
    reasoned_response_part = response_data.split(
        "Reasoned Response:")[-1].strip()
    assert len(reasoned_response_part) > 0


def test_inference_missing_instruction():
    # Test inference with missing instruction
    input_text = "Choose A, B, C or D as your solution."
    response = client.post(
        "/ask",
        params={"input": input_text}
    )

    # FastAPI will return a 422 if required fields are missing or invalid
    assert response.status_code == 422


def test_inference_with_long_input():
    # Test inference with a long input text
    response = client.post(
        "/ask",
        params={"instruction": long_instruction}
    )

    assert response.status_code == 200
    response_data = response.text
    assert "Reasoned Response" in response_data
    # Check if there is text after "Reasoned Response:"
    reasoned_response_part = response_data.split(
        "Reasoned Response:")[-1].strip()
    assert len(reasoned_response_part) > 0


def test_invalid_request_structure():
    # Test an invalid request structure
    response = client.post(
        "/ask",
        params={"invalid_field": "test"}
    )

    # FastAPI should raise a 422 error for missing required fields
    assert response.status_code == 422


def test_empty_model_response():
    # Test when model returns no tokens (edge case)
    instruction = ""
    input_text = ""
    response = client.post(
        "/ask",
        params={"instruction": instruction, "input": input_text}
    )

    assert response.status_code == 200
    response_data = response.text
    assert "Reasoned Response" in response_data
    # Check if there is text after "Reasoned Response:"
    reasoned_response_part = response_data.split(
        "Reasoned Response:")[-1].strip()
    assert len(reasoned_response_part) > 0
