import requests
import os

folder = "worddocs"

if not os.path.exists(folder):
    os.makedirs(folder)

with open('links.txt') as file:
    for line in file:
        url = line.split('https')[-1]
        myfile = requests.get('https'+ url.rstrip())
        a = line.split('/')[-1].rstrip()
#print(type(a))
#print(a)
        open(folder + '/' + a, 'wb').write(myfile.content)

#https://likegeeks.com/downloading-files-using-python/
#I want this to download the files from the url and put them into a new file called?!
#Also something about converting files?

