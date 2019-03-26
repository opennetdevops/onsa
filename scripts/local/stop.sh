#!/bin/bash
pkill -f manage.py
pkill -f rails
pkill -f puma
killall node
pkill -f app.py
