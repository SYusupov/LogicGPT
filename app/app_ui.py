import requests
import json
import streamlit as st

# Define the platypus_prompt
platypus_prompt = """
Below is a question or task that requires logical reasoning to solve,
along with additional context or information. Provide a detailed and
well-reasoned response that demonstrates clear logical thinking.

### Question/Task:
{}

### Input:
{}

### Reasoned Response:
"""

def generate_response(prompt, model='finetuned_mistral'):
    url = 'http://ollama:11434/api/generate'
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": model,
        "prompt": prompt
    }
    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
    
    for line in response.iter_lines():
        if line:
            # Each line is a JSON object
            json_data = json.loads(line.decode('utf-8'))
            word = json_data.get('response', '')
            done = json_data.get('done', False)
            if word:
                # Yield words or tokens as they come
                yield word
            if done:
                break

def main():
    st.title("Streamlit Chatbot with Ollama")

    # Initialize session state to store the conversation
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Input form for user to type their message
    with st.form(key='chat_form'):
        question_task = st.text_area("Question/Task:", key='question_task')
        input_text = st.text_area("Input (optional):", key='input_text')
        submit_button = st.form_submit_button(label='Send')

    # Error if both fields are empty
    if submit_button and not question_task and not input_text:
        st.error("Please provide a 'Question/Task' before sending.")

    if submit_button and question_task:
        # Construct the prompt using platypus_prompt
        prompt = platypus_prompt.format(question_task, input_text if input_text else '')

        # Append user's message to the conversation
        st.session_state['messages'].append({
            'sender': 'user',
            'question_task': question_task,
            'input_text': input_text if input_text else None  # Handle empty input case
        })

        # Placeholder for the bot's response
        bot_message_placeholder = st.empty()

        # Generate the bot's response and display it word by word
        bot_response = ''
        for word in generate_response(prompt):
            bot_response += word
            # Update the placeholder with the new bot response
            bot_message_placeholder.markdown(f"**Bot:** {bot_response}")
        
        # Append bot's response to the conversation
        st.session_state['messages'].append({'sender': 'bot', 'text': bot_response})

    # Display conversation history in grey with horizontal lines between each response
    
    if st.session_state['messages']:
        st.markdown("### History")
        st.markdown("---")
    
    for message in st.session_state['messages']:
        if message['sender'] == 'user':
            st.markdown(f"<span style='color: grey;'>**Question/Task:** {message['question_task']}</span>", unsafe_allow_html=True)
            if message['input_text']:
                st.markdown(f"<span style='color: grey;'>**Input:** {message['input_text']}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color: grey;'>**Bot:** {message['text']}</span>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
