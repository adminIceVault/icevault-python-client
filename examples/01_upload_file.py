from icevault import AsyncClient


async def upload_files():
    client = AsyncClient(
        api_key="API_KEY",
    )

    await client.storages.upload_files(
        ["file.png", "file2.png", ...],
        storage_class="STANDARD",
        archive_name="api_test.zip",
    )

if __name__ == "__main__":
    """"""
    import asyncio
    asyncio.run(upload_files())

