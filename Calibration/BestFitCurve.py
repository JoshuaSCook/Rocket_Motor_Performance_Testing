# -*- coding: utf-8 -*-
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib import rc

#### Data
data = np.genfromtxt('FSR_calibration_data.csv', dtype=None, names=True, delimiter =",")

x = []
y = []
for row in data:
    x.append(round(row[1], 2))
    y.append(round(row[0], 2))

################################################################
#### Best fit line
sum_x = 0
for value in x:
    sum_x += value

sum_y = 0
for value in y:
    sum_y += value

sum_xy = 0
for valueA in x:
    for valueB in y:
        if x.index(valueA) == y.index(valueB):
            sum_xy += (valueA * valueB)

sum_xx = 0
for value in x:
    sum_xx += (value * value)

#### Calculate the slope
n = 17
m = (sum_xy - ((sum_x) * (sum_y) / n)) / (sum_xx - ((sum_x ** 2) / n))

#### Calculate the y-intercept
mean_x = sum_x / n
mean_y = sum_y / n

b = mean_y - (m * mean_x)

print "Slope:", m
print "y-Intercept:", b

x_line = np.linspace(0, 100)

################################################################
# Initiation
matplotlib.rcParams['axes.unicode_minus'] = False
fig = plt.figure()
ax = fig.add_subplot(111)

# Add the points to the plot
ax.plot(x, y, 'ro--', markersize=12, markeredgecolor='none')
ax.plot(x_line ,(m * x_line) + b, '#CCCCCC')

# Labels and Axes
ax.set_title('Best Fit', fontsize='30')
ax.set_xlabel('FSR Reading', fontsize='20')
ax.set_ylabel('Actual Weight (g)', fontsize='20')
ax.set_xlim(0, 50)
ax.set_ylim(0, 100)
matplotlib.rc('xtick', labelsize=16)
matplotlib.rc('ytick', labelsize=16)
plt.tight_layout()

# Open Plot in Pyplot
plt.show()
