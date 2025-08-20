import os
import json
import traceback
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQgenerator import combined_chain

load_dotenv()

with open("./Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

st.set_page_config(page_title="MCQ Creator", layout="centered")
st.title("📝 MCQ Generator App")

st.markdown(
    """
    This application allows you to generate multiple-choice questions (MCQs)
    from a PDF or text file using a Hugging Face model 🤗 and LangChain 🦜⛓️.
    """
)

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])
    mcq_count = st.number_input("Number of MCQs", min_value=1, max_value=50)
    subject = st.text_input("Subject", max_chars=20)
    difficulty = st.text_input(
        "Difficulty Level", max_chars=20, placeholder="Simple / Medium / Hard"
    )
    submit_btn = st.form_submit_button("Generate MCQs")

quiz_df = None

if submit_btn:
    if uploaded_file is None or not subject or not difficulty:
        st.warning("Please fill out all fields and upload a file.")
    else:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(uploaded_file)
                response = combined_chain(
                    {
                        "system_msg": "/no_think Answer very briefly and do not explain your reasoning.",
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "difficulty": difficulty,
                        "response_json": json.dumps(RESPONSE_JSON),
                    }
                )

                quiz = response.get("quiz")
                review = response.get("review")

                if quiz:
                    table_data = get_table_data(quiz)
                    if table_data:
                        quiz_df = pd.DataFrame(table_data)
                        quiz_df.index += 1
                    else:
                        st.error("Could not extract table data.")
                else:
                    st.error("No MCQ data returned.")

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error generating MCQs. Check logs for details.")

if quiz_df is not None:
    st.success("✅ MCQs ready! Click below to download.")
    csv_data = quiz_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download MCQs as CSV",
        data=csv_data,
        file_name="generated_mcqs.csv",
        mime="text/csv",
    )
