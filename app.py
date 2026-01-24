from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from openai import OpenAI

app = Flask(__name__)

# ===== OPENAI =====
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ===== UPLOAD CONFIG =====
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        message = request.form.get("message", "").strip()
        file = request.files.get("file")

        image_url = None
        reply_text = None

        # ===== IMAGE HANDLE =====
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)
            image_url = "/" + save_path  # browser access path

        # ===== TEXT ONLY → AI REPLY =====
        if message:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=message
            )

            reply_text = response.output_text

        return jsonify({
            "reply": reply_text,
            "image": image_url
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "AI error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
