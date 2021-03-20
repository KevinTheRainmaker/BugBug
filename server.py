from flask import Flask, render_template, request, redirect, send_file
from indeedScrapper import give_me_job
from exporter import save_to_file
import datetime

t = datetime.datetime.now()
y = t.year
m = t.month
d = t.day
date = str(y)+'-'+str(m)+'-'+str(d)

app = Flask("BugBug")

fakeDB = {}

@app.route("/")
def home():
  return render_template('home2.html')

@app.route("/report")
def report():
  render_template('loading.html')
  word = request.args.get('word').strip()
  if word != '':
    word = word.capitalize()
    jobExist = fakeDB.get(word)
    if jobExist:
        jobs = jobExist
    else:
      jobs = give_me_job(word)
      fakeDB[word] = jobs
  else:
    return redirect('/')
  return render_template('report2.html', keyword=word, jobs=jobs, resultNum=len(jobs))


  

@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.capitalize()
        jobs = fakeDB.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs,word)
        return send_file("jobs.csv", mimetype = 'text/csv; charset=x-EBCDIC-KoreanAndKoreanExtended')
    except:
        return redirect("/")

app.run(host='0.0.0.0')