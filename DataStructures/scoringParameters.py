"""
Classes that hold the scoring parameters from the json scoring file and makes them more accesible

:Author: David Engel
:Email: entrymissing@gmail.com
"""

import json
from gridScoringStruct import gridScores

class scoringParameters:
    """
    The class that captures all the scoring parameters and can be passed around to the scoring functions
    
    >>> from settingsStruct import settingsStruct
    >>> x = scoringParameters(settingsStruct('Test Study/settings.ini'))
    """
    def __init__(self, settings):
        self.scoringParameters = json.load(open(settings['General']['ScoringFile'], 'r'))['ScoreTasks']
    
    def __iter__(self):
        return self.scoringParameters.__iter__()
    
    def __getitem__(self, taskName):
        for curTask in self.scoringParameters:
            if curTask['TaskName'] == taskName:
                return curTask
        
        print 'Task {} not found.'.format(taskName)
        raise KeyError
    
class combinationParameters:
    """
    The class that captures all the parameters for combining tasks after they've been scored
    
    >>> from settingsStruct import settingsStruct
    >>> x = combinationParameters(settingsStruct('Test Study/settings.ini'))
    """
    def __init__(self, settings):
        tempParameters = json.load(open(settings['General']['ScoringFile'], 'r'))['CombineTasks']
        self.allParameters = {curParam.keys()[0]:curParam.values()[0] for curParam in tempParameters}
    
    def __iter__(self):
        return self.allParameters.__iter__()

    def __getitem__(self, taskName):
        return self.allParameters[taskName]

    
class ciComputationParameters:
    """
    The class that captures all the parameters for computing ci tasks after they've been scored
    
    >>> from settingsStruct import settingsStruct
    >>> x = ciComputationParameters(settingsStruct('Test Study/settings.ini'))
    """
    def __init__(self, settings):
        tempParameters = json.load(open(settings['General']['ScoringFile'], 'r'))['ComputeCI']
        self.allParameters = {curParam.keys()[0]:curParam.values()[0] for curParam in tempParameters}
    
    def __iter__(self):
        return self.allParameters.__iter__()

    def __getitem__(self, taskName):
        return self.allParameters[taskName]
        
if __name__ == '__main__':
    from settingsStruct import settingsStruct

    x = combinationParameters(settingsStruct('../Test Study/settings.ini'))
    
    for y in x:
        print y