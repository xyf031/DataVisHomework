# -*- coding: utf-8 -*-
# __author__ = 'XYF 2014210871'

import numpy as np


def Azimuthal(data):
    # Azimuthal equidistant projection
    # The center point is the north pole
    # return [x, y]
    longitude = data[0] * np.pi / 180
    latitude = data[1] * np.pi / 180
    rou = np.pi / 2 - latitude
    thi = longitude
    return [rou * np.sin(thi), -1 * rou * np.cos(thi)]


def Sinusoidal(data):
    # Sinusoidal projection
    # return x
    longitude = data[0] * np.pi / 180
    latitude = data[1] * np.pi / 180
    return longitude * np.cos(latitude)


def Mercator(latitude):
    # Mercator Projection
    # return y
    return np.log(np.tan(np.pi * latitude / 360 + np.pi / 4))


def DrawCity(cityPoint, citySize, flag, mypl, c='r'):

    # Calculate the coordinates
    aziX, aziY, sinX, sinY, merX, merY = [], [], [], [], [], []
    if flag == 1:
        aziXY = [Azimuthal(line) for line in cityPoint]
        aziX = [line[0] for line in aziXY]
        aziY = [line[1] for line in aziXY]

    if flag == 2:
        sinX = [Sinusoidal(line) for line in cityPoint]
        sinY = [line[1] for line in cityPoint]

    if flag == 3:
        merX = [line[0] for line in cityPoint]
        merY = [Mercator(max(line[1], -85)) for line in cityPoint]  # For Mercator Method, draw between 85 N and 85 S

    # The Points
    xPlot = []
    yPlot = []
    if flag == 1:
        xPlot = aziX
        yPlot = aziY
    else:
        if flag == 2:
            xPlot = sinX
            yPlot = sinY
        else:
            xPlot = merX
            yPlot = merY
            mypl.axis([-200, 200, Mercator(-86), Mercator(86)])

    for i in range(0, len(citySize)):
        if citySize[i] > 5000000:
            mypl.plot(xPlot[i], yPlot[i], '.', color=c, alpha=0.5, markersize=10*citySize[i]/5000000)
            mypl.plot(xPlot[i], yPlot[i], 'w.', alpha=0.95, markersize=1)

    # Return the map
    print('----------myDrawPoint\n')
    return mypl
