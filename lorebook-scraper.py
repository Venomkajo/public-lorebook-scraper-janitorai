import asyncio
import json
from playwright.async_api import async_playwright
from lorebook_formatter import convert_array_to_dict

async def nuclear_extract(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) # headless True doesn't work
        page = await browser.new_page()

        await page.goto(url)

        await page.wait_for_load_state("networkidle")

        await page.click("button._viewButton_lb2ff_277")

        await page.wait_for_timeout(2000)

        lorebook = await page.evaluate("""
            () => {
                function deepSearch(obj, seen = new WeakSet()) {
                    if (!obj || typeof obj !== 'object') return null;
                    if (seen.has(obj)) return null;
                    seen.add(obj);

                    if (typeof obj === 'string' && obj.length > 100) {
                        try {
                            const parsed = JSON.parse(obj);
                            if (isLorebook(parsed)) return normalizeLorebook(parsed);
                        } catch {}
                    }

                    for (const key of Object.keys(obj)) {
                        try {
                            const val = obj[key];
                            if (typeof val === 'string' && val.length > 100) {
                                try {
                                    const parsed = JSON.parse(val);
                                    if (isLorebook(parsed)) return normalizeLorebook(parsed);
                                } catch {}
                            }
                            if (typeof val === 'object') {
                                const found = deepSearch(val, seen);
                                if (found) return found;
                            }
                        } catch {}
                    }
                    return null;
                }

                function isLorebook(data) {
                    if (!data) return false;
                    if (Array.isArray(data) && data.length > 0) {
                        return !!(data[0].content && data[0].key);
                    }
                    return !!(data.content && data.key);
                }

                function normalizeLorebook(data) {
                    if (Array.isArray(data)) return data;
                    if (data.entries) return data.entries;
                    return [data]; // Single entry, wrap in array
                }

                const root = document.getElementById('root');
                if (!root) return null;
                const fiberKey = Object.keys(root).find(k => k.includes('react'));
                if (!fiberKey) return null;

                return deepSearch(root[fiberKey]);
            }
        """)
        
        lorebook_title = "Unnamed Lorebook"
        try:
            title_locator = page.locator("h2._title_lb2ff_344")
            if await title_locator.count() > 0:
                lorebook_title = await title_locator.first.text_content(timeout=3000) or "Unnamed Lorebook"
        except:
            pass

        lorebook_description = ""
        try:
            desc_locator = page.locator("p._description_lb2ff_355")
            if await desc_locator.count() > 0:
                lorebook_description = await desc_locator.first.text_content(timeout=3000) or ""
        except:
            pass

        await browser.close()

        return {
            "title": lorebook_title.strip() if lorebook_title else "Unnamed Lorebook",
            "description": lorebook_description.strip() if lorebook_description else "",
            "lorebook": lorebook,
        } if lorebook else None

def main():

    print("Welcome to the JanitorAI Lorebook Scraper!")
    print("Takes around 5 seconds per lorebook if url is correct.")

    while True:
        url = input("Enter the JanitorAI lorebook URL (or nothing to quit): ")
        if not url:
            break

        result = asyncio.run(nuclear_extract(url))

        if result != None:
            safe_title = result['title'].replace("/", "-").replace("\\", "-")
            
            with open(f"{safe_title}.json", "w") as f:
                json.dump(convert_array_to_dict(result['lorebook'], result['title'], result['description']), f, indent=4)
            print(f"Lorebook data extracted successfully and saved to {safe_title}.json")
        else:
            print("No lorebook found at the provided URL. Please check the URL and try again.")

        if input("Do you want to extract another lorebook? (y/n): ").lower() != 'y':
            break

main()