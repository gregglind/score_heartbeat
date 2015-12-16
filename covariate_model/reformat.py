

import csv
import fileinput
import sys
import json
import logging

import codecs

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

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

def reformat(flowids, other):
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
          dnt = int(extra['doNotTrack']),
          channel = d['channel'],
          locale = d['locale'],
          received = d['received_ts'],
          version = d['version'],
          series = int(d['version'].split('.')[0])
        )
        yield out
      except Exception as e:
        print d
        print extra
        print flowids[flowid]
        raise e

def write(iterator, csvfile=sys.stdout):
  first = iterator.next()
  #with open(fn, 'w') as csvfile:
  fieldnames = sorted(first.keys());
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
  writer.writerow(first)
  for i in iterator:
    writer.writerow(i)


if __name__ == "__main__":
  flowids = get_flowids(list(csv.DictReader(open(sys.argv[1]))))
  thedata = csv.DictReader(open(sys.argv[2]),delimiter="\t")
  outiter = reformat(flowids, thedata)
  write(outiter, sys.stdout)

