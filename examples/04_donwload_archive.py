from icevault import AsyncClient
import os

async def restore_file():
    client = AsyncClient(
        api_key="API_KEY",
    )

    archives = await client.archives.filter(
        archive_filter={
            "status": "uploaded",
            "search": "test.zip"
        },
    )
    filename = "test.zip"
    for i in archives.items:
        result = await client.archives.download(i.uuid, filename)
        print(f"File downloaded: {os.path.isfile(filename)}, {os.path.getsize(filename)}")

if __name__ == "__main__":
    """"""
    import asyncio
    asyncio.run(restore_file())

