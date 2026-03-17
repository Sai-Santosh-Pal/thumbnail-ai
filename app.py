from flask import Flask, render_template, request
import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


def action(title, ideas, inspo_base64, assets_base64):
    API_KEY = os.getenv("API_KEY")

    url = "https://ai.hackclub.com/proxy/v1/chat/completions"

    content = []
    content.append({
        "type": "text",
        "text": f"""Modify the provided base thumbnail using the base image and the attached inspiration assets.

Context
Video Title: {title}
Core Ideas / Hook: {ideas}

Task
Create a high-impact YouTube thumbnail optimized for CTR.

Instructions
- Use the base image as the primary foundation of the thumbnail.
- Use the attached inspiration images (inspo assets) as visual references for composition, layout, color grading, subject emphasis, and text styling.
- Extract strong visual patterns from the inspiration assets such as:
  • subject placement  
  • contrast and lighting  
  • color palette  
  • background treatment  
  • text style and size  
  • emotional emphasis
- Adapt these strategies to the base image rather than copying the inspiration directly.
- If helpful, incorporate visual elements inspired by the assets (glow, highlights, emphasis shapes, gradients, arrows, etc.).

Image Enhancement
- Improve overall lighting and exposure.
- Increase contrast and dynamic range so the subject stands out strongly.
- Add cinematic lighting such as rim light, glow, or directional highlights to separate the subject from the background.
- Enhance color vibrancy while keeping tones clean and not oversaturated.
- Sharpen key subjects while slightly softening background elements for depth.

Design Requirements
- Maintain a clean 16:9 YouTube thumbnail composition.
- Ensure one dominant focal subject.
- Use strong contrast so the subject pops from the background.
- If text is added, keep it minimal (1–4 words) and very large.
- Ensure readability at small sizes.
- Avoid clutter or multiple competing elements.

Goal
Produce a polished, visually striking YouTube thumbnail that combines:
- the base image
- inspiration asset design strategies
- improved lighting and clarity
- strong YouTube thumbnail design principles.""""
    })

    # add inspiration images
    for img in inspo_base64:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{img}"}
        })

    # add assets images
    for img in assets_base64:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{img}"}
        })

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

    img_data_url = data["choices"][0]["message"]["images"][0]["image_url"]["url"]

    return img_data_url


@app.route("/upload", methods=["POST"])
def upload():
    assets_imgs = request.files.getlist("assets")
    inspo_imgs = request.files.getlist("inspiration")

    video_title = request.form.get("video-title")
    ideas = request.form.get("ideas")

    assets_base64 = []
    inspo_base64 = []

    # convert assets to base64
    for a in assets_imgs:
        if a:
            image_bytes = a.read()
            assets_base64.append(base64.b64encode(image_bytes).decode())

    # convert inspiration to base64
    for i in inspo_imgs:
        if i:
            image_bytes = i.read()
            inspo_base64.append(base64.b64encode(image_bytes).decode())

    image_url = action(video_title, ideas, inspo_base64, assets_base64)

    return f"<img src='{image_url}'>"


if __name__ == "__main__":
    app.run(debug=True, port=5600)
