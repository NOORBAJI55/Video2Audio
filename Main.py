from flask import Flask, render_template, request, send_file, Response
from moviepy import VideoFileClip
import os
import time

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

progress = 0  # global variable to track progress

@app.route("/", methods=["GET", "POST"])
def index():
    global progress
    if request.method == "POST":
        progress = 0  # reset progress

        if "video" not in request.files:
            return "No file uploaded", 400
        
        file = request.files["video"]
        if file.filename == "":
            return "No file selected", 400
        
        # Save uploaded file
        video_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(video_path)

        # Support any video format
        base_name = os.path.splitext(file.filename)[0]
        output_filename = f"{base_name}.mp3"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        # Convert to MP3 with fake progress update
        clip = VideoFileClip(video_path)
        duration = clip.duration

        # Simulate progress updates
        for i in range(1, 6):
            progress = i * 20  # 20%, 40%, ...
            time.sleep(0.3)    # simulate small delay
        
        clip.audio.write_audiofile(output_path)
        progress = 100  # done

        # Send file and delete after sending
        def generate():
            with open(output_path, "rb") as f:
                yield from f
            os.remove(video_path)
            os.remove(output_path)

        return Response(generate(), headers={
            "Content-Disposition": f"attachment; filename={output_filename}",
            "Content-Type": "audio/mpeg"
        })

    return render_template("Full_App.html")

@app.route("/progress")
def get_progress():
    return {"progress": progress}

if __name__ == "__main__":
    app.run(debug=True)
