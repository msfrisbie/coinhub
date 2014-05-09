#!/usr/bin/python

from github import Github
from datetime import datetime,date,timedelta
from time import sleep
import json

# Fill these out:

GITHUB_USERNAME = ''
GITHUB_PASSWORD = ''
NUMBER_OF_DAYS_IN_BETWEEN_DATAPOINTS = 1
KEYWORDS_TO_SEARCH_FOR = ['stripe','paypal','bitcoin','btc','dogecoin']

def date_to_qstr(date):
  return str(date.year)+'-'\
    +('0' if date.month < 10 else '')+str(date.month)+'-'\
    +('0' if date.day < 10 else '')+str(date.day)

def query_count(qstr,qday):
  print qstr, qday
  try:
    return g.search_repositories(qstr+' created:<'+qday).totalCount
  except:
    print "Rate limit hit, trying again in 15 seconds..."
    sleep(15)
    print "Trying again..."
    return query_count(qstr,qday)

# date of satoshi paper release
# dday = date(year=2008,month=10,day=31)

g = Github(GITHUB_USERNAME,GITHUB_PASSWORD)

# from jan 1 2008 to now
dday = date(year=2008,month=1,day=1)
today = datetime.now().date()
interval = timedelta(days=NUMBER_OF_DAYS_IN_BETWEEN_DATAPOINTS)
keywords = KEYWORDS_TO_SEARCH_FOR

data = {}

for k in keywords:
  refdate = dday
  data[k] = []
  while refdate < today:
    data[k].append([
      date_to_qstr(refdate),
      query_count(k,date_to_qstr(refdate))
    ])
    refdate += interval

f = open('github_stats_by_'+str(interval.days)+'_days.json','w')
f.write(json.dumps(data))
f.close()
