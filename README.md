# JanitorAI Lorebook Scraper

A Python tool to extract lorebooks from JanitorAI by crawling the React Fiber tree. Only works for PUBLIC lorebooks.

## Features

- Extracts lorebook entries, title, and description
- Handles dynamic React content
- Interactive CLI for batch extraction
- Optional title/description fallback handling
- Formatted for SillyTavern import

## Installation

Install dependencies:

```bash
SETUP_AND_RUN.sh
```

## Usage

Run the scraper:

```bash
python lorebook-scraper.py
```

## How It Works

1. Launches a browser and navigates to the lorebook page
2. Clicks the "View" button to load full content
3. Crawls the React Fiber tree to find the lorebook data structure
4. Extracts title and description from DOM elements (optional)
5. Passes data through the lorebook-formatter for consistent output

## Troubleshooting

**"No lorebook found"**
- Check that the URL is a valid JanitorAI lorebook page

**Browser window doesn't open**
- Run `SETUP_AND_RUN.sh` to install the browser

## Requirements

- Python 3.8+
- playwright
- chromium browser (installed via Playwright)
- lorebook-formatter
