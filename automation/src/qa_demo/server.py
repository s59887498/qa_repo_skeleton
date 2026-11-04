"""Small local test target; not a production application or authentication system."""

from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
from urllib.parse import urlsplit
from uuid import uuid4


class DemoServer(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 64

    def __init__(self):
        super().__init__(("127.0.0.1", 0), Handler)
        self.items = {}
        self.lock = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass  # No request headers, credentials, or payloads in logs.

    def respond(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/health":
            return self.respond(200, {"status": "ok"})
        if path == "/ui":
            data = Path(__file__).with_name("demo.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            return self.wfile.write(data)
        if path.startswith("/items/"):
            with self.server.lock:
                item = self.server.items.get(path.removeprefix("/items/"))
            return self.respond(200, item) if item else self.respond(404, {"error": "not_found"})
        self.respond(404, {"error": "not_found"})

    def do_POST(self):
        if urlsplit(self.path).path != "/items":
            return self.respond(404, {"error": "not_found"})
        # A synthetic role switch for teaching RBAC assertions, not authentication.
        if self.headers.get("X-Demo-Role") != "editor":
            return self.respond(403, {"error": "forbidden"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 4096:
                raise ValueError("invalid_length")
            data = json.loads(self.rfile.read(length))
        except (ValueError, UnicodeDecodeError):
            return self.respond(400, {"error": "invalid_json"})
        name = data.get("name") if isinstance(data, dict) else None
        if not isinstance(name, str) or not 1 <= len(name.strip()) <= 20:
            return self.respond(422, {"error": "invalid_name"})
        item = {"id": str(uuid4()), "name": name.strip()}
        with self.server.lock:
            self.server.items[item["id"]] = item
        self.respond(201, item)

    def do_DELETE(self):
        path = urlsplit(self.path).path
        if not path.startswith("/items/"):
            return self.respond(404, {"error": "not_found"})
        if self.headers.get("X-Demo-Role") != "editor":
            return self.respond(403, {"error": "forbidden"})
        with self.server.lock:
            item = self.server.items.pop(path.removeprefix("/items/"), None)
        self.respond(200 if item else 404, {"deleted": bool(item)})


@contextmanager
def demo_server():
    server = DemoServer()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
