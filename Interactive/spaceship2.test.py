#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename      : spaceship2.test.py
# Author        : Yang Leo (JeremyRobturtle@gmail.com)
# Last Modified : 2014-05-17
'''Test for spaceship2.py
'''
import simplegui
from spaceship2 import Derivatives, Vector2D, ImageInfo, SpriteInfo, Sprite
from spaceship2 import cart_to_polar, polar_to_cart

# test derivatives
d = Derivatives(3, 4, 1)
print d

d.update(-1)
print d

d.update(3)
print d

d.update()
print d

print d[0]

# test Cartesian
p1 = Vector2D(2, 3)
p2 = Vector2D(5, 7)
#p3 = Vector2D() # should raise
#p4 = Vector2D(1, 2, 3) # should raise
print p1, p2

print p1 + p2
print p1.dist(p2)

# test derivatives(Cartesian)
d = Derivatives(Vector2D(0, 0), Vector2D(3, 4), Vector2D(0, 10))
print d

d.update(Vector2D(3, -3))
print d

d.update()
print d

print d[0]

print "test of ImageInfo"
img1 = ImageInfo("http://www.baidu.com/icon.png", [60, 40], animated = True, n_tiled = [2])
print img1.size
print img1.get_center() # tiled 1
print img1.get_center(1) # tiled 2
img1.draw(simplegui.Canvas(), [100, 200], [600, 400], 0, 1)
img1.draw(simplegui.Canvas(), [100, 200], [600, 400], 0, 1)
img1.draw(simplegui.Canvas(), [100, 200], [600, 400], 0, 1)

# test of SpriteInfo
si = SpriteInfo([30, 20], 15, 50, "http://www.baidu.com/sound.mp3")

p = Vector2D(3, 4)
print cart_to_polar(p)
print polar_to_cart(cart_to_polar(p))

pl = cart_to_polar(p)
pl[1] -= 0.9272952180016123
print polar_to_cart(pl)
