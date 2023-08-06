import re
import numpy as np
from earthquakepy import timeseries


def read_peer_nga_file(filepath, scale_factor=1):
    """
    Reads PEER NGA record file and generates a timeseries object.

    Parameters
    ----------
    filepath (string): PEER NGA file path
    scale_factor: Scaling factor, default = 1

    Returns
    -------
    TimeSeries object
    """
    with open(filepath, "r") as f:
        lines = f.readlines()
        nlines = len(lines)

    for n in range(nlines):
        line = lines[n]
        if n == 0:
            pass
        elif n == 1:
            eq, eqDate, station, component = [l.strip() for l in line.strip("\n").split(",")]
        elif n == 2:
            yunit = line.strip()
        elif n == 3:
            npts = int(re.match(r".*= *([0-9]*),.*", line)[1])
            dt = float(re.match(r".*= *(0?\.[0-9]*) SEC", line)[1])
            duration = dt * npts
            y = np.zeros(int(npts))
        else:
            elms = line.strip("\n").split()
            nelms = len(elms)
            i = (n - 4) * nelms
            j = i + nelms
            y[i:j] = [float(e) for e in elms]

    ts = timeseries.TimeSeries(dt, y*scale_factor)
    ts.set_tunit("s")
    ts.set_yunit(yunit)
    ts.set_eqname(eq)
    ts.set_eqdate(eqDate)
    ts.set_station(station)
    ts.set_component(component)
    ts.set_npts(npts)
    ts.set_dt(dt)
    ts.set_duration(duration)
    ts.set_filepath(filepath)
    return ts


def read_raw_timeseries_file(filename, **kwargs):
    """
    Reads a raw file readable by numpy.genfromtxt(). The first column is assumed as time and second column as ordinates. Accepts all arguments supported by genfromtxt().

    Parameters
    ----------
    filename: (str) filename of the file containing raw data

    Returns
    -------
    Timeseries object
    """
    data = np.genfromtxt(filename, **kwargs)
    ts = timeseries.TimeSeries(data[:, 0], data[:, 1])
    return ts
