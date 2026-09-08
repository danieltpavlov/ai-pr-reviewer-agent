import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ Грешка: GEMINI_API_KEY липсва в .env файла!")

client = genai.Client(api_key=api_key)


# Дефинираме строгата схема на изхода
class ReviewReport(BaseModel):
    summary: str = Field(description="Кратко резюме на направените промени в кода.")
    security_risks: list[str] = Field(
        description="Списък с потенциални уязвимости, изтекли тайни или съображения за сигурност.")
    recommendations: list[str] = Field(
        description="Списък с препоръки за подобрение на кода, форматирането или архитектурата.")


def analyze_code_diff(pr_title: str, diff_text: str) -> ReviewReport:
    """
    Анализира Diff код и връща типизиран обект ReviewReport.
    """
    prompt = f"""
Ти си старши софтуерен инженер и експерт по киберсигурност.
Направи детайлен Code Review на следния Pull Request.

Заглавие на PR: {pr_title}

Промени в кода (Diff):
\"\"\"
{diff_text}
\"\"\"

Анализирай промените внимателно и попълни съответните полета на български език.
"""

    print("🤖 AI агентът анализира кода през Gemini (Structured Output)...")

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ReviewReport,
            "temperature": 0.1,  # Ниска температура за максимална точност и обективност
        }
    )

    # Парсваме резултата директно в нашия Pydantic модел
    parsed_report = ReviewReport.model_validate_json(response.text)
    return parsed_report