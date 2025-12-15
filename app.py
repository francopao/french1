import streamlit as st
import json
import random
from gtts import gTTS
from io import BytesIO

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="French Trading Tutor",
    layout="centered"
)

st.title("🇫🇷 French Trading Tutor")

# --------------------------------------------------
# MODE
# --------------------------------------------------
mode = st.radio(
    "Selecciona modo:",
    ["Commute (audio)", "Desk (lectura)", "Review rápido"]
)

# --------------------------------------------------
# LOAD CONTENT
# --------------------------------------------------
with open("content/fx.json", "r", encoding="utf-8") as f:
    fx_data = json.load(f)

lesson = random.choice(fx_data)

# --------------------------------------------------
# CONTENT
# --------------------------------------------------
st.subheader("📈 Contexto FX")

if mode == "Commute (audio)":
    mp3_fp = BytesIO()
    tts = gTTS(lesson["text"], lang="fr")
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    st.audio(mp3_fp, format="audio/mp3")

st.markdown(f"**🗞️ Frase:** {lesson['text']}")
st.markdown(f"**❓ Pregunta:** {lesson['question']}")

if mode == "Review rápido":
    st.markdown("**🔑 Keywords:**")
    st.write(", ".join(lesson["keywords"]))
