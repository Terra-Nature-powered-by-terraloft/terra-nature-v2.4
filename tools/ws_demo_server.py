#!/usr/bin/env python3
import http.server
import socketserver
import pathlib

PUBLIC_DIR = pathlib.Path(__file__).resolve().parent.parent / 'public'

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

if __name__ == '__main__':
    port = 8000
    with socketserver.TCPServer(('', port), Handler) as httpd:
        print(f'Serving {PUBLIC_DIR} at http://localhost:{port}')
        httpd.serve_forever()
