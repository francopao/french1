import streamlit as st
import json
import random
from gtts import gTTS
import os
from tracker import update_progress

st.set_page_config(layout="centered")
st.title("🇫🇷 French Trading Tutor")

mode = st.radio("Modo:", ["Commute", "Desk"])

with open("content/fx_fi_dialogues.json") as f:
    dialogs = json.load(f)

filtered = [d for d in dialogs if mode.lower() in d["mode"]]
dialog = random.choice(filtered)

st.subheader(f"{dialog['category']} | {dialog['topic']}")

# Audio
tts = gTTS(dialog["text"], lang="fr")
tts.save("audio/temp.mp3")
st.audio("audio/temp.mp3")

st.write(dialog["text"])
st.write("❓", dialog["question"])

if st.button("Marcar como completado"):
    update_progress(
        dialog_id=dialog["id"],
        keywords=dialog["keywords"],
        minutes=7 if mode == "Commute" else 12
    )
    st.success("Session guardada ✔️")
