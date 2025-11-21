import requests
import os
import re

SERPAPI_KEY = os.environ.get("SERPAPI_KEY")
SCHOLAR_ID = os.environ.get("SCHOLAR_ID")

def get_scholar_metrics():
    try:
        url = "https://serpapi.com/search"
        params = {
            "engine": "google_scholar_author",
            "author_id": SCHOLAR_ID,
            "api_key": SERPAPI_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        cites = data["cited_by"]["table"][0]["citations"]["all"]
        h_index = data["cited_by"]["table"][1]["h_index"]["all"]
        i10_index = data["cited_by"]["table"][2]["i10_index"]["all"]

        return cites, h_index, i10_index

    except Exception as e:
        print("Error:", e)
        return None, None, None


def update_index(citations, hindex, i10index):
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(r"\{\{CITATIONS\}\}", str(citations), content)
    content = re.sub(r"\{\{HINDEX\}\}", str(hindex), content)
    content = re.sub(r"\{\{I10INDEX\}\}", str(i10index), content)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)


def main():
    cites, h, i10 = get_scholar_metrics()

    if cites is None:
        print("Failed to fetch metrics.")
        return

    update_index(cites, h, i10)
    print("Metrics updated successfully.")


if __name__ == "__main__":
    main()
