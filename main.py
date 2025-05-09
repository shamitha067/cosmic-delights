import webview
import threading
from app import app  # Your Flask app

def run_flask():
    app.run(port=5000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    webview.create_window("ASL Translator", "http://localhost:5000")

