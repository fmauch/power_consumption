#!/usr/bin/env python

from __future__ import print_function
import argparse
import pandas
import datetime
from collections import Counter


import gtk

import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import scipy.integrate as integrate


COSTS_PER_KWH = 0.2356


def dateparse(timestring):
    return datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M')


def plot_time_based(time_data, data):
    ax = plt.gca()
    plt.subplots_adjust(top=0.98, bottom=0.02, left=0.05, right=0.98, hspace=0.25,
                        wspace=0.35)
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(time_data, data)
    plt.ylabel('Wirkleistung')
    plt.title('Leistungsverlauf')

    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Evaluate logging data from el4000')
    parser.add_argument('filename', type=str, help='csv file containing the data')

    args = parser.parse_args()
    print('Analyzing data from {}'.format(args.filename))

    consumption_data = pandas.read_csv(
        args.filename, delimiter=',', parse_dates=True, date_parser=dateparse, index_col='timestamp', header=0)
    consumption_data = consumption_data.sort_index()
    # consumption_data = consumption_data.drop_duplicates()

    timestamps = consumption_data.index.values
    voltages = consumption_data.voltage.values
    currents = consumption_data.current.values
    cos_phi = consumption_data.power_factor.values

    powers = voltages * currents * cos_phi

    duplicates = [x for x, cnt in Counter(timestamps).iteritems() if cnt > 1]
    print(duplicates)


    power_average = np.mean(powers)
    NANOSECS_TO_HOURS = 3600 * 1000000000
    print('Average power consumption: {}'.format(power_average))
    print('Time passed: {}'.format((timestamps[-1] - timestamps[0]).astype('float')/(24 * NANOSECS_TO_HOURS)))

    energy_total = integrate.simps(powers, timestamps.astype('float') / NANOSECS_TO_HOURS) / 1000
    print('Total energy used: {} kWh'.format(energy_total))

    print('Estimated energy consumption in one year: {} kWh'.format(power_average * 365.25 * 24 / 1000))
    print('Estimated annual costs: {} EUR'.format((power_average * 365.25 * 24 / 1000) * COSTS_PER_KWH))

    plot_time_based(timestamps, powers)


if __name__ == "__main__":
    main()
