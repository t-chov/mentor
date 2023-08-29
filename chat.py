import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema import HumanMessage


openai_api_key = st.secrets['openai']['api_key']
chat = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    role = "human" if isinstance(msg, HumanMessage) else "ai"
    st.chat_message(role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("human").write(prompt)
    res = chat.predict_messages(st.session_state.messages)
    st.session_state.messages.append(res)
    st.chat_message("ai").write(res.content)
