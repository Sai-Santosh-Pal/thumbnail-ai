from flask import Flask, render_template, request
import os
import base64
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

global status
status = ""         

UPLOAD = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD

@app.route("/")
def home():
    return render_template("index.html")

def action(title, ideas, inspo, assets):
    load_dotenv()

    try:
        API_KEY = os.getenv("API_KEY")
    except Exception as e:
        API_KEY = str(input("Hack Club AI API Key - "))

    url = "https://ai.hackclub.com/proxy/v1/chat/completions"
    
    content = []
    content.append({"type": "text", "text": f"Modify the thumbnail use the assets as well as the base img: here is some important info too - {title}, {ideas}"})
    for i in inspo:
        with open(i, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode()
        toAppend = {"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
        content.append(toAppend)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemini-2.5-flash-image",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "modalities": ["image", "text"],
        "image_config": {
            "aspect_ratio": "16:9"
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    # Get generated image
    img_data_url = data["choices"][0]["message"]["images"][0]["image_url"]["url"]

    # Remove data:image/png;base64,
    img_base64 = img_data_url.split(",")[1]

    # Save image
    with open("generated.png", "wb") as f:
        f.write(base64.b64decode(img_base64))

    return "Image saved as generated.png\n\n\n\n" + content


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

    print(all_assets)
    print("\n\n\n\n")
    print(all_inspos)
    return action(video_title, ideas, all_inspos, all_assets)

if __name__ == "__main__":
    app.run(debug=True, port=5600) 