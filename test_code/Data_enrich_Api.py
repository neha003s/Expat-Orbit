import requests
from urllib.parse import unquote
import time
from fastapi import FastAPI, Query
from bs4 import BeautifulSoup

app = FastAPI()

def extract_relevant_urls(raw_hrefs):
    relevant_urls = []
    for href in raw_hrefs:
        if href.startswith("https://www.falconebiz.com/company/") or href.startswith("https://www.falconebiz.com/director/"):
            relevant_urls.append(href)
    return relevant_urls

def google_search_for_falconebiz(cin, max_pages=1):
    base_url = "https://www.google.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    falconebiz_urls = []

    for page in range(max_pages):
        start = page * 10
        params = {"q": f"cin {cin} site:falconebiz.com", "start": start}
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("a", href=True)
            raw_hrefs = [result['href'] for result in results]
            falconebiz_urls.extend(extract_relevant_urls(raw_hrefs))
        else:
            break

        time.sleep(5)

    return falconebiz_urls

@app.get("/falconebiz-urls")
def get_falconebiz_urls(
    cin: str = Query(..., description="The CIN to search for Falconebiz URLs"),
    max_pages: int = Query(1, description="Number of Google search pages to scrape")
):
    urls = google_search_for_falconebiz(cin, max_pages)
    return {"status": "success" if urls else "error", "falconebiz_urls": urls or "No Falconebiz URLs found"}

def main():
    cin = input("Enter the CIN: ")
    falconebiz_urls = google_search_for_falconebiz(cin)
    if falconebiz_urls:
        for url in falconebiz_urls:
            print(f"Falconebiz URL: {url}")
    else:
        print("No Falconebiz URLs Found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
