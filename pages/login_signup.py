import streamlit as st
import requests
import json
import plotly.express as px
from argon2 import PasswordHasher

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
login_signup = st.selectbox("Choose to login or signup", ["Choose", "Login", "Sign Up"], key="login_signup_option")
if login_signup == "Login":
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        with open("/Users/hd/Documents/Learning(VS Code)/Airmosphere/data.json/users.json", "r") as f:
            existing_data = json.load(f)
        user_exists = any(user["email"] == email and PasswordHasher().verify(user["password"], password) for user in existing_data)
        if user_exists:
            st.success("Login successful!")
            st.switch_page("pages/app.py")
        else:
            st.error("Email or password not found!")
elif login_signup == "Sign Up":
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        ph = PasswordHasher()
        data = {"email": email, "password": ph.hash(password)}
        with open('/Users/hd/Documents/Learning(VS Code)/Airmosphere/data.json/users.json', 'r') as f:
            existing_data = json.load(f)
        existing_data.append(data)
        with open('/Users/hd/Documents/Learning(VS Code)/Airmosphere/data.json/users.json', 'w') as f:
            json.dump(existing_data, f, indent = 1)
        st.success("Sign up successful!")
        st.switch_page("pages/app.py")
