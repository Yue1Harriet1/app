from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import streamlit as st


@st.experimental_singleton()
def connect_to_gsheet():
    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[SCOPE],
    )

    service = build("sheets", "v4", credentials=credentials)
    gsheet_connector = service.spreadsheets()
    return gsheet_connector

def get_gsheet_data(connector) -> pd.DataFrame:
    values = (
        connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:E",
        )
        .execute()
    )

    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    return df

def add_row_to_gsheet(connector, row) -> None:
    values = (
        connector.values()
        .append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:E",
            body=dict(values=row),
            valueInputOption="USER_ENTERED",
        )
        .execute()
    )

def connect(where:str="googlesheet"):
	if ("google" in where.lower()) & ("sheet" in where.lower()):
		connector = connect_to_gsheet()
	return(connector)

def get_data(connector, where:str="googlesheet") -> pd.DataFrame:
	if ("google" in where.lower()) & ("sheet" in where.lower()):
		df = get_gsheet_data(connector)  

	return(df)

def add_row(connector, row, where:str="googlesheet") -> None:
	if ("google" in where.lower()) & ("sheet" in where.lower()):
		add_row_to_gsheet(connector, row)

