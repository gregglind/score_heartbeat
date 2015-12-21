

import csv
import fileinput
import json
import logging
import sys
import time

import codecs

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

DAY = 86400

def get_flowids(L):
  return dict([v['URL Variable: flowid'], v] for v in L)

'''
10376493  1 1449623889390 NA  heartbeat-by-user-first-impression  6f4244db-1f5b-4b68-a5d9-1201dc6732cd  Please rate Firefox Please rate Firefox 27  NULL  5 1449623889390 0 0 0 UNK aurora  42.0a2  en-us - - 0 {}  {"addons": []}  {"crashes": {}, "defaultBrowser": false, "doNotTrack": false, "engage": [], "numflows": 0, "plugins": {}, "searchEngine": "google", "syncSetup": false} 0 - 2015-12-08 17:18:10 UNK

'''

'''
{"crashes": {},
"defaultBrowser": true,
"doNotTrack": false,
"engage": [],
"flashVersion": "19.0.0.245",
"numflows": 0,
"plugins": {"Adobe Acrobat": "9.0.0.332", "CANON iMAGE GATEWAY Album Plugin Utility": "3.0.5.0", "Google Update": "1.3.29.1", "PriceMeterLiveUpdate Update": "1.3.23.0", "Shockwave Flash": "19.0.0.245", "VLC Web Plugin": "2.0.2.0", "Yahoo Application State Plugin": "1.0.0.7"}
"searchEngine": null, "syncSetup": false}
'''


def clockSkewed(server, local):
  """ clock is more than a day off """
  # both are in js ms scale
  s = int(time.mktime(time.strptime(server, "%Y-%m-%d %H:%M:%S"))) * 1000
  l = int(local)
  #print s, l, server, local, abs(s-l)
  return abs(s-l) > (24 * 60 * 60 * 1000)


def fxOutofDate(version, ts, releases):
  # this needs improving!  the firefox-json file doesn't have all channel dates.
  # this will be 'right' only for release
  try:
    ts = int(time.mktime(time.strptime(ts, "%Y-%m-%d %H:%M:%S")))
    my = releases['firefox-'+version]
    d = int(time.mktime(time.strptime(my['date'], "%Y-%m-%d")))
    return ( ts - d ) > (8*7*DAY)  # 8 weeks
  except (KeyError) as e:
    return False
  except Exception as e:
    logging.warn("%s %s", version, ts)
    raise e

def hasSilverLight(plugin_list):
  return any(('silverlight' in x.lower() for x in plugin_list))

def reformat(flowids, other, releases):
  for d in other:
    flowid = d['flow_id']
    if flowid in flowids:
      logging.debug(flowids[flowid])
      logging.debug(d)
      out = dict()
      # parse extras
      # parse score
      # push new listy thing
      score = flowids[flowid]['URL Variable: score']
      extra = json.loads(d['extra'])
      logging.debug(extra)

      # does it really have the extra fields?
      if 'defaultBrowser' not in extra:
        continue

      try:
        engine = extra.get('searchEngine',None)

        out = dict(
          flowid = flowid,
          score = int(score),
          defaultBrowser = int(bool(extra['defaultBrowser'])), # n/a shows as NO.
          searchEngine = engine or "other",
          weirdEngine = int(not bool(engine)),
          hasFlash = int("flashVersion" in extra),
          oldFx =  int(fxOutofDate(d['version'], d['received_ts'], releases)),
          silverlight = int(hasSilverLight(extra['plugins'].keys())),
          clockSkewed = int(clockSkewed(d['received_ts'], d['updated_ts'])),
          dnt = int(extra['doNotTrack']),
          channel = d['channel'],
          locale = d['locale'],
          received = d['received_ts'],
          version = d['version'],
          series = int(d['version'].split('.')[0]),
          extra = json.dumps(extra)
        )
        yield out
      except Exception as e:
        print d
        print extra
        print flowids[flowid]
        raise e

def write(iterator, csvfile=sys.stdout):
  first = iterator.next()
  fieldnames = sorted(first.keys())

  # make extra last
  fieldnames.pop(fieldnames.index('extra'))
  fieldnames.append('extra')
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
  writer.writerow(first)
  for i in iterator:
    writer.writerow(i)


if __name__ == "__main__":
  flowids = get_flowids(list(csv.DictReader(open(sys.argv[1]))))
  thedata = csv.DictReader(open(sys.argv[2]),delimiter="\t")
  dates = json.load(open(sys.argv[3]))
  outiter = reformat(flowids, thedata, dates['releases'])
  write(outiter, sys.stdout)

