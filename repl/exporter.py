import pandas as pd
import datetime

t = datetime.datetime.now()
y = t.year
m = t.month
d = t.day
date = str(y)+'-'+str(m)+'-'+str(d)

# def save_to_file(jobs, keyword):
#     file = open("jobs.csv", mode = "w", encoding="ansi")
#     writer = csv.writer(file)
#     writer.writerow(["Title", "Company", "Location", "Link"])
#     for job in jobs:
#       writer.writerow(list(job.values()))
#     return
    
def save_to_file(jobs, keyword):
  df = pd.DataFrame(jobs)
  filename = f'./[{date}]Jobs({keyword}).xlsx'
  return df.to_excell(filename)