#!/bin/sh
# Script for input PIN code of SIM card(0000 in this case) when rebooting.
# Use this only when you open the PIN lock on your SIM card.
adb shell reboot
sleep 45
adb shell input text 0000
sleep 2
adb shell input keyevent 66

