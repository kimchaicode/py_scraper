import requests
from bs4 import BeautifulSoup


def extract_last_page(word):
    url = f"https://stackoverflow.com/jobs?q={word}&r=true"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find("a", {"class": "s-link"})["title"]
    company, location = html.find("h3").find_all("span", recursive=False)
    company = company.get_text(strip=True)
    link = html['data-jobid']
    return {
        'title': title,
        'company': company,
        "apply": f"https://stackoverflow.com/jobs/{link}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(
            f"https://stackoverflow.com/jobs?q=python&r=true&pg={page}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
            
    return jobs


def get_stack_jobs(word):
    last_page = extract_last_page(word)
    jobs = extract_jobs(last_page)
    return jobs
