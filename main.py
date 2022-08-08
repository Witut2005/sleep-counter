
import csv
import argparse
import os

import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
from pylab import *

Parser = argparse.ArgumentParser()

Parser.add_argument('-file', required=True)
Parser.add_argument('-add', nargs='+', required=False)
Parser.add_argument('-stats', action='store_true', required=False)

Parser.add_argument('-dates', action='store_true', required=False)
Parser.add_argument('-start', action='store_true', required=False)
Parser.add_argument('-end', action='store_true', required=False)
Parser.add_argument('-sleep', action='store_true', required=False)
Parser.add_argument('-delete', required=False)

Arguments = Parser.parse_args()


if Arguments.add is not None:
    if len(Arguments.add) != 3:
        sys.exit('You must specify 3 values (date, hour you went to sleep, hour when you woke up)')

line = 0
buf = None
with open(Arguments.file, 'r') as file:
    buf = file.readlines()
    while True:
        try:
            if buf[line][0:10] == str(Arguments.add[0]):
                sys.exit('You cant specify the same date twice')

        except IndexError:
            break
        line = line + 1

ion()
plt.show(block=True)


Data = []

dates = []
hour_start = []
hour_end = []
total_hours = []

with open(Arguments.file) as CsvFile:
    File = csv.reader(CsvFile, delimiter=',')
    for x in File:
        Data.append(x)


for x in Data:
    dates.append(x[0])
    hour_start.append(dt.datetime(year=1, month=1, day=1, hour=int(x[1][0:2]), minute=int(x[1][3:5]), second=0, microsecond=0))
    hour_end.append(dt.datetime(year=1, month=1, day=1, hour=int(x[2][0:2]), minute=int(x[2][3:5]), second=0, microsecond=0))
    total_hours.append(abs((hour_end[-1] - hour_start[-1]).total_seconds()))

if Arguments.add is not None:
    with open(Arguments.file, 'a') as CsvFile:
        for x in Arguments.add:
            CsvFile.write(str(x) + ',')
        CsvFile.write('\n')

if Arguments.dates:
    for x in dates:
        print(x)

if Arguments.start:
    for x in hour_start:
        print(str(x.hour) + ':' + str(x.minute))

if Arguments.end:
    for x in hour_end:
        print(str(x.hour) + ':' + str(x.minute))

if Arguments.sleep:
    for x in total_hours:
        print(round(x / 3600, 2))

if Arguments.delete is not None:
    line = 0
    buf = None
    with open(Arguments.file, 'r') as file:
        buf = file.readlines()
        while True:
            try:
                if buf[line][0:10] == str(Arguments.delete):
                    file.close()
                    break

            except IndexError:
                break
            line = line + 1

    with open(Arguments.file, 'w+') as file:
        tmp = 0
        for x in buf:
            if tmp != line:
                file.write(x)
            tmp = tmp + 1

if Arguments.stats:

    tmp_list = []
    for x in total_hours:
        tmp_list.append(round(x / 3600, 2))

    tmp_list_dates = []
    for x in dates:
        tmp_list_dates.append(str(x))

    print(tmp_list)
    print(tmp_list_dates)

    a = np.array(tmp_list_dates, dtype=str)
    b = np.array(tmp_list, dtype=float)
    plt.plot(a, b)
    plt.ylabel('Number of hours')
    plt.xlabel('Date')
    input()


