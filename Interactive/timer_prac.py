#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename      : timer_prac.py
# Author        : Yang Leo (JeremyRobturtle@gmail.com)
# Last Modified : 2014-04-16
'''Practice code on 8 - 1
'''
import simplegui
import random

# Global variables
_INTERVAL = 2000
_CANVAS_WID = 500
_CANVAS_HEI = 300
_LOCATION = (0, 0)
msg = "Timer Practice"

# Handlers
def draw(canvas):
    canvas.draw_text(msg, _LOCATION, 36, "Red")

def tick():
    x = random.randrange(0, _CANVAS_WID)
    y = random.randrange(0, _CANVAS_HEI)
    global _LOCATION
    _LOCATION = (x, y)

def update_msg(text):
    global msg
    msg = text

# Frame & Timer
f = simplegui.create_frame("Timer practice", _CANVAS_WID, _CANVAS_HEI)
timer = simplegui.create_timer(_INTERVAL, tick)

# Register event handlers
f.set_draw_handler(draw)
f.add_input("Message", update_msg, 200)

# Start
f.start()
timer.start()
