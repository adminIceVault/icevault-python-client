import asyncio
import os
import tempfile
from pathlib import Path
import pyzipper


def _sync_compress(src_files: list[Path], archive_path: Path, password: str | None) -> None:
    """"""
    with pyzipper.AESZipFile(
        archive_path,
        "w",
        compression=pyzipper.ZIP_DEFLATED,
        encryption=pyzipper.WZ_AES if password else None
    ) as zf:
        if password:
            zf.setpassword(password.encode("utf-8"))

        for file_path in src_files:
            if not file_path.exists():
                continue

            with file_path.open("rb") as src_f, zf.open(file_path.name, "w") as dest_f:
                while chunk := src_f.read(65536):  # Читаємо по 64 КБ
                    dest_f.write(chunk)


async def create_secure_archive(
    file_paths: list[str | Path],
    password: str | None = None,
    custom_temp_dir: str | Path | None = None,
) -> Path:
    """
    Asynchronously creates a password-protected zip archive using pyzipper.
    100% pure Python, cross-platform, memory-safe, non-blocking for Event Loop.
    """
    if not file_paths:
        raise ValueError("The list of file paths cannot be empty.")

    target_dir = Path(custom_temp_dir) if custom_temp_dir else Path(tempfile.gettempdir())
    target_dir.mkdir(parents=True, exist_ok=True)

    archive_path = target_dir / f"vault_archive_{os.getpid()}_{len(file_paths)}.zip"
    src_files = [Path(p).resolve() for p in file_paths]

    await asyncio.to_thread(_sync_compress, src_files, archive_path, password)

    return archive_path
