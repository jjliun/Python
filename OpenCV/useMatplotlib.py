#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Filename      : useMatplotlib.py
# Author        : Yang Leo (JeremyRobturtle@gmail.com)
# Last Modified : 2014-04-03
'''Demo using Matplotlib
'''
import numpy as np
import cv2
from matplotlib import pyplot as plt
img = cv2.imread('lena.jpg', cv2.CV_LOAD_IMAGE_GRAYSCALE)
plt.imshow(img, cmap='gray', interpolation="bicubic")
plt.xticks([]), plt.yticks([])
plt.show()
