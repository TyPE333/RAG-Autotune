import requests
from bs4 import BeautifulSoup
import random
import time
import json

def get_random_wikipedia_page_title():
    """Fetches a random Wikipedia page title."""
    api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "random",
        "rnnamespace": 0,  # 0 for articles
        "rnlimit": 1,
        "format": "json",
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data["query"]["random"][0]["title"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching random page title: {e}")
        return None

def fetch_wikipedia_page_content(title, page_id):
    """Fetches the content of a Wikipedia page and formats it."""
    url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the main content
        content_div = soup.find('div', {'id': 'mw-content-text'})
        content = ""
        if content_div:
            paragraphs = content_div.find_all('p')
            content = "\n".join([p.get_text() for p in paragraphs])
        else:
            content = "Could not extract main content."

        return {"id": f"wiki_{page_id}", "title": title, "text": content}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content for '{title}': {e}")
        return None

if __name__ == "__main__":
    num_pages_to_fetch = 100
    wikipedia_data = []
    page_counter = 1

    for i in range(num_pages_to_fetch):
        print(f"Fetching page {i+1}/{num_pages_to_fetch}...")
        title = get_random_wikipedia_page_title()
        if title:
            page_data = fetch_wikipedia_page_content(title, page_counter)
            if page_data:
                wikipedia_data.append(page_data)
                page_counter += 1
            time.sleep(1)  # Be respectful to Wikipedia's servers

    print("\nSuccessfully fetched and formatted data for", len(wikipedia_data), "Wikipedia pages.")

    # Save the data to a JSON file
    with open("C:/Users/rohan/OneDrive/Documents/Downloads/Resume projects May 2025/RAG-Autotune/data/corpus.jsonl", "w", encoding="utf-8") as f:
        json.dump(wikipedia_data, f, indent=4)
    print("\nData saved to 'wikipedia_sample_data_formatted.json' in the desired format.")

    # Example of the first fetched item
    if wikipedia_data:
        print("\nExample of the first fetched item:")
        print(json.dumps(wikipedia_data[0], indent=4))
    else:
        print("\nNo data was fetched.")