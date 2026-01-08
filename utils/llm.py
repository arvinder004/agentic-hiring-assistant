import streamlit as st
from langchain_groq import ChatGroq
import os

def get_llm():
    """
        Initialize and return the LLM
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("API Key not found. Please set it in your environment variables as GROQ_API_KEY.")
        st.stop()
    
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        groq_api_key=api_key
    )
