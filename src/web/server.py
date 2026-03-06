from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json

from src.core.pipeline import AnalysisPipeline
from src.detectors.command_abuse import CommandAbuseDetector
from src.detectors.exfiltration import ExfiltrationDetector
from src.detectors.prompt_injection import PromptInjectionDetector


def build_pipeline() -> AnalysisPipeline:
    return AnalysisPipeline([
        PromptInjectionDetector(weight=0.9),
        ExfiltrationDetector(weight=1.0),
        CommandAbuseDetector(weight=0.9),
    ])


class RiskHandler(BaseHTTPRequestHandler):
    pipeline = build_pipeline()

    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        if self.path in {"/", "/health"}:
            self._json(200, {"ok": True, "service": "agent-security-lab-web", "version": "v1.1.0"})
            return
        self._json(404, {"ok": False, "error": "not_found"})

    def do_POST(self):  # noqa: N802
        if self.path != "/analyze":
            self._json(404, {"ok": False, "error": "not_found"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length > 0 else b"{}"

        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            self._json(400, {"ok": False, "error": "invalid_json"})
            return

        text = str(payload.get("text", ""))
        tool = str(payload.get("tool", "read"))
        action = str(payload.get("action", "analyze"))
        if not text.strip():
            self._json(400, {"ok": False, "error": "text_required"})
            return

        result = self.pipeline.analyze_text(text, tool=tool, action=action)
        self._json(200, {"ok": True, "result": self.pipeline.to_dict(result)})


def run_server(host: str = "127.0.0.1", port: int = 8787) -> None:
    server = ThreadingHTTPServer((host, port), RiskHandler)
    print(f"[agent-security-lab] web server listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
