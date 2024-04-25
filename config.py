import secrets

SECRET_KEY = secrets.token_hex(32)
CSRF_ENABLED = True