import os
from dotenv import load_dotenv
from github import Github, Auth
from ai_reviewer import analyze_code_diff

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def run_agent():
    auth = Auth.Token(GITHUB_TOKEN)
    g = Github(auth=auth)

    repo_name = "danieltpavlov/test-pr-repo"
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(1)

    print(f"📥 Извличане на промените за PR #{pr.number}: {pr.title}...")

    diff_content = ""
    for file in pr.get_files():
        diff_content += f"\n--- Файл: {file.filename} ---\n"
        diff_content += file.patch if file.patch else "Няма текстови промени."

    if not diff_content.strip():
        print("Няма открити промени за анализ.")
        return

    # 1. Изпращаме кода за анализ към Gemini
    review_result = analyze_code_diff(pr.title, diff_content)

    print("\n================= РЕЗУЛТАТ ОТ AI АНАЛИЗА =================")
    print(review_result)
    print("==========================================================")

    # 2. Добавяме ясен брандинг от агента в началото на коментара
    comment_body = (
        "🤖 **AI Code Review Agent Report**\n\n"
        f"{review_result}\n\n"
        "---\n*Генерирано автоматично от моето локално AI Agent приложение.*"
    )

    # 3. Публикуваме коментара директно в GitHub PR-а
    print("\n🚀 Публикуване на коментара в GitHub...")
    try:
        comment = pr.create_issue_comment(comment_body)
        print(f"✅ Коментарът е публикуван успешно! Линк: {comment.html_url}")
    except Exception as e:
        print(f"❌ Грешка при публикуване на коментара: {e}")

if __name__ == "__main__":
    run_agent()