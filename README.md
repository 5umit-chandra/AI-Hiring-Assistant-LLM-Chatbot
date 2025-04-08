# 🤖 **AI-Powered Hiring Assistant Chatbot**

## 📄 **Project Overview**

*Hiring Assistant Chatbot* is an intelligent, Streamlit-based chatbot designed to streamline the initial candidate screening process. It gathers essential candidate information and poses **5 tailored technical questions** based on the candidate’s declared tech stack and years of experience. The chatbot uses the GitHub Marketplace GPT-4o model, enabling free usage of what would otherwise be a paid OpenAI API key—all while maintaining identical functionality to the standard OpenAI implementation (aside from the BASE_URL).

### <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="40" height="22"> Live Demo
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://langchain-chatbot.streamlit.app/)  

<img width="860" alt="Image" src="https://github.com/user-attachments/assets/0f79e257-6b83-468a-9d48-d3a038921163" />

---

## ✨ **Key Features**

- **Cost-Efficient AI:** Uses GitHub Marketplace's GPT-4o model (free) instead of paid OpenAI API.
- **Smart Screening:**
  - ✅ Automated info collection *(contact, experience, tech stack)*
  - 🧠 Context-aware technical questions tailored to candidate's experience level
- **Real-time Conversational UI:** Powered by Streamlit.
- **Data Management:** Auto-saves candidate conversations in JSON format.

---

## 🛠️ **Installation Instructions**

### 📥 **Clone the Repository**

```bash
git clone https://github.com/yourusername/AI-Hiring-Assistant-LLM-Chatbot.git
cd AI-Hiring-Assistant-LLM-Chatbot
```

### ⚙️ **Environment Setup**

1. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. **Install Required Libraries:**

   ```bash
   pip install -r requirements.txt
   ```

### 🔒 **Configure Environment Variables**

1. Create a `.env` file in the root directory.
2. Add your GitHub token *(acts as a fallback if not provided via the sidebar)*:

   ```plaintext
   GITHUB_TOKEN=your_github_token_here
   ```

> **Note:** The `.env` file is ignored by Git due to the included `.gitignore`.

### ▶️ **Run the Application**

```bash
streamlit run app.py
```

---

## 📚 **Usage Guide**

### 💻 **User Interface**

- **Welcome Screen:** Once running, the web-based interface displays a friendly welcome message and an instruction guide for the candidate.
- **GitHub Token Prompt:** If the `GITHUB_TOKEN` is not preset (via `.env`), you’ll be prompted in the sidebar to enter the token securely.

### 🔄 **Conversational Flow**

1. **Greeting & Information Collection:**  
   The chatbot greets the user and collects candidate details *(full name, email, phone, years of experience, position applied for, current location, and tech stack)*.

2. **Technical Evaluation:**  
   Based on the candidate’s declared tech stack and experience, exactly **5 technical questions** are generated dynamically.

3. **Conclusion:**  
   The conversation concludes with a thank-you message. The entire conversation is saved locally in the `submissions` folder.

4. **Exit Protocol:**  
   Type **exit** at any time to end the conversation.

---

## ⚙️ **Technical Details**

### 🧰 **Framework & Libraries**

- **Streamlit:** Building and rendering the web-based chat interface.
- **OpenAI (via GitHub Marketplace GPT-4o model):** Handles natural language generation *(integration identical to standard OpenAI API except for the BASE_URL)*.
- **dotenv:** Loads environment variables securely from a `.env` file.
- **Others:**  
  - `json` for saving conversation logs.
  - `datetime` for timestamping conversation files.
  - Native Python libraries.

### 🏗️ **Architectural Decisions**

- **Modular Design:**  
  The code is partitioned into modules such as:
  - **`app.py`** – Chat interface.
  - **`prompts.py`** – Contains preset greeting, system prompts, and thank-you messages.

- **Session State Management:**  
  Uses Streamlit’s session state to manage conversation data, ensuring continuity across interactions.

- **Extensibility:**  
  The design allows easy updates to prompt content and technical question logic based on candidate responses.

---

## 💬 **Prompt Design**

### 🔄 **Structured Conversational Flows**

- **Phase 1 – Information Collection:**  
     Gathers key candidate data *(name, email, phone, etc.)* before proceeding to technical evaluation.

- **Phase 2 – Technical Evaluation:**  
     Uses the candidate's tech stack and years of experience to dynamically generate **exactly 5 questions** with difficulty levels adjusted based on experience:
  - **Fallback and Correction:** If the candidate’s response is unclear or off-topic, the chatbot rephrases or redirects queries politely.
  - **Interaction Control:** One question is asked at a time. The chatbot waits for an answer before proceeding.
  - **Clear Boundaries:** The bot does not ask more than **5 questions** or deviate into non-technical topics.
  - **Controlled Conversation End:** After the 5th technical question, a thank-you prompt signals the end of the dialogue and triggers the conversation-saving process.

---

## 💡 **Challenges & Solutions**

- **Challenge:** *Securely managing the API key/token for the LLM.*  
  **Solution:** Utilize a `.env` file to store the sensitive `GITHUB_TOKEN` locally and include it in `.gitignore`. Provide a secure text input in the Streamlit sidebar as a fallback.

- **Challenge:** *Ensuring the chatbot follows the multi-step screening process (info gathering → technical questions).*  
  **Solution:** Use a detailed `SYSTEM_PROMPT` that outlines the two distinct phases, specifies the required information, and sets constraints on question number and type.

- **Challenge:** *Generating technical questions that are relevant and appropriately difficult for the candidate.*  
  **Solution:** Include specific instructions in the `SYSTEM_PROMPT` to base questions on the candidate's declared tech stack and adjust difficulty based on years of experience *(beginner, moderate, advanced)*.

- **Challenge:** *Accessing powerful LLM capabilities without incurring costs.*  
  **Solution:** Leverage the free GitHub Marketplace GPT-4o model by configuring the standard OpenAI Python client to use the model’s specific Azure endpoint and authenticate using a GitHub token.

---

## 🔧 **Code Quality & Structure**

- **Structure & Readability:**
  - Organized into logical files (**`app.py`**, **`prompts.py`**).
  - Uses modular functions *(e.g., `initialize_chat_data`, `render_history`, `handle_user_input`, `_save_conversation`)*.
  - Consistent naming conventions enhance readability.
  
- **Documentation:**
  - Inline comments explain code sections.
  - Docstrings for key functions describe their purpose, arguments, and behavior.
  
- **Version Control:**
  - Uses Git for version control.
  - The repository includes a **`.gitignore`** file to exclude sensitive information *(`.env`)* and unnecessary files *(venv/, __pycache__/)*.
  
- **Maintainability:**
  - Separating prompts into **`prompts.py`** makes updates easier.
  - Modular function design simplifies debugging and adding new features.

---

## 📁 **Project Structure**

```plaintext
AI-Hiring-Assistant-LLM-Chatbot/
├── submissions/           # Stores saved conversation logs as JSON files
├── app.py                 # Main Streamlit chat application controller
├── prompts.py             # Contains greeting, system prompts, and thank you messages
├── requirements.txt       # Lists project dependencies
├── readme.md              # This documentation file
├── .gitignore             # Specifies files/directories to be ignored by Git
└── .env                   # Environment configuration (ignored by Git)
```
