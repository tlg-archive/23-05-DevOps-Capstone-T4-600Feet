#!/bin/bash

# Start the VNC server
x11vnc -forever -usepw -create &

# Start the Python application
python main.py
