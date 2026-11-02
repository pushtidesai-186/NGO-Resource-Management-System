NGO Resource & Volunteer Management System
========================================
WINDOWS:
1. Install Python 3.10+ from https://www.python.org/downloads/ (tick Add Python to PATH).
2. Extract this ZIP and open the folder in VS Code.
3. Terminal > New Terminal, then run:
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
4. Open http://127.0.0.1:5000

MAC / LINUX:
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python app.py

SQLite database ngo.db is created automatically. This demo has CRUD/search for
donors, beneficiaries, resources, volunteers, interns and events, plus reports.
Before real deployment, implement authentication, access control, validation,
backups and appropriate privacy/security protections.
