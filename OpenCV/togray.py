#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename      : toGrey.py
# Author        : Yang Leo (JeremyRobturtle@gmail.com)
# Last Modified : 2014-04-03
'''Show a image in grey scale
press 'Esc' to quit
press 's' to save grey image
'''
import numpy as np
import cv2
img = cv2.imread('lena.jpg', cv2.CV_LOAD_IMAGE_GRAYSCALE)
cv2.imshow('gray image', img)
k = cv2.waitKey(0)
if k is 27: # Esc key
    cv2.destroyAllWindows()
elif k is ord('s'):
    cv2.imwrite('lenagray.jpg', img)
    cv2.destroyAllWindows()
