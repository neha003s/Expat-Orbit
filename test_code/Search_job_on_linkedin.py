import requests
from bs4 import BeautifulSoup

keyword = input("Enter the keyword to search: ")
#keyword = "Google"

# Construct the search URL
url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}"

# Make a GET request to the URL
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36"
}
response = requests.get(url, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    # Parse job listings
    job_titles = soup.find_all("h3", class_="base-search-card__title")
    companies = soup.find_all("h4", class_="base-search-card__subtitle")

    # Print job listings
    for job, company in zip(job_titles, companies):
        print(f"Job Title: {job.text.strip()}, Company: {company.text.strip()}")
else:
    print("Failed to retrieve data. Please check your internet connection or URL.")
