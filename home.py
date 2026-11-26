import streamlit as st
import requests
import json
import plotly.express as px

st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}

[data-testid="collapsedControl"] {
    display: none;
}
.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(0, 229, 255, 0.12), transparent 30%),
        radial-gradient(circle at 85% 75%, rgba(36, 123, 255, 0.13), transparent 35%),
        linear-gradient(135deg, #030712, #071525, #020617);

    background-attachment: fixed;
}
</style>
""", unsafe_allow_html=True)
st.set_page_config(
    page_title="Airmosphere",
    page_icon="🌍",
    layout="wide"
)
st.title("Airmosphere")
st.caption("Explore the air and the atmosphere around the world.")
st.divider()
if st.button("Get Started"):
    st.switch_page("pages/login_signup.py")
