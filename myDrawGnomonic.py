# -*- coding: utf-8 -*-
# __author__ = 'XYF 2014210871'

import numpy as np


def Gnomonic(point, longiCenter=0, latiCenter=90):
    # Gnomonic projection
    # return [x, y]
    tmp0 = min(180, max(-180, point[0]))
    tmp1 = min(90, max(35, point[1]))
    longitude = tmp0 * np.pi / 180
    latitude = tmp1 * np.pi / 180
    cosC = np.sin(latiCenter)*np.sin(latitude) + np.cos(latiCenter)*np.cos(longitude-longiCenter)*np.cos(latitude)
    x = np.cos(latitude) * np.sin(longitude-longiCenter) / cosC
    y = (np.cos(latiCenter)*np.sin(latitude)-np.sin(latiCenter)*np.cos(longitude-longiCenter)*np.cos(latitude)) / cosC

    return [x, y]


def DrawRegion(landShape, landParts, mypl, linewid, fill=False, fillc='g'):
    # Calculate the coordinates
    gnoXY = [Gnomonic(line, latiCenter=90) for line in landShape]
    gnoX = [line[0] for line in gnoXY]
    gnoY = [line[1] for line in gnoXY]

    # The Regions
    xPlot = gnoX
    yPlot = gnoY
    if fill:
        for i in range(0, len(landParts) - 1):
            mypl.plot(xPlot[landParts[i]:(landParts[i+1]-1)], yPlot[landParts[i]:(landParts[i+1]-1)],
                      'k-', linewidth=linewid)
            if landParts[i+1] - landParts[i] > 1:
                tmpX = xPlot[landParts[i]:(landParts[i+1]-1)]
                tmpX.extend([xPlot[landParts[i]]])
                tmpY = yPlot[landParts[i]:(landParts[i+1]-1)]
                tmpY.extend([yPlot[landParts[i]]])
                mypl.fill_between(tmpX, tmpY, 0, facecolor=fillc, edgecolor='')
            print(str(i) + ':\t' + str(landParts[i]))
    else:
        for i in range(0, len(landParts) - 1):
            mypl.plot(xPlot[landParts[i]:(landParts[i+1]-1)], yPlot[landParts[i]:(landParts[i+1]-1)], 'k-', linewidth=linewid)
            print(str(i) + ':\t' + str(landParts[i]))
    print('----------myDrawLine-Gnomonic\n')

    # Return the map
    return mypl


def DrawMapPoint3(cityPoint, mypl, size=2, c='r', type='-', linewid=1):

    # Calculate the coordinates
    gnoXY = [Gnomonic(line, latiCenter=90) for line in cityPoint]
    gnoX = [line[0] for line in gnoXY]
    gnoY = [line[1] for line in gnoXY]

    # The Points
    xPlot = gnoX
    yPlot = gnoY

    mypl.plot(xPlot, yPlot, type, color=c, markersize=size, linewidth=linewid)
    print('----------myDrawPoint3\n')
    return mypl
