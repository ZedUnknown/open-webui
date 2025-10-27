export CORS_ALLOW_ORIGIN="http://localhost:5173;http://localhost:8080"
PORT="${PORT:-8080}"
uvicorn open_webui.main:app --port $PORT --host 0.0.0.0 --forwarded-allow-ips '*' --reload

# [same command]:
# python -m uvicorn open_webui.main:app --host 0.0.0.0 --port 8080 --reload