import streamlit as st
from langchain_core.messages import SystemMessage

from utils.llm import get_llm

FIELD_PROMPTS = {
    "name": "What's your full name?",
    "email": "Great! What's your email address?",
    "phone": "Thanks! What's your phone number? (Please provide a 10-digit number with/wthout country code)",
    "years_experience": "How many years of professional experience do you have? (Enter 0 if you're a fresh graduate)",
    "desired_position": "What position are you applying for? (e.g., Backend Developer, Data Scientist)",
    "location": "Where are you currently located?",
    "tech_stack": "Finally, what's your tech stack? Please list the programming languages, frameworks, and tools you're proficient with(seperated with commas)."
}

def generate_greeting():
    """
        Generate initial greeting message
    """
    greeting = """
            Welcome to TalentScout!

            I'm your recruitment assistant, and I'm here to help you through our screening process. 

            I'll guide you step-by-step through the interview. Let's start with some basic information about you.

            What's your full name?
        """
    
    return greeting


def generate_field_prompt(field_name):
    """
        Generate prompt for the next field
    """
    return FIELD_PROMPTS.get(field_name, "Please provide the information.")


def generate_confirmation_prompt():
    """
        Generate confirmation prompt with summary
    """
    confirmation = """Great! I have all the information I need.

        Let me confirm what we have:
            - Name: {name}
            - Email: {email}
            - Phone: {phone}
            - Experience: {years_experience} years
            - Position: {desired_position}
            - Location: {location}
            - Tech Stack: {tech_stack}

        Would you like to update any of this information? 

        You can say something like:
            - "Update email to newemail@example.com"
            - "Change phone to 9876543210"
            - Or simply say "No" or "Looks good" to continue to the technical interview.""".format(**st.session_state.candidate_data)
    
    return confirmation


def generate_technical_question(tech_stack, question_number):
    """
    Generate a technical question based on the candidate's tech stack
    """
    llm = get_llm()
    
    prompt = f"""You are a technical interviewer. Generate a single, clear technical interview question for a candidate.

Candidate's Tech Stack: {tech_stack}
Question Number: {question_number} of 5

Generate a question that:
- Tests practical knowledge of their stated technologies
- Is appropriate for their tech stack
- Varies in difficulty (mix of fundamental and advanced topics)
- Is specific and clear

Return ONLY the question, no additional text or numbering."""
    
    try:
        response = llm.invoke([SystemMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        fallback_questions = [
            f"Can you explain a challenging problem you've solved using {tech_stack.split(',')[0].strip()}?",
            f"What are the key principles you follow when designing scalable applications?",
            f"How do you approach debugging complex issues in production?",
            f"Describe your experience with version control and collaboration workflows.",
            f"What testing strategies do you implement in your projects?"
        ]
        return fallback_questions[question_number - 1]


def generate_irrelevant_response():
    """
        Generate a polite response for irrelevant queries
    """
    responses = [
        "I appreciate your question, but I'm specifically designed to help with the recruitment screening process. ",
        "That's an interesting question, but I'm here to conduct your interview screening. ",
        "I'd love to help, but my role is to assist with your job application. ",
    ]
    
    import random
    base_response = random.choice(responses)
    
    if st.session_state.stage == 1:
        if st.session_state.confirmation_pending:
            return base_response + "Please let me know if you'd like to update any information (e.g., 'update email to john@example.com') or say 'no' to continue."
        else:
            current_field = st.session_state.current_field
            field_name = current_field.replace("_", " ")
            return base_response + f"Let's continue - I need your {field_name}."
    elif st.session_state.stage == 2:
        return base_response + f"Please answer the current technical question (Question {st.session_state.question_count}/5)."
    
    return base_response + "Let's get back to the interview."


def generate_conclusion():
    """
        Generate conclusion message
    """
    conclusion = f""" **Interview Complete!**

Thank you, {st.session_state.candidate_data['name']}, for taking the time to complete our screening process!

**Next Steps:**
1. Our team will review your responses within 2-3 business days
2. You'll receive an email at **{st.session_state.candidate_data['email']}** with our decision
3. If selected, we'll schedule a follow-up interview with our technical team

**What to Expect:**
- We evaluate candidates based on technical knowledge, problem-solving ability, and communication skills
- Selected candidates will move forward to a live coding round
- The entire process typically takes 1-2 weeks

Thank you for your interest in joining our team! We wish you the best of luck. 🚀

*Your interview data has been securely saved.*"""
    
    return conclusion
