"""Web UI for calculator.py — run this, then open http://localhost:8000."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from calculator import evaluate

# Hosting services (Render, Railway, etc.) set PORT and need the server to
# listen on all interfaces; locally it stays private to this machine.
PORT = int(os.environ.get("PORT", 8000))
HOST = os.environ.get("HOST", "0.0.0.0" if "PORT" in os.environ else "127.0.0.1")
MAX_EXPRESSION_LENGTH = 200

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Calculator</title>
<style>
  :root { --bg:#f2f2f5; --card:#fff; --key:#e9e9ee; --op:#ff9f0a; --fn:#d4d4dc; --text:#1c1c1e; --muted:#8e8e93; --err:#d70015; }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#000; --card:#1c1c1e; --key:#333; --fn:#505055; --text:#f2f2f7; --muted:#8e8e93; --err:#ff453a; }
  }
  * { box-sizing:border-box; }
  body { margin:0; min-height:100vh; display:grid; place-items:center; background:var(--bg);
         font-family:-apple-system,system-ui,sans-serif; color:var(--text); padding:16px; }
  .calc { width:100%; max-width:360px; background:var(--card); border-radius:24px; padding:20px;
          box-shadow:0 10px 30px rgba(0,0,0,.12); }
  .display { text-align:right; padding:8px 4px 16px; min-height:110px; display:flex; flex-direction:column; justify-content:flex-end; }
  #expr { width:100%; border:none; background:transparent; color:var(--muted); font-size:20px; text-align:right; outline:none; }
  #result { font-size:44px; font-weight:300; overflow-x:auto; white-space:nowrap; min-height:54px; }
  #result.error { color:var(--err); font-size:22px; }
  .keys { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; }
  button { border:none; border-radius:16px; padding:16px 0; font-size:20px; background:var(--key); color:var(--text); cursor:pointer; }
  button:active { filter:brightness(.85); }
  button.fn { background:var(--fn); font-size:16px; }
  button.op { background:var(--op); color:#fff; }
  .history { margin-top:16px; font-size:14px; color:var(--muted); max-height:120px; overflow-y:auto; }
  .history div { padding:2px 0; cursor:pointer; text-align:right; }
</style>
</head>
<body>
<div class="calc">
  <div class="display">
    <input id="expr" placeholder="0" autocomplete="off" autofocus>
    <div id="result">0</div>
  </div>
  <div class="keys">
    <button class="fn" data-k="sqrt(">√</button>
    <button class="fn" data-k="**">xʸ</button>
    <button class="fn" data-k="pi">π</button>
    <button class="fn" data-k="ans">ans</button>
    <button class="fn" data-k="sin(">sin</button>
    <button class="fn" data-k="cos(">cos</button>
    <button class="fn" data-k="tan(">tan</button>
    <button class="fn" data-k="log(">log</button>
    <button class="fn" data-a="clear">C</button>
    <button class="fn" data-k="(">(</button>
    <button class="fn" data-k=")">)</button>
    <button class="op" data-k="/">÷</button>
    <button data-k="7">7</button><button data-k="8">8</button><button data-k="9">9</button>
    <button class="op" data-k="*">×</button>
    <button data-k="4">4</button><button data-k="5">5</button><button data-k="6">6</button>
    <button class="op" data-k="-">−</button>
    <button data-k="1">1</button><button data-k="2">2</button><button data-k="3">3</button>
    <button class="op" data-k="+">+</button>
    <button data-k="0">0</button><button data-k=".">.</button>
    <button class="fn" data-a="back">⌫</button>
    <button class="op" data-a="eq">=</button>
  </div>
  <div class="history" id="history"></div>
</div>
<script>
  const expr = document.getElementById('expr');
  const result = document.getElementById('result');
  const history = document.getElementById('history');
  let ans = 0;

  async function calculate() {
    const e = expr.value.trim();
    if (!e) return;
    const res = await fetch('/api/calc', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({expression: e, ans})
    });
    const data = await res.json();
    if (data.error) {
      result.textContent = data.error;
      result.className = 'error';
    } else {
      ans = data.result;
      result.textContent = data.result;
      result.className = '';
      const row = document.createElement('div');
      row.textContent = e + ' = ' + data.result;
      row.onclick = () => { expr.value = e; expr.focus(); };
      history.prepend(row);
      expr.value = '';
    }
  }

  document.querySelectorAll('.keys button').forEach(b => b.addEventListener('click', () => {
    const a = b.dataset.a;
    if (a === 'eq') calculate();
    else if (a === 'clear') { expr.value = ''; result.textContent = '0'; result.className = ''; }
    else if (a === 'back') expr.value = expr.value.slice(0, -1);
    else expr.value += b.dataset.k;
    expr.focus();
  }));

  expr.addEventListener('keydown', ev => {
    if (ev.key === 'Enter') { ev.preventDefault(); calculate(); }
    if (ev.key === 'Escape') { expr.value = ''; }
  });
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body, content_type):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE, "text/html; charset=utf-8")
        else:
            self._send(404, "Not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/calc":
            self._send(404, "Not found", "text/plain")
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length > 1000:
                raise ValueError("request too large")
            payload = json.loads(self.rfile.read(length) or b"{}")
            expression = str(payload.get("expression", ""))
            if len(expression) > MAX_EXPRESSION_LENGTH:
                raise ValueError(f"expression too long (max {MAX_EXPRESSION_LENGTH} characters)")
            ans = payload.get("ans", 0)
            if not isinstance(ans, (int, float)) or isinstance(ans, bool):
                ans = 0
            value = evaluate(expression, {"ans": ans})
            body = {"result": value}
        except ZeroDivisionError:
            body = {"error": "Error: division by zero"}
        except (SyntaxError, ValueError, TypeError, OverflowError) as exc:
            body = {"error": f"Error: {exc}"}
        self._send(200, json.dumps(body), "application/json")


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Calculator UI running at http://localhost:{PORT}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
