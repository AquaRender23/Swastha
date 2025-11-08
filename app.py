from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import os
import requests
from werkzeug.security import generate_password_hash, check_password_hash


#Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
SENDER_EMAIL = os.getenv('EMAIL_USER')
SENDER_PASSWORD = os.getenv('EMAIL_PASSWORD')


app = Flask(__name__)
app.secret_key = 'a_secret_key'


#Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = SENDER_EMAIL
app.config['MAIL_PASSWORD'] = SENDER_PASSWORD
mail = Mail(app)


#SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


#Landing page route
@app.route('/')
def landing():
    return render_template('landing_page.html')


#Emergency Email main page
@app.route('/emergency-email')
def emergency_email():
    return render_template('emergency_email_main.html')


#Emergency Email setup
@app.route('/setup-emergency-email', methods=['GET', 'POST'])
def setup_emergency_email():
    if request.method == 'POST':
        emails = [request.form.get(f'email{i}') for i in range(1, 5)]
        session['emergency_emails'] = emails
        flash("Emergency contacts updated.", "success")
        return redirect(url_for('landing'))
    existing_emails = session.get('emergency_emails', ["", "", "", ""])
    return render_template('setup_emergency_email.html', emails=existing_emails)


#Emergency Email send route
@app.route('/send-emergency-email', methods=['POST'])
def send_emergency_email():
    emails = session.get('emergency_emails', ["", "", "", ""])
    subject = "EMERGENCY ALERT - Immediate Attention Needed"
    message_body = "This is an emergency alert triggered from Swastha app. Please check on the sender immediately."
    msg = EmailMessage()
    msg['From'] = SENDER_EMAIL
    msg['Subject'] = subject
    msg.set_content(message_body)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            for recipient in emails:
                if recipient:
                    msg['To'] = recipient
                    smtp.send_message(msg)
                    del msg['To']
        flash(f"Emergency emails sent to: {', '.join(filter(None, emails))}", "success")
    except Exception as e:
        flash(f"Failed to send emails: {str(e)}", "danger")
    return redirect(url_for('emergency_email'))

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')  # Make sure this template exists in your templates folder


#Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate inputs
        if not email or not username or not password or not confirm_password:
            flash("Please fill in all fields.", "danger")
            return redirect(url_for('register'))
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash(f"User {username} registered successfully!", "success")
        return redirect(url_for('homepage'))
    return render_template('register.html')


#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


# Gemini API Chatbot (POST)
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'answer': 'Please ask a question.'})
    payload = {
        "model": "gemini-2.5-flash",
        "contents": [
            {"role": "user", "parts": [{"text": f"Answer briefly: {question}"}]}
        ]
    }
    GEMINI_API_URL = (
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" +
        GEMINI_API_KEY
    )
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        print("Gemini raw response:", response.text)
        response.raise_for_status()
        result = response.json()
        answer = (
            result.get('candidates', [{}])[0]
            .get('content', {})
            .get('parts', [{}])[0]
            .get('text', 'Sorry, no answer from Gemini.')
        )
        return jsonify({'answer': answer})
    except Exception as e:
        print("Gemini API error:", e)
        import traceback
        traceback.print_exc()
        if hasattr(e, 'response') and e.response is not None:
            print("Status:", e.response.status_code)
            print("Response text:", e.response.text)
        return jsonify({'answer': 'Error communicating with Gemini API.'}), 500


#Chatbot frontend
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


@app.route('/chatbot/chat')
def chatbot_chat():
    return render_template('chatbot_interface.html')


#Trio Tracker
tracker_state = {
    "water_taken": 0,
    "water_goal": 10,
    "sleep_hours": 0,
    "sleep_goal": 8,
    "meds_taken": 0,
    "meds_goal": 5,
    "water_reminder": "8:00 PM",
    "sleep_reminder": "10:00 PM",
}


@app.route('/trio_tracker')
def trio_tracker():
    return render_template('trio_tracker.html', **tracker_state)


@app.route('/log_water', methods=['POST'])
def log_water():
    tracker_state["water_taken"] = min(tracker_state["water_taken"] + 1, tracker_state["water_goal"])
    return redirect(url_for('trio_tracker'))


@app.route('/add_sleep', methods=['POST'])
def add_sleep():
    tracker_state["sleep_hours"] += 0.5
    if tracker_state["sleep_hours"] > tracker_state["sleep_goal"]:
        tracker_state["sleep_hours"] = tracker_state["sleep_goal"]
    return redirect(url_for('trio_tracker'))


@app.route('/mark_meds', methods=['POST'])
def mark_meds():
    tracker_state["meds_taken"] = min(tracker_state["meds_taken"] + 1, tracker_state["meds_goal"])
    return redirect(url_for('trio_tracker'))


#Nearby hospitals main page
@app.route('/nearby_hospitals')
def nearby_hospitals():
    return render_template('nearby_hospitals.html')


#Hospital search using Overpass API - AJAX POST endpoint
def find_hospitals_osm(lat, lon, radius=5000):
    query = f"""
    [out:json];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      way["amenity"="hospital"](around:{radius},{lat},{lon});
      relation["amenity"="hospital"](around:{radius},{lat},{lon});
    );
    out center;
    """
    url = "https://overpass-api.de/api/interpreter"
    response = requests.post(url, data={'data': query})
    if response.status_code != 200:
        print("Error from Overpass API:", response.status_code)
        return []
    data = response.json()
    hospitals = []
    for element in data.get('elements', []):
        name = element['tags'].get('name', 'Unnamed hospital')
        # For ways/relations 'center' has lat/lon; for nodes use lat/lon directly
        if 'center' in element:
            lat = element['center']['lat']
            lon = element['center']['lon']
        else:
            lat = element.get('lat')
            lon = element.get('lon')
        hospitals.append({
            'name': name,
            'latitude': lat,
            'longitude': lon
        })
    return hospitals


@app.route('/search_hospitals', methods=['POST'])
def search_hospitals():
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')
    radius = data.get('radius', 5000)
    hospitals = find_hospitals_osm(lat, lon, radius)
    return jsonify(hospitals)


#FloBuddy page
@app.route('/flobuddy')
def flobuddy():
    return render_template('flobuddy.html')


#Test route (optional)
@app.route('/test')
def test():
    return "Test page works!"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
