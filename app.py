
import streamlit as st
from pathlib import Path

# Configure the application page
st.set_page_config(
    page_title="AI Personalized Learning Coach",
    page_icon="🧠",
    layout="wide"
)

# Load custom CSS
def load_css():
    css_file = Path(__file__).parent / "assets" / "style.css"

    with open(css_file, encoding="utf-8") as file:
        st.markdown(
            f"<style>{file.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# Main application title


st.markdown("""
<div class="main-title">
    <span class="title-emoji">🧠</span>
    <span class="title-text">AI Personalized Learning Coach</span>
</div>
""", unsafe_allow_html=True)



# Welcome banner
st.markdown("""
<div class="hero-banner">
    <h1>Welcome, Learner! 👋</h1>
    <h3>Learn smarter. Grow faster.</h3>
    <p>
        Your personal AI-powered learning companion.
        Learn smarter, practice better, and achieve your goals.
    </p>
</div>
""", unsafe_allow_html=True)

# Learning Journey section
st.markdown("""
<div class="learning-section">
    <h2>🚀 Your Learning Journey Starts Here</h2>
    <p>
        Our AI Learning Coach will help you create
        personalized study plans, practice quizzes,
        and track your learning progress.
    </p>
</div>
""", unsafe_allow_html=True)

# Getting Started section
st.markdown("""
<div class="getting-started">
    <p>
        🎯 Ready to start learning?
        Your personalized learning journey begins here!
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🧭 Navigation")

st.sidebar.markdown("""
<div class="sidebar-welcome">
    <p>👋 Welcome to your learning space!</p>
    <p>✨ Your learning journey starts here.</p>
</div>
""", unsafe_allow_html=True)
