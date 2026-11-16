"""Serve one folder to YouTube Studio only, so Studio's page can fetch a master over 10 MB.

Usage:  python3 -I serve_for_studio.py <folder> [port=8791]
Then, on https://studio.youtube.com/.../videos/upload?d=ud, run in the page (javascript_tool):

  window.__up = 'fetching'; (async () => { try {
    const r = await fetch('http://127.0.0.1:8791/<file>.mp4'); const b = await r.blob();
    const f = new File([b], '<file>.mp4', { type: 'video/mp4' });
    const input = document.querySelector('input[type=file]');
    const dt = new DataTransfer(); dt.items.add(f); input.files = dt.files;
    input.dispatchEvent(new Event('change', { bubbles: true }));
    window.__up = 'injected ' + (b.size / 1e6).toFixed(1) + ' MB';
  } catch (e) { window.__up = 'error: ' + e.message; } })(); 'started'

and poll `window.__up`. The first fetch from localhost makes Chrome ask the owner to allow
local network access for studio.youtube.com; only the owner can grant it.
"""
import http.server, sys

ROOT = sys.argv[1]
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8791


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "https://studio.youtube.com")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def log_message(self, *a):
        pass


http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
