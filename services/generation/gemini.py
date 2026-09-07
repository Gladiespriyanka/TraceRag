import asyncio

from google import genai

from packages.core.config import settings


class GeminiProvider:
    def __init__(self):
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    async def generate(self, prompt: str) -> str:

        def generate_sync():
            response = self.client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
            )

            return response.text or ""

        return await asyncio.to_thread(generate_sync)