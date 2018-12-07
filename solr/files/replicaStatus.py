import time
import requests
import sys
from datetime import datetime
from solrutil import getStatus, getId
import logging
import re

logging.getLogger().setLevel(logging.INFO)
report = {}

# TO Be used for further , not related to alerting.
def format(c,vm,state):

    report[c].append({
     vm : state
    })

 
def getDown(c, status):

  report[c]=[]
  d = status['cluster']['collections'][c]['shards']
  for k,v in d.items():
      for i,j in d[k]['replicas'].items():

          vm = d[k]['replicas'][i]['node_name'].split(':')[0].strip(
          '".c.my-dummy-project.internal"'
          )
          state = d[k]['replicas'][i]['state']
          format(c, vm, state)
          found = re.search('us-central1-[f,b,c,a]', vm)

          if found:
              zone = found.group(0)
          else:
              log.fatal(
              "{} could not find match for the zone".format(
              datetime.now()
              ))

              sys.exit(1)

          hostId = getId(vm)

          if state != 'active':
               print "not active"

          logging.info("{}  {} has status {}".format(
                 datetime.now(),vm, state
              ))


def main():
    collections = ['c1','c2','c3']
    status = getStatus()
    for c in collections:
        getDown(c, status)
main()
