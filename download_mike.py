import glob
import os
import requests
import docx2txt
import shutil

doc_folder = "worddocs"
text_folder = "text"

if not os.path.exists(doc_folder):
    os.makedirs(doc_folder)

if not os.path.exists(text_folder):
    os.makedirs(text_folder)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

len_links = file_len("links.txt")

with open("links.txt") as file:
    for i, line in enumerate(file):
        url = line.split("https")[-1]
        progress = (i+1)/len_links*100
        name = url.rstrip().split("/")[-1]
        printstr = "\rDownloading [{:.1f}%]: {}".format(progress,name)
        term_width,_ = shutil.get_terminal_size()
        print(printstr+" "*(term_width-len(printstr)), end="\r", flush=True)
        myfile = requests.get("https" + url.rstrip())
        a = line.split("/")[-1].rstrip()
        if a.split(".")[-1] != "docx":
            a = a+".docx"
        open(doc_folder + "/" + a, "wb").write(myfile.content)

for i,x in enumerate(glob.glob("worddocs/*.docx")):
    progress = (i+1)/len_links*100
    printstr = "\rConverting [{:.1f}%]: {}".format(progress, x)
    term_width,_ = shutil.get_terminal_size()
    print(printstr + " "*(term_width-len(printstr)), end="\r", flush=True)
    text = docx2txt.process(x)
    fname = x.split("/")
    fname = fname[-1].replace("docx", "txt")
    with open(text_folder + "/" + fname, "w") as f:
        f.write(x)

print("\nDone!")
