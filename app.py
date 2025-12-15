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

# Función IA para generar un nuevo caso FX
def generate_new_fx_case(existing_lessons):
    """
    Genera UN nuevo caso FX/FI compatible con fx.json
    usando ejemplos reales como referencia de estilo.
    """

    # Tomamos 2–3 ejemplos reales para anclar estilo
    examples = random.sample(existing_lessons, min(3, len(existing_lessons)))

    examples_text = json.dumps(examples, ensure_ascii=False, indent=2)

    prompt = f"""
Tu es un trader FX & Fixed Income senior dans une banque européenne.

Tâche :
- Générer UN NOUVEAU cas de marché FX/FI.
- Même style, même structure que les exemples.
- Sujet réaliste (BCE, Fed, taux, FX, macro globale).
- Langage professionnel de trading desk.
- Pas de fiction, pas de storytelling.

IMPORTANT :
- Retourne UNIQUEMENT un objet JSON valide.
- Respecte STRICTEMENT cette structure.

Structure attendue :
{{
  "id": "...",
  "domain": ["FX", "Rates" ou "Macro"],
  "level": "...",
  "scenario": "...",
  "text": "...",
  "question": "...",
  "keywords": [...],
  "theory": [...],
  "desk_phrase": "...",
  "follow_up": "..."
}}

Exemples existants :
{examples_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    # Convertimos el JSON generado a dict Python
    new_case = json.loads(response.choices[0].message.content)

    return new_case

# Selector
use_ai_case = st.checkbox("🧠 Générer un nouveau cas avec l’IA", value=False)


# Función IA (bloque 4.3)

level = st.selectbox(
    "🎯 Nivel de francés:",
    ["Débutant total", "Intermédiaire", "Desk-ready"]
)
# NUEVO 


def generate_oral_question(level="beginner"):
    """
    Genera una pregunta oral FX / Monetary Policy / Fixed Income
    orientada a desk profesional.
    """

    prompt = f"""
Tu es un senior trader FX & Fixed Income à la BCE.

Objectif :
- Poser UNE question orale à un junior trader.
- Niveau : {level}
- Sujet : FX, politique monétaire, taux d’intérêt.
- Toujours relié à un événement de marché récent ou typique
  (BCE, Fed, inflation, croissance, surprises macro).

Contraintes :
- Question courte, orale, naturelle.
- Orientation pratique (impact marché).
- Pas de jargon académique inutile.

Exemple de structure :
"Suite à [événement], comment cela affecte-t-il
le taux de change et la courbe des taux ?"

Retourne UNIQUEMENT la question (en français).
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()

def speak(text):
    mp3_fp = BytesIO()
    tts = gTTS(text, lang="fr")
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    st.audio(mp3_fp, format="audio/mp3")

def evaluate_answer(question, user_answer, level="beginner"):
    """
    Evalúa respuesta como lo haría un desk head.
    """

    prompt = f"""
Tu es responsable du desk FX & Rates à la BCE.

Question posée :
{question}

Réponse du candidat :
{user_answer}

Évalue selon :
1. Compréhension macro
2. Lien politique monétaire → FX → taux
3. Logique de marché (pas théorie pure)
4. Clarté de l’expression (français professionnel)

Retour attendu :
- Verdict global (🟢 OK / 🟠 Moyen / 🔴 Insuffisant)
- 2–3 points forts/faibles
- Une reformulation idéale (courte)
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content




# --------------------------------------------------
# MODE
# --------------------------------------------------
#mode = st.radio(
#    "Selecciona modo:",
#    ["Commute (audio)", "Desk (lectura)", "Review rápido"]
#)
mode = st.radio(
    "Selecciona modo:",
    ["Commute (audio)", "Desk (lectura)", "Review rápido", "🎤 Oral Desk Training"]
)

# --------------------------------------------------
# LOAD CONTENT
# --------------------------------------------------
with open("content/fx.json", "r", encoding="utf-8") as f:
    fx_data = json.load(f)

if use_ai_case:
    lesson = generate_new_fx_case(fx_data)
else:
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

# ===== ORAL DESK TRAINING (NUEVO) =====
elif mode == "🎤 Oral Desk Training":
    st.subheader("🎧 Question du desk")

    if st.button("🎙️ Nouvelle question"):
        question = generate_oral_question(level=user_level)
        st.session_state["oral_question"] = question

    if "oral_question" in st.session_state:
        st.markdown(f"**Question :** {st.session_state['oral_question']}")
        speak(st.session_state["oral_question"])

        user_answer = st.text_area(
            "🗣️ Ta réponse (comme en entretien):",
            height=150
        )

        if st.button("📊 Évaluer ma réponse"):
            feedback = evaluate_answer(
                st.session_state["oral_question"],
                user_answer,
                level=user_level
            )
            st.markdown("### 🧠 Feedback du desk")
            st.markdown(feedback)


