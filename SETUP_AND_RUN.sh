#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Playwright install
playwright install chromium --with-deps

# Run the application
python lorebook-scrapper.py