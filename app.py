from flask import Flask, render_template, request, jsonify
from fuzzywuzzy import fuzz, process
import json
import random

app = Flask(__name__)

# Load intents from intents.json
with open('intents.json') as file:
    intents = json.load(file)

class Chatbot:
    def __init__(self, intents):
        self.intents = intents

    def get_response(self, user_message):
        user_message = user_message.lower()  # Convert user message to lowercase

        # Create a list of all patterns from intents
        all_patterns = [(pattern, intent['tag']) for intent in self.intents['intents'] for pattern in intent['patterns']]

        # Use fuzzywuzzy's process.extract to find the closest matching pattern
        closest_match = process.extractOne(user_message, [pattern for pattern, tag in all_patterns], scorer=fuzz.partial_ratio)

        # If a close match is found with a score of 70 or more
        if closest_match and closest_match[1] >= 70:
            matched_pattern = closest_match[0]
            matched_tag = next(tag for pattern, tag in all_patterns if pattern == matched_pattern)

            # Find the corresponding intent and return a random response
            for intent in self.intents['intents']:
                if intent['tag'] == matched_tag:
                    return random.choice(intent['responses'])

        return "Sorry, I didn't quite understand that. Could you please rephrase?"

# Create chatbot instance
chatbot = Chatbot(intents)

@app.route('/')
def index():
    return render_template('index.html')  # Load the chat HTML page

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_message = request.json.get('message')  # Get the user message from the request
        bot_response = chatbot.get_response(user_message)  # Get the bot's response
        return jsonify({'response': bot_response})  # Return response as JSON
    except Exception as e:
        return jsonify({'response': 'An error occurred: ' + str(e)})

if __name__ == '__main__':
    app.run(debug=True)
