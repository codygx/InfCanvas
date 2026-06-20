from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from datetime import datetime
from urllib.parse import unquote

DEFAULT_SAVE_PATH = os.path.dirname(os.path.abspath(__file__))
SAVE_PATH = os.path.abspath(os.path.expanduser(os.environ.get("LAYOUT_DIR", DEFAULT_SAVE_PATH)))

class Handler(BaseHTTPRequestHandler):

    def send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def get_safe_filename(self):
        filename = unquote(self.path.lstrip("/"))
        if not filename:
            return None
        if os.path.basename(filename) != filename:
            return None
        if not filename.endswith(".json"):
            return None
        return filename

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors()
        self.end_headers()

    def do_GET(self):
        os.makedirs(SAVE_PATH, exist_ok=True)

        # Root path → return list of files
        if self.path == "/" or self.path == "":
            files = [f for f in os.listdir(SAVE_PATH) if f.endswith(".json")]
            files.sort(reverse=True)

            self.send_response(200)
            self.send_cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(files).encode("utf-8"))
            return

        # File path → return the JSON file
        filename = self.get_safe_filename()
        if not filename:
            self.send_response(400)
            self.send_cors()
            self.end_headers()
            self.wfile.write(b"Invalid filename")
            return

        file_path = os.path.join(SAVE_PATH, filename)

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                data = f.read()

            self.send_response(200)
            self.send_cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.send_cors()
            self.end_headers()
            self.wfile.write(b"File not found")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length)
        layout = json.loads(data.decode("utf-8"))

        os.makedirs(SAVE_PATH, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(SAVE_PATH, f"layout_{timestamp}.json")

        with open(file_path, "w") as f:
            json.dump(layout, f, indent=2)

        self.send_response(200)
        self.send_cors()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "OK", "file": os.path.basename(file_path)}).encode("utf-8"))

    def do_DELETE(self):
        os.makedirs(SAVE_PATH, exist_ok=True)

        filename = self.get_safe_filename()
        if not filename:
            self.send_response(400)
            self.send_cors()
            self.end_headers()
            self.wfile.write(b"Invalid filename")
            return

        file_path = os.path.join(SAVE_PATH, filename)
        if not os.path.exists(file_path):
            self.send_response(404)
            self.send_cors()
            self.end_headers()
            self.wfile.write(b"File not found")
            return

        os.remove(file_path)
        self.send_response(200)
        self.send_cors()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "deleted", "file": filename}).encode("utf-8"))

server = HTTPServer(("localhost", 9000), Handler)
print("Save server running on http://localhost:9000")
print(f"Layout folder: {SAVE_PATH}")
server.serve_forever()
