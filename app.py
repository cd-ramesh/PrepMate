import streamlit as st
import requests

API_URL = "http://localhost:3000/api/v1/prediction/840b62c4-f65e-4143-b30d-dec438f2002e"

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'input_disabled' not in st.session_state:
    st.session_state.input_disabled = False

st.set_page_config(page_title="PrepMate", page_icon="🤖")

st.title("PrepMate 🤖")
st.markdown("""
**PrepMate** is your AI-powered companion for acing placement preparations! Whether it's cracking interviews or clearing doubts, PrepMate is here to assist you every step of the way. Let's gear up for success together!
""")

def display_chat():
    for entry in st.session_state.chat_history:
        if entry['role'] == 'userMessage':
            st.markdown(f"""
            <div style='background-color: #dcf8c6; padding: 10px; border-radius: 10px; width: fit-content; margin-bottom: 10px;'><strong>You:</strong><br>{entry['content']}</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background-color: #ece5dd; padding: 10px; border-radius: 10px; width: fit-content; margin-bottom: 10px;'><strong>PrepMate:</strong><br>{entry['content']}</div>
            """, unsafe_allow_html=True)

display_chat()

user_input = st.text_input("Type your message here:", disabled=st.session_state.input_disabled)

if st.button("Send", disabled=st.session_state.input_disabled):
    if user_input:
        st.session_state.chat_history.append({'role': 'userMessage', 'content': user_input})
        st.session_state.input_disabled = True
        bot_response = query({"question": user_input, "history": st.session_state.chat_history})
        st.session_state.chat_history.append({'role': 'apiMessage', 
                                              'content': bot_response.get('text')})
        st.session_state.input_disabled = False
        st.experimental_rerun()

