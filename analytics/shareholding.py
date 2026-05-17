import requests
from bs4 import BeautifulSoup


def get_shareholding(ticker):

    url = f"https://www.screener.in/company/{ticker}/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"id": "shareholding"})

    data = []

    if table:
        rows = table.find_all("tr")

        for row in rows[1:]:
            cols = row.find_all("td")

            if len(cols) >= 2:
                data.append({
                    "Category": cols[0].text.strip(),
                    "Holding": cols[1].text.strip()
                })

    return data