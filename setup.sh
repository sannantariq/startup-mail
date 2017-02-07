#!/bin/sh
echo "Setting up..."
echo "Changing permissions..."
chmod +x startup_mailer.py
echo "Overwriting /etc/rc.local..."
cp rc.local /etc/
