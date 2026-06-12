from icevault import AsyncClient


async def restore_file():
    client = AsyncClient(
        api_key="API_KEY",
    )

    archives = await client.archives.filter(
        archive_filter={
            "status": "ARCHIVED",
            "search": "vault"
        },
    )
    for i in archives.items:
        result = await client.archives.restore(i.uuid)

if __name__ == "__main__":
    """"""
    import asyncio
    asyncio.run(restore_file())

