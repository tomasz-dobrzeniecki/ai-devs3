import streamlit as st
import openai

openai.api_key = st.secrets["openai"]["api_key"]

st.title("AI do Ratowania Świata 🌍")

prompt = st.text_input("Zadaj pytanie sztucznej inteligencji")
try:
    if st.button("Wyślij"):
        response = openai.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "Answer the following question briefly and precisely. Provide only the answer, without additional explanation."},
                {"role": "user", "content": prompt}
            ]
        )
        st.write(response.choices[0].message.content)
except Exception as e:
    st.error(f"Wystąpił błąd: {e}")