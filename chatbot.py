# Import necessary packages
import json
import random
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import nltk
nltk.download('punkt')

# Declare WordNetLemmatizer
from nltk.stem import snowball
snowballStemmer = snowball.SnowballStemmer("english")

class Chatbot:
    def __init__(self):
        self.intent_list = []
        self.train_data = []
        self.train_label = []
        self.responses = {}
        self.vectorizer = None
        self.train_data_bow = []
        self.clf_nb = None
        self.load_json()
        self.feature_extraction()
        self.model_training()

    
    # Function to preprocess text
    def text_preprocessing(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        stem_tokens = []
        for token in tokens:
            stem_tokens.append(snowballStemmer.stem(token.lower()))

        for token in stem_tokens:
            if not token.isalnum():
                stem_tokens.remove(token)
        return " ".join(stem_tokens)
    
    def load_json(self):
        with open("intents.json") as f:
            data = json.load(f)
        
        for intent in data['intents']:
            for text in intent['text']:
                preprocessed_text = self.text_preprocessing(text)
                self.train_data.append(preprocessed_text)
                self.train_label.append(intent['intent'])
                # add to list of class
                
            self.intent_list.append(intent['intent'])
            self.responses[intent['intent']] = intent["responses"]
    
    def feature_extraction(self):
        self.vectorizer = CountVectorizer()
        self.vectorizer.fit(self.train_data)
        self.train_data_bow = self.vectorizer.transform(self.train_data)
    
    def model_training(self):
        self.clf_nb = MultinomialNB()
        self.clf_nb.fit(self.train_data_bow, self.train_label)
    
    def chatbot_response(self, query):
        query_processed = self.text_preprocessing(query)
        query_bow = self.vectorizer.transform([query_processed])
        predicted = self.clf_nb.predict(query_bow)
        max_proba = max(self.clf_nb.predict_proba(query_bow)[0])

        if max_proba < 0.08:
            predicted = ['noanswer']
        
        bot_response = ""
        numOfResponses = len(self.responses[predicted[0]])
        chosenResponse = random.randint(0, numOfResponses-1)

        if predicted[0] == "TimeQuery":
            bot_response = eval(self.responses[predicted[0]][chosenResponse])
        else:
            bot_response = self.responses[predicted[0]][chosenResponse]

        return bot_response





