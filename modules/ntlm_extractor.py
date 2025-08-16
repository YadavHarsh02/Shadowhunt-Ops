# modules/ntlm_extractor.py

def run(payload: dict):
    """
    Simulated NTLM Extractor Module
    """
    sample_file = payload.get("sample", "")

    # Only allow "dummy" files for safety
    if "dummy" not in sample_file.lower():
        return {"status": "error", "details": "Only dummy sample files allowed in DEV mode."}

    # Example simulated hashes
    hashes = [
        "aad3b435b51404eeaad3b435b51404ee:32ed87bdb5fdc5e9cba88547376818d4",
        "aad3b435b51404eeaad3b435b51404ee:5f4dcc3b5aa765d61d8327deb882cf99"
    ]

    details = f"Extracted {len(hashes)} hashes from {sample_file}: {', '.join(hashes)}"
    return {"status": "ok", "details": details}
