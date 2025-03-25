import streamlit as st
import requests
import json
import cv2
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile

# ✅ DeepSeek AI API Credentials
API_KEY = st.secrets["general"]["api_key"]  # Secure API Key Retrieval
SITE_URL = "https://yourwebsite.com"
SITE_NAME = "My AI Assistant"

# ✅ DeepSeek AI URL
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ✅ Initialize Text-to-Speech Engine (Jarvis Voice)
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Voice Speed
engine.setProperty('volume', 1.0)  # Volume

# ✅ Streamlit Page Config
st.set_page_config(page_title="Jarvis AI Assistant", page_icon="🤖")
st.title("🤖 Jarvis AI Assistant (With Voice + Face Detection)")

# ✅ DeepSeek AI Function
def get_deepseek_response(messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": SITE_URL,
        "X-Title": SITE_NAME,
    }

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": messages
    }

    response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        reply_text = response.json()["choices"][0]["message"]["content"]
        return reply_text
    else:
        return "⚠️ Sorry Sir, I couldn't understand that."

# ✅ Function: Text to Jarvis Voice (AI Will Speak)
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ✅ Function: Recognize Speech from User
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ **Jarvis Sun Raha Hai... Bolo Kuch!**")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            st.success(f"✅ Aapne Kaha: {text}")
            return text
        except sr.UnknownValueError:
            st.error("⚠️ Samajh Nahi Aaya! Dobara Bolo.")
            return None
        except sr.RequestError:
            st.error("⚠️ Speech Recognition Server Down!")
            return None

# ✅ Face Detection Function
def detect_face():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    st.write("🔍 **Jarvis Tumhari Shakal Pehchan Raha Hai...**")

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # ✅ Rectangle Draw Karega Face Pe
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Face Detection - Jarvis', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    st.success("✅ **Face Detection Closed!**")

# ✅ Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Start Conversation Button
if st.button("🎙️ Jarvis Se Baat Karo"):
    user_input = listen()

    if user_input:
        # ✅ Add User Message to Chat
        st.session_state.messages.append({"role": "user", "content": user_input})

        # ✅ Display User Message
        with st.chat_message("user"):
            st.markdown(user_input)

        # ✅ Get Response from DeepSeek AI
        with st.chat_message("assistant"):
            with st.spinner("🤔 Jarvis Soch Raha Hai..."):
                reply = get_deepseek_response(st.session_state.messages)
                st.markdown(reply)

                # ✅ AI Will Speak the Reply (Jarvis Style)
                speak(f"{reply}")

                # ✅ Add Assistant Message to Chat
                st.session_state.messages.append({"role": "assistant", "content": reply})

# ✅ Face Detection Button
if st.button("🧑‍💻 Detect Face"):
    detect_face()
