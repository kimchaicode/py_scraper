import requests
from bs4 import BeautifulSoup


def get_wework_jobs(word):
    url = f"https://weworkremotely.com/remote-jobs/search?term={word}&button="
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("li", {"class": "feature"})
    jobs = []
    for result in results:
        title = result.find("span", {"class": "title"}).string
        company = result.find("span", {"class": "company"}).string
        link = company.parent.parent["href"]
        jobs.append({
            "title": title,
            "company": company,
            "apply": f"https://weworkremotely.com{link}"
        })

    return jobs
