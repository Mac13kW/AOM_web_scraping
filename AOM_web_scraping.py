# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 17:41:13 2015

@author: Maciej

This script is an example of web scraping.

We will go through the AOM websites from 100 to 2600 and will be looking
for names of individuals in one of these roles:

Organizer:
Discussant:
Participant:
Facilitator:
Presenter:
Speaker:
Chair:

First we import all the tools we will need to accomplish the job.
"""
import urllib
import re
import csv
from time import time
from os.path import expanduser
from os import makedirs
from os.path import exists

start = time()  # this little timer will help us measure how long it takes

'''
First let's create a folder for the output file in the user's folder
'''
_path = expanduser('~/Python_BC/')  # change to select a different folder
if not exists(_path):
    makedirs(_path)

LoL = []  # we are creating an empty list to store the results

for x in range(100, 2600):  # iterating over the AOM sessions
    aomurl = ('http://program.aom.org/2014/submission.asp?mode='
              'ShowSession&SessionID=' + str(x) + '&print=true')
    urlopen = urllib.urlopen(aomurl)  # open the url
    _page = urlopen.read()  # and read the file

    '''
    Now we want to search each line of the text file for the lines that
    start with one of the session members' roles
    '''
    m = re.findall('(Organizer:.*$|Discussant:.*$|Participant:.*$|'
                   'Facilitator:.*$|Presenter:.*$|Speaker:.*$|Chair:.*$)'
                   , _page, re.MULTILINE)

    '''
    First time we run the code we will notice that those sessions which
    may have a word 'chair' in the title or description will be also
    recorded and will later produce an error message (like session 122).

    We need to find a way to deal with such exceptions. Normally it takes
    some time to figure out all possible exceptions.
    '''
    p = []  # an empty list to capture people and their affiliations
    for y in range(len(m)):
        if "<strong>" in m[y]:
            name = re.search('%s(.*)%s' % ('<strong>', '</strong>'),
                             m[y]).group(1)
            affiliation = re.search('%s(.*)%s' % ('; ', '; <'), m[y]).group(1)
            p.append(name + ', ' + affiliation)
    print 'session: ' + str(x) + ' names: ' + str(p)
    '''
    The print command is not necessary but it is a good practice to have
    the code print something as the code is running so that you know
    that it does and that everything is going well. Here we want to
    know how many sessions are still left and what is being written to
    the p list.
    '''
    LoL.append(p)  # we are recording the names and affiliations

# The only thing left to do is to save our output

filename = _path + 'output_WS.csv'
with open(filename, "wb") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(LoL)

elapsed_time = time() - start
print('total time = ' + str(elapsed_time))

# END OF LINE
