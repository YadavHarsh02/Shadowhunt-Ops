from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from config import Config
from database.models import db, AttackLog
from modules import run_module
from reports.generator import generate_simple_report
from datetime import datetime
import json
from urllib.parse import urlparse

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)

    @app.route("/")
    def ui():
        return render_template("dashboard.html")

    @app.route("/api/health")
    def health():
        return jsonify({
            "status": "ok",
            "message": "ShadowHunt Ops API up",
            "test_mode": app.config.get("TEST_MODE", True)  # FIX: default True
        })

    @app.route("/api/logs", methods=["GET"])
    def get_logs():
        rows = AttackLog.query.order_by(AttackLog.timestamp.desc()).limit(50).all()
        return jsonify([{
            "id": r.id,
            "module": r.module,
            "target": r.target,
            "output": r.output,
            "success": r.success,
            "timestamp": r.timestamp.isoformat() + "Z"
        } for r in rows])

    @app.route("/api/report", methods=["POST"])
    def make_report():
        data = request.get_json(force=True) or {}
        filename = data.get("filename", f"report-{int(datetime.utcnow().timestamp())}.pdf")
        logs = AttackLog.query.order_by(AttackLog.timestamp.asc()).all()
        rows = [{
            "module": r.module,
            "target": r.target,
            "output": r.output,
            "timestamp": r.timestamp.isoformat() + "Z"
        } for r in logs]
        path = f"reports/{filename}"
        generate_simple_report(path, "ShadowHunt Ops – Activity Report", rows)
        return jsonify({"status": "ok", "file": path})

    @app.route("/api/attack/<module>", methods=["POST"])
    def attack(module):
        payload = request.get_json(force=True) or {}

        # Safety: enforce allowlist for restricted modules
        if not _is_allowed_target(app.config, module, payload):
            return jsonify({
                "status": "error",
                "details": "Target not in allowlist (localhost only in DEV)."
            }), 400

        result = run_module(module, payload)

        # Persist log
        log = AttackLog(
            module=module,
            target=_extract_target(payload),
            input_params=json.dumps(payload),
            output=result.get("details", ""),
            success=result.get("status") == "ok"
        )
        db.session.add(log)
        db.session.commit()

        return jsonify({
            "status": result.get("status"),
            "details": result.get("details"),
            "log_id": log.id
        })

    return app


def _extract_target(payload: dict) -> str:
    # Try to pull a host/URL field for logging
    for k in ("url", "target", "host"):
        if k in payload and payload[k]:
            v = payload[k]
            if isinstance(v, str) and v.startswith("http"):
                try:
                    return urlparse(v).netloc or v
                except Exception:
                    return v
            return v
    return "unknown"


def _is_allowed_target(cfg, module: str, payload: dict) -> bool:
    # For Brute-Force and SQLi in DEV, skip allowlist
    if module in ["brute-force", "sql-injection"]:
        return True

    # For other modules, allow only localhost/127.0.0.1
    t = _extract_target(payload)
    host = t.split(":")[0]
    return host in getattr(cfg, "ALLOWLIST_TARGETS", set())


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
