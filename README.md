# IceVault Python SDK

[![CI](https://github.com/your-org/ice-vault-python-client/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/ice-vault-python-client/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/icevault.svg)](https://pypi.org/project/icevault/)
[![Python versions](https://img.shields.io/pypi/pyversions/icevault.svg)](https://pypi.org/project/icevault/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python client library for the [IceVault](https://icevault.example) REST API.

## Features

- **Sync & async** — `Client` and `AsyncClient` built on [httpx](https://www.python-httpx.org/)
- **Typed models** — request/response validation with [Pydantic v2](https://docs.pydantic.dev/)
- **Fully typed** — strict static analysis with MyPy
- **Modern tooling** — Ruff for linting and formatting, pytest for testing

## Requirements

- Python 3.11+

## Installation

```bash
pip install icevault
```

Or with [Poetry](https://python-poetry.org/):

```bash
poetry add icevault
```

## Quick start

```python
from icevault import Client

with Client(api_key="your-api-key") as client:
    # Call API resources here once implemented
    ...
```

Async usage:

```python
import asyncio

from icevault import AsyncClient


async def main() -> None:
    async with AsyncClient(api_key="your-api-key") as client:
        ...


asyncio.run(main())
```

## Development

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-org/ice-vault-python-client.git
cd ice-vault-python-client
poetry install --with dev
```

Run the quality checks:

```bash
poetry run ruff check .
poetry run ruff format --check .
poetry run mypy src tests
poetry run pytest
```

## License

MIT © [IceVault](https://github.com/adminIceVault)

