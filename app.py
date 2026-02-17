import streamlit as st
from huggingface_hub import InferenceClient
import os

# 🔑 Setup Hugging Face client
hf_client = InferenceClient(
    model="meta-llama/Llama-3.1-8B-Instruct",
    token=os.getenv("HF_TOKEN")
)

# 🌐 Page setup
st.set_page_config(page_title="Youth Mental Wellness", page_icon="🌱", layout="centered")

# Sidebar Navigation
page = st.sidebar.radio("📌 Navigate", ["Home", "Chat with AI", "Resources", "Emergency Help", "About"])

# 🚨 Crisis words
crisis_words = ["suicide", "self-harm", "kill myself", "hopeless"]

# ------------------ HOME ------------------
if page == "Home":
    st.title("🌱 Youth Mental Wellness")
    st.subheader("by PSYCHNOVA")
    st.subheader("Building resilience, Nurturing minds")
    st.write("👉 Use the sidebar to navigate. Start chatting with AI or explore resources.")

# ------------------ CHAT ------------------
elif page == "Chat with AI":
    st.title("🗨️ Confidential AI Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a kind, empathetic, supportive mental wellness guide for youth."}
        ]

    # Show chat history
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    user_input = st.chat_input("Type your message here...")

    if user_input:
        st.chat_message("user").write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # 🚨 Crisis detection
        if any(word in user_input.lower() for word in crisis_words):
            ai_reply = "⚠️ It seems you’re in distress. Please reach out immediately to a trusted person or local helpline."
        else:
            try:
                prompt = ""
                for msg in st.session_state.messages[-6:]:
                    prompt += f"{msg['role'].upper()}: {msg['content']}\n"

                response = hf_client.text_generation(
                    prompt,
                    max_new_tokens=200,
                    temperature=0.7
                )

                ai_reply = response

            except Exception as e:
                ai_reply = f"❌ Error: {str(e)}"

        st.chat_message("assistant").write(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# ------------------ RESOURCES ------------------
elif page == "Resources":
    st.title("📚 Resources for Mental Wellness")
    st.markdown("""
    - [Headspace: Mindfulness & Meditation](https://www.headspace.com/)  
    - [NAMI: National Alliance on Mental Illness](https://www.nami.org/Home)  
    - [WHO: Mental Health](https://www.who.int/health-topics/mental-health)  
    - [TED Talks on Mental Health](https://www.ted.com/topics/mental+health)  
    """)

# ------------------ HELP ------------------
elif page == "Emergency Help":
    st.title("🚨 Emergency Help")
    st.warning("If you are in crisis, please reach out immediately:")
    st.markdown("""
    - 📞 **US**: 988 (Suicide & Crisis Lifeline)  
    - 📞 **India**: +91-9582208181 (Snehi Helpline)  
    - 📞 **UK**: 116 123 (Samaritans)  
    """)

# ------------------ ABOUT ------------------
elif page == "About":
    st.title("ℹ️ About This Platform")
    st.write("""
    This is an **AI-powered youth mental wellness app** built with Generative AI.

    ✅ Confidential Chat  
    ✅ Helpful Resources  
    ✅ Emergency Contacts  
    ✅ Supportive & Stigma-Free  

    ⚠️ **Disclaimer:** This is not a substitute for professional medical advice.
    """) 

