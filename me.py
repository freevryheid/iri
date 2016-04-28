#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pandas import DataFrame, to_numeric
from scipy.signal import welch
# from math import ceil
# from numpy import log10
from numpy import pi
from scipy.signal import butter, lfilter
from matplotlib.pylab import plt


class Prof(object):

    def __init__(self, pdf, scl, dx):
        self.scl = scl
        self.pdf = pdf*scl
        self.dx = dx*scl
        self.n = len(pdf.index)


class PRO:

    def __init__(self):
        self.prof = []

    def open(self, file):
        with open(file, 'r') as f:
            rec = 1
            for line in f:
                if rec == 1:
                    data = line.strip().split(',')
                    if data[0] != 'HEAD3':
                        print('Missing HEAD3 record in pro file')
                        return self.prof
                    else:
                        self.date = data[1]
                        self.district = data[2]
                        self.county = data[3]
                        self.hwy = data[4]
                        self.brm = data[5]
                        self.lane = data[6]
                if rec == 2:
                    data = line.strip().split(',')
                    if data[0] != 'CMET3':
                        print('Missing CMET3 record in pro file')
                        return self.prof
                    else:
                        self.profiler = data[1]
                        self.surf = data[2]
                        self.operator = data[3]
                        self.serial = data[4]
                        self.cutoff = data[5]
                        self.certcode = data[6]
                        self.certdate = data[7]
                if rec == 3:
                    data = line.strip().split(',')
                    self.man = data[0]
                    self.elev_unit = data[1]
                    self.path = data[2]
                    self.dist = data[3]
                    self.dist_unit = data[4]
                if rec == 4:
                    data = line.strip().split(',')
                    self.lat = data[0]
                    self.lon = data[1]
                    self.alt = data[2]
                    self.head = data[3]
                    self.speed = data[4]
                if rec == 5:
                    self.comment = line.strip()
                if rec >= 6:
                    data = line.strip().split(',')
                    if len(data) == 2 or len(data) == 7:  # one wheelpath profilers
                        print('not implemented for one wheelpath profilers')
                        return
                    elif len(data) == 3:  # two wheelpath profilers
                        self.prof.append({
                            'LEFT': data[0],
                            'RIGHT': data[1],
                            'CMT': data[2]
                        })
                    elif len(data) == 8:  # two wheelpath profilers with GPS
                        self.prof.append({
                            'LEFT': data[0],
                            'RIGHT': data[1],
                            'CMT': data[2],
                            'LAT': data[3],
                            'LON': data[4],
                            'ALT': data[5],
                            'HEAD': data[6],
                            'SPD': data[7]
                        })
                rec += 1
            return self.prof


def butter_bandpass(lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

if __name__ == "__main__":
    # pdf = pd.read_csv('prof.csv')
    # scl = 0.3048  # ft -> m
    # dx = 0.2069167  # ft
    # prof = Prof(pdf, scl, dx)

    p = PRO()
    prof = p.open('Test_Run1.PRO')
    df = DataFrame(prof, columns=['LEFT', 'RIGHT', 'CMT', 'LAT', 'LON', 'ALT', 'HEAD', 'SPD'])
    left = to_numeric(df.LEFT)

    scl_x = 0.0254  # in -> m
    scl_y = 2.54e-5  # mils -> m

    dx = float(p.dist)*scl_x
    fs = 2*pi/dx
    fn = fs/2

    left = left*scl_y

    # sampling freq
    # samples per second (time domain)
    # samples per metre (spatial domain)
    # fs = 1/prof.dx
    # fn = fs/2  # Nyquist freq
    # nperseg = 1024
    nperseg = 2048

    # # low pass 0.25 m, high pass 200ft
    # # b, a = butter_bandpass(1/0.25, 1/(200*scl), fs)
    # b, a = butter(2, (1/0.25)/fn)

    # left = prof.pdf.LEFT
    # left = lfilter(b, a, left)
    f, P = welch(left, fs=fs, nperseg=nperseg)
