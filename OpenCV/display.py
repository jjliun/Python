#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename      : display.py
# Author        : Yang Leo (JeremyRobturtle@gmail.com)
# Last Modified : 2014-04-03
'''Display a image, press any key to quit
'''
import numpy as np
import cv2
img = cv2.imread('lena.jpg')
cv2.imshow('window', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
