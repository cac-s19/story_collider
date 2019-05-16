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
plt.title(author)
plt.plot(results[:,0],results[:,1], label="Polarity")
plt.plot(results[:,0],results[:,2], label="Subjectivity")
plt.legend()
plt.xlabel("Window #")
plt.show()
