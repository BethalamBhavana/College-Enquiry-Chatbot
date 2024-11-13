import json
import random
import re

class Chatbot:
    def __init__(self):
        # Load intents from the JSON file
        with open("intents.json") as file:
            self.intents = json.load(file)

    def get_response(self, user_message):
        user_message = user_message.lower()  

        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                # Use regex or simple pattern matching to find a match
                if re.search(r'\b' + re.escape(pattern.lower()) + r'\b', user_message):
                    return random.choice(intent['responses'])

        # If no pattern matches, return a default response
        return "I'm sorry, I didn't understand that. Can you please rephrase?"

# For testing the Chatbot class directly
if __name__ == "__main__":
    chatbot = Chatbot()
    while True:
        user_message = input("You: ")
        bot_response = chatbot.get_response(user_message)
        print(f"Bot: {bot_response}")
