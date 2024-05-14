import streamlit as st
from streamlit_chat import message
from time import sleep  # Import sleep for demonstration purposes

# Call set_page_config() as the first command
st.set_page_config(page_title="KnowledgeBaseAI", page_icon=":sparkles:")

st.markdown("<h1 style='text-align: center;'>KnowledgeBaseAI</h1>", unsafe_allow_html=True)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]


if 'prompt_history' not in st.session_state:
    st.session_state['prompt_history'] = []

with st.sidebar:
    st.write("")  # Add some space at the top
    st.markdown("**Ninja History**")

    if st.session_state['prompt_history']:
        for i, prompt in enumerate(st.session_state['prompt_history']):
            st.text_area(f"Turtle {i + 1}:", value=prompt, height=20, key=f"prompt_{i}")

response_container = st.container()
container = st.container()

with container:
    st.write("")  # Add some space at the top

    with st.form(key='my_form', clear_on_submit=True):  # Avoid clearing the form on submit
        col1, col2 = st.columns([3, 1])  # Splitting the layout into two columns

        user_input = st.text_input("Ninja Turtle :", key='input')
        submit_button = st.form_submit_button(label='Send')

    if user_input:
        # Store user input in session state
        st.session_state['prompt_history'].append(user_input)

        st.session_state['past'].append(user_input)

        # Simulate response generation with sleep
        with st.spinner("Have patience Ninja, we are generating confidential details..."):
            sleep(2)  # Simulating response generation time
            from KBServer import generate_response

            output = generate_response(user_input)
            st.session_state['generated'].append(output)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user1')
            message(st.session_state["generated"][i], key=str(i))

