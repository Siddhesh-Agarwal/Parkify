import streamlit as st
from core import Parking, ParkingData

st.set_page_config(
    page_title="Exit Data Management",
    # page_icon="./assets/logo.svg",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None,
    },
)

st.title("Project Parkify")

if st.form("exit-data", clear_on_submit=True):
    reg_no = st.text_input(
        label="Enter vehicle registration number",
        max_chars=12,
        placeholder="Vehicle reg. no.",
    ).upper()
    if st.form_submit_button("Submit"):
        parking = Parking(10, 20)
        if parking.occupied_slots() == 0:
            st.error("Sorry, parking lot is empty")
        else:
            pass
