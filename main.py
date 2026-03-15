from flask import Flask, render_template, request
import os

app = Flask(__name__)

global status
status = ""

UPLOAD = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD

@app.route("/")
def home():
    return render_template("index.html")

def analyze(title, ideas, inspo, assets):
    print(title, ideas, inspo, assets)
    return "Done"

@app.route("/upload", methods=["POST"])
def upload():
    all_assets = []
    all_inspos = [] 

    assets_imgs = request.files.getlist("assets")
    inspo_imgs = request.files.getlist("inspiration")
    video_title = request.form.get("video-title")
    ideas = request.form.get("ideas")

    print(assets_imgs)
    print("\n")
    print(inspo_imgs)
    for a in assets_imgs:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], f"ASSETS_{a.filename}")
        a.save(filepath)
        all_assets += filepath

    for i in inspo_imgs:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], f"INSPO_{i.filename}")
        all_inspos += f"INSPO_{i.filename}"
        i.save(filepath)

    return analyze(video_title, ideas, all_inspos, all_assets)

if __name__ == "__main__":
    app.run(debug=True, port=5600) 