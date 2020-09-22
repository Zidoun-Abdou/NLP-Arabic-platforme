import os

from nltk import StanfordSegmenter
import re

NER_list_added = ["لندليام","كما"]
os.environ['STANFORD_MODELS'] = 'stanford-segmenter-2018-10-16/data/'
os.environ['JAVAHOME'] = 'D:/Program Files/Java/jdk1.8.0_171'
os.environ['CLASSPATH'] = 'stanford-segmenter-2018-10-16'

segmenter = StanfordSegmenter('stanford-segmenter-2018-10-16/stanford-segmenter-3.9.2.jar')
segmenter.default_config('ar')

x = open("sample.txt", "r", encoding="utf-8")

text =""

for line in x :
            text  =text+line
t = text.split()


temp1 = open("temp1.txt","w",encoding="utf-8")
temp2 = open("temp2.txt","w",encoding="utf-8")

outstr=""""""
ner = """"""

for word in t :
            #print("word : ",word)
            if word not in NER_list_added:
                temp1 = open("temp1.txt", "w", encoding="utf-8")
                temp1.write(word)

            else:
                temp2 = open("temp2.txt", "w", encoding="utf-8")
                temp2.write(word+" ")
                ner=word

            temp1.close()
            temp2.close()

            s = segmenter.segment_file('temp1.txt')
            temp1 = open("temp1.txt", "w", encoding="utf-8")
            temp1.truncate()
            temp1.close()

            outstr+=ner+" "+s.strip()+" "
            ner =""
            s=""

outfile = open("outfile.txt","w",encoding="utf-8")
outfile.write(outstr.strip(''))
outfile.close()
print("output -- " ,outstr ," -- output")




