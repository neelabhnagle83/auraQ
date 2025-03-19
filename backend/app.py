from flask import Flask, request, jsonify
from ai_analysis import analyze_mood
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp  # Importing authentication routes

app = Flask(__name__)

# Set CORS for specific routes
CORS(app, resources={r"/auth/*": {"origins": "http://127.0.0.1:5500"},
                     r"/analyze": {"origins": "http://127.0.0.1:5500"}})  # Combined CORS policy

bcrypt = Bcrypt(app)

# Secret key for JWT (change it in production)
app.config["JWT_SECRET_KEY"] = "supersecretkey"
jwt = JWTManager(app)

# Register Blueprints (for modular routes)
app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        print(f"DEBUG: Received Data: {data}")  # 🔍 Check what is sent

        if not data or "story" not in data:
            return jsonify({"error": "No story provided"}), 400

        story = data["story"].strip()
        if not story:
            return jsonify({"error": "Story cannot be empty"}), 400

        # Get mood and feedback using the analyze_mood function
        mood_feedback = analyze_mood(story)

        print(f"DEBUG: Mood: {mood_feedback['mood']}, Feedback: {mood_feedback['feedback']}")  # 🔍 Log AI response

        if mood_feedback["mood"] == "Unknown":
            return jsonify({"error": "Failed to analyze mood"}), 500

        return jsonify(mood_feedback)  # Return the mood and feedback dynamically

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")  # Log errors in console
        return jsonify({"error": "Internal Server Error"}), 500

# Vercel handler function
def handler(event, context):
    """Vercel entrypoint for handling requests."""
    return app(event, context)

if __name__ == "__main__":
    app.run(debug=True)
