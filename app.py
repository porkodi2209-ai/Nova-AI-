import os
import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="Nova AI", page_icon="🤖")

st.title("🤖 Nova AI")
st.caption("Your intelligent AI assistant")

# Get token from terminal
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    st.error("HF_TOKEN not found.")
    st.stop()

client = InferenceClient(
    api_key=HF_TOKEN,
    provider="groq"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your message...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": """
You are Nova AI, a helpful AI assistant.

Reply in Tamil or Tanglish when the user uses Tamil or Tanglish.
Reply in English when the user uses English.
Give simple explanations for programming and student questions.
"""
                        }
                    ] + st.session_state.messages,
                    max_tokens=1024,
                    temperature=0.7
                )

                answer = response.choices[0].message.content

                st.write(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error("Something went wrong.")
                st.write(str(e))