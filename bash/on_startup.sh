#!/bin/sh
sleep 15
# setup wifi -- initial command is `wpa_passphrase Your_SSID Your_passwd`
ip link set wlan0 down
ip link set wlan0 up
wpa_supplicant -B -iwlan0 -c/etc/wpa_supplicant.conf -Dwext
sudo dhclient wlan0
# check if we have internet
wget --spider www.google.com
if [ "$?" != 0 ]; then
  echo "No internet!"
  sleep 20
fi
cd /home/pi/Desktop/hondetector
source venv/bin/activate
sudo python detect_hon.py
