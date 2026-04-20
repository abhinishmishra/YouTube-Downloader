from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import uuid
import yt_dlp

app = Flask(__name__)

# Folder setup
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    try:
        data = request.get_json()
        url = data.get("url", "").strip()
        typ = data.get("type", "mp4")
        

        if not url:
            return jsonify({"success": False, "error": "Please enter URL"})

        uid = str(uuid.uuid4())[:8]
        outtmpl = os.path.join(DOWNLOAD_DIR, uid + ".%(ext)s")

        # Main yt-dlp options (Chrome cookies removed)
        opts = {
            "outtmpl": outtmpl,
            "quiet": True,
            "noplaylist": True,
            "nocheckcertificate": True,
            "ffmpeg_location": r"C:\Users\abhin.LAPTOP-EKBM7SSA.000\Downloads\ffmpeg-2026-04-16-git-5abc240a27-full_build\bin\ffmpeg-2026-04-16-git-5abc240a27-full_build\bin"
            
        
        }

        # MP3 Download
        if typ == "mp3":
            opts["format"] = "bestaudio/best"
            opts["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]

        # MP4 Download
        else:
           
            opts["format"] = "bestvideo+bestaudio/best"
            opts["merge_output_format"] = "mp4"
            opts["format"] = "best[ext=mp4]/best"
            
        # Download
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

        # Find downloaded file
        for f in os.listdir(DOWNLOAD_DIR):
            if f.startswith(uid):
                return jsonify({
                    "success": True,
                    "file": f
                })

        return jsonify({"success": False, "error": "File not found"})

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route("/file/<name>")
def file(name):
    return send_from_directory(DOWNLOAD_DIR, name, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)