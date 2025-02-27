# Chatbot Application

This is a Flask-based chatbot application powered by DialoGPT.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Tsudhonihm/chatbo/chatbot-project.git
   cd chatbot-project
2. Create a virtual environment and install dependencies:
    bash
    Copy python -m venv venv
3.   source venv/bin/activate  # On Windows: venv\Scripts\activate
     pip install -r requirements.txt
     Run the Flask app: bash Copy python app.py
4  Test the /message endpoint:

    bash:
   Copy curl -X POST http://127.0.0.1:5000/message \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello, how are you?"}'
