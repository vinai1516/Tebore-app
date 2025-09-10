import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------- CONFIG ----------
st.set_page_config(page_title="Telangana Cultural Books", layout="centered")

DATA_FILE = "users.csv"

# ---------- EMAIL SETTINGS ----------
SENDER_EMAIL = "ravilalavinai@gmail.com"  # Replace with your Gmail
SENDER_PASSWORD = "vinai@123"  # Use Gmail App Password
RECEIVER_EMAIL = "ravilalavinai@gmail.com"

def send_email(username, email, contact):
    try:
        subject = "New User Registration - Telangana Cultural Books"
        body = f"""
        A new user has registered on Telangana Cultural Books website.

        Username: {username}
        Email: {email}
        Contact: {contact}
        """

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        st.error(f"⚠️ Email could not be sent: {e}")
        return False

# ---------- HELPER FUNCTIONS ----------
def load_users():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["username", "email", "contact", "password"])

def save_users(df):
    df.to_csv(DATA_FILE, index=False)

# ---------- MAIN NAVIGATION ----------
menu = st.sidebar.radio("📌 Navigate", ["Home", "Register", "Login"])

# ---------- HOME PAGE ----------
if menu == "Home":
    st.title("📚 Telangana Cultural Books")
    st.write("""
        Welcome to the **Telangana Cultural Books** portal!  
        Discover the rich heritage, traditions, and culture of Telangana through our curated collection of books.
    """)

    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6d/Kakatiya_Kala_Toranam.jpg", caption="Kakatiya Kala Toranam", use_container_width=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/4d/Ramappa_Temple_Front_View.jpg", caption="Ramappa Temple - UNESCO Heritage", use_container_width=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6a/Charminar_skyline.jpg", caption="Charminar - Pride of Hyderabad", use_container_width=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/5a/Bathukamma_Festival_Telangana.jpg", caption="Bathukamma Festival - Telangana's Cultural Pride", use_container_width=True)

# ---------- REGISTRATION PAGE ----------
elif menu == "Register":
    st.title("📝 User Registration")

    with st.form("register_form"):
        username = st.text_input("Enter Username")
        email = st.text_input("Enter Email ID")
        contact = st.text_input("Enter Contact No")
        password = st.text_input("Setup Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        register_btn = st.form_submit_button("Register")

    if register_btn:
        users = load_users()

        if not username or not email or not contact or not password or not confirm_password:
            st.error("⚠️ Please fill all fields.")
        elif password != confirm_password:
            st.error("❌ Passwords do not match.")
        elif username in users["username"].values:
            st.error("⚠️ Username already exists. Please choose another.")
        else:
            new_user = pd.DataFrame(
                [[username, email, contact, password]],
                columns=["username", "email", "contact", "password"],
            )
            users = pd.concat([users, new_user], ignore_index=True)
            save_users(users)

            # Send email notification
            if send_email(username, email, contact):
                st.success(f"✅ Registration successful! Welcome, {username}. An email has been sent to the admin.")
            else:
                st.warning("⚠️ Registered, but email notification failed.")

# ---------- LOGIN PAGE ----------
elif menu == "Login":
    st.title("🔑 User Login")

    with st.form("login_form"):
        login_username = st.text_input("Username")
        login_password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

    if login_btn:
        users = load_users()
        if login_username in users["username"].values:
            stored_password = users.loc[users["username"] == login_username, "password"].values[0]
            if login_password == stored_password:
                st.success(f"🎉 Welcome back, {login_username}!")
                st.write("Explore our Telangana Cultural Books collection 📖")
            else:
                st.error("❌ Incorrect password.")
        else:
            st.error("⚠️ Username not found. Please register first.")

    # Forgot Password Section
    st.markdown("### 🔒 Forgot Password?")
    with st.form("forgot_form"):
        forgot_username = st.text_input("Enter your registered Username")
        forgot_btn = st.form_submit_button("Recover Password")

    if forgot_btn:
        users = load_users()
        if forgot_username in users["username"].values:
            email = users.loc[users["username"] == forgot_username, "email"].values[0]
            st.info(f"📧 Password recovery instructions will be sent to your registered email: {email}")
        else:
            st.error("⚠️ Username not found. Please register first.")
