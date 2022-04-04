import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}


def get_ok_jobs(word):
    url = f"https://remoteok.io/remote-{word}-jobs"
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    #first one is an ad, so that works differently
    results = soup.find_all("td", {"class": "company_and_position"})[1:]

    jobs = []
    for result in results:
        title = result.find("h2").string
        company = result.find("h3").string
        link = result.find("a")["href"]
        jobs.append({
            'title': title,
            'company': company,
            'apply': f"https://remoteok.io{link}"
        })

    return jobs
