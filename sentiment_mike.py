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


if __name__ == "__main__":
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