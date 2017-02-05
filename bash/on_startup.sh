#!/bin/sh
sleep 15
wget --spider www.google.com
if [ "$?" != 0 ]; then
  echo "No internet!"
  sleep 20
fi
cd /home/pi/Desktop/hondetector
source venv/bin/activate
sudo python detect_hon.py