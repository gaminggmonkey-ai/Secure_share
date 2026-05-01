from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import sqlite3
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create DB
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files (
        id TEXT PRIMARY KEY,
        filename TEXT,
        password TEXT,
        expiry TEXT,
        downloads INTEGER
    )''')
    conn.commit()
    conn.close()

init_db()

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Upload
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    password = request.form.get("password")
    expiry_minutes = int(request.form.get("expiry"))

    if file:
        file_id = str(uuid.uuid4())
        filename = file.filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file_id + "_" + filename)
        file.save(filepath)

        expiry_time = datetime.now() + timedelta(minutes=expiry_minutes)

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO files VALUES (?, ?, ?, ?, ?)",
                  (file_id, filename, password, expiry_time, 0))
        conn.commit()
        conn.close()

        link = url_for("download", file_id=file_id, _external=True)
        return render_template(
    "success.html",
    link=link,
    filename=filename,
    expiry_minutes=expiry_minutes
)

    return redirect("/")

# Download route
@app.route("/download/<file_id>", methods=["GET", "POST"])
def download(file_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM files WHERE id=?", (file_id,))
    file = c.fetchone()

    if not file:
        return "Invalid link"

    filename, password, expiry, downloads = file[1], file[2], file[3], file[4]

    # Check expiry
    if datetime.now() > datetime.fromisoformat(expiry):
        return "Link expired"

    # Password check
    if password:
        if request.method == "POST":
            entered = request.form["password"]
            if entered != password:
                return "Wrong password"
        else:
            return render_template("download.html", file_id=file_id)

    # Increase download count
    c.execute("UPDATE files SET downloads=? WHERE id=?", (downloads+1, file_id))
    conn.commit()
    conn.close()

    # Serve file
    for f in os.listdir(UPLOAD_FOLDER):
        if f.startswith(file_id):
            return send_from_directory(UPLOAD_FOLDER, f, as_attachment=True)

    return "File not found"
@app.route("/download_manual", methods=["POST"])
def download_manual():
    file_input = request.form["file_id"]
    password = request.form.get("password")

    # Extract ID from full URL if pasted
    if "/" in file_input:
        file_id = file_input.split("/")[-1]
    else:
        file_id = file_input

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM files WHERE id=?", (file_id,))
    file = c.fetchone()

    if not file:
        return "Invalid file ID"

    filename, stored_password, expiry, downloads = file[1], file[2], file[3], file[4]

    # Expiry check
    if datetime.now() > datetime.fromisoformat(expiry):
        return "Link expired"

    # Password check
    if stored_password:
        if password != stored_password:
            return "Incorrect password"

    # Increase download count
    c.execute("UPDATE files SET downloads=? WHERE id=?", (downloads+1, file_id))
    conn.commit()
    conn.close()

    # Send file
    for f in os.listdir(UPLOAD_FOLDER):
        if f.startswith(file_id):
            return send_from_directory(UPLOAD_FOLDER, f, as_attachment=True)

    return "File not found"

if __name__ == "__main__":
    app.run(debug=True)