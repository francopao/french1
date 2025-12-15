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

# ===== COMMUTE MODE =====
if mode == "Commute (audio)":
    mp3_fp = BytesIO()
    tts = gTTS(lesson["text"], lang="fr")
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    st.audio(mp3_fp, format="audio/mp3")

    st.markdown(f"**🗞️ Headline:** {lesson['text']}")

# ===== DESK MODE =====
elif mode == "Desk (lectura)":
    st.markdown(f"**🗞️ Market Brief:** {lesson['text']}")

    if "desk_phrase" in lesson:
        st.markdown(f"**🗣️ Desk talk:** _{lesson['desk_phrase']}_")

    st.markdown(f"**❓ Trader question:** {lesson['question']}")

    if "follow_up" in lesson:
        st.markdown(f"**🔮 Follow-up:** {lesson['follow_up']}")

# ===== REVIEW MODE =====
elif mode == "Review rápido":
    st.markdown("### 🔑 Keywords")
    st.write(", ".join(lesson.get("keywords", [])))

    st.markdown("### 🧠 Théorie clé")
    for t in lesson.get("theory", []):
        st.markdown(f"- {t}")
