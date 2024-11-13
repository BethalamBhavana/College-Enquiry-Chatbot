import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
import json
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents file
with open('intents.json') as file:
    intents = json.load(file)

# Initialize lists
patterns = []
classes = []
responses = []

# Process intents
for intent in intents['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        responses.append(intent['responses'])
    if intent['tag'] not in classes:
        classes.append(intent['tag'])

# Create training data
X_train = patterns
y_train = [intent['tag'] for intent in intents['intents'] for _ in intent['patterns']]

# Initialize a text processing pipeline with CountVectorizer and MultinomialNB
model = Pipeline([
    ('vectorizer', CountVectorizer(tokenizer=nltk.word_tokenize, preprocessor=lambda x: x.lower())),
    ('classifier', MultinomialNB())
])

# Train the model
model.fit(X_train, y_train)

# Save models and data
with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('models/classes.pkl', 'wb') as f:
    pickle.dump(classes, f)

with open('models/responses.pkl', 'wb') as f:
    pickle.dump(responses, f)
