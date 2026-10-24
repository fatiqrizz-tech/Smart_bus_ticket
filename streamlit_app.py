"""Streamlit entry point for Smart Bus Reservation System."""
import streamlit as st
from smart_bus.ui.streamlit_pages import render_app

st.set_page_config(page_title="Smart Bus Reservation", page_icon="🚌", layout="wide")
render_app()
