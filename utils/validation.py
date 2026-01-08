import streamlit as st
import re
from langchain_core.messages import SystemMessage
import json

from utils.llm import get_llm

def validate_and_save_field(field_name, value):
    """
        Validate and save field value
    """
    if value is None:
        return False
    
    # Email validation
    if field_name == "email":
        email_str = str(value)
        if "@" not in email_str:
            return False
        parts = email_str.split("@")
        if len(parts) != 2:
            return False
        domain = parts[1]
        if "." not in domain or domain.startswith(".") or domain.endswith("."):
            return False
        if "," in email_str or " " in email_str:
            return False
    
    # Phone validation
    if field_name == "phone":
        phone_digits = re.sub(r'\D', '', str(value))
        if len(phone_digits) != 10:
            return False
        value = phone_digits
    
    #YOE validation
    if field_name == "years_experience":
        try:
            value = int(value) if isinstance(value, (int, float)) else int(value)
            if value < 0:
                return False
        except:
            return False
    
    st.session_state.candidate_data[field_name] = value
    return True


def check_message_relevance(user_message, current_context):
    """
        Check if the user message is relevant to the recruitment process
    """
    llm = get_llm()
    
    relevance_prompt = f"""
        You are a recruitment chatbot filter. Determine if the user's message is relevant to a job recruitment screening process.

        User message: "{user_message}"
        Context: {current_context}

        A message is RELEVANT if it:
        - Provides personal information (name, email, phone, experience, position, location, skills)
        - Answers the current question being asked
        - Asks clarifying questions about the job or interview process
        - Expresses willingness to continue or provides acknowledgments
        - Requests to update previously provided information

        A message is IRRELEVANT if it:
        - Asks general knowledge questions (capitals, math problems, trivia, science facts)
        - Requests unrelated tasks (writing stories, translating text, jokes)
        - Contains off-topic conversation
        - Asks about unrelated topics (weather, sports, entertainment)

        Respond with ONLY one word: RELEVANT or IRRELEVANT
    """
    
    try:
        response = llm.invoke([SystemMessage(content=relevance_prompt)])
        result = response.content.strip().upper()
        return "RELEVANT" in result
    except Exception as e:
        return True


def detect_update_request(user_message):
    """
        Detect if user wants to update information
    """
    llm = get_llm()
    
    update_prompt = f"""
        Analyze if the user wants to UPDATE previously provided information.

       User message: "{user_message}"
        Available fields: name, email, phone, years_experience, desired_position, location, tech_stack

        Determine:
        1. Does the user want to update something? (yes/no)
        2. If yes, which field? (use exact field names above)
        3. If yes, what's the new value?

        Return ONLY a JSON object:
        {{"wants_update": true/false, "field": "field_name or null", "new_value": "value or null"}}

        Examples:
        - "update email to john@example.com" -> {{"wants_update": true, "field": "email", "new_value": "john@example.com"}}
        - "change my phone number to 1234567890" -> {{"wants_update": true, "field": "phone", "new_value": "1234567890"}}
        - "no" or "looks good" -> {{"wants_update": false, "field": null, "new_value": null}}
        """
    
    try:
        response = llm.invoke([SystemMessage(content=update_prompt)])
        content = response.content.strip()
        
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        pass
    
    return {"wants_update": False, "field": None, "new_value": None}


def extract_field_value(user_message, field_name):
    """
        Extract specific field value from user message
    """
    llm = get_llm()
    
    field_descriptions = {
        "name": "the person's full name",
        "email": "a valid email address",
        "phone": "a phone number (with or without country code)",
        "years_experience": "number of years of experience (use 0 for fresh graduates or no experience)",
        "desired_position": "job position/role they're applying for",
        "location": "their current location (city, state, or country)",
        "tech_stack": "programming languages, frameworks, and tools they know (as a comma-separated string)"
    }
    
    extraction_prompt = f"""
        Extract {field_descriptions[field_name]} from the user's message.

        User message: "{user_message}"

        Rules:
            - If the information is clearly present, extract it
            - For years_experience: if they say "fresher", "fresh graduate", "no experience", or "0", return 0
            - For tech_stack: provide as comma-separated values
            - If the information is NOT present or unclear, return null

        Return ONLY a JSON object with this format: {{"value": <extracted_value>}}

        Examples:
            - For name: {{"value": "John Doe"}}
            - For email: {{"value": "john@example.com"}}
            - For years_experience: {{"value": 3}} or {{"value": 0}}
            - For tech_stack: {{"value": "Python, Django, React, PostgreSQL"}}
            - If not found: {{"value": null}}
    """
    
    try:
        response = llm.invoke([SystemMessage(content=extraction_prompt)])
        content = response.content.strip()
        
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            extracted_data = json.loads(json_match.group())
            return extracted_data.get("value")
    except Exception as e:
        pass
    
    return None
