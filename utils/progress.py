import streamlit as st

def calculate_progress():
    """
        Calculate interview progress percentage
    """
    if st.session_state.stage == 1:
        collected = sum([1 for v in st.session_state.candidate_data.values() if v is not None])
        return int((collected / 7) * 40)
    elif st.session_state.stage == 2:
        answered = len(st.session_state.technical_qa)
        return 40 + int((answered / 5) * 50)
    elif st.session_state.stage >= 3:
        return 100
    return 0


def render_progress_bar():
    """
        Render progress bar at the top
    """
    progress = calculate_progress()
    st.progress(progress / 100, text=f"Interview Progress: {progress}%")
