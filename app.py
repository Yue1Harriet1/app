import streamlit as st
import pandas as pd
from typing import Dict
from utils import db

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "1QlPTiVvfRM82snGN6LELpNkOwVI1_Mp9J9xeJe-QoaA"
SHEET_NAME = "Database"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"










st.set_page_config(page_title="Bug report", page_icon="( ͡° ͜ʖ ͡°)", layout="centered")

st.title("( ͡° ͜ʖ ͡°) Bug report!")

gsheet_connector = connect_to_gsheet()

"""
st.sidebar.write(
    f"This app shows how a Streamlit app can interact easily with a [Google Sheet]({GSHEET_URL}) to read or store data."
)
"""

"""
st.sidebar.write(
    f"[Read more](https://docs.streamlit.io/knowledge-base/tutorials/databases/public-gsheet) about connecting your Streamlit app to Google Sheets."
)
"""

form = st.form(key="annotation")

with form:
    cols = st.columns((1, 1))
    author = cols[0].text_input("Report author:")
    bug_type = cols[1].selectbox(
        "Bug type:", ["Front-end", "Back-end", "Data related", "404"], index=2
    )
    comment = st.text_area("Comment:")
    cols = st.columns(2)
    date = cols[0].date_input("Bug date occurrence:")
    bug_severity = cols[1].slider("Bug severity:", 1, 5, 2)
    submitted = st.form_submit_button(label="Submit")


if submitted:
    add_row_to_gsheet(
        gsheet_connector, [[author, bug_type, comment, str(date), bug_severity]]
    )
    st.success("Thanks! Your bug was recorded.")
    st.balloons()

expander = st.expander("See all records")
with expander:
    st.write(f"Open original [Google Sheet]({GSHEET_URL})")
    st.dataframe(get_data(gsheet_connector))
