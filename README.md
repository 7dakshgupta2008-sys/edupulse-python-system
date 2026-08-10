# Student Academic Management System (SHA-256 Hashing Edition)

A complete Student Academic Management System built using **Python (Flask), C, Java, HTML5, CSS3, XAMPP MySQL, and Interactive Student AI Chatbot**, with **Cryptographic SHA-256 Password Hashing Security**.

---

## 🔒 SHA-256 Password Hashing Security

All user passwords are encrypted using Python's `hashlib.sha256()` before being stored in `database.json` and XAMPP MySQL `student_db`.

| Role | Login ID | Password | Stored SHA-256 Hash |
| :--- | :--- | :--- | :--- |
| **Student** | `STU-101` | `student123` | `cd6357efdd966de8dae3f193f0641838647ef7b9101f358352661c94488b0244` |
| **Admin** | `admin@school.com` | `admin123` | `8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918` |
| **Teacher** | `teacher@school.com` | `teacher123` | `909405d41f1737be7049aa69b50b55c2763b65ef399c55bdfcf0bfd6501c5f8e` |
| **Parent** | `robert@parent.com` | `parent123` | `eb2a370e7e174b0ed18fa7419e71ec50875e546114eb3b4831fb40f438a2e7df` |

---

## 🚀 How to Run in VS Code

1. Open VS Code ➔ Open Folder: `C:\Users\gupta\.gemini\antigravity\scratch\edupulse-python-system`
2. Open Terminal (`Ctrl + ~`) ➔ Run:
   ```bash
   python app.py
   ```
3. Open browser:  
   👉 **http://localhost:5000/login**
