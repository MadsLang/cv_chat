import streamlit as st
import os
from openai import OpenAI

#
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

llm_client = OpenAI()
with open('cv.txt', 'r') as file:
    cv = file.read()
system_prompt = f"You are a helpful assistant. You must ONLY answer questions about this cv by Mads Lang Sørensen: {cv}"

user_name = 'you'

st.title("Ask a question about my CV!")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_history = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("For example: What is Mads' experience with NLP?"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message(user_name):
        st.markdown(prompt)

    with st.chat_message("CV-BOT", avatar="🤖"):
        message_placeholder = st.empty()
        response = ""

        with st.spinner():
            response = llm_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ]
            )

            st.session_state.chat_history += response.choices[0].message.content

        message_placeholder.markdown(
            response.choices[0].message.content,
            unsafe_allow_html=True
        )
    
    st.session_state.messages.append({"role": "CV-BOT", "content": response.choices[0].message.content})