#!/usr/bin/
#PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
# script
# Optionally set PYTHONPATH
#export PYTHONPATH=/path/to/python/libraries:$PYTHONPATH
#ps -ef | grep python | grep -v grep | awk '{print $2}' | xargs kill

PID=`ps -eaf | grep python | grep -v grep | awk '{print $2}'`
if [[ "" !=  "$PID" ]]; then
echo "killing $PID"
kill -9 $PID
fi

sleep 1s # Waits 5 seconds.

#sudo python python_projects/pms3003-g3/iot-monitor-dht.py &

nohup python /home/pi/python_projects/pms3003-g3/iot-monitor-dht.py > /home/pi/log.out 2>&1 &
