import streamlit as st
from datetime import datetime

from utils.export import export_candidate_data

def render_sidebar():
    """
        Render sidebar with information
    """
    st.sidebar.markdown("---")
    
    if "show_interview_progress" not in st.session_state:
        st.session_state.show_interview_progress = False

    if st.sidebar.button("Click to view Interview Progress"):
        st.session_state.show_interview_progress = not st.session_state.show_interview_progress

    if st.session_state.show_interview_progress:
        stages = {
            1: "Info Gathering",
            2: "Technical Interview",
            3: "Completed"
        }

        current_stage = min(st.session_state.stage, 4)
        for stage_num, stage_name in stages.items():
            if stage_num < current_stage:
                st.sidebar.markdown(f"✅ {stage_name}")
            elif stage_num == current_stage:
                st.sidebar.markdown(f"▶️ **{stage_name}**")
            else:
                st.sidebar.markdown(f"⚪ {stage_name}")
    
    st.sidebar.markdown("---")

    if st.session_state.stage >= 3:
        if st.sidebar.button("📥 Download Interview Data"):
            data = export_candidate_data()
            st.sidebar.download_button(
                label=" Download JSON",
                data=data,
                file_name=f"candidate_{st.session_state.candidate_data.get('name', 'unknown').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
