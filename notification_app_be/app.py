from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():

    return jsonify({

        "message":
        "Notification Backend Running"

    }), 200


@app.route("/notifications")
def get_notifications():

    token = os.getenv("ACCESS_TOKEN")

    url = (
        "http://4.224.186.213/"
        "evaluation-service/notifications"
    )

    headers = {

        "Authorization":
        f"Bearer {token}"
    }

    try:

        response = requests.get(
            url,
            headers=headers
        )

        if response.status_code != 200:

            return jsonify({

                "error":
                "Failed to fetch notifications"

            }), response.status_code

        data = response.json()

        return jsonify(data), 200

    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500


@app.route("/priority")
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

    return jsonify({

        "notifications":
        sorted_notifications[:10]

    }), 200


if __name__ == "__main__":

    app.run(debug=True)