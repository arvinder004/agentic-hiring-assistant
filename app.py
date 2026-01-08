from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from utils.session_state import init_session_state
from utils.validation import check_message_relevance, detect_update_request, validate_and_save_field, extract_field_value
from utils.prompts import generate_conclusion, generate_confirmation_prompt, generate_field_prompt, generate_greeting, generate_irrelevant_response, generate_technical_question
from utils.progress import render_progress_bar
from utils.sidebar import render_sidebar

FIELD_ORDER = ["name", "email", "phone", "years_experience", "desired_position", "location", "tech_stack"]

FIELD_PROMPTS = {
    "name": "What's your full name?",
    "email": "Great! What's your email address?",
    "phone": "Thanks! What's your phone number? (Please provide a 10-digit number with/wthout country code)",
    "years_experience": "How many years of professional experience do you have? (Enter 0 if you're a fresh graduate)",
    "desired_position": "What position are you applying for? (e.g., Backend Developer, Data Scientist)",
    "location": "Where are you currently located?",
    "tech_stack": "Finally, what's your tech stack? Please list the programming languages, frameworks, and tools you're proficient with(seperated with commas)."
}

def get_next_field():
    """
        Get the next field that needs to be collected
    """
    for field in FIELD_ORDER:
        if st.session_state.candidate_data[field] is None:
            return field
    return None

def transition_to_stage_2():
    """
        Transition from info gathering to technical interview
    """
    st.session_state.stage = 2
    st.session_state.question_count = 1
    st.session_state.confirmation_pending = False
    
    tech_stack = st.session_state.candidate_data["tech_stack"]
    question = generate_technical_question(tech_stack, 1)
    
    st.session_state.current_question = question
    st.session_state.waiting_for_answer = True
    
    intro = f"""Perfect! Let's begin the technical assessment.

**Question 1/5:**

{question}"""
    
    return intro

def handle_technical_answer(user_message):
    """
        Handle technical answer and move to next question or conclusion
    """

    current_msg_id = len(st.session_state.messages)
    
    st.session_state.technical_qa.append({
        "question_number": st.session_state.question_count,
        "question": st.session_state.current_question,
        "answer": user_message
    })
    
    st.session_state.last_answer_message_id = current_msg_id
    
    if st.session_state.question_count >= 5:
        st.session_state.stage = 3
        st.session_state.current_question = None
        st.session_state.waiting_for_answer = False
        return generate_conclusion()
    
    st.session_state.question_count += 1
    
    question = generate_technical_question(
        st.session_state.candidate_data["tech_stack"],
        st.session_state.question_count
    )
    
    st.session_state.current_question = question
    st.session_state.waiting_for_answer = True  

    return f"Thank you for your answer!\n\n**Question {st.session_state.question_count}/5:**\n\n{question}"


if "show_privacy_notice" not in st.session_state:
    st.session_state.show_privacy_notice = False

if st.sidebar.button("View Data Handling Policy"):
    st.session_state.show_privacy_notice = not st.session_state.show_privacy_notice

if st.session_state.show_privacy_notice:
    st.sidebar.info(
        """
        **Privacy Notice:**
        
        All responses collected during this screening process are:
        - Used solely for recruitment evaluation purposes
        - Stored securely and treated as confidential
        - Accessible only to authorized HR personnel
        - Retained for 90 days unless you're selected for further interviews
        
        We respect your privacy and comply with data protection regulations.
        """
    )

st.sidebar.markdown("---")

if "show_candidate_info" not in st.session_state:
    st.session_state.show_candidate_info = False

if st.sidebar.button("View Candidate Information"):
    st.session_state.show_candidate_info = not st.session_state.show_candidate_info

if st.session_state.show_candidate_info:
    data = st.session_state.candidate_data
    info_collected = any(v is not None for v in data.values())

    if info_collected:
        for field, label in [
            ("name",  "Name"),
            ("email", "Email"),
            ("phone", "Phone"),
            ("years_experience", "Experience"),
            ("desired_position", "Position"),
            ("location", "Location"),
            ("tech_stack", "Tech Stack")
        ]:
            value = data.get(field)
            if value is not None:
                display_value = f"{value} years" if field == "years_experience" else value
                st.sidebar.markdown(f"**{label}**: {display_value}")
            else:
                st.sidebar.markdown(f"**{label}**: Not provided yet")
    else:
        st.sidebar.info("Information will appear here as you provide it during the interview.")

init_session_state()

def main():
    st.set_page_config(
        page_title="TalentScout - Recruitment Bot",
        page_icon="📝",
        layout="wide"
    )

    render_sidebar()

    st.title("TalentScout Recruitment Screening")

    render_progress_bar()

    st.markdown("---")

    if not st.session_state.initialized:
        greeting = generate_greeting()
        st.session_state.messages.append({
            "role": "assistant",
            "content": greeting
        })
        st.session_state.initialized = True

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.stage < 3:
        if user_input := st.chat_input("Type your response here..."):
            with st.chat_message("user"):
                st.markdown(user_input)

            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    context = f"Stage {st.session_state.stage}"
                    if st.session_state.stage == 1 and not st.session_state.confirmation_pending:
                        context += f" - collecting {st.session_state.current_field}"
                    elif st.session_state.confirmation_pending:
                        context += " - waiting for confirmation or updates"

                    is_relevant = check_message_relevance(user_input, context)

                    if not is_relevant:
                        response = generate_irrelevant_response()
                        st.markdown(response)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response
                        })

                    elif st.session_state.stage == 1:
                        
                        if st.session_state.confirmation_pending:
                            update_request = detect_update_request(user_input)
                            
                            if update_request["wants_update"] and update_request["field"]:
                                field = update_request["field"]
                                new_value = update_request["new_value"]
                                
                                if validate_and_save_field(field, new_value):
                                    field_name = field.replace("_", " ").title()
                                    response = f"Updated {field_name} to: {new_value}\n\n"
                                    response += "Would you like to update anything else, or shall we continue to the technical interview?"
                                else:
                                    response = f"Invalid value for {field}. Please provide a valid value or say 'no' to continue."
                                
                                st.markdown(response)
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": response
                                })
                            else:
                                response = transition_to_stage_2()
                                st.markdown(response)
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": response
                                })
                        else:
                            current_field = st.session_state.current_field
                            
                            field_value = extract_field_value(user_input, current_field)
                            
                            if validate_and_save_field(current_field, field_value):
                                next_field = get_next_field()
                                
                                if next_field:
                                    st.session_state.current_field = next_field
                                    response = generate_field_prompt(next_field)
                                else:
                                    st.session_state.confirmation_pending = True
                                    response = generate_confirmation_prompt()
                            else:
                                field_name = current_field.replace("_", " ")
                                response = f"I couldn't quite get that. Could you please provide your {field_name}?"
                                
                                if current_field == "email":
                                    response = "Please provide a valid email address (e.g., name@example.com)."
                                elif current_field == "phone":
                                    response = "Please provide a valid 10-digit phone number (e.g., 9876543210)."
                                elif current_field == "years_experience":
                                    response = "Please provide the number of years of experience (e.g., 5, or 0 for fresh graduates)."
                            
                            st.markdown(response)
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": response
                            })
                    
                    elif st.session_state.stage == 2:
                        response = handle_technical_answer(user_input)
                        st.markdown(response)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response
                        })
            
            st.rerun()
    
    elif st.session_state.stage == 3:
        st.success("Interview completed! Check the sidebar to download your interview data.")

if __name__ == "__main__":
    main()