import argparse
import os
from dotenv import load_dotenv
from github import Github, Auth
from ai_reviewer import analyze_code_diff

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def build_markdown_comment(report) -> str:
    """Генерира красив Markdown формат от Pydantic отчета."""
    sec_items = "\n".join([f"- ⚠️ {risk}" for risk in
                           report.security_risks]) if report.security_risks else "- ✅ Няма открити рискове за сигурността."
    rec_items = "\n".join([f"- 💡 {rec}" for rec in
                           report.recommendations]) if report.recommendations else "- ✅ Няма забележки към качеството на кода."

    return f"""🤖 ### **AI Pull Request Reviewer Report**

#### 📋 **Резюме**
{report.summary}

---

#### 🔒 **Сигурност и рискове**
{sec_items}

---

#### 💡 **Препоръки**
{rec_items}

---
*Генерирано автономно от [AI PR Reviewer Agent](https://github.com/danieltpavlov/ai-pr-reviewer-agent).*
"""


def run_agent(repo_name: str, pr_number: int):
    if not GITHUB_TOKEN:
        print("❌ Грешка: Липсва GITHUB_TOKEN в .env файла!")
        return

    auth = Auth.Token(GITHUB_TOKEN)
    g = Github(auth=auth)

    print(f"📥 Свързване с {repo_name} и извличане на PR #{pr_number}...")
    try:
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
    except Exception as e:
        print(f"❌ Грешка при достъп до GitHub: {e}")
        return

    diff_content = ""
    for file in pr.get_files():
        # Пропускаме големи или автоматично генерирани файлове
        if file.filename.endswith((".lock", "-lock.json", ".png", ".jpg", ".svg")):
            continue
        diff_content += f"\n--- Файл: {file.filename} ---\n"
        diff_content += file.patch if file.patch else "Няма текстови промени."

    if not diff_content.strip():
        print("ℹ️ Няма файлове за преглед.")
        return

    # Изпълняваме AI анализа
    report = analyze_code_diff(pr.title, diff_content)

    # Оформяме коментара
    comment_body = build_markdown_comment(report)

    # Публикуваме в GitHub
    print("\n🚀 Публикуване на структурирания коментар в GitHub...")
    try:
        comment = pr.create_issue_comment(comment_body)
        print(f"✅ Успешно публикувано: {comment.html_url}")
    except Exception as e:
        print(f"❌ Грешка при публикуване: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Автономен AI PR Reviewer Agent.")
    parser.add_argument("--repo", type=str, default="danieltpavlov/test-pr-repo",
                        help="Име на репозиторито (напр. user/repo)")
    parser.add_argument("--pr", type=int, default=1, help="Номер на Pull Request-а")

    args = parser.parse_args()
    run_agent(args.repo, args.pr)