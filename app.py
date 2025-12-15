import streamlit as st
import json
import random
from gtts import gTTS
from io import BytesIO
from openai import OpenAI


# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="French Trading Tutor",
    layout="centered"
)

st.title("🇫🇷 French Trading Tutor")

# Función IA (bloque 4.3)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def adapt_lesson_with_ai(lesson_text, level):
    prompt = f"""
Tu es un formateur FX et Fixed Income pour un trading desk européen.

Objectif :
- Adapter le texte pour un étudiant qui ne parle pas français.
- Garder STRICTEMENT le contexte FX / macro / taux.
- Langage simple, phrases courtes.
- Pas de concepts nouveaux.

Niveau de l'étudiant : {level}

Texte original :
{lesson_text}


Donne une version adaptée en français.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

# Función IA (bloque 4.3)

level = st.selectbox(
    "🎯 Nivel de francés:",
    ["Débutant total", "Intermédiaire", "Desk-ready"]
)


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

# Uso de IA SOLO cuando tenga sentido
display_text = lesson["text"]

if level == "Débutant total":
    display_text = adapt_lesson_with_ai(lesson["text"], level)


# --------------------------------------------------
# CONTENT
# --------------------------------------------------
st.subheader("📈 Contexto FX")

# ===== COMMUTE MODE =====
if mode == "Commute (audio)":
    mp3_fp = BytesIO()
    tts = gTTS(display_text, lang="fr")
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    st.audio(mp3_fp, format="audio/mp3")

    st.markdown(f"**🗞️ Headline:** {display_text}")

# ===== DESK MODE =====
elif mode == "Desk (lectura)":
    st.markdown(f"**🗞️ Market Brief:** {display_text}")

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

