#!/bin/bash
echo "Lancement des tests pytest..."
PYTHONPATH=. pytest tests/test_main.py
