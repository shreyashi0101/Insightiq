import streamlit as st
import requests
import random

API_URL = "https://insightiq-lah8.onrender.com/"

st.set_page_config(
    page_title="InsightIQ",
    page_icon="",
    layout="wide"
)

# -------------------------
# Session State
# -------------------------

if "stage" not in st.session_state:
    st.session_state.stage = "answer"

if "student_answer" not in st.session_state:
    st.session_state.student_answer = ""

if "probe" not in st.session_state:
    st.session_state.probe = ""

if "result" not in st.session_state:
    st.session_state.result = None

if "question_id" not in st.session_state:
    st.session_state.question_id = random.randint(1, 25)

# -------------------------
# Header
# -------------------------

st.title(" InsightIQ")
st.subheader(
    "Diagnostic Intelligence for Adaptive Assessment"
)

question_id = st.session_state.question_id

question_data = requests.get(
    f"{API_URL}/question/{question_id}"
).json()

# ====================================================
# STAGE 1 : ANSWER QUESTION
# ====================================================

if st.session_state.stage == "answer":

    st.markdown("## Assessment Question")

    st.info(
        question_data["question"]
    )

    answer = st.text_input(
        "Enter your answer"
    )

    if st.button("Submit Answer"):

        response = requests.post(
            f"{API_URL}/evaluate",
            json={
                "question_id": question_id,
                "student_answer": answer
            }
        ).json()

        if response["stage"] == "completed":

            st.success(
                "✅ Correct Answer!"
            )

        else:

            st.session_state.stage = "reasoning"

            st.session_state.student_answer = answer

            st.session_state.probe = response["probe"]

            st.rerun()

# ====================================================
# STAGE 2 : SOCRATIC INTERVIEW
# ====================================================

elif st.session_state.stage == "reasoning":

    st.markdown("## Socratic Follow-Up")

    st.warning(
        st.session_state.probe
    )

    reasoning = st.text_area(
        "Explain how you got your answer"
    )

    if st.button("Analyze Reasoning"):

        result = requests.post(
            f"{API_URL}/diagnose",
            json={
                "question_id": question_id,
                "student_answer":
                    st.session_state.student_answer,
                "reasoning": reasoning
            }
        ).json()

        st.session_state.result = result

        st.session_state.stage = "diagnosis"

        st.rerun()

# ====================================================
# STAGE 3 : DIAGNOSIS
# ====================================================

elif st.session_state.stage == "diagnosis":

    result = st.session_state.result

    ai = result["ai_analysis"]

    st.markdown("## Diagnostic Insight")

    st.error(
        "❌ Incorrect Answer"
    )

    st.write(
        "**Student Answer:**",
        result["student_answer"]
    )

    st.write(
        "**Correct Answer:**",
        result["correct_answer"]
    )

    st.write(
        "**Misconception:**",
        ai["misconception"]
    )

    st.write(
        "**Learning Gap:**",
        ai["learning_gap"]
    )

    st.write(
        "**Confidence:**",
        ai["confidence"]
    )

    st.progress(
        int(ai["confidence"] * 100)
    )

    st.divider()

    st.subheader("Teacher Insight")

    st.info(
        f"""
Learning Gap:
{ai['learning_gap']}

Misconception:
{ai['misconception']}

Recommended Next Assessment:
{result['next_recommended_skill']}
"""
    )

    st.divider()

    st.subheader("Adaptive Recommendation")

    st.success(
        result["next_recommended_skill"]
    )

    if st.button("Start New Assessment"):

        available_ids = list(range(1, 26))

        if st.session_state.question_id in available_ids:
            available_ids.remove(
                st.session_state.question_id
            )

        st.session_state.question_id = random.choice(
            available_ids
        )

        st.session_state.stage = "answer"

        st.session_state.student_answer = ""

        st.session_state.probe = ""

        st.session_state.result = None

        st.rerun()
