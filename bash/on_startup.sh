#!/bin/sh
sleep 15
wget --spider www.google.com
if [ "$?" != 0 ]; then
  echo "No internet!"
  sleep 20
fi
sudo python /home/pi/Desktop/detect_hon.py