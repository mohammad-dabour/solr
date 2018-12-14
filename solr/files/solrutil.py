import requests
import sys
import os
import googleapiclient.discovery
import random
import socket
import ast
import logging
from datetime import datetime

"""
 This file to be utlized internal. This is not config file.
 Only code can write it and modifiy it and always has one location.
 getInstances() will write into this file location /tmp/solrvms.
 And will renew when necessary.
"""

solrvms = '/tmp/solrvms'

logging.getLogger().setLevel(logging.INFO)

def getDoc(vm):

    try:
         status = requests.get('http://'+str(vm)+':8983/solr/admin/collections?action=clusterstatus&wt=json')
         if status.status_code == 200:
              return status.json()

         else:
              logging.fatal("{} status code was {}".format(
              datetime.now(),str(status.status_code)))
              sys.exit(1)

    except Exception, e:

         logging.fatal("{} something wrong, could be connectivity issue {}"
         .format(datetime.now(),str(e)))
         sys.exit(2)


def verfiyHost(vm):
     try:

         socket.gethostbyname(vm)
         return True
     except socket.error:
         return False

def getInstances():
    """
    for now it supports only one region
    Later i will parametrize them or add as config
    """
    zones = ['us-central1-f','us-central1-b', 'us-central1-c','us-central1-a']
    project = 'my-dummy-project'

    compute = googleapiclient.discovery.build('compute', 'v1')
    for zone in zones:
        result = compute.instances().list(project=project, zone=zone).execute()
        """
            The file won't be changed unless e one of the instances not found
            Or the file itself was not found.
            Then it will renew them and double check.
            We do not have high frequency changes in Solr Vms
            So file should be fine to live for longer period.
        """
        if 'items' in result:
           with open(solrvms,'a+') as solr:
               for instance in result['items']:

                   if 'solr-'+project in instance['name']:
                       solr.write("{'"+instance['name']+"':"
                                  +str(instance['id'])+"}\n")


def getId(vm):

    if  os.path.isfile(solrvms) and os.stat(solrvms).st_size > 0:

        # The loop here because we're looping over strings.
        # Then onverting them to dictionaries.

        for line in open(solrvms,'r').readlines():

            if ast.literal_eval(line).has_key(vm):
                return str(ast.literal_eval(line)[vm])
    else:
        logging.fatal("{} VM does not exist or File is empty".format(
        datetime.now()))

        sys.exit(3)



def getHost():

    host = None

    if not os.path.isfile(solrvms):
        getInstances() #regenerate VMs file

    elif os.stat(solrvms).st_size == 0:
        count = 0
        # Belwo will exectue only if file exits but  empty
        # It will try 3 times before failing.
        # It is very rare case but may happen due to human error!.

        while os.stat(solrvms).st_size <= 0 and count < 3:
            getInstances()
            count+=1
            if os.stat(solrvms).st_size <= 0 and count >= 3:
                logging.fatal("{} VM hosts are not found after 3 retrys."
                .format(datetime.now()))
                sys.exit(3)

    # We should shuffel those VMs and not keep hitting same VMs for each request
    # In such case we make sure, we're not opening many threads on same VMs.
    # we're not building up into the heap of this VMs.
    # behave as ZKclient shuffel  instances randomly to load balance connections

    hosts = [host.strip('\n\r') for host in open(solrvms,'r').readlines() ]
    vmindex = random.randint(1, len(hosts)-1)

    # We're sure only one key exists.
    host = str(ast.literal_eval(hosts[vmindex]).keys()[0])+".c.my-dummy-project.internal"

    if verfiyHost(host):
        return host


    return None

def getStatus():

    status  = {}
    host = getHost()

    if host:
        status = getDoc(host)
    else:
        logging.fatal("{} Host value is None".format(
        datetime.now()))
        sys.exit(4)

    return status




