# Secure_share
#  Secure File Sharing System

This project is a simple web application that allows users to upload files and share them securely using a generated link.

The main idea was to build something practical where a file can be shared with control — like adding a password and setting an expiry time.

---

# What this project does

- Upload a file from your system  
- Generate a unique download link  
- Option to add a password for protection  
- Set expiry time (in minutes)  
- Download file using the link or manually entering ID  

---

# Why I built this

I wanted to try something more backend-focused and had also faced may issues regarding sharing files through links and downloading those files withoutany proper security for the files being shared.

This project helped me understand:
- how file uploads work in web apps  
- how to store and retrieve data using a database  
- how to manage access control (password + expiry)  
- how to connect frontend forms with backend logic  

---

# Tech Stack

- Python (Flask)  
- SQLite  
- HTML, CSS, JavaScript  

---

# Project Structure

secure_file_app/
│
├── uploads/
├── templates/
│   ├── index.html
│   ├── success.html
│   └── download.html
│
├── static/
│   └── style.css
│
├── app.py
├── database.db
└── requirements.txt

How it works
-Upload a file and optionally set password + expiry
-A unique link is generated
-The link can be shared
-The file can be downloaded using:
--direct link
--or manually entering the file ID
