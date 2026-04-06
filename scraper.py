import requests
from bs4 import BeautifulSoup

def get_clean_seo_data(url: str) -> dict | str:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except requests.RequestException as e:
        return f"Error fetching page: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    meta_title = soup.title.string.strip() if soup.title else "No Title"

    meta_desc = soup.find("meta", attrs={"name": "description"})
    desc_content = meta_desc["content"] if meta_desc else "No Description"

    og_title = soup.find("meta", property="og:title")
    og_desc = soup.find("meta", property="og:description")
    canonical = soup.find("link", rel="canonical")
    h1_tags = [h.get_text(strip=True) for h in soup.find_all("h1")]

    page_text = soup.get_text(separator=' ', strip=True)

    return {
        "title": meta_title,
        "description": desc_content,
        "og_title": og_title["content"] if og_title else None,
        "og_description": og_desc["content"] if og_desc else None,
        "canonical_url": canonical["href"] if canonical else None,
        "h1_tags": h1_tags,
        "body_preview": page_text[:3000],
    }


# Test it out
data = get_clean_seo_data("https://www.google.com")  # Or any URL you want!
print(data)
