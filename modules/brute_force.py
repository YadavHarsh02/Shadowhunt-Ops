# modules/brute_force.py (Lab-safe replacement)

import time
import requests

def run(payload: dict) -> dict:
    """
    Lab-safe brute-force simulation against a test login server (localhost only).
    
    payload:
        target: URL of test login endpoint (e.g., http://127.0.0.1:5001/login)
        username: account to test
        wordlist: list of passwords to try
    """
    # Extract payload
    target = payload.get("target", "http://127.0.0.1:5001/login")
    username = payload.get("username", "admin")
    wordlist = payload.get("wordlist", ["1234", "password", "admin123", "letmein"])
    
    # Safety: ensure target is localhost
    if not target.startswith("http://127.0.0.1") and not target.startswith("http://localhost"):
        return {
            "status": "error",
            "module": "brute-force",
            "details": "Target not allowed. Only localhost testing is permitted."
        }

    results = []
    for pwd in wordlist:
        time.sleep(0.2)  # small delay to simulate real attack speed
        try:
            # Send POST request to local test server
            r = requests.post(target, data={"username": username, "password": pwd})
            # Check success condition in returned page text
            success = "Welcome" in r.text or "Logged in" in r.text
            status = "success" if success else "fail"
        except Exception as e:
            status = f"fail ({str(e)})"
        results.append({"username": username, "password": pwd, "status": status})

    # Determine if any password succeeded
    success_pwd = next((r["password"] for r in results if r["status"] == "success"), None)
    
    return {
        "status": "ok",
        "module": "brute-force",
        "details": f"Tested {len(wordlist)} passwords on {target}. Success: {success_pwd}",
        "attempts": results  # optional, logs all attempts
    }
