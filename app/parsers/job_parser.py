import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def parse_job_url(url):
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {response.status_code}")

    soup = BeautifulSoup(response.text, "lxml")

    # ---- LinkedIn specific attempt ----
    linkedin_desc = soup.find("div", {"class": "description__text"})
    if linkedin_desc:
        return linkedin_desc.get_text(separator="\n").strip()

    # ---- Generic fallback ----
    paragraphs = soup.find_all("p")
    text = "\n".join([p.get_text() for p in paragraphs])

    if not text.strip():
        raise Exception("Could not extract job description.")

    return text.strip()