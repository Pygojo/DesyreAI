import streamlit as st
import requests

# 1. YOUR PERMANENT CLOUD LINK
# We add /chat because that is the 'route' we created in Flask
COLAB_URL = "https://court-refinance-presented-hispanic.trycloudflare.com/chat"

st.set_page_config(page_title="Desyre Assistant", page_icon="🤖")

# --- SIDEBAR STATUS ---
with st.sidebar:
    st.title("System Status")
    try:
        # A quick check to see if the brain is online
        # Note: This only works if you added a 'GET' route to Flask,
        # but the chat will work regardless!
        st.success("Cloud Brain: Connected")
    except:
        st.error("Cloud Brain: Offline")

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

st.title("Desyre: AI Chat Assistant")

# 2. INITIALIZE CHAT HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. DISPLAY CHAT HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. USER INPUT & COMMUNICATION
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send the request to Google Colab
    with st.chat_message("assistant"):
        with st.status("Desyre is thinking...", expanded=False) as status:
            try:
                # We send the prompt to your static ngrok URL
                response = requests.post(
                    COLAB_URL, json={"prompt": prompt}, timeout=120
                )

                if response.status_code == 200:
                    answer = response.json().get("Desyre")
                    status.update(label="Response received!", state="complete")
                else:
                    answer = f"Error: Cloud returned status {response.status_code}"
                    status.update(label="Cloud Error", state="error")

            except Exception as e:
                answer = f"Connection Error: Is the Colab cell running? \n\n({e})"
                status.update(label="Connection Failed", state="error")

        # Show the final answer
        st.markdown(answer)

    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})
