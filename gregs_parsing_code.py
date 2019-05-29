# coding: utf-8

# In[126]:


import numpy as np
from textblob import TextBlob

# wiki = TextBlob("Python is a high-level, general_purpose programming language")
import matplotlib.pyplot as plt
import pandas as pd

filename = "hanselgretel.txt"
transcript = TextBlob(open(filename).read())

transcript.sentiment
# Get Start and End Indices of Sentences
sentiments = []
import matplotlib.pyplot as plt

get_ipython().run_line_magic("matplotlib", "inline")


for s in transcript.sentences:
    sentiments.append(s.sentiment.subjectivity)

plt.plot(sentiments)
print(max(sentiments))
plt.ylabel("sentiment")
plt.xlabel("sentence")
# sentiments.head()


# In[107]:


plt.plot(bool(1), bool(0))
