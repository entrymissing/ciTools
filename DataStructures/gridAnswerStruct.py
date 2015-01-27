"""
Structs and functions to work with grid answer files from ladon

:Author: David Engel
:Email: entrymissing@gmail.com
"""

import csv

#TODO Write docstring and doctests
class GridAnswers:
    def __init__(self, filename):
        self.answers = {}
        
        #open the reader and skip the header
        with open(filename, 'r') as fp:
            csvReader = csv.reader(fp)
            csvReader.next()
            
            #read the answers into a dict
            for curLine in csvReader:
                self.answers[curLine[4].lower().strip()] = curLine[6].lower().strip()
                

    def __iter__(self):
        return self.answers.__iter__()
    
    def __getitem__(self, key):
        return self.answers[key.lower().strip()]
    
if __name__ == '__main__':
    ga = GridAnswers('../Test Study/Data/XVal Session 21/Grid Items XVal Session 21.csv')
    for x in ga:
        print x, ga[x
                    ]