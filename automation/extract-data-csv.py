# This script extracts selected data from a log file into
# a csv. The log file is stored in the path presented by the myFile.

import os
import csv

#Reads data from a log file
myFile = 'C:\Users\oliveia\Desktop\Logs\matlab.log'

important = []
keep_phrases = ["Server's System Date and Time:","TIMESTAMP","(MLM) OUT:"]

openFile = open(myFile, 'r')

with openFile as f:
    f = f.readlines()

#Filters data
for line in f:
    for phrase in keep_phrases:
        if phrase in line:
            important.append(line)
            break

#Checks which part of the filtered data is from 2016
indices = []
for i, elem in enumerate(important):
    if '2016' in elem:
        indices.append(i)

#Checks which part of the filtered data is from 2017
indicess = []
for i, elem in enumerate(important):
    if '2017' in elem:
        indicess.append(i)

#Delete 2017 chunk of data
del important[indicess[0]:]


#Delete useless lines from 2016
for elem in indices:
    important[elem] = ""

importants = filter(None,important)


#Structures data
time = [i.split('(', 1)[0] for i in importants]
time_rest = [i.split('(', 1)[1] for i in importants]

toolbox = [i.split('"')[1] for i in time_rest]
toolbox_rest = [i.split('" ')[1] for i in time_rest]
user = [i.split('@')[0] for i in toolbox_rest]

#Exports data to a csv file
rows = zip(time,toolbox,user)
with open('Output.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(('Time','Toolbox','Username'))
    for row in rows:
        writer.writerow(row)


       


