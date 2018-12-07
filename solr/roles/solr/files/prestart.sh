#!/bin/bash
. /etc/default/solr.in.sh

if [ ! -f /tmp/ZK ]; then
   ZK=$(curl "http://metadata.google.internal/computeMetadata/v1/instance/attributes/ZK" -H "Metadata-Flavor: Google")
   echo "$ZK:2181" >/tmp/ZK
fi

## Cleaning the PID file incase of suddent crash.
ZK=$(cat /tmp/ZK)
zkurl=$(echo "$ZK"|awk -F ':' '{print $1" "$2}')

zkstatus=$(echo stat|nc $zkurl|grep "Mode:"|awk '{print $2}')
echo $zkstatus
if [ "$zkstatus" != "follower" ] && [ "$zkstatus" != "leader" ]; then

echo "ZK is not in essemble mode"
exit 1
fi

solrp=$(ps auxww | grep start.jar | grep -w $SOLR_PORT | grep -v grep | awk '{print $2}' | sort -r)


if [  -z $(ps auxww | grep start.jar | grep -w $SOLR_PORT | grep -v grep | awk '{print $2}' | sort -r) ] # if no prcess but "$SOLR_PID_DIR/solr-$SOLR_PORT.pid still exists clean it up.
then

    if  [ -f $SOLR_PID_DIR/solr-$SOLR_PORT.pid ]; then
         rm -f "$SOLR_PID_DIR/solr-$SOLR_PORT.pid"
    fi
fi
