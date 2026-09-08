import os
from dotenv import load_dotenv
from google import genai

# Зареждаме GEMINI_API_KEY от .env файла
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ Грешка: GEMINI_API_KEY липсва в .env файла!")

# Инициализираме новия клиент на Google GenAI
client = genai.Client(api_key=api_key)


def analyze_code_diff(pr_title: str, diff_text: str) -> str:
    """
    Приема заглавие на PR и извлечения Diff код,
    след което връща структуриран преглед от Gemini.
    """
    prompt = f"""
Ти си опитен старши софтуерен инженер и специалист по сигурност.
Твоята задача е да направиш бърз и стегнат Code Review на промените в следния Pull Request.

Заглавие на PR: {pr_title}

Промени в кода (Diff):
\"\"\"
{diff_text}
\"\"\"

Моля, форматирай отговора си в Markdown със следните три ясни секции:
1. 📋 **Резюме на промените**: Обясни накратко какво прави този код.
2. 🔒 **Сигурност и потенциални рискове**: Провери за хардкоднати тайни, API ключове, пароли или логически пропуски.
3. 💡 **Препоръки за подобрение**: Дай съвет за чист код, тестове или документация (ако е приложимо).

Бъди конструктивен, точен и пиши на български език.
"""

    print("🤖 AI агентът анализира кода през Gemini...")

    # Използваме бързия и икономичен модел gemini-3.6-flash
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text