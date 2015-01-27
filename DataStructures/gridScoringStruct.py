"""
A class that loads and returns scores for grid task answers

:Author: David Engel
:Email: entrymissing@gmail.com
"""

import json

class gridScores:
    """
    Read the scores from a json file and return them via task, answer keys
    All lookups will be case insensitive and ignoring leading and trailing whitespaces
    If the answer isn't found in the answer key it will return -1
    Looking up a non existing task raises a KeyError
    
    >>> from settingsStruct import settingsStruct
    >>> settings = settingsStruct('Test Study/settings.ini')
    >>> gridScorer = gridScores(settings)
    >>> gridScorer.getScore('Memory - Video and Image Trial [1,1]', 'Bird')
    1.0
    >>> gridScorer.getScore('   mEmOrY - Video and Image TRIal [1,1]', '   bIRD   ')
    1.0
    >>> gridScorer.getScore('   mEmOrY - Video and Image TRIal [1,1]', '   bIRD   ')
    1.0
    >>> gridScorer.getScore('Unscramble Words [5,2]', '   bIRD   ')
    -1
    >>> gridScorer.getScore('Non Existing Task', 'bIRD')
    Traceback (most recent call last):
    .
    .
    KeyError
    """
    def __init__(self, settings):
        #read the JSON file
        tempScoringTable = json.load(open(settings['Scoring']['Correct Grid Answers'], 'r'))
        
        self.scoringTable = {}
        
        #make the answers all lower case since we should be case insensitive
        for curTask in tempScoringTable:
            tempAnswers = {}
            for curAnswer in tempScoringTable[curTask]:
                tempAnswers[curAnswer.lower()] = tempScoringTable[curTask][curAnswer]
            self.scoringTable[curTask.lower()] = tempAnswers
        
    def getScore(self, task, answer):
        task = task.lower().strip()
        answer = answer.lower().strip()
        #if the task is not in the scoring table raise an exception
        if not task in self.scoringTable:
            print 'Error: Task {} not found in grid scoring json file.'.format(task)
            raise KeyError
        
        #if the answer is not in the scoring table return -1
        if not answer in self.scoringTable[task]:
            return -1
        
        #return the score
        return self.scoringTable[task][answer]
    
if __name__ == '__main__':
    from settingsStruct import settingsStruct
    
    settings = settingsStruct('../Test Study/settings.ini')
    gs = gridScores(settings)
    
    print gs.getScore('Memory - Video and Image Trial [1,', 'BIrd')