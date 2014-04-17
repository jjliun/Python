#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename      : project3.py
# Author        : Yang Leo (JeremyRobturtle@gmail.com)
# Last Modified : 2014-04-17
'''Game: Stop Watch'''
import simplegui
# define global variables
_TIME_10TH_SEC = 0
SCORE = 0
TRIES = 0
# flags
_TIMER_STOPPED = True

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(time_10th_sec):
    time_sec = time_10th_sec / 10
    digit_10th_sec = time_10th_sec % 10
    time_min = time_sec / 60
    digits_sec = time_sec % 60
    return "%d:%02d.%d" % (time_min, digits_sec, digit_10th_sec)

# define event handlers for buttons; "Start", "Stop", "Reset"
def timer_start():
    global _TIMER_STOPPED
    if not _TIMER_STOPPED: return

    _TIMER_STOPPED = False
    timer.start()

def timer_stop():
    global _TIMER_STOPPED
    if _TIMER_STOPPED: return

    _TIMER_STOPPED = True
    timer.stop()

    digit_10th_sec = _TIME_10TH_SEC % 10
    if digit_10th_sec == 0:
        global SCORE
        SCORE = SCORE + 1

    global TRIES
    TRIES = TRIES + 1

def timer_reset():
    timer.stop()
    global _TIME_10TH_SEC, SCORE, TRIES, _TIMER_STOPPED
    _TIME_10TH_SEC = SCORE = TRIES = 0
    _TIMER_STOPPED = True

# define event handler for timer with 0.1 sec interval
def succ_time():
    global _TIME_10TH_SEC
    _TIME_10TH_SEC = _TIME_10TH_SEC + 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(_TIME_10TH_SEC), (50,95), 40, "Green")
    canvas.draw_text("%d/%d" % (SCORE, TRIES), (150,35), 30, "Green")

# create frame
f = simplegui.create_frame("Stop Watch", 200, 150)
timer = simplegui.create_timer(100, succ_time)

# register event handlers
f.add_button("Start", timer_start)
f.add_button("Stop", timer_stop)
f.add_button("Reset", timer_reset)
f.set_draw_handler(draw)

# start frame
f.start()
