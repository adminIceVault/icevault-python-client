import asyncio
import os
from pathlib import Path
import typing
from urllib.parse import urlparse, parse_qs
import httpx
from pydantic import BaseModel


class Part(BaseModel):
    part_no: int
    url: str


class PartEtag(BaseModel):
    part_no: int
    etag: str


async def upload_part(
    parts: list[Part],
    file_path: str,
    chunk_size: int,
    headers: dict = {},
) -> str:
    """"""
    headers_ = {"Content-Type": "application/octet-stream"}
    headers_.update(headers)
    result: list[PartEtag] = []
    async with httpx.AsyncClient() as client:
        with open(file_path, "rb") as f:
            for i in parts:
                chunk_data = f.read(chunk_size)
                response: Response = await client.put(
                    i.url,
                    content=chunk_data,
                    headers=headers_,
                )
                etag = response.headers.get("etag") or response.headers.get("ETag")
                result.append(
                    PartEtag(
                        part_no=i.part_no,
                        etag=etag,
                    )
                )
    return result
