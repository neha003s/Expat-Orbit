import requests
import pandas as pd
from urllib.parse import unquote
import time
from bs4 import BeautifulSoup
import json 

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

            falconebiz_urls = extract_relevant_urls(raw_hrefs)
        else:
            print(f"Error fetching Google page {page + 1}. HTTP status: {response.status_code}")
            break

        time.sleep(5)

    return falconebiz_urls

def format_directors_details(urls):
    director_details = []
    for url in urls:
        if "director" in url:
            parts = url.split("/")[-2:]  
            director_details.append({
                "director_name": unquote(parts[-1].replace("-", " ")),  
                "director_url": url
            })
    return json.dumps(director_details)  
def update_csv_with_director_details(csv_file_path, cin, director_urls):
    
    df = pd.read_csv(csv_file_path)
    df.columns = df.columns.str.strip()  
    print("CSV Headers:", '    '.join(df.columns))

    if cin in df['CIN'].values:
        formatted_details = format_directors_details(director_urls)
        df.loc[df['CIN'] == cin, 'Directors Details'] = formatted_details
        
        df.to_csv(csv_file_path, index=False)
        print("Updated Directors Details for CIN", cin, "in the CSV file.\n")
    else:
        print(f"CIN {cin} not found in the CSV file.")

def main():
    cin = input("Enter the CIN: ")
    falconebiz_urls = google_search_for_falconebiz(cin)

    if falconebiz_urls:
        print("\nCompany and Directors URLs:")
        for url in falconebiz_urls:
            print(f"Relevant Falconebiz URL Found: {url}")
        
        csv_file_path = "/mnt/d/data_excel/2024/csv/new-Company-and-LLP-incorporation-Feb.csv"
        update_csv_with_director_details(csv_file_path, cin, falconebiz_urls)
    else:
        print("No relevant Falconebiz URLs found.")

if __name__ == "__main__":
    main()
