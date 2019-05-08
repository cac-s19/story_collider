import docx2txt
import os

x = os.listdir('worddocs/')
for i in x:
    text = docx2txt.process(i)
    print(i)
    



# will need to be a for loop to go through worddocs
# then put them into Txt directory
#https://github.com/ankushshah89/python-docx2txt
