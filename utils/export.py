from datetime import datetime
import json
import streamlit as st
from utils.database import save_interview_data

def export_candidate_data():
    """
    Export candidate data to JSON format and save it to MongoDB.
    """
    export_data = {
        "timestamp": datetime.now().isoformat(),
        "candidate_info": st.session_state.candidate_data,
        "technical_interview": st.session_state.technical_qa,
        "interview_stage_completed": st.session_state.stage
    }
    
    # Save to MongoDB
    try:
        inserted_id = save_interview_data(export_data)
        st.success(f"Data saved to MongoDB with ID: {inserted_id}")
    except Exception as e:
        st.error(f"Failed to save data to MongoDB: {e}")
    
    # Return JSON for download
    return json.dumps(export_data, indent=2)