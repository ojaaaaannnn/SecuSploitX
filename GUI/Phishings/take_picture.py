import subprocess
from flask import Flask, request, send_from_directory , render_template
import os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cloudflared_path = os.path.join(BASE_DIR, "cloud_flare", "cloudflared.exe")

if os.path.exists(cloudflared_path):
    subprocess.Popen([cloudflared_path, "tunnel", "--url", "http://localhost:5000"])
else:
    print(f"cloudflared.exe not found at {cloudflared_path}")

UPLOAD_DIR = os.path.join(os.getcwd(), 'uploads', 'session1')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files
    saved_files = []

    for key in files:
        file = files[key]
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        filename = f"{timestamp}-{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        file.save(file_path)
        saved_files.append(filename)

    print("Files saved:", saved_files)
    return {"status": "success", "files": saved_files}, 200

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory(os.getcwd(), path)

@app.route('/')
def index():
    return render_template('omegale.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
