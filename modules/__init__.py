# modules/__init__.py
from .brute_force import run as brute_force_run
from .sql_injection import run as sql_injection_run
from .ntlm_extractor import run as ntlm_extractor_run
from .recon_scanner import run as recon_scanner_run

MODULES = {
    "brute-force": brute_force_run,
    "sql-injection": sql_injection_run,
    "ntlm-extractor": ntlm_extractor_run,
    "recon-scanner": recon_scanner_run,
}

def run_module(name: str, payload: dict) -> dict:
    if name not in MODULES:
        return {"status": "error", "details": f"Unknown module: {name}"}
    return MODULES[name](payload)
