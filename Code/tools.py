import streamlit as st
import os
import textwrap
from IPython.display import display
from IPython.display import Markdown
import streamlit as st
import google.generativeai as genai

def tools():
    st.header("AI Tools")

    st.write("""
        Welcome to the AI tools page. Here you can interact with our AI tool.
    """)

    genai.configure(api_key=os.getenv("GeminiProKey"))
    model = genai.GenerativeModel('gemini-pro')

    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history = [])

    st.title("Your Personal AI Assistant")

    def role_to_streamlit(role):
        if role != "model":
            return role
        else:
            return "assistant"

    for message in st.session_state.chat.history:
        with st.chat_message(role_to_streamlit(message.role)):
            st.markdown((message.parts[0].text))

    if prompt := st.chat_input("What can I do for you?"):
        st.chat_message("user").markdown(prompt)
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        
if __name__ == "__main__":
    tools()
