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
        email_str = str(value).strip().lower()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email_str):
            return False
        value = email_str
    
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

    update_keywords = ["change", "update", "correct", "fix", "modify", "replace", "wrong", "mistake"]
    user_lower = user_message.lower()
    
    wants_update = any(keyword in user_lower for keyword in update_keywords)
    
    if wants_update:
        field_patterns = {
            "name": ["name"],
            "email": ["email"],
            "phone": ["phone", "number"],
            "years_experience": ["experience", "years", "yoe"],
            "desired_position": ["position", "role", "job", "applying"],
            "location": ["location", "city", "located", "from", "based"],
            "tech_stack": ["tech", "stack", "technology", "skills", "programming", "languages"]
        }
        
        detected_field = None
        for field, keywords in field_patterns.items():
            if any(keyword in user_lower for keyword in keywords):
                detected_field = field
                break
        
        if detected_field:
            new_value = None
            
            for keyword in ["to ", "as "]:
                if keyword in user_lower:
                    parts = user_lower.split(keyword, 1)
                    if len(parts) > 1:
                        new_value = parts[1].strip()
                        break
            
            if new_value:
                return {"wants_update": True, "field": detected_field, "new_value": new_value}
            else:
                return {"wants_update": True, "field": detected_field, "new_value": None}
    
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
        
        json_match = re.search(r'\{.*?\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        print(f"Error detecting update request: {e}")
        pass
    
    return {"wants_update": False, "field": None, "new_value": None}


def extract_field_value(user_message, field_name):
    """
        Extract specific field value from user message
    """
    if field_name == "name":
        words = user_message.strip().split()
        if len(words) <= 4 and len(user_message) < 50:
            irrelevant = ["the", "is", "i'm", "my", "name", "is", "called", "i", "am"]
            relevant_words = [w for w in words if w.lower() not in irrelevant]
            if relevant_words:
                return " ".join(relevant_words)
    
    if field_name == "email":
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, user_message)
        if match:
            return match.group(0)
    
    if field_name == "phone":
        phone_pattern = r'\d{10}'
        match = re.search(phone_pattern, user_message)
        if match:
            return match.group(0)
        phone_with_separators = re.sub(r'[^\d]', '', user_message)
        if len(phone_with_separators) >= 10:
            return phone_with_separators[:10]
    
    if field_name == "years_experience":
        if any(keyword in user_message.lower() for keyword in ["fresher", "fresh graduate", "no experience", "0 years", "just graduated", "beginner"]):
            return 0
        numbers = re.findall(r'\d+', user_message)
        if numbers:
            return int(numbers[0])
    
    if field_name == "desired_position":
        if len(user_message) < 100:
            filler_words = ["i'm", "i am", "applying for", "looking for", "want", "interested in", "position", "role", "job", "as", "a", "an"]
            cleaned = user_message.lower()
            for word in filler_words:
                cleaned = re.sub(r'\b' + re.escape(word) + r'\b', '', cleaned).strip()
            if cleaned and len(cleaned) > 2:
                return cleaned.title()
    
    if field_name == "location":
        if len(user_message) < 50:
            filler_words = ["i'm", "i am", "located in", "from", "based in", "live in", "city", "state", "country"]
            cleaned = user_message.lower()
            for word in filler_words:
                cleaned = re.sub(r'\b' + re.escape(word) + r'\b', '', cleaned).strip()
            if cleaned and len(cleaned) > 1:
                return cleaned.title()
    
    if field_name == "tech_stack":
        if "," in user_message:
            return user_message.strip()
        tech_keywords = ["python", "java", "javascript", "typescript", "react", "django", "node", "sql", "postgres", "mongodb", "docker", "kubernetes", "aws", "git", "html", "css", "c++", "c#", ".net", "php", "ruby", "golang", "rust", "kotlin", "swift", "flutter", "vue", "angular", "spring", "fastapi", "express", "flask"]
        if any(keyword in user_message.lower() for keyword in tech_keywords):
            filler_words = ["i know", "i'm proficient in", "i have", "experience with", "skilled in", "expertise in", "familiar with", "and", ","]
            cleaned = user_message.lower()
            for word in filler_words:
                cleaned = cleaned.replace(word, "").strip()
            if cleaned and len(cleaned) > 2:
                return cleaned.strip()
            return user_message.strip()
    
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
        json_match = re.search(r'\{.*?\}', content, re.DOTALL)
        if json_match:
            extracted_data = json.loads(json_match.group())
            return extracted_data.get("value")
    except Exception as e:
        print(f"Error extracting {field_name}: {e}")
        pass
    
    return None
