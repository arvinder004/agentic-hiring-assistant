import streamlit as st
from datetime import datetime
import json

def export_candidate_data():
    """
        Export candidate data to JSON format with questions and answers
    """
    export_data = {
        "timestamp": datetime.now().isoformat(),
        "candidate_info": st.session_state.candidate_data,
        "technical_interview": st.session_state.technical_qa,
        "interview_stage_completed": st.session_state.stage
    }
    
    return json.dumps(export_data, indent=2)
