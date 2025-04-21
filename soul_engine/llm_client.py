# llm_client.py

from abc import ABC, abstractmethod
from google import genai
from .prompts import soul_extraction_prompt
from dotenv import load_dotenv
import os
import json

load_dotenv()

class LLMClient(ABC):
    @abstractmethod
    def extract_identity_traits(self, user_input: str) -> dict:
        """Extract structured identity traits from raw user input."""
        pass


class GeminiClient(LLMClient):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        # Instantiate the new Google GenAI client
        self.client = genai.Client(api_key=api_key)

    def extract_identity_traits(self, user_input: str) -> dict:
        # Build the prompt using the centralized template
        prompt = soul_extraction_prompt(user_input)
        try:
            # Call Gemini's text generation endpoint
            response = self.client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=[prompt]
            )
            # The SDK returns .text on the response
            text = response.text
            if not text:
                raise ValueError("Received empty response from Gemini API.")

            json_text = text.strip()
            # Strip markdown JSON fences if present
            if json_text.startswith("```json"):
                json_text = json_text[7:]
            if json_text.endswith("```"):
                json_text = json_text[:-3]

            return json.loads(json_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse Gemini JSON response: {e}\nRaw response: {text}")
        except Exception as e:
            raise RuntimeError(f"Error calling Gemini API: {e}")
