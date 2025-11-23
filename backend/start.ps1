$host.UI.RawUI.WindowTitle = "Open WebUI: 8080"
function prompt { "> " }

conda activate AI-3.12.11
python -m uvicorn open_webui.main:app --host 0.0.0.0 --port 8080 --reload
