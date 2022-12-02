import streamlit as st
from core import ParkingData, Parking

st.set_page_config(
    page_title="Entry data Management",
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

with st.form("entry-data", clear_on_submit=True):
    st.subheader("Entry details")
    vtype = st.selectbox("Vehicle Type", ["Private car", "Van", "Taxi"])
    reg_no = st.text_input(
        label="Enter vehicle registration number",
        max_chars=12,
        placeholder="Vehicle reg. no.",
    ).upper()
    if st.form_submit_button("Submit") and reg_no:
        parking = Parking(10, 20)
        slot = parking.get_slot()
        if slot is not None:
            data = ParkingData(vehicle_type=vtype, reg_no=reg_no, slot=slot)
            st.success(f"Your slot number is {slot[:2]} on floor {slot[2]}")
            st.write(data)
        else:
            st.error("Sorry, parking lot is full")
