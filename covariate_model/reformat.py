

import csv
import fileinput
import sys

def get_flowids(L):
  return dict([v['URL Variable: flowid'], v] for v in L)

if __name__ == "__main__":
  flowids = get_flowids(list(csv.DictReader(open(sys.argv[1]))))
