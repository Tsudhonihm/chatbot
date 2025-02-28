from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
import traceback
from transformers import AutoTokenizer, AutoModelForCausalLM

# Initialize the Flask app
app = Flask(__name__)

# Load environment variables
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://anything-boes.com").split(",")
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///app.db")  # Default SQLite database

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Define a sample model (optional, if you don't already have one)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Apply CORS
CORS(app, resources={r"/message": {"origins": ALLOWED_ORIGINS}})

# Load DialoGPT tokenizer and model globally
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small", padding_side="left")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

# Home route to serve index.html (optional)
@app.route('/')
def home():
    return render_template('index.html')

# Message route to handle user input
@app.route('/message', methods=['POST'])
def message():
    try:
        # Get the JSON payload from the request
        data = request.get_json()
        
        # Check if the message key exists and is not empty
        if not data or 'message' not in data:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        if len(user_message) > 500:
            return jsonify({'error': 'Message is too long'}), 400
        
        # Encode the user's input
        input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors="pt")
        
        # Generate a response using DialoGPT
        response_ids = model.generate(
            input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=2,
            top_p=0.95,
            top_k=50,
            do_sample=True
        )
        
        # Decode the bot's response
        bot_response = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        # Return the response as JSON
        return jsonify({'response': bot_response}), 200
    
    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Error: {str(e)}\nTraceback: {traceback.format_exc()}")
        # Return a generic error message to the client
        return jsonify({'error': 'An unexpected error occurred'}), 500

# Run the app
if __name__ == '__main__':
    # Get the PORT from the environment variable, defaulting to 8080 if not set
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
