from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# =========================
# LOAD ENV FILE
# =========================

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=env_path)

# =========================
# CREATE FLASK APP
# =========================

app = Flask(__name__)

# =========================
# GET ACCESS TOKEN
# =========================

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Notification Backend Running"
    }), 200

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy"
    }), 200


# =========================
# FETCH NOTIFICATIONS
# =========================

@app.route("/notifications", methods=["GET"])
def get_notifications():

    url = "http://4.224.186.213/evaluation-service/notifications"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    try:

        response = requests.get(
            url,
            headers=headers
        )

        print("STATUS CODE:", response.status_code)

        print("RESPONSE:", response.text)

        try:

            data = response.json()

        except Exception:

            data = {
                "raw_response": response.text
            }

        return jsonify(data), response.status_code

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/priority", methods=["GET"])
def priority_notifications():

    notifications = [

        {
            "type": "Placement",
            "message": "Google Hiring",
            "timestamp": 5
        },

        {
            "type": "Results",
            "message": "Results Published",
            "timestamp": 3
        },

        {
            "type": "Event",
            "message": "Hackathon",
            "timestamp": 1
        }
    ]

    priority_map = {

        "Placement": 1,
        "Results": 2,
        "Event": 3
    }

    sorted_notifications = sorted(

        notifications,

        key=lambda notification: (

            priority_map[
                notification["type"]
            ],

            -notification["timestamp"]
        )
    )

    top_notifications = (
        sorted_notifications[:10]
    )

    return jsonify({

        "notifications":
        top_notifications

    }), 200

if __name__ == "__main__":

    app.run(debug=True)