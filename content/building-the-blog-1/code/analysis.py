#! /usr/bin/python3

import codecs
from datetime import datetime, timedelta

from scipy.stats import pearsonr
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import matplotlib.style as style
import math
import numpy as np
import cartopy.crs as ccrs


def eqlen(arr1, arr2):
    """
    Function that compares the len of 2 arrays and cut the largest to
    the len of the smallest
    """
    if len(arr1) > len(arr2):
        arr21 = [x for i, x in enumerate(arr1) if i < len(arr2)]
        arr22 = arr2
    elif len(arr1) < len(arr2):
        arr21 = arr1
        arr22 = [x for i, x in enumerate(arr2) if i < len(arr1)]
    else:
        arr21 = arr1
        arr22 = arr2
        print("the two arrays have the same value!")
    return arr21, arr22


# load sismic data
post_path = "/home/vicente/desarrollo/vicenteyanez-webpage/content/weather-earthquakes/code/"
eqfile = "{}ANSS_Andes.xyz".format(post_path)
eqdate = np.loadtxt(eqfile, usecols=[0], skiprows=2, dtype=datetime,
                    converters={0: lambda s: datetime.strptime(s.decode('utf-8'), '%Y/%m/%d')})
eqlat = np.loadtxt(eqfile, usecols=[2], skiprows=2)
eqlon = np.loadtxt(eqfile, usecols=[3], skiprows=2)
eqMw = np.loadtxt(eqfile, usecols=[5], skiprows=2,
                  converters={5: lambda s: 0. if s == b'Unk' else s})

# load the weather data
results = "/home/vicente/desarrollo/webscrapping/results_dirmeteo/"
estac_list = "{}estac_list.txt".format(results)
filecp = codecs.open(estac_list, encoding='cp1252')
lat_list = np.loadtxt(filecp, dtype=float, usecols=[3], delimiter=";")
filecp = codecs.open(estac_list, encoding='cp1252')
lon_list = np.loadtxt(filecp, dtype=float, usecols=[4], delimiter=";")
filecp = codecs.open(estac_list, encoding='cp1252')
station_list = np.loadtxt(filecp, dtype='S40', usecols=[0], delimiter=";")

datasave = []
stacoef = []
data = []
station_list = ['Carriel Sur, Concepción.']  # go directly to carriel sur
for i, filename in enumerate(station_list):
    # station_name = filename.decode('cp1252')
    station_name = filename
    station_file = "{}{}.txt".format(results, station_name)

    year = np.loadtxt(station_file, usecols=[0], delimiter=";")
    day = np.loadtxt(station_file, usecols=[1], delimiter=";")
    tdate = [datetime(year=int(year[i]), month=1, day=1) +
             timedelta(days=int(day[i])) for i, y in enumerate(year)]
    mean = np.loadtxt(station_file, usecols=[2], delimiter=";",
                      converters={2: lambda s:
                                  float('nan') if s == b'.' else s})
    tmin = np.loadtxt(station_file, usecols=[3], delimiter=";",
                      converters={3: lambda s:
                                  float('nan') if s == b'.' else s})
    tmax = np.loadtxt(station_file, usecols=[4], delimiter=";",
                      converters={4: lambda s:
                                  float('nan') if s == b'.' else s})

    # number of earthquakes for day
    eq4day = []
    initial_date = datetime(year=2005, month=1, day=1)
    allthetime = [initial_date + timedelta(days=i) for i in range(0, 3514)]
    for dat in allthetime:
        eqindat = [eq for u, eq in enumerate(eqdate) if eq == dat and
                   eqlat[u] > lat_list[i]-2 and eqlat[u] < lat_list[i]+2 and
                   eqlon[u] > lon_list[i]-2 and eqlon[u] < lon_list[i]+2]
        eq4day.append(float(len(eqindat)))  # of earthquakes in the date 'dat'

    # calculate pearsonr correlation coeficient for the i-station
    coef1, coef2 = eqlen(eq4day, mean)
    coef1 = [x for i, x in enumerate(coef1) if not math.isnan(coef2[i])]
    coef2 = [x for i, x in enumerate(coef2) if not math.isnan(coef2[i])]
    ccoef = pearsonr(coef1, coef2)

    # save the data
    data.append([lat_list[i], lon_list[i], ccoef[0]])
    datasave.append([station_name, lat_list[i], lon_list[i], ccoef[0]])
    pathfile = "{}corr_coef.txt".format(post_path)
    # np.savetxt(pathfile, datasave, fmt='%s', delimiter=';')
    print("calculation for the station {}.- {} finished".format(i,
                                                                station_name))

    # plot temperatus vs Mw in Concepcion
    if station_name == 'Carriel Sur, Concepción.':
        style.use('fivethirtyeight')

        fig, (ax1, ax2) = plt.subplots(2, sharex=True)

        # x axes with datetime values!!!
        ax1.set_xlim(datetime(2005, 1, 1), datetime(2015, 1, 1))
        ax2.set_xlim(datetime(2005, 1, 1), datetime(2015, 1, 1))

        # ax1.set_yticks(range(0, 140, 20))
        ax2.set_yticks(range(0, 20, 5))
        # ax2.set_xticks([datetime(d, 1, 1) for d in range(2005, 2016, 1)])

        ax1.tick_params(labelsize=9)
        ax2.tick_params(labelsize=9)

        ax1.set_ylabel('número de sismos', size=10)
        ax2.set_ylabel('º celcius', size=10)
        ax2.set_xlabel('año', size=10)

        fig.subplots_adjust(hspace=0.01)

        # plot
        ax1.plot(allthetime, eq4day)
        ax2.plot(tdate, mean)

        # zero line
        ax1.axhline(y=0, color='black', linewidth=1.3, alpha=.7)
        ax2.axhline(y=0, color='black', linewidth=1.3, alpha=.7)

        # english title
        eng_title = "No, there is no correlation"
        eng_sub = ""
        # spanish title
        esp_title = "No hay relación entre sismicidad y temperatura"
        esp_sub = "\
El índice de correlación tiene un valor de {:8.6f} (-1=correlación negativa, \
0=sin correlación, 1=correlación positiva)".format(ccoef[0])

        # set text
        ax1.text(x=datetime(2005, 1, 1), y=133, s=esp_title, fontsize=20,
                 weight='bold', alpha=.75)
        ax1.text(x=datetime(2005, 1, 1), y=123, s=esp_sub, fontsize=14,
                 weight='bold', alpha=.75)
        # set that thing of the bottom
        ax2.text(x=datetime(2004, 5, 1), y=-3.4,
                 s='             CC Blind Geologist                                                                                                         Fuente temperaturas: Dirección Metereológica de Chile | Sismicidad: Centro Sismológico de Chile                        ',
                 fontsize=11, color='#f0f0f0', backgroundcolor='grey')
        plt.legend()

"""
# print stadistic values of the earthquakes

print("Mw max: {}".format(eqMw.max()))
print("Mw min: {}".format(eqMw.min()))
plt.figure(3)
plt.hist(eqMw, bins=30)
"""
plt.show()
print("End!")
