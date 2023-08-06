import numpy as np
from numba import njit


@njit(parallel=True)
def find_pressure_feet(values, samplerate):
    fstderiv = np.diff(values, 1)
    fstderiv = np.append(fstderiv, np.nan)
    sndderiv = np.diff(fstderiv, 1)
    sndderiv = np.append(sndderiv, np.nan)
    sndderiv = sndderiv * (fstderiv > 0)
    risingStarts, risingStops = sliding_search_zois(sndderiv, samplerate)
    outlen = min([len(x) for x in (risingStarts, risingStops)])
    outarr = np.empty(outlen, dtype=np.int64)
    for i in range(outlen):
        start = risingStarts[i]
        stop = risingStops[i]
        outarr[i] = start + np.argmax(sndderiv[start:stop])
    return outarr


@njit
def roll_with(a, w, f, center=True):
    n = len(a) - w + 1
    # buf = np.empty(n)
    buf = np.empty(len(a))
    for i in range(n):
        buf[i] = f(a[i : i + w])
    return buf


@njit
def roll_quant7(a, w, center=True):
    n = len(a) - w + 1
    # buf = np.empty(n)
    buf = np.empty(len(a))
    for i in range(n):
        buf[i] = np.nanquantile(a[i : i + w], 0.7)
    return buf


@njit(parallel=True)
def sliding_search_zois(a, samplerate, sumcoef=4, quantcoef=3):
    winsum = samplerate // sumcoef
    winquant = int(samplerate * quantcoef)
    sq = a**2
    integral = roll_with(sq, winsum, np.nansum)
    thres = roll_quant7(integral, winquant)
    risings = integral > thres
    risingvar = np.diff(risings.astype(np.int8))
    risingStarts = np.flatnonzero(risingvar > 0)
    risingStops = np.flatnonzero(risingvar < 0)
    risingStops = risingStops[risingStops > risingStarts[0]]
    return (risingStarts, risingStops)


@njit(parallel=True)
def calc_heartrate(feetidx, samplerate):
    dfeet = np.diff(feetidx)
    dfeet_s = dfeet / samplerate
    # Result in beats per minute
    return 60 / dfeet_s
