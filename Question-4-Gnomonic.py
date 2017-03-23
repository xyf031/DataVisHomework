# -*- coding: utf-8 -*-
# __author__ = 'XYF 2014210871'

import os
import numpy as np
import matplotlib.pyplot as pl
import myDrawGnomonic


# ----------Read Data----------
fRead = open('/Users/XYF/Documents/PyCharm/DataViHW03/data/regions.txt')
tmp1 = [line.split('|') for line in fRead.readlines()]
fRead.close()
regionNames = [line[0] for line in tmp1]
regionLevel = [int(line[1]) for line in tmp1]

tmp1 = os.popen('ls /Users/XYF/Documents/PyCharm/DataViHW03/data/regions')
tmp2 = tmp1.read().split()
tmp1.close()
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
backColor = '#111032'
fillC = ['#0099ff', '#0087ff', '#0075ff', '#0064eb', '#0054d7', '#0045c3', '#0036af']  # 1 highest, 7 lowest.
airLineColor = 'r'
beijingColor = 'w'
Dpi = 300

mypl = pl.subplot(111, axisbg=backColor)
pl.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0, hspace=0)
mypl.spines['right'].set_color('none')
mypl.spines['top'].set_color('none')
mypl.spines['left'].set_color('none')
mypl.spines['bottom'].set_color('none')
mypl.set_xticks([])
mypl.set_yticks([])

for i in range(0, len(regionParts)):
    print('*****Region: ' + str(i) + ' *****')
    mypl = myDrawGnomonic.DrawRegion(regionShape[i], regionParts[i], mypl, 0.15, fill=True, fillc=fillC[regionLevel[i]-1])


# ----------Draw AirLine----------
def getXYZ(point):
    longi = np.pi * point[0] / 180
    lati = np.pi * point[1] / 180
    x = np.cos(lati) * np.cos(longi)
    y = np.cos(lati) * np.sin(longi)
    z = np.sin(lati)
    return [x, y, z]


def getLL(xyz):
    lati = np.arcsin(xyz[2]) * 180 / np.pi
    x = xyz[0]
    y = xyz[1]
    if x == 0:
        if y >= 0:
            longi = 90
        else:
            longi = -90
    else:
        if x > 0:
            longi = np.arctan(y / x) * 180 / np.pi
        else:
            if y >= 0:
                longi = np.arctan(y / x) * 180 / np.pi + 180
            else:
                longi = np.arctan(y / x) * 180 / np.pi - 180
    return [longi, lati]


begin = [116.55, 40.5]  # Beijing's longitude and altitude
end = [-118.25, 34.05]  # Los Angeles' longitude and altitude
p1 = getXYZ(begin)
p2 = getXYZ(end)

A = (p1[1]*p2[2] - p2[1]*p1[2]) / (p1[0]*p2[1] - p2[0]*p1[1])
B = (p2[0]*p1[2] - p1[0]*p2[2]) / (p1[0]*p2[1] - p2[0]*p1[1])

squareSum = A*A + B*B
zRange0 = squareSum / (squareSum + 1)
zRange1 = np.linspace(1, -1, 2000, endpoint=True)

xRange = []
yRange = []
zRange = []
tmpX = []
tmpY = []
tmpZ = []
for i in zRange1:
    if squareSum-i*i*(squareSum+1) >= 0:
        delta = A*np.sqrt(squareSum-i*i*(squareSum+1))
        y1 = (delta - B*i) / squareSum
        y2 = (-delta - B*i) / squareSum
        x1 = -(B*y1 + i) / A
        x2 = -(B*y2 + i) / A
        yRange.append(y1)
        xRange.append(x1)
        zRange.append(i)
        tmpY.append(y2)
        tmpX.append(x2)
        tmpZ.append(i)

airLineXYZ = []
airLine = []
tmp0 = len(tmpY)
for i in range(0, tmp0):
    yRange.append(tmpY[tmp0-1 - i])
    xRange.append(tmpX[tmp0-1 - i])
    zRange.append(tmpZ[tmp0-1 - i])
for i in range(0, len(xRange)):
    airLineXYZ.append([xRange[i], yRange[i], zRange[i]])
    airLine.append(getLL(airLineXYZ[i]))

airLine.append(airLine[0])
mypl = myDrawGnomonic.DrawMapPoint3(airLine, mypl, c=airLineColor, linewid=1)
mypl = myDrawGnomonic.DrawMapPoint3([begin, end], mypl, size=8, c=beijingColor, type='.')

# ----------Save Figure----------
print('\n\n----------Saving...----------\n')
pl.savefig('WorldMap-Gnomonic-' + str(Dpi) + 'dpi.png', dpi=Dpi)
# pl.show()


