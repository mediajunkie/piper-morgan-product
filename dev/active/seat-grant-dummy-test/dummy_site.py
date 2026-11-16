#!/usr/bin/env python3
"""A throwaway local page for the seat-grant dummy test (CIO, 2026-11-15).

Serves http://127.0.0.1:8791/whoami. It answers "signed in as seat-dummy" when the request
carries the cookie ``dummy_session`` (any value), else "signed out". It never prints or
echoes the cookie's value. It stands in for a signed-in page; nothing real is involved.
"""

import http.server
import sys

PORT = 8791


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 (http.server's name)
        cookies = self.headers.get("Cookie", "")
        names = {c.split("=", 1)[0].strip() for c in cookies.split(";") if c.strip()}
        body = "signed in as seat-dummy" if "dummy_session" in names else "signed out"
        data = f"<html><body><p id='who'>{body}</p></body></html>".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):  # keep the request line, and so any header, out of the log
        return


if __name__ == "__main__":
    http.server.HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    sys.exit(0)
