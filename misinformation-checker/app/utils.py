import requests
from bs4 import BeautifulSoup

def scrape_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        scraped_text = ' '.join([para.get_text() for para in paragraphs])
        return scraped_text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def check_with_fact_check_api(query, api_key):
    api_url = f'https://factchecktools.googleapis.com/v1alpha1/claims:search?key={api_key}'
    try:
        response = requests.get(api_url, params={'query': query})
        response.raise_for_status()
        data = response.json()
        claims = data.get('claims', [])
        fact_check_results = []
        for claim in claims:
            text = claim.get('text', 'No text available')
            claim_review = claim.get('claimReview', [])
            for review in claim_review:
                publisher = review.get('publisher', {}).get('name', 'Unknown Publisher')
                rating = review.get('textualRating', 'No Rating')
                fact_check_results.append(f"{text} (Source: {publisher}, Rating: {rating})")
        return fact_check_results
    except Exception as e:
        print(f"Error with Fact-Check API: {e}")
        return []
