from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_model():

    pipe = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        device=0
    )

    return pipe


def ask_finance(question):

    model = load_model()

    prompt = f"""
You are a professional financial analyst.

Explain clearly in 5-6 sentences.

Question: {question}

Answer:
"""

    result = model(
        prompt,
        max_new_tokens=500,
        temperature=0.6,
        top_p=0.9,
        repetition_penalty=1.2,
        do_sample=True
    )

    text = result[0]["generated_text"]

    # remove prompt from output
    answer = text.replace(prompt, "")

    return answer.strip()