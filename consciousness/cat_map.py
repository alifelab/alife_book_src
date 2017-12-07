#!/usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.ndimage import imread


img_array = imread(sys.argv[1])
x_size = img_array.shape[1]
y_size = img_array.shape[0]
x, y = np.meshgrid(range(x_size), range(y_size))
x_map = (2*x + y) % x_size
y_map = (x + y) % y_size

fig = plt.figure()
img = plt.imshow(img_array, cmap=plt.cm.gray)

def update(frame):
    if frame == 0:
        return
    global img_array
    img_array = img_array[y_map, x_map]
    img.set_array(img_array)
    img.axes.set_title(frame)

anim = animation.FuncAnimation(fig, update, interval = 100)
plt.show(anim)
