

# Code review

I'm going to take [`sentiment.py`](https://github.com/cac-s19/story_collider/blob/2ea0315d08c57ff104ec74a3407ab92458db2788/sentiment.py) as it existed at this git hash: 2ea0315d08c57ff104ec74a3407ab92458db2788 and do a "code review".



```py
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
```


The code works! I'm going to start with a few big picture things, then go line by line. All of my advice will also be given though the lense of [PEP 8](https://www.python.org/dev/peps/pep-0008/) which is python's style guide. 
 1. Use a [`if __name__ == "__main__"` guard](https://stackoverflow.com/a/419185) so someone could import `moving_average` from your code. 
 1. Use an automated linter like [flake8](http://flake8.pycqa.org/en/latest/) so you don't have to remember all of the style recomendations.

I'll now highlight some specific bits of code and how they can be imporved.
```py
def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
```
This function is pretty good, but could use more descipritve varable names as well as some [docstrings](https://www.python.org/dev/peps/pep-0257/#what-is-a-docstring) 


```py
def moving_average(data, window_size=3):
    """Calculate a moving average.
    
    data -- 1d numpy array
    
    Keyword arguments:
    window_size -- How many points to average over (default 3)
    """
    cumsum = np.cumsum(a, dtype=float)
    cumsum[window_size:] = cumsum[window_size:] - cumsum[:-window_size]
    return cumsum[window_size - 1:] / window_size
```

I'm not exactly sure what the function does or how it works, but its a start of a docstring.

```py
filename = "transcripts/sc0-inspiration.txt"
transcript = TextBlob(open(filename).read())
```

We should use a context manager when reading in files to make sure that the file gets closed when we are done reading it. This is important since open file descriptors use resources and also can cause issues if another program wants to modify the file we left open.

```py
filename = "transcripts/sc0-inspiration.txt"
with open(filename,'r') as f:
    transcript = TextBlob(f.read())
```

Now the file will be closed automatcally for us after we read it

```py
polx = []; poly = []
subx = []; suby = []
```

Not the most pythonic way of declaring varables, we can group them like this since they are related.

```py
polx, poly = [], []
subx, suby = [], []
```

```py
# Initialize variables
numWords = len(transcript.words)                                # Number of words in transcript
segLength = 10000 if numWords > 100000 else int(numWords/5)     # Segment / window length
numWindows = numWords - segLength                               # Number of windows to analyze sentiment from
```
Comments like `Initialize variables` are not really that useful. Use comments when its not clear whats going on in the code and inlined comments start with 2 spaces. The recomended style for python varables is snake_case, not camelCase. Python also supports using `_` to make numbers esier to read.

```py
num_words = len(transcript.words)  # Number of words in transcript                               
seg_length = 10_000 if num_words > 10_0000 else int(num_words/5) 
num_windows = num_words - seg_length  # Number of windows to analyze sentiment from
```



```py
# Print out variables
print("numWords:", numWords); print("segLength:", segLength); print("numWindows:", numWindows)
```

Don't put more than one statement on a line using `;`. We can use f strings here as well.

```py
# Print out variables
print(f"numWords: {numWords} \n segLength: {segLength} \n numWindows: {numWindows})
```

I wasn't sure if you want them printing on new lines, so I kept in the `\n`

Taking everything from above + making a few more changes, this is what we have now:

```py
import time

import matplotlib.pyplot as plt
import numpy as np
from textblob import TextBlob


def moving_average(data, window_size=3):
    """Calculate a moving average.

    data -- 1d numpy array

    Keyword arguments:
    window_size -- How many points to average over (default 3)
    """
    cumsum = np.cumsum(data, dtype=float)
    cumsum[window_size:] = cumsum[window_size:] - cumsum[:-window_size]
    return cumsum[window_size - 1 :] / window_size


# Fun examples included: raven.txt, hanselgretel.txt, icarus.txt
# Note: It seems that TextBlob does not like parsing through copy-pasted end quotes.
#       If you're getting UnicodeDecodeError, that could the problem.
filename = "transcripts/sc0-inspiration.txt"
with open(filename, "r") as f:
    transcript = TextBlob(f.read())

polx, poly = [], []
subx, suby = [], []

num_words = len(transcript.words)  # Number of words in transcript
seg_length = 10_000 if num_words > 10_0000 else int(num_words / 5)
num_windows = num_words - seg_length  # Number of windows to analyze sentiment from

# Print out variables
# Print out variables
print(
    f"Number of Words: {num_words} \nSegment Lenght: {seg_length} \nNumber of Windows: {num_windows}"
)

# Conduct the sentiment analysis!! We do this according to Reagan's method of gathering all the
# words in a sliding window of the text. Each window is analyzed as a whole for sentiment.
print("Conducting SC Analysis...")
# Let's keep track of how long this takes; bigger files may become a problem
startTime = time.time()
# We use the TextBlob ngrams() function to retrieve all the possible windows of our
# specified segLength in the transcript
for index, window in enumerate(transcript.ngrams(seg_length)):
    poly.append(TextBlob(" ".join(window)).sentiment.polarity)
    polx.append(len(poly))
    # Report quarterly progress during analysis
    if index % int((num_windows / 4)) == 0:
        print(
            "Finished window",
            index,
            "/",
            num_windows,
            "[",
            round((index / num_windows) * 100, 2),
            "% ]",
        )

# Report how long the analysis took
print("SC Analysis Runtime:", round(time.time() - startTime, 2), "seconds")

# Time to graph! set up the plot with axes and labels
plt.title(filename)
# plt.ylim(-1, 1)
plt.plot(polx, poly, linewidth=1, label="polarity")
# plt.plot(moving_average(poly,n=10), linewidth = 1, label = "polarity")
# plt.plot(moving_average(suby,n=20), linewidth = 1, label = "subjectivity")
plt.xlabel("sentence #")
plt.legend()
plt.show()
```
