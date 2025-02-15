import streamlit as st
import requests
import google.generativeai as genai
import speech_recognition as sr
from deep_translator import GoogleTranslator
from googletrans import Translator
from gtts import gTTS
import tempfile
import os
import datetime

# API Configuration
GEMINI_API_KEY = "AIzaSyBYJvAGWjDCVtFmPKgqPNFEwWAoAgf2WEU"
genai.configure(api_key=GEMINI_API_KEY)
translator = Translator()
recognizer = sr.Recognizer()

# User Authentication
USERNAME = "admin"
PASSWORD = "password"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "search_history" not in st.session_state:
    st.session_state.search_history = []

def login_page():
    st.set_page_config(page_title="🔐 Login | Slang Decoder", page_icon="🔑", layout="centered")
    st.title("🔐 Login to Slang Decoder")
    username = st.text_input("Enter Username:", placeholder="Enter your username")
    password = st.text_input("Enter Password:", type="password", placeholder="Enter your password")
    if st.button("Sign In"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Please try again!")

if not st.session_state.logged_in:
    login_page()
else:
    st.set_page_config(page_title="🌍 Slang Decoder Pro", page_icon="🔥", layout="wide")
    
    # Sidebar Navigation
    st.sidebar.title("🔄 Menu")
    if st.sidebar.button("🏠 Home"):
        st.sidebar.info("Coming Soon!")
    if st.sidebar.button("📜 Recent History"):
        if st.session_state.search_history:
            for entry in reversed(st.session_state.search_history):
                st.sidebar.markdown(f'<div title="{entry["date"].strftime("%Y-%m-%d %H:%M:%S")}">📌 {entry["search"]}</div>', unsafe_allow_html=True)
        else:
            st.sidebar.info("No recent history available.")
    if st.sidebar.button("⚙️ Settings"):
        st.sidebar.info("Coming Soon!")
    
    # Logout button at the bottom
    if st.sidebar.button("🔒 Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    # UI Header
    st.markdown("""
        <div style="text-align: center; background: #708090; padding: 20px; border-radius: 15px; color: white;">
            <h1>🔥 Slang Decoder Pro</h1>
            <p>Decode and translate slang phrases effortlessly!</p>
        </div>
    """, unsafe_allow_html=True)

    # Language Selection
    languages = {
        "English": "en", "Hindi (हिन्दी)": "hi", "Bengali (বাংলা)": "bn",
        "Telugu (తెలుగు)": "te", "Marathi (मराठी)": "mr", "Tamil (தமிழ்)": "ta",
        "Urdu (اردو)": "ur", "Gujarati (ગુજરાતી)": "gu", "Malayalam (മലയാളം)": "ml",
        "Kannada (ಕನ್ನಡ)": "kn", "Spanish (Español)": "es", "French (Français)": "fr",
        "German (Deutsch)": "de", "Chinese (中文)": "zh-cn", "Japanese (日本語)": "ja",
        "Russian (Русский)": "ru", "Korean (한국어)": "ko"
    }
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("🌎 Translate from:", list(languages.keys()))
    with col2:
        target_lang = st.selectbox("🎯 Translate to:", list(languages.keys()))
    
    # Input Mode Selection
    st.markdown("#### 🎧 Select Input Method")
    mode = st.radio("Choose an input method:", ["✍ Text Input", "🎤 Microphone Input", "🎵 Audio File Input"], horizontal=True)
    
    # Functions
    def get_slang_meaning(sentence):
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(f"Explain this slang phrase in simple terms: {sentence}")
            return response.text.strip().split("\n")[0]
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def translate_text(text, src, dest):
        try:
            return GoogleTranslator(source=src, target=dest).translate(text)
        except Exception as e:
            return f"❌ Translation Error: {str(e)}"
    
    def text_to_speech(text, lang):
        try:
            tts = gTTS(text=text, lang=lang)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_file.name)
            return temp_file.name
        except Exception as e:
            return None
    
    def speech_to_text(audio_file, lang):
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio_data, language=lang)
            except Exception as e:
                return f"❌ Speech Recognition Error: {str(e)}"
    
    def record_audio():
        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except Exception as e:
            return f"❌ Speech Recognition Error: {str(e)}"
    
    detected_text = ""
    if mode == "✍ Text Input":
        user_input = st.text_area("Enter your slang phrase here:")
        detected_text = user_input
    elif mode == "🎵 Audio File Input":
        audio_file = st.file_uploader("Upload an audio file (WAV/MP3):", type=["wav", "mp3"])
        if audio_file:
            detected_text = speech_to_text(audio_file, languages[source_lang])
            st.write(f"🗣 Detected Speech: {detected_text}")
    elif mode == "🎤 Microphone Input":
        if st.button("🎤 Record from Microphone"):
            detected_text = record_audio()
            st.write(f"🗣 Detected Speech: {detected_text}")
    
    if detected_text:
        if "❌" not in detected_text:
            translated_text = translate_text(detected_text, languages[source_lang], "en")
            slang_meaning = get_slang_meaning(translated_text)
            final_translation = translate_text(slang_meaning, "en", languages[target_lang])
            st.success(f"💬 Meaning in {target_lang}: {final_translation}")
            st.session_state.search_history.append({"date": datetime.datetime.now(), "search": detected_text})
            audio_path = text_to_speech(final_translation, languages[target_lang])
            if audio_path:
                st.audio(audio_path, format="audio/mp3")
                os.remove(audio_path)
        else:
            st.warning("⚠ Could not process input. Please try again!")
    
    st.markdown("---")
    st.markdown("👨‍💻 Built with ❤ using Streamlit, Gemini AI, Google Translate & Speech Recognition")
