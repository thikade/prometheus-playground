import os
import yaml
import datetime as dt

from flask import Flask


app = Flask(__name__)

counter = 0
time  = dt.datetime.now()

with open(os.environ['SCRAPE_TAPE'], 'r') as f:
    data = yaml.safe_load(f)
    scrapes = data['scrapes']
    interval = data.get('interval', None)

# default to -1: return a new value from scapes array immediately!
if not interval: interval = -1

app.logger.warn("change interval: {:d}s".format(interval)) 
app.logger.warn("number of scrapes: {:d}".format(len(scrapes))) 


@app.route('/metrics')
def metrics():
    
    global counter
    global time
    resp = scrapes[min(counter, len(scrapes) - 1)]
    newTime = dt.datetime.now()
    if (newTime - time).total_seconds() > interval: # after each interval we will output a new value from scape array
        counter += 1
        time = newTime
    
    buf = "# INFO interval={:d} samples={:d}\n{:s}".format(interval, len(scrapes), resp['data'])
    return buf, resp['status_code']

