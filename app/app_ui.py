import streamlit as st
import requests

# Define the FastAPI URL (assuming it's running locally)
API_URL = "http://localhost:8000/ask"

# Streamlit UI configuration
st.title("LogicGPT Model Inference")
st.write("This interface allows you to interact with the LogicGPT model by providing instructions and optional input.")

# Create a form for the user to input data
with st.form(key="inference_form"):
    instruction = st.text_input("Instruction", placeholder="Enter your task or question here.")
    input_text = st.text_area("Input (Optional)", placeholder="Enter additional context or input here.")
    
    # Submit button for the form
    submit_button = st.form_submit_button(label="Ask the Model")

# When the form is submitted, make a POST request to the FastAPI app
if submit_button:
    if instruction.strip() == "":
        st.warning("Instruction is required to make a query!")
    else:
        with st.spinner("Fetching response from the model..."):
            # Send data to FastAPI app as JSON
            response = requests.post(API_URL, json={"instruction": instruction, "input": input_text})
            
            # Handle the response
            if response.status_code == 200:
                result = response.json()
                
                # Extract the Reasoned Response and completion tokens
                reasoned_response = result["choices"][0]["text"].split("### Reasoned Response:")[-1].strip()
                completion_tokens = result["usage"]["completion_tokens"]
                
                # Display the Reasoned Response and completion tokens
                st.success("Model response:")
                st.write(f"Reasoned Response: {reasoned_response}")
                st.write(f"Completion Tokens: {completion_tokens}")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
