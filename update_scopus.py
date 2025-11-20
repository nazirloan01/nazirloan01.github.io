import json
import requests
import re
import os

SCOPUS_ID = "56997291000"

def get_scopus_metrics(api_key):
    # BASIC view (publicly accessible)
    url = f"https://api.elsevier.com/content/author/author_id/{SCOPUS_ID}?view=BASIC"
    headers = {"X-ELS-APIKey": api_key}

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("Error:", r.text)
        return None

    data = r.json()
    author = data["author-retrieval-response"][0]

    # BASIC view provides h-index and citation-count
    h_index = author.get("h-index", "N/A")
    citations = author["coredata"].get("citation-count", "N/A")

    # Public API does not support i10-index
    i10_index = "N/A"

    return citations, h_index, i10_index


def update_html(citations, h_index, i10_index):
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("{{CITATIONS}}", str(citations))
    html = html.replace("{{HINDEX}}", str(h_index))
    html = html.replace("{{I10INDEX}}", str(i10_index))

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)


def main():
    api_key = os.getenv("SCOPUS_API_KEY")

    if not api_key:
        print("Missing API key")
        return

    metrics = get_scopus_metrics(api_key)
    if metrics:
        update_html(*metrics)
        print("Scopus metrics updated successfully!")
    else:
        print("Failed to retrieve metrics.")


if __name__ == "__main__":
    main()
