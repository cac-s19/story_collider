import time
import platform

# This fixes NSInvalidArgumentException from tkinter on OSX
if platform.system() == "Darwin":
    import matplotlib

    matplotlib.use("TkAgg")
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt

import numpy as np
from textblob import TextBlob
import argparse
import os


def moving_average(data, window_size=3):
    """Calculate a moving average.

    data -- 1d numpy array

    Keyword arguments:
    window_size -- How many points to average over (default 3)
    """
    cumsum = np.cumsum(data, dtype=float)
    cumsum[window_size:] = cumsum[window_size:] - cumsum[:-window_size]

    return cumsum[window_size - 1 :] / window_size


def analyze_sentiment(filename):
    """Performs sentiment analysis using textblob.

    filename -- txt file containing story tanscript 
    (first name is assumed to be author's name)
    """

    with open(filename, "r") as f:
        author = f.readline().rstrip()
        transcript = TextBlob(f.read())

    # Keep a list of polarity and subjectivity
    polx, poly = [], []
    suby = []

    num_words = len(transcript.words)  # Number of words in transcript
    seg_length = 10_000 if num_words > 10_0000 else int(num_words / 5)
    num_windows = num_words - seg_length  # Number of windows to analyze sentiment from

    # Print out variables
    print(
        f"Number of Words: {num_words} \nSegment Length: {seg_length} \nNumber of Windows: {num_windows}"
    )

    # Conduct the sentiment analysis!! We do this according to Reagan's method of gathering all the
    # words in a sliding window of the text. Each window is analyzed as a whole for sentiment.
    print(f"Conducting SC Analysis on {author}...")
    # Let's keep track of how long this takes; bigger files may become a problem
    startTime = time.time()

    # We use the TextBlob ngrams() function to retrieve all the possible windows of our
    # specified segLength in the transcript
    for index, window in enumerate(transcript.ngrams(seg_length)):
        poly.append(TextBlob(" ".join(window)).sentiment.polarity)
        polx.append(len(poly))

        suby.append(TextBlob(" ".join(window)).sentiment.subjectivity)

        # Report quarterly progress during analysis
        if index % int((num_windows / 4)) == 0:
            print(
                "Finished window {}/{} [{:.2f}%]".format(
                    index, num_windows, index / num_windows * 100
                )
            )

    # storing as np array is easier to write to csv
    results = np.stack([polx, poly, suby]).transpose()

    # Report how long the analysis took
    print("SC Analysis Runtime:", round(time.time() - startTime, 2), "seconds")

    return author, results


if __name__ == "__main__":
    # Fun examples included: raven.txt, hanselgretel.txt, icarus.txt
    # Note: It seems that TextBlob does not like parsing through copy-pasted end quotes.
    #       If you're getting UnicodeDecodeError, that could the problem.

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-f",
        "--input_file",
        type=str,
        required=True,
        help="Text file (.txt) on which to do sentiment analysis",
    )

    parser.add_argument(
        "-s",
        "--save",
        dest="save",
        action="store_true",
        help="Save the resulting plot as plots/author_name.png (default=False)",
    )

    parser.set_defaults(save=False)

    args = parser.parse_args()
    filename = args.input_file

    author, results = analyze_sentiment(filename)

    # Time to graph! set up the plot with axes and labels
    plt.title(author)
    plt.plot(results[:, 0], results[:, 1], linewidth=1, label="Polarity")
    plt.xlabel("Window #")
    plt.legend()

    if args.save == True:
        plots_folder = "plots"
        csv_folder = "csv"

        if not os.path.exists(plots_folder):
            os.makedirs(plots_folder)

        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)

        fname = author.replace(" ", "")  # Remove spaces
        plt.savefig(f"plots/{fname}.png")
        plt.close()
        print(f"Plot saved to plots/{fname}.png")

        np.savetxt(
            f"csv/{fname}.csv",
            results,
            delimiter=",",
            header="window #, polarity, subjectivity",
        )
        print(f"Data save to csv/{fname}.csv")

    else:
        plt.show()
