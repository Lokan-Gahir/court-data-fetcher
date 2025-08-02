# Court Data Fetcher & Dashboard
![App Screenshot](screenshot.png)

A Flask web app to fetch case details from Delhi High Court with dashboard.

## Features
- Search by case type/number/year
- View parties, dates, and documents
- SQLite database storage
- CAPTCHA handling with manual solve

## Setup
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   playwright install
Run the app:

bash
python app.py
Access at http://localhost:5000

CAPTCHA Handling
Manual solving during development (20-second pause).

Database
SQLite stores all queries at database/court_data.db.

For educational purposes only.

text

---

### **Step-by-Step GitHub Upload**

#### **1. Prepare Your Files**
Ensure your project has:
court-data-fetcher/
├── app.py
├── requirements.txt
├── .gitignore
└── database/ (empty - SQLite will auto-create)