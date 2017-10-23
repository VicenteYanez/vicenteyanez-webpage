#! /usr/bin/python3

import calendar
from datetime import date, datetime, timedelta
import requests
import re
import time
import os

import numpy as np
from bs4 import BeautifulSoup


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12)
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])

    return date(year, month, day)


def toYearFraction(date):
    def sinceEpoch(date):  # returns seconds since epoch
        return time.mktime(date.timetuple())
    s = sinceEpoch

    year = date.year
    startOfThisYear = datetime(year=year, month=1, day=1)
    startOfNextYear = datetime(year=year+1, month=1, day=1)

    yearElapsed = s(date) - s(startOfThisYear)
    yearDuration = s(startOfNextYear) - s(startOfThisYear)
    fraction = yearElapsed/yearDuration

    return date.year + fraction


session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/2010\
0101 Firefox/54.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,\
image/webp,*/*;q=0.8"}
# configuring the saving directory
thisfile = os.path.dirname(os.path.abspath(__file__))
pathdata = "{}/results_dirmeteo/".format(thisfile)
pathfile = "{}/estac_list.txt".format(pathdata)
if not os.path.isdir(pathdata):
    os.mkdir(pathdata)

# load station info
url = 'http://164.77.222.61/climatologia/php/menuProductos.php#'
html = session.get(url, headers=headers)

# making the soup
soup = BeautifulSoup(html.text, "html.parser")
stalist = soup.findAll('div', {'class': 'flotante'})

# searching the data
station = []
ide = []
height = []
latitude = []
longitude = []
for tag in stalist:
    station.append(tag.find('td', {'colspan': '2'}).get_text())
    ide.append(tag['id'])
    height.append(tag.find('table').findAll('tr')[1].findAll('td')[1].get_text())
    latitude.append(tag.find('table').findAll('tr')[2].findAll('td')[1].get_text())
    longitude.append(tag.find('table').findAll('tr')[3].findAll('td')[1].get_text())

# cleaning the data
patron = r'\s*(.*[^\s{2,}])\s+'
station2 = [re.search(patron, line).group(1) for line in station]

patron2 = r'(\d+)\s+Metros.'
height2 = [float(re.search(patron2, line).group(1)) for line in height]

patron3 = r'([-*]\d+.\d+)\s+Grados.'
latitude2 = [float(re.search(patron3, line).group(1)) for line in latitude]
longitude2 = [float(re.search(patron3, line).group(1)) for line in longitude]

datasaved = np.array([station2, ide, height2, latitude2, longitude2]).T
np.savetxt(pathfile, datasaved, fmt='%s', delimiter=';')

print("It finished the station list download \n")

# cicle for take the data of each station for every date available
error_info = []
for i, sta in enumerate(station2):
    staid = ide[i]
    baseurl = "http://164.77.222.61/climatologia/php/temperaturaMensual.php"
    file_station_i = "{}/{}.txt".format(pathdata, sta)

    # check if the file exist, if it exist pass to the next station
    if os.path.isfile(file_station_i):
        continue
    # Interval
    dat = date(2005, 1, 1)  # initial date
    dat_f = date(2015, 1, 1)  # final date

    # variable to save the data
    year = []
    dia = []
    minima = []
    maxima = []
    media = []

    stop_values = ['Promedio Mensual', 'Absoluta Mensual']
    while dat < dat_f:
        dat = dat.replace(day=1)  # restart in case of miss handle exception
        newurl = "{}?IdEstacion={}&FechaIni={}".format(baseurl, staid, dat)
        print("Ok, I'm doing {}".format(newurl))
        # load the data
        try:
            # making the soup
            html_i = session.get(newurl, headers=headers)
            soup_i = BeautifulSoup(html_i.text, "html.parser")
            # remember: if findAll can't find anything returns a empty list
            # if find() can't find anything returns a None object
            trlist = soup_i.findAll('tr', {'class': 'detalle02'})
            # if there is no data: break it!!
            if trlist is None or not trlist:
                print("no data in {} on date {}".format(sta, dat))
                dat = add_months(dat, 1)
                continue
            for tr in trlist:
                try:
                    arethere = (tr.findAll('td')[1].get_text() or
                                tr.findAll('td')[2].get_text() or
                                tr.findAll('td')[4].get_text())
                    thatsnotapoint = (tr.findAll('td')[1].get_text() != '.' or
                                      tr.findAll('td')[2].get_text() != '.' or
                                      tr.findAll('td')[4].get_text() != '.')
                    # break if you reach the final of the table
                    if tr.findAll('td')[0].get_text() in stop_values:
                        break
                    # if there is data save it
                    elif arethere and thatsnotapoint:
                        year.append(dat.year)
                        dia.append(dat.timetuple().tm_yday)
                        media.append(tr.findAll('td')[1].get_text())
                        minima.append(tr.findAll('td')[2].get_text())
                        maxima.append(tr.findAll('td')[4].get_text())
                        dat = dat + timedelta(days=1)
                    # pass if there is no more data
                    else:
                        dat = dat + timedelta(days=1)

                except(AttributeError) as e:
                    print("Exception is :", e)
                    error_info.append([sta, dat])
        except(ConnectionError) as e:
            print("Exception is :", e)
            error_info.append([sta, dat])

        # End of the date loop
        print("Hold on a sec, I am taking a little nap....zzzzz.")
        time.sleep(10)

    # saving all the data from the station i
    data_station_i = np.array([year, dia, media, minima, maxima]).T
    np.savetxt(file_station_i, data_station_i, fmt='%s', delimiter=';')

    print("Download of the station {} finished\n".format(sta))

# saving error logs
errorfile = "{}/errors.txt".format(pathdata)
np.savetxt(errorfile, error_info, fmt='%s', delimiter=';')

print("###############################################/n Scrapping complete!")
