from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .django_embed import build_embed_context, render_embed_block


def _page_html() -> str:
    context = build_embed_context()
    block = render_embed_block(context)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Halley Tracker Preview</title>
  <style>
    :root {{
      color-scheme: light dark;
      --bg: #0b1020;
      --panel: #161d34;
      --text: #e9eefc;
      --muted: #9aa7c4;
      --accent: #6dcff6;
      --ring: #2a3456;
    }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background: radial-gradient(circle at top right, #1a2448 0, var(--bg) 50%);
      color: var(--text);
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 24px;
    }}
    .preview {{
      width: min(760px, 100%);
      border: 1px solid var(--ring);
      background: color-mix(in oklab, var(--panel) 88%, black 12%);
      border-radius: 16px;
      padding: 20px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.35);
    }}
    .title {{
      margin: 0 0 12px;
      font-size: 14px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--muted);
    }}
    .halley-tracker {{
      border: 1px solid var(--ring);
      border-radius: 12px;
      padding: 16px;
      background: rgba(255, 255, 255, 0.03);
    }}
    .halley-tracker h3 {{
      margin: 0 0 10px;
      color: var(--accent);
      font-size: 22px;
    }}
    .halley-tracker p {{
      margin: 6px 0;
      font-size: 16px;
      line-height: 1.4;
    }}
    .halley-updated {{
      color: var(--muted);
      font-size: 14px;
    }}
  </style>
</head>
<body>
  <main class="preview">
    <p class="title">Halley Tracker Standalone Preview</p>
    {block}
  </main>

  <script>
    function formatCountdown(totalSeconds) {{
      let remaining = Math.max(0, totalSeconds);
      const years = Math.floor(remaining / (365 * 24 * 60 * 60));
      remaining %= (365 * 24 * 60 * 60);
      const months = Math.floor(remaining / (30 * 24 * 60 * 60));
      remaining %= (30 * 24 * 60 * 60);
      const days = Math.floor(remaining / (24 * 60 * 60));
      remaining %= (24 * 60 * 60);
      const hours = Math.floor(remaining / (60 * 60));
      remaining %= (60 * 60);
      const minutes = Math.floor(remaining / 60);
      const seconds = remaining % 60;
      
      return `${{years}} Years ${{months}} Months ${{days}} Days ${{hours}} Hours ${{minutes}} Minutes ${{seconds}} Seconds`;
    }}

    const tracker = document.querySelector('.halley-tracker');
    if (tracker) {{
      let countdownSeconds = parseInt(tracker.getAttribute('data-countdown-seconds'), 10);
      const countdownText = document.getElementById('halley-countdown-text');
      
      if (countdownText) {{
        setInterval(() => {{
          countdownSeconds--;
          countdownText.textContent = formatCountdown(countdownSeconds);
        }}, 1000);
      }}
    }}
  </script>
</body>
</html>"""


class PreviewHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 (BaseHTTPRequestHandler API)
        if self.path not in ("/", "/index.html"):
            self.send_response(404)
            self.end_headers()
            return
        payload = _page_html().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


def run_standalone_server(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = ThreadingHTTPServer((host, port), PreviewHandler)
    print(f"Halley Tracker preview running at http://{host}:{port}")
    server.serve_forever()
