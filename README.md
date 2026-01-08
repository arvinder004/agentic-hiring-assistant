# TalentScout Chatbot

TalentScout Chatbot is a recruitment assistant built using **Streamlit** and **LangChain**. It guides candidates through a recruitment screening process, collecting their information, conducting a technical interview, and exporting the data for further evaluation. The chatbot also integrates with **MongoDB** to store interview data securely.

---

## **Live Demo**
You can access the live version of the TalentScout Chatbot here:

👉 **[TalentScout Chatbot Live](https://hiring-assistant-arvinder.streamlit.app/)**

---

## **Project Overview**
TalentScout Chatbot is designed to streamline the recruitment process by automating candidate screening. It collects candidate information, conducts technical interviews, tracks progress, and stores the data in a MongoDB database for further evaluation. The chatbot uses **LangChain** for prompt generation and **Streamlit** for the user interface.

---

## **Features**
- **Candidate Information Collection**: Collects personal details like name, email, phone, experience, and tech stack.
- **Technical Interview**: Asks technical questions based on the candidate's tech stack.
- **Progress Tracking**: Displays interview progress in real-time.
- **Data Export**: Allows exporting interview data in JSON format.
- **MongoDB Integration**: Automatically saves interview data to a MongoDB database.
- **Privacy Notice**: Displays a data handling policy to ensure transparency.

---

## **Installation Instructions**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/talentscout-chatbot.git
   cd talentscout-chatbot
   ```

2. **Install Dependencies**:
   Ensure you have Python installed. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key and MongoDB connection string:
   ```
   GROQ_API_KEY=your_groq_api_key
   MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/<database>?retryWrites=true&w=majority
   ```

4. **Run the App**:
   Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

5. **Access the App**:
   Open the app in your browser at `http://localhost:8501`.

---

## **Usage Guide**
1. **Start the Application**:
   - Launch the app locally or access the live demo link.
   - Follow the chatbot's instructions to provide your information.

2. **Complete the Interview**:
   - Answer the technical questions based on your tech stack.
   - Track your progress using the progress bar.

3. **Export Data**:
   - After completing the interview, the data is automatically saved to MongoDB.
   - You can also download the data in JSON format.

---

## **Technical Details**
### **Libraries Used**
- **Streamlit**: For building the interactive web application.
- **LangChain**: For generating dynamic prompts and interacting with the LLM (ChatGroq).
- **pymongo**: For integrating with MongoDB.
- **dotenv**: For managing environment variables.

### **Model Details**
- **LLM**: ChatGroq (model: `llama-3.3-70b-versatile`) is used for prompt generation and information extraction.

### **Architectural Decisions**
- **Modular Design**: The code is divided into utility files for better maintainability.
- **Session State**: Used to manage the state of the application, including candidate data and interview progress.
- **MongoDB Integration**: Ensures secure and scalable storage of interview data.

---

## **Prompt Design**
### **Information Gathering**
Prompts are crafted to collect specific candidate details, such as name, email, phone, experience, and tech stack. For example:
- `"What's your full name?"`
- `"What position are you applying for?"`

### **Technical Question Generation**
Prompts dynamically generate technical questions based on the candidate's tech stack. For example:
- `"Generate a technical question for a candidate proficient in Python and Django."`

### **Relevance Check**
Prompts ensure user messages are relevant to the recruitment process. Irrelevant messages are politely redirected.

---

## **Challenges & Solutions**
### **Challenge 1: Handling Irrelevant User Input**
- **Problem**: Users might provide irrelevant input during the interview.
- **Solution**: Implemented a relevance check using LangChain prompts to filter irrelevant messages and redirect users.

### **Challenge 2: MongoDB Integration**
- **Problem**: MongoDB's `ObjectId` is not JSON serializable.
- **Solution**: Converted `ObjectId` to a string before exporting data.

### **Challenge 3: Dynamic Prompt Generation**
- **Problem**: Generating diverse and meaningful technical questions.
- **Solution**: Used LangChain's LLM capabilities to craft prompts based on the candidate's tech stack.

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

## **Future Improvements**
- Add support for multiple languages.
- Enhance the technical question generation with more diverse question types.
- Integrate authentication for HR personnel to access candidate data.
- Implement persistent session storage for long-running interviews.

---

## **Contributors**
- **Your Name**: Developer and Maintainer