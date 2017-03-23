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


def DrawRegion(landShape, landParts, flag, mypl, c, linewid, name='', fill=False, fillc='g'):
    # flag = 1/2/3/4

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

    # The shores
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
            mypl.plot(xPlot[landParts[i]:(landParts[i+1]-1)], yPlot[landParts[i]:(landParts[i+1]-1)],
                      'k-', linewidth=linewid)
            print(str(i) + ':\t' + str(landParts[i]))
    print('----------myDrawLine\n')

    # Return the map
    if len(name) > 0:
        mypl.text(np.mean(xPlot), np.mean(yPlot), name, fontsize=2, color='0.6',
                  horizontalalignment='center', verticalalignment='center')

    return mypl


def DrawLongLat(flag, c, linewid, mypl, jumpLati=15, jumpLong=30):

    # The basic longitudes and latitudes
    lati = range(-90, 105, jumpLati)
    longi = range(-180, 195, jumpLong)
    latiS = range(-90, 91, 1)
    longiS = range(-180, 181, 1)

    if flag == 1:
        for i in lati:
            tmp1 = [Azimuthal([line, i]) for line in longiS]
            tmp2 = [line[0] for line in tmp1]
            tmp3 = [line[1] for line in tmp1]
            if i == 0:
                mypl.plot(tmp2, tmp3, '--', color=c[0], linewidth=3*linewid[0])
            else:
                if i == 90 or i == -90:
                    mypl.plot(tmp2, tmp3, '-', color='k')  # linewidth=linewid[0]
                else:
                    mypl.plot(tmp2, tmp3, '--', color=c[0], linewidth=linewid[0])
        for i in longi:
            tmp1 = [Azimuthal([i, line]) for line in latiS]
            tmp2 = [line[0] for line in tmp1]
            tmp3 = [line[1] for line in tmp1]
            if i == 0:
                mypl.plot(tmp2, tmp3, '--', color=c[0], linewidth=3*linewid[0])
            else:
                mypl.plot(tmp2, tmp3, '--', color=c[0], linewidth=linewid[0])
    else:
        if flag == 2:
            for i in lati:
                tmp1 = [Sinusoidal([line, i]) for line in longiS]
                if i == 0:
                    mypl.plot(tmp1, [i] * len(tmp1), '--', color=c[0], linewidth=2*linewid[0])
                else:
                    mypl.plot(tmp1, [i] * len(tmp1), '--', color=c[0], linewidth=linewid[0])
            for i in longi:
                tmp1 = [Sinusoidal([i, line]) for line in latiS]
                if i == 0:
                    mypl.plot(tmp1, latiS, '--', color=c[0], linewidth=3*linewid[0])
                else:
                    if i == 180 or i == -180:
                        mypl.plot(tmp1, latiS, 'k-') # , color=c[0], linewidth=linewid[0]
                    else:
                        mypl.plot(tmp1, latiS, '--', color=c[0], linewidth=linewid[0])
        else:
            for i in lati:
                # tmp1 = [Azimuthal([line, i]) for line in longiS]
                tmp2 = longiS
                tmp3 = [Mercator(max([i, -85]))] * len(tmp2)
                if i == 0:
                    mypl.plot(tmp2, tmp3, '--', color=c[0], linewidth=3*linewid[0])
                else:
                    mypl.plot(tmp2, tmp3, '--', color=c[0], linewidth=linewid[0])

            for i in longi:
                tmp1 = [Mercator(min([max([line, -85]), 85])) for line in latiS]
                if i == 0:
                    mypl.plot([i]*len(latiS), tmp1, '--', color=c[0], linewidth=3*linewid[0])
                else:
                    mypl.plot([i]*len(latiS), tmp1, '--', color=c[0], linewidth=linewid[0])

    # The frame of the whole map
    if flag == 3:
        tmp1 = [-181, 181, 181, -181, -181]
        tmp2 = [85, 85, -85, -85, 85]
        tmp3 = map(Mercator, tmp2)
        mypl.plot(tmp1, tmp3, 'k-')

    return mypl