import json
import re

from services.generation.gemini import GeminiProvider
from services.generation.prompts import build_grounded_prompt


class AnswerGenerator:
    def __init__(self):
        self.llm = GeminiProvider()

    def _parse_json(self, raw: str) -> dict:
        """
        Parse Gemini JSON output robustly.

        Gemini may return:
        1. Pure JSON
        2. JSON wrapped in ```json ... ```
        3. JSON with surrounding whitespace/text
        """

        raw = (raw or "").strip()

        # Case 1: Markdown JSON code fence
        fenced = re.search(
            r"```(?:json)?\s*(.*?)\s*```",
            raw,
            re.DOTALL | re.IGNORECASE,
        )

        if fenced:
            raw = fenced.group(1).strip()

        # Case 2: Find the outermost JSON object if extra text exists
        if not raw.startswith("{"):
            start = raw.find("{")
            end = raw.rfind("}")

            if start != -1 and end != -1 and end > start:
                raw = raw[start:end + 1]

        return json.loads(raw)

    async def answer(self, query: str, contexts: list[dict]) -> dict:

        if not contexts:
            return {
                "answer": "[INSUFFICIENT_EVIDENCE]",
                "citations": [],
            }

        raw = await self.llm.generate(
            build_grounded_prompt(query, contexts)
        )

        try:
            result = self._parse_json(raw)

            answer = str(result.get("answer", "")).strip()
            citations = result.get("citations", [])

            if not answer:
                answer = "[INSUFFICIENT_EVIDENCE]"

            if not isinstance(citations, list):
                citations = []

            return {
                "answer": answer,
                "citations": citations,
            }

        except Exception as exc:
            print(f"Gemini JSON parsing failed: {exc}")

            # Don't expose raw JSON as the answer.
            return {
                "answer": raw.strip(),
                "citations": [],
            }