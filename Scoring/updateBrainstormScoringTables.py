"""
Updating the scoring tables. The scoring tables are calculated by counting how many groups got
a specific answer. Each answer is worth 1 point as base value and up to one additional point if
no one found the answer and 0 points if everyone got the answer.
Example: If every group answered one example from the category "build a wall" the score for that will be 1.0
If half the groups answered from the category "use as paperweight" the score will be 1.5

The scoring table is stored as a JSON file representing a list of lists. Each list item contains
a) a list of all synonyms for this category
b) the score for that category

:Author: David Engel
:Email: entrymissing@gmail.com
"""

from brainstormFileInterface import loadBrainstormingCorrectAnswersFile
from DataStructures.sessionData import readStudy
from brainstormFileInterface import importBrainstormBrickFile, importBrainstormEquationsFile, importBrainstormWordsFile
import json

def updateScoringTable(settings):
    """
    Function that get's called to update the scoring tables. Calls the function that does that,
    takes the new scoring table as the return value and writes it to the output file.
    This setup is done to allow for proper unit testing without involving the writing out step
 
    The scoring table is stored as a JSON file representing a list of lists. Each list item contains
    a) a list of all synonyms for this category
    b) the score for that category
    
    The JSON file is written to the file designated in the settings file   
    """
    #setup the loader functions
    loaderFunctions = {'brainstormbrick':importBrainstormBrickFile,
                       'brainstormobject': importBrainstormBrickFile,
                       'brainstormwords':importBrainstormWordsFile,
                       'brainstormequations':importBrainstormEquationsFile}

    #cycle the tasks that we need to regenerate the scoring tables for
    for curBrainstormTask in settings['Update Brainstorming Scoring Tables']:
        if settings['Update Brainstorming Scoring Tables'][curBrainstormTask] == True:
            #call the calculation function
            scoringTable = calculateScoringTable(settings, curBrainstormTask)

            #dump the table
            outFile = settings['Brainstorming'][curBrainstormTask + ' Scoring Table']
            with open(outFile, 'w+') as fp:
                json.dump( scoringTable, fp, indent = 4)
            
def calculateScoringTable(settings, curBrainstormTask):
    """
    Updating the scoring tables. The scoring tables are calculated by counting how many groups got
    a specific answer. Each answer is worth 1 point as base value and up to one additional point if
    no one found the answer and 0 points if everyone got the answer.
    Example: If every group answered one example from the category "build a wall" the score for that will be 1.0
    If half the groups answered from the category "use as paperweight" the score will be 1.5
    
    The function gets the settings structure and the name of the brainstorming task.
    Allowed brainstorming tasks are the ones that have loader Functions and parameters in the
    settings file
    
    The function returns a scoring table
    >>> from DataStructures.settingsStruct import settingsStruct
    >>> settings = settingsStruct('Test Study/settings.ini')
    >>> scoringTable = calculateScoringTable(settings, 'brainstormbrick')
    >>> scoringTable[2]
    [['bang open', 'use to open something up (banging it)'], 2.0]
    """
    sessions = readStudy(settings)
    
    #setup the loader functions
    loaderFunctions = {'brainstormbrick':importBrainstormBrickFile,
                       'brainstormobject': importBrainstormBrickFile,
                       'brainstormwords':importBrainstormWordsFile,
                       'brainstormequations':importBrainstormEquationsFile}

    #load the synonym table for the correct answers
    correctAnswerFile = settings['Brainstorming'][curBrainstormTask + ' Correct Answers']
    synonymTable = loadBrainstormingCorrectAnswersFile( correctAnswerFile )
    
    #init the loader func
    loaderFunc = loaderFunctions[curBrainstormTask]
    
    #initialze the scoring table which is a list of cateogories containing score and list of synonyms
    scoringTable = []
    for curCategory in synonymTable:
        scoringTable.append([synonymTable[curCategory],0.0])
        
    #cyce the sessions and count how often each category occurs
    for curSession in sessions:
        #load the file
        allAnswers = loaderFunc( curSession[curBrainstormTask])
        
        #cycle answers and categories and count how often each occurs
        for curIndex in xrange(len(scoringTable)):
            for curAnswer in allAnswers:
                if curAnswer in scoringTable[curIndex][0]:
                    scoringTable[curIndex][1] += 1
                    break

    #cycle categories and normalize the counts
    for curIndex in xrange(len(scoringTable)):
        tempI = scoringTable[curIndex][1]
        if scoringTable[curIndex][1] > 0:
            scoringTable[curIndex][1] = 2.0 - ((scoringTable[curIndex][1]-1) / float(len(sessions)))
        else:
            scoringTable[curIndex][1] = 2.0

    return scoringTable
