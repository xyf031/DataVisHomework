# -*- coding: utf-8 -*-
# __author__ = 'XYF 2014210871'

import matplotlib.pyplot as pl
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


def DrawTaiwanJapan(landShape, landParts, flag, mypl, linewid, fillc='g'):
    # Calculate the coordinates
    aziX, aziY, sinX, sinY, merX, merY = [], [], [], [], [], []
    if flag == 1:
        aziXY = [Azimuthal(line) for line in landShape]
        aziX = [line[0] for line in aziXY]
        aziY = [line[1] for line in aziXY]

    if flag == 2:
        sinX = [Sinusoidal(line) for line in landShape]
        sinY = [line[1] for line in landShape]

    if flag == 3:
        merX = [line[0] for line in landShape]
        merY = [Mercator(max(line[1], -85)) for line in landShape]  # For Mercator Method, draw between 85 N and 85 S

    # The Region
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
    for i in range(0, len(landParts) - 1):
        mypl.plot(xPlot[landParts[i]:(landParts[i+1]-1)], yPlot[landParts[i]:(landParts[i+1]-1)],
                  '-', color=fillc, linewidth=linewid[1])
        if landParts[i+1] - landParts[i] > 1:
            tmpX = xPlot[landParts[i]:(landParts[i+1]-1)]
            tmpX.extend([xPlot[landParts[i]]])
            tmpY = yPlot[landParts[i]:(landParts[i+1]-1)]
            tmpY.extend([yPlot[landParts[i]]])
            mypl.fill_between(tmpX, tmpY, 0, facecolor=fillc, edgecolor='')

    return mypl


# ----------Read Data----------
# Japan region num = 115
# Taiwan num = 231
tmp2 = ['115', '231']
regionShape = []
regionParts = []
regionNum = tmp2
for i in tmp2:
    fRead = open('/Users/XYF/Documents/PyCharm/DataViHW03/data/regions/' + i + '/landshape.txt')
    tmp1 = [map(float, line.strip('\r\n').split()) for line in fRead.readlines()]
    fRead.close()
    regionShape.append(tmp1)
    fRead = open('/Users/XYF/Documents/PyCharm/DataViHW03/data/regions/' + i + '/landparts.txt')
    tmp3 = [int(line) for line in fRead.readlines()]
    fRead.close()
    tmp3.append(len(tmp1))
    regionParts.append(tmp3)

# ----------Draw Regions----------
mypl = pl.subplot(111)
pl.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0, hspace=0)
mypl.spines['right'].set_color('none')
mypl.spines['top'].set_color('none')
mypl.spines['left'].set_color('none')
mypl.spines['bottom'].set_color('none')
mypl.set_xticks([])
mypl.set_yticks([])
Flag = 3

fillC = ['#00FF00', '#FF0000']
for i in range(0, len(regionParts)):
    mypl = DrawTaiwanJapan(regionShape[i], regionParts[i], Flag, mypl, [0.1, 0.15], fillc=fillC[i])

# ----------Save Figure----------
print('----------Saving...----------\n')
pl.savefig('Taiwan-Japan-' + str(Flag) + '-300dpi.png', dpi=300, transparent=True)
# pl.show()

