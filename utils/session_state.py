import streamlit as st


def init_session_state():
    """
        Initialize all session state variables
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "stage" not in st.session_state:
        st.session_state.stage = 1
    
    if "candidate_data" not in st.session_state:
        st.session_state.candidate_data = {
            "name": None,
            "email": None,
            "phone": None,
            "years_experience": None,
            "desired_position": None,
            "location": None,
            "tech_stack": None
        }
    
    if "current_field" not in st.session_state:
        st.session_state.current_field = "name"
    
    if "confirmation_pending" not in st.session_state:
        st.session_state.confirmation_pending = False
    
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0
    
    if "technical_qa" not in st.session_state:
        st.session_state.technical_qa = []

    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    
    if "waiting_for_answer" not in st.session_state:
        st.session_state.waiting_for_answer = False
    
    if "last_answer_message_id" not in st.session_state:
        st.session_state.last_answer_message_id = None
    
    if "initialized" not in st.session_state:
        st.session_state.initialized = False
