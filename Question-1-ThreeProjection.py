# -*- coding: utf-8 -*-
# __author__ = 'XYF 2014210871'

import os
import matplotlib.pyplot as pl
import myDrawLine
import myDrawCity


# ----------Read Data----------
# fRead = open('/Users/XYF/Documents/PyCharm/DataViHW03/data/landshape.txt')
# landShape = [map(float, line.strip('\r\n').split()) for line in fRead.readlines()]
# fRead.close()
#
# fRead = open('/Users/XYF/Documents/PyCharm/DataViHW03/data/landparts.txt')
# landParts = [int(line) for line in fRead.readlines()]
# fRead.close()
# landParts.append(len(landShape))  # !!!

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

fRead = open('/Users/XYF/Documents/PyCharm/DataViHW03/data/cities.txt')
tmp1 = [line.split('|') for line in fRead.readlines()]
fRead.close()
cityNames = [line[0] for line in tmp1]
cityLevel = [int(line[1]) for line in tmp1]
cityXY = [[float(line[2]), float(line[3])] for line in tmp1]
cityLongi = [line[0] for line in cityXY]
cityLati = [line[1] for line in cityXY]


# ----------Draw Regions----------
# for i in range(0, len(regionParts)):
#     mypl = pl.subplot(111)
#     mypl = myDrawLine.DrawMap(regionShape[i], regionParts[i], 3, mypl, ['0.9'],
#                           [0.1, 0.15], regionNames[i], longAndLati=True, fill=True, fillc='g')
#     print('*****Region: ' + str(i) + ' Finished*****')
#     pl.savefig('regionMapFill/' + regionNum[i] + '-' + regionNames[i] + '-' + str(regionLevel[i]) + '.png', dpi=300)
#     pl.close()

backColor = '#111032'
longiColor = ['0.5']
cityColor = 'w'
# fillC = ['#00d300', '#00be00', '#00ab00', '#009700', '#008400', '#007100', '#005e00']  # 1 highest, 7 lowest.
fillC = ['#0099ff', '#0087ff', '#0075ff', '#0064eb', '#0054d7', '#0045c3', '#0036af']  # 1 highest, 7 lowest.
Flag = 3
Dpi = 300

mypl = pl.subplot(111, axisbg=backColor)
pl.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99, wspace=0, hspace=0)
mypl.spines['right'].set_color('none')
mypl.spines['top'].set_color('none')
mypl.spines['left'].set_color('none')
mypl.spines['bottom'].set_color('none')
mypl.set_xticks([])
mypl.set_yticks([])

# mypl = myDrawLine.DrawLongLat(Flag, longiColor, [0.1, 0.15], mypl, jumpLong=30)
for i in range(0, len(regionParts)):
    print('*****Region: ' + str(i) + ' *****')
    mypl = myDrawLine.DrawRegion(regionShape[i], regionParts[i],
                                 Flag, mypl, ['0.9'], 0.15, fill=True, fillc=fillC[regionLevel[i]-1])

# ----------Draw City----------
mypl = myDrawCity.DrawCity(cityXY, cityLevel, Flag, mypl, c=cityColor)

# ----------Save Figure----------
print('\n\n----------Saving...----------\n')
pl.savefig('WorldMap-' + str(Flag) + '-' + str(Dpi) + 'dpi.png', dpi=Dpi)
# pl.show()