import openai
import streamlit as st
from openai import Completion
from streamlit_chat import message

openai.api_key = "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"

start_chat_log = '''You: Hello, how are you?
Noah: I am doing great.
You: What is your gender?
Noah: I am a male.
You: Who made you?
Noah: Jonah made me. I took 8 hours to develop!
You: Who developed you?
Noah: I was made by Jonah. I took 8 hours to develop!
'''


def append_interaction_to_chat_log(question, answer, log):
    log = f'{log}You: {question}\nNoah: {answer}\n'
    return log

def generate_response(question, log):
    prompt = f'{log}You: {question}\nNoah:'
    response = Completion.create(
        prompt=prompt, engine="text-davinci-003", stop=["\nYou:"], temperature=1,
        top_p=1, frequency_penalty=0, presence_penalty=0, best_of=1,
        max_tokens=1024)
    answer = response.choices[0].text.strip()
    return answer



st.title("Noah Chat")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def get_text():
    input_text = st.text_input("You:", "Hello, Noah! How are you?", key="input")
    return input_text


if 'log' not in st.session_state:
    st.session_state['log'] = '''You: Hello, how are you?
Noah: I am doing great.
You: What is your gender?
Noah: I am a male.
You: Who made you?
Noah: Jonah made me. I took 8 hours to develop!
You: Who developed you?
Noah: I was made by Jonah. I took 8 hours to develop!
'''

user_input = get_text()

if user_input:
    loge = st.session_state["log"]
    output = generate_response(user_input, loge)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
    log = append_interaction_to_chat_log(user_input, output, log=loge)
    print("APPEND LOG: " + log)
    st.session_state.log = log

if st.session_state['generated']:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
