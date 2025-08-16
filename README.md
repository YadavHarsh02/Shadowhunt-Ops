# ShadowHunt Ops

**ShadowHunt Ops** is a simulated cybersecurity dashboard for educational purposes.  
It includes modules for Brute-Force, SQL Injection, NTLM extraction, and Recon scanning—all in simulation mode.  
**For lab/test targets only. No real attacks executed.**

## Features
- Health Check API
- Simulated Brute-Force
- Simulated SQL Injection
- NTLM Extractor (simulated)
- Recon Scanner (simulated)
- Logs and Reporting

## Prerequisites
- Python 3.10+  
- Git
- Virtual environment (venv)
- SQLite (default DB included)

## Setup Instructions
1. **Clone the repository**
```bash
git clone https://github.com/YadavHarsh02/Shadowhunt-Ops.git
cd Shadowhunt-Ops

2. **Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows

3. **Install Dependencies
pip install -r requirements.txt

4.Run the application
python app.py

5. Open the dashboard
In your browser, navigate to: http://127.0.0.1:5000

6. Usage Notes

- All modules are simulated for lab/test purposes.

- Avoid pointing modules at real external systems.

- Logs are saved in the local SQLite database (shadowhunt.db) and can be viewed via the dashboard.

- Reports can be generated directly from the dashboard using the "Generate Report" feature.
