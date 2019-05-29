import numpy as np
import platform
import glob

# This fixes NSInvalidArgumentException from tkinter on OSX
if platform.system() == "Darwin":
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
from scipy.signal import savgol_filter


def odd(f):
    """Rounds up to the neareat odd number."""
    return int(np.ceil(f)//2*2+1)


if __name__ == "__main__":
    deg = 8 # degree of polynomial fit
    polyfit_dict = {}

    for csvfile in glob.glob("csv/*.csv"):
        filename = csvfile
        results = np.genfromtxt(filename, delimiter=',', skip_header=1)
        author = filename.split("/")[-1].strip(".csv")

        # Normalize the polarity data
        # by shiting by the the mean
        # and scaling by the std dev

        pol = results[:,1]
        pol_norm = (pol-np.mean(pol))/np.std(pol)

        # Smooth the data

        smooth_window = odd(len(pol_norm)//10)
        smooth_pol = savgol_filter(pol_norm, smooth_window, 1)

        # Get percentage of story

        percent = results[:,0]/results[-1,0]*100

        # Fit smoothed, normalized data to polynomial
        sm_coeffs = np.polyfit(percent,smooth_pol,deg)

        # Save coefficients to dict under author name
        polyfit_dict[author] = sm_coeffs


