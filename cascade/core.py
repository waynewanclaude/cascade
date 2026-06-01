import os
import sys
import json
import socket
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Multi-threaded server to handle simultaneous dynamic dynamic visual audit queries lag-free."""
    pass

class Cascade:
    # Class-level variable to store active application configuration during dynamic loading
    active_instance = None

    def __init__(self, title="Cascade Dashboard", orientation="horizontal", persistence_path="browser"):
        self.title = title
        self.orientation = orientation
        self.persistence_path = "browser"  # Enforce browser profile localStorage
        self.root_callback = None
        self.callbacks = {}  # Maps callback_name -> function
        Cascade.active_instance = self

    def root_panel(self):
        """Decorator registering the level 0 starting visual widget callback."""
        def decorator(func):
            self.root_callback = func
            return func
        return decorator

    def panel(self, name):
        """Decorator registering dynamic callbacks for deeper visual columns cascade."""
        def decorator(func):
            self.callbacks[name] = func
            return func
        return decorator

    def run(self, working_dir=""):
        # Detect first open local port starting from 8000
        port = 8000
        while True:
            try:
                tester = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tester.bind(("127.0.0.1", port))
                tester.close()
                break
            except OSError:
                port += 1

        server_address = ("127.0.0.1", port)
        app_ref = self

        class CascadeRequestHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                # Silence standard terminal logs for cleaner developer experience
                pass

            def set_cache_control_headers(self):
                # Enforce aggressive cache suppression: prevent stale browser data
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")

            def do_GET(self):
                if self.path == "/":
                    # Serve packaged Visual Shell index.html
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.set_cache_control_headers()
                    self.end_headers()
                    
                    package_dir = os.path.dirname(os.path.abspath(__file__))
                    html_path = os.path.join(package_dir, "index.html")
                    
                    try:
                        with open(html_path, "r", encoding="utf-8") as f:
                            html_content = f.read()
                        self.wfile.write(html_content.encode("utf-8"))
                    except Exception as e:
                        err_msg = f"Error loading visual workspace: {e}"
                        self.wfile.write(err_msg.encode("utf-8"))
                        
                elif self.path == "/api/layout":
                    # Expose dashboard baselines
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.set_cache_control_headers()
                    self.end_headers()
                    
                    layout_payload = {
                        "title": app_ref.title,
                        "orientation": app_ref.orientation,
                        "persistence_mode": "browser"
                    }
                    self.wfile.write(json.dumps(layout_payload).encode("utf-8"))
                    
                elif self.path == "/api/root":
                    # Serve starting Level 0 panel
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.set_cache_control_headers()
                    self.end_headers()
                    
                    if app_ref.root_callback is None:
                        err_res = {"error": "No root panel registered. Use @app.root_panel()"}
                        self.wfile.write(json.dumps(err_res).encode("utf-8"))
                        return
                        
                    try:
                        widget = app_ref.root_callback()
                        res = {
                            "widget_type": widget.type_name,
                            "widget_data": widget.serialize()
                        }
                        self.wfile.write(json.dumps(res).encode("utf-8"))
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
                else:
                    self.send_response(404)
                    self.end_headers()

            def do_POST(self):
                if self.path == "/api/callback":
                    # Parse Dynamic Auditing Cascade Dispatcher parameters
                    content_length = int(self.headers["Content-Length"])
                    post_data = self.rfile.read(content_length)
                    payload = json.loads(post_data.decode("utf-8"))
                    
                    callback_name = payload.get("callback")
                    clicked_row = payload.get("row") # Row dictionaries or Candle properties
                    
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.set_cache_control_headers()
                    self.end_headers()
                    
                    if callback_name not in app_ref.callbacks:
                        err_res = {"error": f"Callback '{callback_name}' is not registered."}
                        self.wfile.write(json.dumps(err_res).encode("utf-8"))
                        return
                        
                    try:
                        handler = app_ref.callbacks[callback_name]
                        widget = handler(clicked_row)
                        res = {
                            "widget_type": widget.type_name,
                            "widget_data": widget.serialize()
                        }
                        self.wfile.write(json.dumps(res).encode("utf-8"))
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
                else:
                    self.send_response(404)
                    self.end_headers()

        print(f"Starting Cascade Local Audit Engine on loopback port {port}...")
        print(f"Open your workspace via: http://127.0.0.1:{port}")
        
        httpd = ThreadedHTTPServer(server_address, CascadeRequestHandler)
        
        # Open user browser dynamically in a non-blocking background thread
        def open_workspace():
            webbrowser.open(f"http://127.0.0.1:{port}")
            
        threading.Timer(0.5, open_workspace).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down Cascade server gracefully.")
            httpd.shutdown()
            sys.exit(0)
