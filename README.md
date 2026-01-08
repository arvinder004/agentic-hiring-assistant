# TalentScout Chatbot

TalentScout Chatbot is a recruitment assistant built using **Streamlit** and **LangChain**. It guides candidates through a recruitment screening process, collecting their information, conducting a technical interview, and exporting the data for further evaluation.

---

## **Live Demo**
You can access the live version of the TalentScout Chatbot here:

👉 **[TalentScout Chatbot Live](https://hiring-assistant-arvinder.streamlit.app/)**

---

## **Features**
- **Candidate Information Collection**: Collects personal details like name, email, phone, experience, and tech stack.
- **Technical Interview**: Asks technical questions based on the candidate's tech stack.
- **Progress Tracking**: Displays interview progress in real-time.
- **Data Export**: Allows exporting interview data in JSON format.
- **Privacy Notice**: Displays a data handling policy to ensure transparency.

---

## **Concepts Used**
1. **Streamlit**: Used for building the interactive web application.
2. **LangChain**: Utilized for generating dynamic prompts and interacting with the LLM (ChatGroq).
3. **Session State**: Manages the state of the application, including candidate data, interview progress, and messages.
4. **Modular Design**: The code is structured into multiple utility files for better maintainability and scalability.

---

## **Directory Structure**
```
talentscout-chatbot/
│
├── app.py                     # Main entry point for the Streamlit app
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── utils/                     # Utility modules for modularity
│   ├── __init__.py            # Makes the folder a Python package
│   ├── session_state.py       # Functions for initializing and managing session state
│   ├── prompts.py             # Functions for generating prompts and messages
│   ├── validation.py          # Functions for validating user inputs
│   ├── llm.py                 # Functions for interacting with the LLM (ChatGroq)
│   ├── progress.py            # Functions for calculating and rendering progress
│   ├── export.py              # Functions for exporting candidate data
│   └── sidebar.py             # Functions for rendering the sidebar
```

---

## **How to Run the Application**
1. **Install Dependencies**:
   - Ensure you have Python installed.
   - Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

2. **Set Environment Variables**:
   - Create a `.env` file in the root directory and add your Groq API key:
     ```
     GROQ_API_KEY=your_groq_api_key
     ```

3. **Run the App**:
   - Start the Streamlit app:
     ```bash
     streamlit run app.py
     ```

4. **Access the App**:
   - Open the app in your browser at `http://localhost:8501`.

---

## **Future Improvements**
- Add support for multiple languages.
- Enhance the technical question generation with more diverse question types.
- Integrate with a database for storing candidate data persistently.
- Add authentication for HR personnel to access candidate data.

---

## **Contributors**
- **Your Name**: Developer and Maintainer