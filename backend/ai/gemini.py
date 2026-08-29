from google import genai
from backend.config import GEMINI_API_KEY


def generate_with_gemini(prompt):

    if not GEMINI_API_KEY:
        print("⚠️ Gemini API key is missing.")
        return None

    try:
        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response and response.text:
            print("✅ Gemini response generated successfully.")
            return response.text

        print("⚠️ Gemini returned an empty response.")
        return None

    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return None