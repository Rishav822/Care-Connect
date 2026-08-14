from flask import Flask, render_template, request, jsonify, session
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from tensorflow.keras.models import load_model
import json
import random
import os
from pymongo import MongoClient  # <--- NEW IMPORT

app = Flask(__name__)
# Replace this with your own strong, random secret key
app.secret_key = os.urandom(24)

# --- MONGODB CONNECTION (NEW) ---
# Ensure MongoDB is running on your machine (default port 27017)
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['medibot_db']    # Creates a database named 'medibot_db'
    profiles = db['profiles']    # Creates a collection named 'profiles'
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")

# --- Load trained model and data files ---
# Ensure these files exist in your folder
lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

# --- Helper Functions ---
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return(np.array(bag))

def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    if not ints:
        return "I'm sorry, I don't understand that. Can you please rephrase?"
        
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    result = "I'm not sure how to respond to that. Could you ask in a different way?"
    for i in list_of_intents:
        if(i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result

def calculate_bmi(weight_kg, height_cm):
    if height_cm <= 0:
        return None, "Invalid height"
        
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    bmi = round(bmi, 2)
    
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obese"
        
    return bmi, category

# --- Flask Routes ---

@app.route("/")
def home():
    session.clear()
    return render_template("index.html")

# --- NEW: PROFILE MANAGEMENT ROUTES ---
@app.route('/save_profile', methods=['POST'])
def save_profile():
    try:
        data = request.json
        # Hardcoded ID for demo purposes (since we removed login)
        user_id = "user_1"
        
        profile_data = {
            "user_id": user_id,
            "name": data.get('name'),
            "age": data.get('age'),
            "gender": data.get('gender'),
            "emergency_contact": data.get('emergencyContact'),
            "allergies": data.get('allergies'),
            "medications": data.get('medications')
        }
        
        # Update if exists, Insert if new (upsert=True)
        profiles.update_one(
            {"user_id": user_id}, 
            {"$set": profile_data}, 
            upsert=True
        )
        
        return jsonify({"status": "success", "message": "Profile saved!"})
    except Exception as e:
        print(f"Error saving profile: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_profile', methods=['GET'])
def get_profile():
    try:
        user_id = "user_1"
        # Find the user's profile, exclude the internal MongoDB '_id'
        user_data = profiles.find_one({"user_id": user_id}, {"_id": 0})
        
        if user_data:
            return jsonify({"status": "success", "data": user_data})
        else:
            return jsonify({"status": "empty", "message": "No profile found"})
    except Exception as e:
        print(f"Error loading profile: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
# ----------------------------------------

@app.route("/get_response", methods=["POST"])
def get_bot_response():
    user_message = request.json['message']
    
    state = session.get('state', 'start')

    ints = predict_class(user_message, model)
    tag = ints[0]['intent'] if ints else None

    # --- State Machine Logic ---
    if state == 'awaiting_name':
        session['name'] = user_message
        session['state'] = 'awaiting_age'
        res = f"Nice to meet you, {session['name']}! How old are you?"

    elif state == 'awaiting_age':
        try:
            session['age'] = int(user_message)
            session['state'] = 'awaiting_weight'
            res = "Got it. What's your current weight in kilograms (e.g., 70)?"
        except ValueError:
            res = "Please enter a valid number for your age (e.g., 25)."

    elif state == 'awaiting_weight':
        try:
            session['weight_kg'] = float(user_message)
            session['state'] = 'awaiting_height'
            res = "Thanks. And what's your height in centimeters (e.g., 175)?"
        except ValueError:
            res = "Please enter a valid number for your weight in kg (e.g., 70.5)."

    elif state == 'awaiting_height':
        try:
            session['height_cm'] = float(user_message)
            bmi, category = calculate_bmi(session['weight_kg'], session['height_cm'])
            
            if bmi is None:
                res = "That doesn't seem like a valid height. Please enter your height in centimeters again (e.g., 175)."
            else:
                session['bmi'] = bmi
                session['bmi_category'] = category
                res = (f"Thank you, {session['name']}. Your BMI is {session['bmi']}, "
                       f"which is considered {category}. "
                       "Now, how can I help you with your medical questions?")
                session['state'] = 'chatting'
                
        except ValueError:
            res = "Please enter a valid number for your height in cm (e.g., 175)."

    elif state == 'start' and tag == 'greeting':
        session['state'] = 'awaiting_name'
        res = "Hello! I'm your medical assistant. To provide more personalized help, I need to ask a few questions. What's your name?"
    
    elif state == 'chatting':
        res = getResponse(ints, intents)
        name = session.get('name', 'Friend')
        
        if tag == 'thanks':
            res = f"You're welcome, {name}!"
        elif tag == 'goodbye':
            res = f"Goodbye, {name}! Stay healthy."
        elif tag == 'greeting':
            res = f"Hello again, {name}! How can I help?"
        elif tag == 'options':
            res = (f"As a {session.get('age','')} year old with a BMI of {session.get('bmi','')} ({session.get('bmi_category','')}), "
                   f"I can help you with general medical info, symptom checking, or first-aid tips. What would you like?")
        
    else: 
        res = getResponse(ints, intents)

    return jsonify({"response": res})

if __name__ == "__main__":
    app.run(debug=True)