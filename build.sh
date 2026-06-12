#!/bin/bash
set -e

echo "1. Running unasync code generation..."
poetry run python generate_sync.py

echo "2. Cleaning up old builds..."
rm -rf dist/

echo "3. Building the wheel and sdist..."
poetry build