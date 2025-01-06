import requests
import pandas as pd
import json
import time
from bs4 import BeautifulSoup

def extract_relevant_links(raw_hrefs):
    valid_links = set()
    for href in raw_hrefs:
        if href.startswith("https://www.linkedin.com/"):
            valid_links.add(href)
    return valid_links

def google_search_for_linkedin(company_name, person_name, max_pages=1):
    base_url = "https://www.google.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    linkedin_urls = set()
    for page in range(max_pages):
        start = page * 5
        params = {"q": f"{company_name} {person_name} site:linkedin.com", "start": start}
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("a", href=True)
            raw_hrefs = [result['href'] for result in results]
            linkedin_urls.update(extract_relevant_links(raw_hrefs))
        else:
            print(f"Error fetching Google page {page + 1}. HTTP status: {response.status_code}")
            break

        time.sleep(5)
    
    return list(linkedin_urls)


def update_csv_with_linkedin_details(csv_file_path, company_name, person_name, linkedin_urls):
    try:
       
        df = pd.read_csv(csv_file_path)
        df.columns = df.columns.str.strip()  # Strip whitespace from headers
        
        # Ensuring 'Linkedin_Urls' column is of string type
        df['Linkedin_Urls'] = df['Linkedin_Urls'].astype(str)
        
        # Checking if the company name exists in the 'Company Name' column
        if company_name in df['Company Name'].values:
            # Get the current LinkedIn URLs (handle missing or NaN values)
            current_links = df.loc[df['Company Name'] == company_name, 'Linkedin_Urls'].values[0]
            
            if pd.isna(current_links) or current_links == 'nan':
                current_links = []
            else:
                current_links = json.loads(current_links)

            # Appending new links and remove duplicates
            all_links = list(set(current_links + linkedin_urls))

            # Updating the row in the DataFrame
            df.loc[df['Company Name'] == company_name, 'Linkedin_Urls'] = json.dumps(all_links)
            df.to_csv(csv_file_path, index=False)
            print(f"Updated LinkedIn URLs for {company_name} in the CSV file.")
        else:
            print(f"{company_name} not found in the CSV file.")
    except Exception as e:
        print(f"Error updating CSV file: {e}")




# Main function
def main():
    company_name = input("Enter the company name: ")
    person_name = input("Enter the person name: ")

    # Search for LinkedIn URLs
    linkedin_urls = google_search_for_linkedin(company_name, person_name)

    if linkedin_urls:
        print("\nLinkedIn URLs Found:")
        for url in linkedin_urls:
            print(f"LinkedIn Link: {url}")

        csv_file_path = "/mnt/d/data_excel/2024/csv/new-Company-and-LLP-incorporation-Feb.csv"
        
        update_csv_with_linkedin_details(csv_file_path, company_name, person_name, linkedin_urls)
    else:
        print("No relevant LinkedIn URLs found.")

if __name__ == "__main__":
    main()
