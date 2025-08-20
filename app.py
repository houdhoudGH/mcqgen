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

st.title("MCQs Creator Application with Hugging Face Model")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or TXT file")
    mcq_count = st.number_input("No. of MCQs", min_value=1, max_value=50)
    subject = st.text_input("Insert Subject", max_chars=20)
    difficulty = st.text_input("Difficulty", max_chars=20, placeholder="Simple")
    button = st.form_submit_button("Create MCQs")


if button and uploaded_file is not None and mcq_count and subject and difficulty:
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

            # Display MCQs
            quiz = response.get("quiz", None)
            if quiz:
                table_data = get_table_data(quiz)
                if table_data:
                    df = pd.DataFrame(table_data)
                    df.index += 1
                    st.subheader("Generated MCQs")
                    st.table(df)
                else:
                    st.error("Error processing quiz data")

            # Display review
            review = response.get("review", None)
            if review:
                st.subheader("Review / Feedback")
                st.text_area("Review", value=review, height=150)

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error generating quiz. Check logs for details.")
