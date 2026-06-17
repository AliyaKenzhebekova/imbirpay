#!/usr/bin/env python3
"""ImbirPay Sync API — общая база данных для всей команды"""

import json, os, threading, sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imbirpay_sync.json')
lock = threading.Lock()

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, encoding='utf-8') as f:
                return json.load(f)
        except: pass
    return {'requests': []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class Handler(BaseHTTPRequestHandler):
    def cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self.cors_headers()
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/requests':
            with lock:
                data = load_data()
            body = json.dumps(data.get('requests', []), ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.cors_headers()
            self.end_headers()
            self.wfile.write(body)
        elif path == '/ping':
            self.send_response(200)
            self.cors_headers()
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/requests':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                requests = json.loads(body.decode('utf-8'))
                with lock:
                    data = load_data()
                    data['requests'] = requests
                    save_data(data)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.cors_headers()
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):
        pass  # тихий режим

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f'ImbirPay API запущен на порту {port}', flush=True)
    server.serve_forever()
