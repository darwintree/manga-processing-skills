import http.server
import socketserver
import json
import argparse
import os
import urllib.parse
import webbrowser
import threading
import sys

# Argument parsing
parser = argparse.ArgumentParser(description='Segment Page Tool')
parser.add_argument('--image', required=True, help='Path to the image file')
parser.add_argument('--chapter', required=True, help='Chapter number')
parser.add_argument('--page', required=True, help='Page number')
args = parser.parse_args()

# Configuration
PORT = 8000
DIRECTORY = os.getcwd()
OUTPUT_DIR = os.path.join(DIRECTORY, 'processed', 'segment')
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f'chapter{args.chapter}_{args.page}.json')

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/':
            self.path = '.agent/skills/segment-page/index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif parsed_path.path == '/image':
            # Serve the requested image
            image_path = os.path.abspath(os.path.join(DIRECTORY, args.image))
            if os.path.exists(image_path) and image_path.startswith(DIRECTORY):
                 # basic security check to ensure we serve files inside the project
                self.path = args.image
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.send_error(404, "Image not found")
                return
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                
                # Save to file
                with open(OUTPUT_FILE, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print(f"Saved segmentation to {OUTPUT_FILE}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok', 'file': OUTPUT_FILE}).encode())
                
                # Shutdown server after saving
                threading.Thread(target=self.server.shutdown).start()
                
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404)

def open_browser():
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == '__main__':
    # Ensure image exists
    full_image_path = os.path.join(DIRECTORY, args.image)
    if not os.path.exists(full_image_path):
        print(f"Error: Image not found at {full_image_path}")
        sys.exit(1)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        print(f"Target Image: {args.image}")
        print(f"Output File: {OUTPUT_FILE}")
        
        # Open browser in a separate thread to not block server start
        threading.Timer(1.0, open_browser).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        print("Server stopped.")
