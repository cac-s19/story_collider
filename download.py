import requests
import os
import glob
import docx2txt

folder = "worddocs"

if not os.path.exists(folder):
    os.makedirs(folder)

with open('links.txt') as file:
    for line in file:
        url = line.split('https')[-1]
        myfile = requests.get('https'+ url.rstrip())
        a = line.split('/')[-1].rstrip()
        open(folder + '/' + a, 'wb').write(myfile.content)

#https://likegeeks.com/downloading-files-using-python/
#I want this to download the files from the url and put them into a new file called?!
#Also something about converting files?
if not os.path.exists('text'):
    os.makedirs('text')
for x in  glob.glob("worddocs/*.docx"):
      print(x)
      text = docx2txt.process(x)
      fname = x.split("/")
      fname = fname[-1].replace("docx","txt")
      with open("text/"+fname,"w") as f:
          f.write(x)
