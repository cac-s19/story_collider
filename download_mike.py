import glob
import os

import requests
import docx2txt

doc_folder = "worddocs"
text_folder = "text"

if not os.path.exists(doc_folder):
    os.makedirs(doc_folder)

if not os.path.exists(text_folder):
    os.makedirs(text_folder)

with open("links.txt") as file:
    for line in file:
        url = line.split("https")[-1]
        myfile = requests.get("https" + url.rstrip())
        a = line.split("/")[-1].rstrip()
        open(doc_folder + "/" + a, "wb").write(myfile.content)

for x in glob.glob("worddocs/*.docx"):
    print(x)
    text = docx2txt.process(x)
    fname = x.split("/")
    fname = fname[-1].replace("docx", "txt")
    with open(text_folder + "/" + fname, "w") as f:
        f.write(x)
