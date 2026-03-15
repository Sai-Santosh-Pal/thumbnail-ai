from flask import Flask, render_template, request
import os
import base64
from dotenv import load_dotenv

load_dotenv() 

try:
    API_KEY = os.getenv("API_KEY")
except Exception as e:
    api_key = str(input("Hack Club AI API Key - "))

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

app = Flask(__name__)

global status
status = ""

UPLOAD = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD

@app.route("/")
def home():
    return render_template("index.html")

def action(title, ideas, inspo, assets):
    return "Done"

@app.route("/upload", methods=["POST"])
def upload():
    all_assets = []
    all_inspos = [] 

    assets_imgs = request.files.getlist("assets")
    inspo_imgs = request.files.getlist("inspiration")
    video_title = request.form.get("video-title")
    ideas = request.form.get("ideas")

    print(type(inspo_imgs))
    for a in assets_imgs:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], f"ASSETS_{a.filename}")
        a.save(filepath)
        all_assets.append(filepath)
    for i in inspo_imgs:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], f"INSPO_{i.filename}")
        i.save(filepath)
        all_inspos.append(filepath)

    # print(all_assets)
    # print("\n\n\n\n")
    # print(all_inspos)
    return action(video_title, ideas, all_inspos, all_assets)

if __name__ == "__main__":
    app.run(debug=True, port=5600) 