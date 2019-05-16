import numpy as np
import platform

# This fixes NSInvalidArgumentException from tkinter on OSX
if platform.system() == "Darwin": 
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt

from scipy.optimize import curve_fit


filename = "csv/EthanHollander.csv"

results = np.genfromtxt(filename, delimiter=',', skip_header=1)

author = filename.split("/")[-1].strip(".csv")


def sin_func(x,a,b,c):
    return a * np.sin(b * x) + c

popt, pcov = curve_fit(sin_func, results[:,0], results[:,1])


plt.title(author)
plt.plot(results[:,0], results[:,1], label="Polarity")
#plt.plot(results[:,0],results[:,2], label="Subjectivity")
plt.plot(results[:,0], sin_func(results[:,0],*popt), 
        label="fit: a={:.3f}, b={:.3f}, c={:.3f}".format(*popt))
plt.legend()
plt.xlabel("Window #")
plt.show()
