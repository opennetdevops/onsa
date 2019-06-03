#!/bin/bash
pkill -f manage.py
pkill -f rails
pkill -f puma
killall node
#pkill -f app.py
kill -9 `netstat -ntap | grep 3001 | awk '{print $7}' | cut -d'/' -f1`

kill -9 `netstat -ntap | grep 3001 | awk '{print $7}' | cut -d'/' -f1`

