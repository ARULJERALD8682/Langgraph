import streamlit as st
from Agents import structed_output_agent
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="Flight Searching Agent")

st.title("Flight Searching Agent")

st.markdown("Ask me about Flight Search Anywhere")

query = st.chat_input("Ask me")

if "chatbot" not in st.session_state:
    st.session_state.chatbot = structed_output_agent(api_key= gemini_api, model_name="gemini-1.5-flash")

if "bot" not in st.session_state:
    st.session_state.bot = st.session_state.chatbot()


if query:
    res = st.session_state.bot.invoke({"messages":[query]}, config={"configurable":{"thread_id":"abc"}})
    if res.get("final_response"):
        st.write(res.get("final_response"))
    else:
        st.write(res.get("messages")[-1].content)



