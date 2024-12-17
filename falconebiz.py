import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

def google_search_for_falconebiz(cin, max_pages=1):
    base_url = "https://www.google.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    falconebiz_urls = []

    for page in range(max_pages):
        start = page * 1
        params = {"q": f"cin {cin} site:falconebiz.com", "start": start}
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("a", href=True)

            for result in results:
                href = result['href']
                print(f"Raw href: {href}")

                # Skiping irrelevant Google search links
                if "/url?q=" in href:
                    # Extract the actual URL
                    extracted_url = href.split("&")[0].replace("/url?q=", "").strip()
                    extracted_url = unquote(extracted_url)

                    # Falconebiz URLs only, ignoring other Google-related links
                    if "falconebiz.com" in extracted_url and ("/company/" in extracted_url or "/director/" in extracted_url):
                        falconebiz_urls.append(extracted_url)

        else:
            print(f"Error fetching Google page {page + 1}. HTTP status: {response.status_code}")
            break

        time.sleep(2)  # Delay to avoiding Google blocking the request

    return falconebiz_urls

cin = input("Enter the CIN: ")

falconebiz_urls = google_search_for_falconebiz(cin)

if falconebiz_urls:
    print("\nRelevant Falconebiz URLs Found:")
    for url in falconebiz_urls:
        print(f"Valid Falconebiz URL: {url}")
else:
    print("No relevant Falconebiz URLs found.")