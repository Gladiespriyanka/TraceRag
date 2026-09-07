from google import genai
from packages.core.config import settings
async def generate_hypothetical(query):
    if not settings.gemini_api_key:return query
    r=await genai.Client(api_key=settings.gemini_api_key).aio.models.generate_content(model=settings.gemini_model,contents=f"Write a short hypothetical passage relevant to this question. Return only the passage. Question: {query}")
    return r.text or query
