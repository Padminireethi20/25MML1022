from flask import Flask, jsonify, request
from datetime import  datetime
import time

app = Flask(__name__)

request_start_time = 0


# LOGGING MIDDLEWARE


@app.before_request
def before_request():

    global request_start_time

    request_start_time = time.time()

    print(f"Method: {request.method}")

    print(f"Endpoint: {request.path}")


@app.after_request
def after_request():

    execution_time = (
        time.time() - request_start_time
    )


    print(f"Status Code: {response.status_code}")

    print(
        f"Execution Time: "
        f"{execution_time:.4f} sec"
    )

    return response


@app.route("/")
def home():

    return jsonify({

        "message":
        "Logging Middleware Running"

    }), 200


@app.route("/health")
def health():

    return jsonify({

        "status": "healthy"

    }), 200


if __name__ == "__main__":

    app.run(debug=True)