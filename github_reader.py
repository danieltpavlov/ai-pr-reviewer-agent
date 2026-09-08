import os
from dotenv import load_dotenv
from github import Github
from github import Auth

# Зареждаме тайните ключове от .env файла
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def fetch_pull_request():
    if not GITHUB_TOKEN:
        print("❌ Грешка: GITHUB_TOKEN не е намерен!")
        return

    # Инициализираме новия начин на автентикация
    auth = Auth.Token(GITHUB_TOKEN)
    g = Github(auth=auth)

    # ⚠️ ЗАБЕЛЕЖКА: Заменете 'repo' с вашето реално GitHub потребителско име,
    # ако името на репозиторито ви е различно.
    repo_name = "repo"

    print(f"Търсене на репозитори: {repo_name}...")

    try:
        repo = g.get_repo(repo_name)
        print(f"✅ Успешно намерен репозитори: {repo.full_name}")

        # Извличаме Pull Request с номер 1
        pr_number = 1
        pr = repo.get_pull(pr_number)

        print(f"\n==========================================")
        print(f"📂 Pull Request #{pr.number}: {pr.title}")
        print(f"👤 Автор: {pr.user.login}")
        print(f"🔗 Линк: {pr.html_url}")
        print(f"==========================================")

        print("\n📝 Променени файлове и съдържание (Diff):")
        # Обхождаме файловете, които са променени в този PR
        files = pr.get_files()
        for file in files:
            print(f"\n- Файл: {file.filename}")
            print(f"  Добавени редове: +{file.additions} | Изтрити редове: -{file.deletions}")
            print(f"  --- Промяна (Patch) ---")
            print(file.patch)
            print(f"------------------------")

    except Exception as e:
        print(f"❌ Възникна грешка при четене на PR: {e}")


if __name__ == "__main__":
    fetch_pull_request()