# """---------------------------------------xxxxxxxxxxxxxxxxxxxxx------------------------------"""
import mysql.connector
import hashlib
import random
import streamlit as st
import asyncio
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import base64
from streamlit_option_menu import option_menu 

# Establish MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="xxxx",
        database="users"
    )

def create_users_table():
    db = get_db_connection()
    print(db)
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    phno VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """)
    db.commit()
    cursor.close()
    db.close()

create_users_table()


def authenticate(email, password):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    if user:
        st.session_state.user_id = user['user_id']  # Set user_id in session state
    return user is not None

def register_user(email, password, name, username, phno):
    if not email or not password or not name or not username or not phno:
        return False, "All fields are required."
    
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO user (email, password, name, username, phno) VALUES (%s, %s, %s, %s, %s)",
            (email, password, name, username, phno)
        )
        db.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    finally:
        cursor.close()
        db.close()

def login_success(message, username):
    st.success(message)
    st.session_state["logged_in"] = True
    st.session_state["user"] = username
    st.experimental_rerun()


def login_page():
    with st.expander("**Login/Signup**", st.session_state.get("logged_in", False)):
        create_tab, login_tab, guest_tab = st.tabs(["**Create Account**", "**Login**", "**Guest Access**"])

        with create_tab:
            with st.form(key="create"):
                email = st.text_input("**Email**")
                name = st.text_input("**Name**")
                username = st.text_input("**Username**")
                phno = st.text_input("**Phone Number**")
                password1 = st.text_input("**Password**", type="password")
                password2 = st.text_input("**Confirm Password**", type="password")
                
                if st.form_submit_button("**Sign Up**"):
                    if not email or not password1 or not name or not username or not phno:
                        st.error("All fields are required.")
                    elif password1 != password2:
                        st.error("Passwords do not match")
                    else:
                        if register_user(email, password1, name, username, phno):
                            st.success("User registered successfully! Please login.")
                            st.experimental_rerun()
                        else:
                            st.error("Email or Username already registered")

        with login_tab:
            with st.form(key="login"):
                email = st.text_input("**Email**")
                password = st.text_input("**Password**", type="password")
                col1,col2 = st.columns(2)
    
                with col1:
                    if st.form_submit_button("**Login**"):
                        if authenticate(email, password):
                            login_success(f"Welcome {email}!", email)
                        else:
                            st.error("Invalid credentials")
                
        with guest_tab:
            if st.button("**Continue as Guest**"):
                st.session_state["logged_in"] = True
                st.experimental_rerun()


    def get_img_as_base64(file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    img = get_img_as_base64("Pdf_Pulse.jpg")

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://static.vecteezy.com/system/resources/previews/004/750/613/non_2x/flat-design-abstract-background-soft-liquid-shapes-template-with-modern-gradient-background-colors-cool-aesthetic-background-design-suitable-for-social-media-post-mobile-app-banner-web-ads-free-vector.jpg");
    background-size: 180%;
    background-position: top left;
    background-repeat: no repeat;
    background-attachment: local;
    }}

    [data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/png;base64,{img}");
    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.markdown("<div class='main'>", unsafe_allow_html=True)

    st.markdown("### Features")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Extract Key Points 🔑**\n\nSummarize lengthy passages, extract key information, and quickly locate what you need. Say hello to an efficient and hassle-free document comprehension journey.")
    
    with col2:
        st.markdown("**Answer Questions about PDF Documents 📃**\n\nPDF Pulse thoroughly analyzes your PDFs, providing insightful answers based on document content. Pdf Pulse ensures effective analysis of PDFs in diverse languages.")
    
    with col3:
        st.markdown("**Interact with your Personal AI 🤖**\n\n Here, you can engage with a sophisticated AI system designed to assist you in answering questions, solving problems, and providing insights on a wide range of topics. Whether you're looking for quick answers, detailed explanations, or simply a conversational partner, your personal AI is here to help.")

    # User Sections
    st.markdown("### Who Can Benefit?")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Students 👨‍💻**\n\nSummarize long textbooks, clarify concepts, get new ideas, and more. Ideal for enhancing learning experiences.")
    
    with col2:
        st.markdown("**Researchers 🕵️**\n\nAnalyze industry reports and professional documents easily. Improve speed, accuracy, and efficiency.")
    
    with col3:
        st.markdown("**Professionals 👨‍🎓**\n\nExplain business reports, analyze financial data, and do market research. Raise work productivity and optimize performance.")

    st.markdown("### How to Chat with PDF Online?")
    st.markdown("""
    1. **Upload A PDF File**: Upload or drag-and-drop the PDF file onto HiPDF's Chat with PDF Page.
    2. **AI Analyzes PDF**: Upon uploading, HiPDF will start analyzing your PDF, extracting its key information.
    3. **Chat with PDF**: Chat with the PDF by asking your questions and receiving answers. Easily copy and paste the answers as needed.
    """)

    # FAQ Section
    with st.expander("FAQs about chatting with PDF online"):
        st.markdown("""
        - **How can I chat with my PDF?** Simply upload your PDF and start chatting using the AI interface.
        - **Do I need to sign up for an account for a chat?** No, you can use the service without signing up.
        - **How many times can I chat with PDF?** There is no limit to the number of times you can chat with your PDFs.
        - **Is there a way to summarize a PDF?** Yes, ChatGPT can summarize a PDF file for you.
        """)

    
    st.markdown("---")
    # Footer
    st.markdown("""
        <style>
        .footer {
            # background-color: skyblue;
            padding: 20px;
            border-top: 1px solid #e0e0e0;
        }
        .footer-column {
            margin-right: 20px;
        }
        .footer-column h5 {
            # margin-bottom: 10px;
        }
        .footer-column a {
            display: block;
            color: #0066cc;
            text-decoration: none;
            margin: 5px 0;
        }
        .footer-column a:hover {
            text-decoration: underline;
        }
        </style>
    """, unsafe_allow_html=True)

    # Footer content
    st.markdown('<div class="footer">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="footer-column">
            <h5>About Us</h5>
            <p>PDF Pulse [Chat with any PDF]: ask questions, get summaries, find information, and more.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="footer-column">
            <h5>Products</h5>
            <a href="https://example.com/use-cases" target="_blank">Use cases</a>
            <a href="https://example.com/api-docs" target="_blank">API docs</a>
            <a href="https://example.com/pricing" target="_blank">Pricing</a>
            <a href="https://example.com/video-tutorials" target="_blank">Video tutorials</a>
            <a href="https://example.com/resources" target="_blank">Resources</a>
            <a href="https://example.com/blog" target="_blank">Blog</a>
            <a href="https://example.com/faq" target="_blank">FAQ</a>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="footer-column">
            <h5>Company</h5>
            <a href="https://example.com/about" target="_blank">About</a>
            <a href="https://example.com/careers" target="_blank">Careers</a>
            <a href="https://example.com/contact" target="_blank">Contact</a>
            <a href="https://example.com/newsroom" target="_blank">Newsroom</a>
            <a href="https://example.com/global-presence" target="_blank">Global Presence</a>
            <a href="https://example.com/founder-speech" target="_blank">Founder's Speech</a>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="footer-column">
            <h5>Follow Us</h5>
            <a href="https://facebook.com" target="_blank">Facebook</a>
            <a href="https://twitter.com" target="_blank">Twitter</a>
            <a href="https://linkedin.com" target="_blank">LinkedIn</a>
            <a href="https://instagram.com" target="_blank">Instagram</a>
            <a href="https://youtube.com" target="_blank">YouTube</a>
            <a href="https://pinterest.com" target="_blank">Pinterest</a>
            <a href="https://reddit.com" target="_blank">Reddit</a>
            <a href="https://github.com" target="_blank">GitHub</a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def userwelcome(msg):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT name FROM user WHERE email = %s", (msg,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return user['name'] if user else 'Guest'

def main():
    st.set_page_config(page_title="PDF Pulse", page_icon=":star:",initial_sidebar_state="collapsed", layout="wide")  
    user_message = st.session_state.get('user', 'Guest')
    user_name = userwelcome(user_message)
    st.markdown(f"""
        <style>
        .success-message {{
            position: fixed;
            top: 50px;
            right: 90px;
            z-index: 1000;
            background-color: #d4edda;
            color: #155724;
            padding: 10px 20px;
            border-radius: 20px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }}
        </style>
        <div class="success-message">
            {"Welcome " + user_name + ". Hope you have a great day ahead!"}
        </div>
    """, unsafe_allow_html=True)
    st.image("Pdf_Pulse.jpg")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state.get("logged_in", False):
        st.sidebar.success(f"Logged in as {st.session_state.get('user', 'Guest')}")
    # else:
    #     login_page()

    if "history" not in st.session_state:
        st.session_state.history = []

    if "uploaded_pdf" not in st.session_state:
        st.session_state.uploaded_pdf = None

    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "Home"

    if not st.session_state["logged_in"]:
        login_page()
    else:
        with st.sidebar:
            selected = option_menu("Menu", ["🏠 Home", "📒 About", "📜 History", "👤 Profile", "🔷 Subscription", "⚙️ Tools"], 
                        icons=["🏠", "📒", "📜", "👤", "🔷", "⚙️"], 
                        menu_icon="cast", default_index=0)

        if st.sidebar.button("Logout"):
            st.session_state["logged_in"] = False
            st.experimental_rerun()

        st.session_state["active_page"] = selected

        if st.session_state["active_page"] == "🏠 Home":
            from Home import main
            main()
        elif st.session_state["active_page"] == "📒 About":
            from about import about
            about()
        elif st.session_state["active_page"] == "📜 History":
            from history import history
            history()
        elif st.session_state["active_page"] == "👤 Profile":
            from user_profile import user_profile
            user_profile()
        elif st.session_state["active_page"] == "🔷 Subscription":
            from subscription import subscription
            subscription()
        elif st.session_state["active_page"] == "⚙️ Tools":
            from tools import tools
            tools()

if __name__ == "__main__":
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    main()
