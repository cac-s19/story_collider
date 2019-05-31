import glob
import os
import requests
import docx2txt
import shutil
import sentiment
import numpy as np


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def download():
    """Downloads all worddocs in links.txt to worddocs folder."""

    doc_folder = "worddocs"

    if not os.path.exists(doc_folder):
        os.makedirs(doc_folder)

    len_links = file_len("links.txt")

    with open("links.txt") as file:
        for i, line in enumerate(file):
            url = line.split("https")[-1]
            progress = (i + 1) / len_links * 100
            name = url.rstrip().split("/")[-1]
            printstr = "\rDownloading [{:.1f}%]: {}".format(progress, name)
            term_width, _ = shutil.get_terminal_size()
            print(printstr + " " * (term_width - len(printstr)), end="\r", flush=True)
            myfile = requests.get("https" + url.rstrip())
            a = line.split("/")[-1].rstrip()
            if a.split(".")[-1] != "docx":
                a = a + ".docx"
            open(doc_folder + "/" + a, "wb").write(myfile.content)


def convert():
    """Converts all worddocs in folder to txt files"""

    text_folder = "text"

    if not os.path.exists(text_folder):
        os.makedirs(text_folder)
    for i, x in enumerate(glob.glob("worddocs/*.docx")):
        progress = (i + 1) / len_links * 100
        printstr = "\rConverting [{:.1f}%]: {}".format(progress, x)
        term_width, _ = shutil.get_terminal_size()
        print(printstr + " " * (term_width - len(printstr)), end="\r", flush=True)
        text = docx2txt.process(x)
        fname = x.split("/")
        fname = fname[-1].replace("docx", "txt")
        with open(text_folder + "/" + fname, "w") as f:
            f.write(text)


if __name__ == "__main__":

    download()
    convert()

    csv_folder = "csv"

    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    txts = glob.glob("text/*.txt")

    for i, txtfile in enumerate(txts):
        author, results = sentiment.analyze_sentiment(txtfile)

        fname = author.replace(" ", "")  # Remove spaces

        np.savetxt(
            f"{csv_folder}/{fname}.csv",
            results,
            delimiter=",",
            header="window #, polarity, subjectivity",
        )

        print(f"Data saved to {csv_folder}/{fname}.csv [{i+1}/{len(txts)}]")

    print("\nDone!")
