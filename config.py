# config.py
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SHADOWHUNT_SECRET", "dev-shadowhunt-key")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'shadowhunt.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEST_NODE = True
    # Safety: only allow explicit test targets
    ALLOWLIST_TARGETS = {"127.0.0.1", "localhost"}
