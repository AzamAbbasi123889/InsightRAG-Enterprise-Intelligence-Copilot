from __future__ import annotations
import json
from app.config import settings

class LLMService:
    def __init__(self):
        self.enabled = bool(settings.llm_api_key)

    def generate(self, question: str, evidence: list[dict], sql_rows: list[dict] | None = None) -> str:
        if not self.enabled:
            return self._fallback(question, evidence, sql_rows or [])
        try:
            import httpx
            prompt = self._prompt(question, evidence, sql_rows or [])
            response = httpx.post(
                f"{settings.llm_base_url.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {settings.llm_api_key}"},
                json={"model": settings.llm_model, "messages": [
                    {"role":"system","content":"You are an enterprise analyst. Use only supplied evidence. Cite source IDs like [doc-1]. If evidence is insufficient, say so."},
                    {"role":"user","content":prompt}
                ], "temperature":0.1}, timeout=45)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception:
            return self._fallback(question, evidence, sql_rows or [])

    def _prompt(self, question, evidence, sql_rows):
        return json.dumps({"question": question, "documents": evidence, "sql": sql_rows}, indent=2)

    def _fallback(self, question, evidence, sql_rows):
        parts = [f"Question: {question}", ""]
        if sql_rows:
            parts.append("Structured-data result:")
            for row in sql_rows[:8]:
                parts.append("- " + ", ".join(f"{k}={v}" for k,v in row.items()))
        if evidence:
            parts.append("\nDocument evidence:")
            for item in evidence[:4]:
                parts.append(f"- [{item['id']}] {item['snippet']}")
        parts.append("\nThis answer is generated in demo fallback mode. Configure LLM_API_KEY for model-generated synthesis.")
        return "\n".join(parts)
