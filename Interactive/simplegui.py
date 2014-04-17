#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename      : simplegui.py
# Author        : Yang Leo (JeremyRobturtle@gmail.com)
# Last Modified : 2014-04-16
'''A pseudo module of simplegui, Only interfaces
'''

# Frame
def create_frame(title, canvas_wid, canvas_hei, pane_wid=88):
    print "Frame create frame with cwid=%d chei=%d pwid=%d" % (canvas_wid, canvas_hei, pane_wid)
    return Frame(title, canvas_wid, canvas_hei, pane_wid)

def create_timer(interval, timer_handler):
    """ timer_handler() """
    return Timer(interval, timer_handler)

class Frame(object):
    def __init__(self, title, canvas_wid, canvas_hei, pane_wid=88):
        self.title = title
        self.cwid = canvas_wid
        self.chei = canvas_hei
        self.pwid = pane_wid

    """Registers"""
    def set_canvas_background(self, bg_s):
        print "Frame set canvas background:", bg_s

    def start(self):
        print "Frame started"

    def set_draw_handler(self, handler):
        print "Frame set draw handler:", str(handler)

    def add_input(self, text, input_handler, width):
        """ input_handler(text) """
        print "Frame add input box with handler: %s" % (input_handler)

    """Helper functions"""
    def get_canvas_textwidth(self, font_size, font):
        return 88 # Just a magic number

# Canvas
class Canvas(object):
    def draw_text(self, text, location, font_size, font_color, font="Time Rome"):
        print "Draw text: %s at (%d, %d)" % (text, location)

    def draw_line(self, point1, point2, line_width, line_color):
        print "Draw line: %s -> %s" % (str(point1), str(point2))

    def draw_polygon(point_list, line_width, line_color, fill_color=None):
        print "Draw polygon", point_list

    def draw_circle(self, center_point, radius, line_width, line_color, fill_color=None):
        print "Draw circle: O%s R%s" % (str(center_point), str(radius))

# Timer
class Timer(object):
    def __init__(self, interval, timer_handler):
        self.interval      = interval
        self.timer_handler = timer_handler

    def start(self):
        print "Timer started with handler: %s" % str(timer_handler)
