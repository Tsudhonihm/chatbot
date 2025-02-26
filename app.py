from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from transformers import AutoTokenizer, AutoModelForCausalLM

# Initialize the Flask app
app = Flask(__name__)

# Apply CORS for your domain only
CORS(app, resources={r"/message": {"origins": "http://anything-boes.com"}})

# Load DialoGPT tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Home route to serve index.html
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
        
        # Encode the user's input
        input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors="pt")

        # Generate a response using DialoGPT
        response_ids = model.generate(
            input_ids,
            max_length=1000,  # Limit the response length
            pad_token_id=tokenizer.eos_token_id,  # Ensure proper padding
            no_repeat_ngram_size=2,  # Avoid repeating phrases
            top_p=0.95,  # Use nucleus sampling
            top_k=50,  # Limit the number of tokens considered
            do_sample=True  # Enable sampling for more diverse responses
        )

        # Decode the bot's response
        bot_response = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        # Return the response as JSON
        return jsonify({'response': bot_response}), 200
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(debug=True, host="0.0.0.0", port=port)
