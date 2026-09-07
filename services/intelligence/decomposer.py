import asyncio
import json
import re

from google import genai

from packages.core.config import settings


class QueryDecomposer:

    def _is_simple_query(self, query: str) -> bool:
        """
        Simple factual/document-specific questions don't need
        LLM-based query decomposition.
        """

        q = query.strip().lower()

        # If a specific document is mentioned, keep the original query.
        if re.search(r"\b[\w-]+\.pdf\b", q):
            return True

        # Short questions are generally simple enough to search directly.
        if len(q.split()) <= 12:
            return True

        return False

    async def decompose(self, query: str) -> list[str]:

        if not settings.gemini_api_key:
            return [query]

        # Avoid an unnecessary Gemini call for simple queries.
        if self._is_simple_query(query):
            print("Simple query detected — skipping Gemini decomposition.")
            return [query]

        def generate():
            client = genai.Client(
                api_key=settings.gemini_api_key
            )

            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=(
                    "Break the following question into independent searchable "
                    "subquestions. Return ONLY a JSON array of strings.\n\n"
                    f"Question: {query}"
                ),
            )

            return response.text or ""

        try:
            raw = await asyncio.to_thread(generate)

            # Remove accidental markdown fences.
            raw = raw.strip()

            if raw.startswith("```"):
                raw = re.sub(r"^```(?:json)?\s*", "", raw)
                raw = re.sub(r"\s*```$", "", raw)

            parsed = json.loads(raw)

            if isinstance(parsed, list):
                questions = [
                    str(item).strip()
                    for item in parsed
                    if str(item).strip()
                ]

                return questions or [query]

        except Exception as exc:
            print(f"Query decomposition failed: {exc}")
            return [query]

        return [query]