from flask import Flask, jsonify, request
from detect import FaceDetector
import os
import json

app = Flask(__name__)
face_detector = FaceDetector(json.loads(os.getenv("GCP_CREDS")))


@app.route("/")
def index():
    return jsonify({"Hello": "Mitek"})


@app.route("/detect_faces", methods=["POST"])
def detect_faces():
    if request.method == "POST":
        data = request.get_json()
        image_url = data.get("image_url")
        image_64 = data.get("image_64")

        if not image_url and not image_64:
            return jsonify({"error": "Missing image_url or image_64 parameter"}), 400

        try:
            if image_64:
                result = face_detector.detect_faces_base64(image_64)
            else:
                result = face_detector.detect_faces_uri(image_url)
            return jsonify({"result": result}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/detect_faces", methods=["GET"])
def curl_example():
    curl_command = "curl -X POST \\\n  http://127.0.0.1:8080/detect_faces \\\n  -H 'Content-Type: application/json' \\\n  -d '{\"image_url\": \"YOUR_IMAGE_URL_HERE\"}'"
    return jsonify({"curl_example": curl_command})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)