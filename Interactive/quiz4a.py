#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename      : quiz4a.py
# Author        : Yang Leo (JeremyRobturtle@gmail.com)
# Last Modified : 2014-04-27
'''Check for overlap
'''
import simplegui

pt = [10, 20]
delta = [3, 0.7]

def draw(canvas):
    canvas.draw_polygon([(50,50), (180,50), (180,140), (50,140)], 1, "White")
    canvas.draw_point(pt, "Red")

def update_pos():
    global pt
    pt = map(sum, zip(pt, delta))

f = simplegui.create_frame("Test overlap", 300, 300)
f.add_button("Go", update_pos)
f.set_draw_handler(draw)

f.start()
