"""Gemini API client for generating certification prep content."""

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


def get_client():
    """Configure and return Gemini client instance."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY가 .env 파일에 설정되지 않았습니다.")
    return genai.Client(api_key=api_key)


def generate_content(client, prompt: str) -> str:
    """Send a prompt to Gemini and return the text response."""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text
