import os
import csv
from flask import Flask, render_template, request, redirect, send_file, abort
from wework import get_wework_jobs
from stack import get_stack_jobs
from ok import get_ok_jobs

os.system("clear")
"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

app = Flask("Finalproject")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/read")
def read():
    word = request.args.get('word')
    if word is None:
        return redirect("/")

    word = word.lower()
    existing_jobs = db.get(word)
    if existing_jobs:
        all_posts = existing_jobs
    else:
        all_posts = get_wework_jobs(word) + get_stack_jobs(word) + get_ok_jobs(
            word)
        db[word] = all_posts
    return render_template(
        "read.html", posts=all_posts, resultsNumber=len(all_posts), word=word)


@app.route("/export")
def export():
    word = request.args.get('word')
    if word is None:
        return redirect("/")

    word = word.lower()
    if word not in db:
      abort(404)
    jobs = db[word]

    path = f"./tmp/{word}.csv"
    file = open(path, mode="w")
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "Link"])

    for job in jobs:
        writer.writerow([job['title'], job['company'], job['apply']])

    return send_file(path, as_attachment=True, attachment_filename=f"{word}.csv")


app.run(host="0.0.0.0")
