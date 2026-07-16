"""
Marvel Website - Python Backend Server (Fallback)
Run with: python server.py
Serves on: http://localhost:3000
"""
import json
import os
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

# Load data
with open(os.path.join(DATA_DIR, 'heroes.json'), 'r', encoding='utf-8') as f:
    HEROES = json.load(f)
with open(os.path.join(DATA_DIR, 'movies.json'), 'r', encoding='utf-8') as f:
    MOVIES = json.load(f)
with open(os.path.join(DATA_DIR, 'comics.json'), 'r', encoding='utf-8') as f:
    COMICS = json.load(f)

MIME_TYPES = {
    '.html': 'text/html',
    '.css':  'text/css',
    '.js':   'application/javascript',
    '.json': 'application/json',
    '.png':  'image/png',
    '.jpg':  'image/jpeg',
    '.svg':  'image/svg+xml',
    '.ico':  'image/x-icon',
}


class MarvelHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"  {self.address_string()} -> {format % args}")

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(body)

    def serve_file(self, filepath):
        ext = os.path.splitext(filepath)[1]
        mime = MIME_TYPES.get(ext, 'application/octet-stream')
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, 'File not found')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip('/')
        params = parse_qs(parsed.query)

        # ─ API Routes ─────────────────────────────────────────
        if path == '/api/health':
            self.send_json({'status': 'ok', 'message': 'Marvel Python API is running!'})

        elif path == '/api/heroes':
            result = list(HEROES)
            if 'search' in params:
                q = params['search'][0].lower()
                result = [h for h in result if q in h['name'].lower() or q in h['realName'].lower()]
            self.send_json({'success': True, 'count': len(result), 'data': result})

        elif path.startswith('/api/heroes/'):
            hero_id = int(path.split('/')[-1])
            hero = next((h for h in HEROES if h['id'] == hero_id), None)
            if hero:
                self.send_json({'success': True, 'data': hero})
            else:
                self.send_json({'success': False, 'message': 'Hero not found'}, 404)

        elif path == '/api/movies':
            result = list(MOVIES)
            if 'phase' in params:
                phase = int(params['phase'][0])
                result = [m for m in result if m['phase'] == phase]
            self.send_json({'success': True, 'count': len(result), 'data': result})

        elif path.startswith('/api/movies/'):
            movie_id = int(path.split('/')[-1])
            movie = next((m for m in MOVIES if m['id'] == movie_id), None)
            if movie:
                self.send_json({'success': True, 'data': movie})
            else:
                self.send_json({'success': False, 'message': 'Movie not found'}, 404)

        elif path == '/api/comics':
            self.send_json({'success': True, 'count': len(COMICS), 'data': COMICS})

        elif path.startswith('/api/comics/'):
            comic_id = int(path.split('/')[-1])
            comic = next((c for c in COMICS if c['id'] == comic_id), None)
            if comic:
                self.send_json({'success': True, 'data': comic})
            else:
                self.send_json({'success': False, 'message': 'Comic not found'}, 404)

        # ─ Static Frontend Files ───────────────────────────────
        else:
            # Map path to frontend file
            rel = path.lstrip('/')
            if rel == '' or rel == 'index.html':
                filepath = os.path.join(FRONTEND_DIR, 'index.html')
            else:
                filepath = os.path.join(FRONTEND_DIR, rel)
                if not os.path.exists(filepath):
                    # Try as page
                    filepath = os.path.join(FRONTEND_DIR, rel + '.html')
            if os.path.isfile(filepath):
                self.serve_file(filepath)
            else:
                self.serve_file(os.path.join(FRONTEND_DIR, 'index.html'))


if __name__ == '__main__':
    PORT = 3000
    server = HTTPServer(('localhost', PORT), MarvelHandler)
    print(f'\n*** Marvel Website (Python Backend) running! ***')
    print(f'Open: http://localhost:{PORT}')
    print(f'API:  http://localhost:{PORT}/api/heroes')
    print(f'\n   Press Ctrl+C to stop.\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n✋ Server stopped.')
