# modules/sql_injection.py (SIMULATED)
def run(payload: dict) -> dict:
    url = payload.get("url", "http://localhost")
    return {
        "status": "ok",
        "module": "sql-injection",
        "details": f"[SIMULATION] Scanned {url} for SQLi patterns using test payloads (no exploitation).",
    }
