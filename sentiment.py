# Imports
import numpy as np
from textblob import TextBlob
import matplotlib.pyplot as plt
import time

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

# Fun examples included: raven.txt, hanselgretel.txt, icarus.txt
# Note: It seems that TextBlob does not like parsing through copy-pasted end quotes.
#       If you're getting UnicodeDecodeError, that could the problem.
filename = "transcripts/sc0-inspiration.txt"
transcript = TextBlob(open(filename).read())
polx = []; poly = []
subx = []; suby = []

# Initialize variables
numWords = len(transcript.words)                                # Number of words in transcript
segLength = 10000 if numWords > 100000 else int(numWords/5)     # Segment / window length
numWindows = numWords - segLength                               # Number of windows to analyze sentiment from

# Print out variables
print("numWords:", numWords); print("segLength:", segLength); print("numWindows:", numWindows)

# Conduct the sentiment analysis!! We do this according to Reagan's method of gathering all the 
# words in a sliding window of the text. Each window is analyzed as a whole for sentiment.
print("Conducting SC Analysis...")
# Let's keep track of how long this takes; bigger files may become a problem
startTime = time.time()
# We use the TextBlob ngrams() function to retrieve all the possible windows of our 
# specified segLength in the transcript
for index,window in enumerate(transcript.ngrams(segLength)):
        poly.append(TextBlob(' '.join(window)).sentiment.polarity)
        polx.append(len(poly))
        # Report quarterly progress during analysis
        if index % int((numWindows / 4)) == 0:
                print("Finished window", index, "/", numWindows, "[", round((index/numWindows)*100, 2), "% ]")

# Report how long the analysis took
print("SC Analysis Runtime:", round(time.time() - startTime, 2), "seconds")

# Time to graph! set up the plot with axes and labels
plt.title(filename)
#plt.ylim(-1, 1)
plt.plot(polx, poly, linewidth = 1, label = "polarity")
#plt.plot(moving_average(poly,n=10), linewidth = 1, label = "polarity")
#plt.plot(moving_average(suby,n=20), linewidth = 1, label = "subjectivity")
plt.xlabel("sentence #")
plt.legend()
plt.show()