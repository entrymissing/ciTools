import json

class ScoreBrainstorm:
    #TODO: add docstring and document score graded
    """
    >>> from DataStructures.settingsStruct import settingsStruct
    >>> settings = settingsStruct('Test Study/settings.ini')
    >>> scorer = ScoreBrainstorm(settings, 'brainstormBrick')
    >>> scorer.getScore(['prop up a bed', 'prop up a chair'])
    (1.8, [])
    >>> scorer.getScore(['something new'])
    (0.0, ['something new'])
    >>> scorer.getScore([' dIg ', ' digA hole  '])
    (2.0, [])
    >>> scorer.getScore([' dIg ', ' digA hole  ', 'prop up a bed', 'something new'])
    (3.8, ['something new'])
    >>> scorer = ScoreBrainstorm(settings, 'brainstormEquations')
    >>> scorer.getScore(['2+8'])
    (1.8, [])
    >>> scorer.getScore(['2+8*3'])
    (0.0, ['2+8*3'])
    >>> scorer = ScoreBrainstorm(settings, 'brainstormWords')
    >>> scorer.getScore(['sun', 'selection'])
    (3.6, [])
    >>> scorer.getScore(['2+8*3'])
    (0.0, ['2+8*3'])
    """
    def __init__(self, settings, brainstormType, scoreGraded = 'True' ):
        self.loadScoringTable( settings, brainstormType, scoreGraded )
    
    def loadScoringTable(self, settings, brainstormType, scoreGraded):
        #load the scoring table and remove all whitespaces
        with open(settings['Brainstorming'][brainstormType + ' Scoring Table'], 'r') as fp:
            self.scoringTable = json.load(fp)
        for curIndex in xrange(len(self.scoringTable)):
            self.scoringTable[curIndex] = [[curAns.replace(' ','').lower().strip() for curAns in self.scoringTable[curIndex][0]], self.scoringTable[curIndex][1]]
        self.scoreGraded = scoreGraded
    
    def getScore( self, brickUsages ):
        #determine the scores
        score = 0.0
        for curSynonym in self.scoringTable:
            for curUsage in brickUsages:
                if curUsage.strip().lower().replace(' ','') in curSynonym[0]:
                    if self.scoreGraded == 'True':
                        score += curSynonym[1]
                    else:
                        score += 1
                    break
        
        #determine which usages are new
        newItems = []
        for curUsage in brickUsages:
            found = False
            for curSynonym in self.scoringTable:
                if curUsage.strip().lower().replace(' ','') in curSynonym[0]:
                    found = True
                    break
            if not found:
                newItems.append(curUsage)
        
        return score, newItems
    
