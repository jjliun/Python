#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename      : simplegui.py
# Author        : Yang Leo (JeremyRobturtle@gmail.com)
# Last Modified : 2014-04-16
'''A pseudo module of simplegui, Only interfaces
'''

# KEY_MAP
KEY_MAP = dict(zip("abcdefghijklmnopqrstuvwxyz0123456789", range(0, 36)))
KEY_MAP = dict(KEY_MAP.items() + [("left", 88), ("right", 89), ("up", 90), ("down", 91)])

# Frame
def create_frame(title, canvas_wid, canvas_hei, pane_wid=88):
    print "Frame create frame with cwid=%d chei=%d pwid=%d" % (canvas_wid, canvas_hei, pane_wid)
    return Frame(title, canvas_wid, canvas_hei, pane_wid)

def create_timer(interval, timer_handler):
    """ timer_handler() """
    return Timer(interval, timer_handler)

def load_image(url):
    return url

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
        """ draw_handler(canvas) """
        print "Frame set draw handler:", str(handler)

    def set_keydown_handler(self, handler):
        """ keydown_handler(key) """
        print "Frame set keydown handler"

    def set_keyup_handler(self, handler):
        """ keyup_handler(key) """
        print "Frame set keyup handler"

    def set_mouseclick_handler(self, mouse_handler):
        """ mouse_handler(position) -- position = [x, y] """
        print "Frame set mouse handler"

    def add_input(self, text, input_handler, width):
        """ input_handler(text) """
        print "Frame add input box with handler: %s" % (input_handler)

    def add_button(self, text, button_handler, width=88):
        """ button_handler() """
        print "Frame add button: %s" % text

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

    def draw_image(self, image, center_src, size_src, center_dst, size_dst, rotation=0):
        print "Draw image {} at {} with size {} of source to {} with size {}".format(image, center_src, center_dst, center_dst, size_dst)

# Timer
class Timer(object):
    def __init__(self, interval, timer_handler):
        self.interval      = interval
        self.timer_handler = timer_handler

    def start(self):
        print "Timer started with handler: %s" % str(timer_handler)
