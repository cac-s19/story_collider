import numpy as np
import platform
import time
from textblob import TextBlob

# This fixes NSInvalidArgumentException from tkinter on OSX
#if platform.system() == "Darwin":
#    import matplotlib

#   matplotlib.use("TkAgg")
#    from matplotlib import pyplot as plt
#else:
#    import matplotlib.pyplot as plt

#from scipy.optimize import curve_fit
#from scipy.signal import savgol_filter

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:]# / n

filename = "transcripts/hanselgretel.txt"
transcript = TextBlob(open(filename).read())
polx = []; poly = []
subx = []; suby = []

num_words = len(transcript.words)
seg_length = 10000 if num_words > 100000 else int(num_words/5)
num_windows = num_words - seg_length

print("num_words:", num_words); print("seg_length:", seg_length); print("num_windows:", num_windows)

print("Conducting SC Analysis...")
start_time = time.time()

for index,window in enumerate(transcript.ngrams(segLength)):
    poly.append(TextBlob(' '.join(window)).sentiment.polarity)
    polx.append(len(poly))
    if index % int((num_windows / 4)) == 0:
        print("Finish window", index, "/", num_windows, "[", round((index/num_windows)*100, 2), "% ]")
print("SC Analysis Runtime:", round(time.time() - start_time, 2), "seconds")

# Time to graph! set up the plot with axes and labels
plt.title(filename)
plt.ylim(-2, 2)
plt.plot(polx, poly, linewidth = 1, label = "polarity")
#plt.plot(moving_average(poly,n=10), linewidth = 1, label = "polarity")
#plt.plot(moving_average(suby,n=20), linewidth = 1, label = "subjectivity")
plt.xlabel("sentence #")
plt.legend()
plt.show()

##trying to fit a sine function
import matplotlib.pyplot as plot

time1 = np.arange(0, 100);
amplitude = np.sin(2)
plot.plot(time1, amplitude)
plot.title('Sine wave')
plot.xlabel('Time')
plot.ylabel('Amplitude=sin(time)')
plot.grid(True, which='both')
plot.axhline(y=0, color='k')
plot.show()




######
#for hanselgretel.txt, there is no header. For other stories, skip_header=1
#results = np.genfromtxt(filename, delimiter=',', skip_header=0)

#author = filename.split("/")[-1].split(".")[0]

#def odd(f):
#    return int(np.ceil(f)//2*2+1)

#pol = results[:,1]
#pol_norm = (pol-np.mean(pol))/np.std(pol)

#smooth_window = odd(len(pol_norm)//10)

#percent = results[:,0]/results[-1,0]*100

#plt.title(author)
#plt.plot(percent, pol_norm, label="Polarity")
#plt.plot(percent, smooth_pol, label="Smoothed Polarity")
#plt.legend()
#plt.xlim([0,100])
#plt.xlabel("Story Progress (%)")
#plt.show()

#np.random.seed(0)

#x_data = np.linspace(0, 100, num=50)
#y_data = np.sin(1.5 * x_data) + np.random.normal(size=50)

#plt.figure(figsize=(6, 4))
#plt.scatter(x_data, y_data)

#from scipy import optimize

#def test_func(x, a, b):
#    return a * np.sin(b * x)

#params, params_covariance = optimize.curve_fit(test_func, x_data, y_data, p0=[2, 2])

#print(params)

#plt.figure(figsize=(6, 4))
#plt.scatter(x_data, y_data, label='Data')
#plt.plot(x_data, test_func(x_data, params[0], params[1]), label='Fitted Function')

#plt.legend(loc='best')

#plt.show()

