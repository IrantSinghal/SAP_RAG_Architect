import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* 1. Fix the Overlap: Add padding to the bottom of the scroll area */
        .main .block-container {
            padding-bottom: 150px !important;
        }

        /* 2. Motiff Glassmorphism Chat Bubbles */
        .stChatMessage {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 15px !important;
            margin-bottom: 15px !important;
            padding: 20px !important;
        }

        /* 3. Style the Input Bar to look modern */
        .stChatInput {
            background-color: #0d1117 !important;
            border-radius: 25px !important;
            border: 1px solid #30363d !important;
        }
        
        /* Hide Streamlit branding for a cleaner look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)