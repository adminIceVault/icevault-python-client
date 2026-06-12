from pathlib import Path
import tokenize
import unasync

# 1. Знаходимо корінь папки з асинхронним кодом
async_dir = Path("src/icevault/_async")

# 2. Збираємо абсолютно всі файли .py всередині цієї папки рекурсивно (включаючи всі підпапки)
#    rglob("*") знайде і archives/archives.py, і якісь нові бакети, юзерів тощо.
file_paths = [str(p) for p in async_dir.rglob("*.py") if p.is_file()]

print(f"Found {len(file_paths)} async files to transform...")

# 3. Запускаємо ансинк
unasync.unasync_files(
    file_paths,
    rules=[
        unasync.Rule(
            fromdir="src/icevault/_async",
            todir="src/icevault/_sync",
            additional_replacements={
                "_async": "_sync",
                "aiter_bytes": "iter_bytes",

                "AsyncClient": "Client",
                "AsyncArchives": "Archives",
                "AsyncStorage": "Storage",
                "async_client": "sync_client",

                "async_zip": "sync_zip",
            }
        )
    ]
)

print("🚀 Sync code generated successfully in src/icevault/_sync/")