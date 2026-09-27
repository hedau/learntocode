# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

The project uses only the Python standard library, so there is nothing to install. It has no build step, linter config, or test suite.

- Run the CLI calculator: `python3 calculator.py` (REPL; `quit`/`exit` to leave, `ans` holds the last result)
- Run the web UI: `python3 calculator_web.py`, then open http://localhost:8000
- Quick check of the evaluator: `python3 -c "from calculator import evaluate; print(evaluate('2 + 3 * (4 - 1)'))"`

## Architecture

- `calculator.py` owns all math. `evaluate(expression, variables)` parses input with `ast.parse(mode="eval")` and walks the tree against allowlists: `BINARY_OPS`, `UNARY_OPS`, `FUNCTIONS`, `CONSTANTS`. Any other node type raises `ValueError`. Never replace this with `eval()`. To add an operator, function, or constant, add it to the matching dict.
- `**` goes through `safe_pow`, which caps the exponent at `MAX_EXPONENT` so inputs like `9**9**9` can't hang the process.
- `calculator_web.py` is a stdlib `ThreadingHTTPServer`. The whole frontend (HTML/CSS/JS) is the `PAGE` string constant; there are no static files. `GET /` serves the page. `POST /api/calc` takes `{expression, ans}` and returns `{result}` or `{error}`, always with HTTP 200.
- `ans` lives in the browser, not on the server. The client sends it with each request and the server only accepts it if it is a real int or float. The server is stateless.
- The server rejects request bodies over 1000 bytes and expressions over `MAX_EXPRESSION_LENGTH` (200). It maps `ZeroDivisionError`, `SyntaxError`, `ValueError`, `TypeError` and `OverflowError` to `{error}` messages. The CLI catches most of the same exceptions separately in `main()`.
- Hosting: when a `PORT` env var is set (Render, Railway, etc.), the server binds `0.0.0.0` on that port. Otherwise it binds `127.0.0.1:8000`. `HOST` overrides the bind address.
- When adding a function to `FUNCTIONS`, also add a button in the `.keys` grid of `PAGE` if it should appear in the UI.
