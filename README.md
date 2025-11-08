# Swastha - Healthcare Support Website

Swastha is a healthcare support web application that helps users find nearby hospitals based on their location. It includes features such as emergency contact setup and email alerts, a chatbot assistant for health advice, period tracking, and more. The app offers quick access to emergency services and personalized health monitoring tools to support users in urgent and daily wellness situations.

---

## Features

- Detect or accept the user’s location to display hospitals nearby.
- Setup and send emergency emails to trusted contacts.
- Chatbot assistant for instant health advice.
- Period tracker and hydration, sleep, and medication health tracker.
- Responsive UI with easy navigation.

---

## Tech Stack

- Python Flask (backend)
- Flask-SQLAlchemy (database ORM)
- Flask-Mail (email sending)
- SQLite (local database)
- HTML, CSS, JavaScript (frontend)
- Overpass API for hospital data
- Gemini API for chatbot responses

---

## Prerequisites

Make sure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)

---

## Installation and Setup

1. **Clone the repository** or download the project files.

2. **Create and activate a virtual environment** (optional but recommended):



python -m venv venv
source venv/bin/activate   \# On Windows use: venv\Scripts\activate



3. **Install required Python packages**:



pip install -r requirements.txt



(If you don't have a `requirements.txt` file, install these manually):



pip install Flask Flask-SQLAlchemy Flask-Mail python-dotenv requests werkzeug



4. **Create a `.env` file** in the root directory with the following variables:



GEMINIAPIKEY=your_gemini_api_key_here
EMAILUSER=your_email@example.com
EMAILPASSWORD=your_email_password_or_app_password



Replace the placeholder values with your actual Gemini API key and email credentials for sending emergency emails.

5. **Initialize the SQLite database**:

Run the following to create database tables:



python createdb.py



---

## Running Locally

1. Make sure your virtual environment is activated (if using one).

2. Run the Flask application:



python app.py



3. By default, the app will run on `http://127.0.0.1:5000/`.

4. Open this URL in your browser to access the app.

---

## Application Structure

- `app.py` - Main Flask app with routes and backend logic.
- `createdb.py` - Script to create the database tables.
- `templates/` - HTML templates for rendering pages.
- `static/` - CSS, JavaScript, and image assets.
- `.env` - Environment variables for API keys and email credentials.

---

## Usage

- Register and log in to the app using your email and password.
- Set up emergency contacts via the Emergency Email section.
- Use the chatbot for health advice.
- Track periods, hydration, sleep, and medication from the provided trackers.
- Search and view nearby hospitals using your location.

---

## Notes

- Ensure your email credentials support SMTP with SSL (Gmail app passwords recommended).
- The nearby hospital search uses the Overpass API (OpenStreetMap).
- The chatbot uses the Gemini API; ensure your API key is valid.
- The app is designed for local development and testing; additional deployment configuration may be required for production.

---

## License

This project is for educational and personal use. Please check licensing before commercial use.

---

If you need help or want to contribute, please reach out.



