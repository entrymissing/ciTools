"""
The evaluator classes and functions that scores the data on a task level (i.e. after the items have already been scored)

:Author: David Engel
:Email: entrymissing@gmail.com
"""

from DataStructures.gridScoringStruct import gridScores
from DataStructures.gridAnswerStruct import GridAnswers
from Scoring.brainstormFileInterface import importBrainstormBrickFile, importBrainstormEquationsFile, importBrainstormWordsFile
from Scoring.brainstormScoring import ScoreBrainstorm
from Scoring.textMatchingClasses import typingTextMatcher, typingNumbersMatcher
from Scoring.exportNewItems import exportNewBrainstormItems
from os.path import getsize
from os import linesep
import numpy as np
import csv
import json
import re

#TODO: Split classes to different files

class basicGridTaskEvaluator:
    """
    Basic data evaluation class that just calculates the sum across all items associated with this task. More specific evaluators are derived from this class
    
    >>> from DataStructures.settingsStruct import settingsStruct
    >>> from Scoring.taskScoringClasses import basicGridTaskEvaluator
    >>> from DataStructures.sessionData import readStudy
    >>> from DataStructures.scoringParameters import scoringParameters
    >>> settings = settingsStruct('Test Study/settings.ini')
    >>> gridEvaluator = basicGridTaskEvaluator(settings)
    >>> sessions = readStudy( settings )
    >>> parameters = scoringParameters( settings )
    >>> scores, newAnswers = gridEvaluator.computeScores( sessions, parameters['Sudoku'] )
    >>> scores
    [32, 14, 3, 24, 38]
    """
    def __init__( self, settings ):
        #store the settings and load the gridScores
        self.settings = settings
        self.gridScores = gridScores(settings)

    def computeScores( self, sessions, parameters ):
        #extract the task name and the task prefix from the xmlNode
        taskName = parameters['TaskName']
        itemPrefix = parameters['ItemPrefix']
        
        scores = []
        newAnswers = {}
        
        #cycle the sessions
        for curSession in sessions:
            #open the gridfile and cycle the answers
            curGridAnswers = GridAnswers(curSession['GridItems'])
            taskScore = 0
            
            for curGridItem in curGridAnswers:
                if curGridItem.startswith(itemPrefix.lower().strip()):
                    itemScore = self.gridScores.getScore(curGridItem, curGridAnswers[curGridItem])
                    
                    #decide between new and known items
                    if itemScore == -1:
                        if not curGridItem in newAnswers:
                            newAnswers[curGridItem] = set(curGridAnswers[curGridItem])
                        else:
                            newAnswers[curGridItem].add(curGridAnswers[curGridItem])
                    else:
                        taskScore += itemScore
                        
            scores.append(taskScore)
        return scores, newAnswers
    
class memoryWordsTaskEvaluator:
    def __init__( self, settings ):
        #store the settings and load the wordList with alternative spellings
        self.settings = settings
        tempWordList = json.load(open(settings['Memory']['Memory Words Ground Truth']))
        
        #make everything lowercase and stripped and create a flat list of all known words to find new typos
        self.correctWordList = []
        self.allKnownWords = []
        for curWord in tempWordList:
            self.correctWordList.append( [curSyn.strip().lower() for curSyn in curWord])
            self.allKnownWords.extend([curSyn.strip().lower() for curSyn in curWord])
        self.allKnownWords = set(self.allKnownWords)            

    def computeScores( self, sessions, parameters ):
       #init the results parameters and preload the file postfix
        scores = []
        newAnswers = []
        
        #cycle the sessions
        for curSession in sessions:
            curScore = 0
            sequenceCorrect = True
            
            #open the memory words file
            with open(curSession['memoryWords']) as fp:
                allWords = fp.read()
                allWords = re.findall(r"\w+",allWords)
                allWords = [curWord.lower().strip() for curWord in allWords]
                
                #we cycle the list with correct words and grant one point for each word that has been remembered
                for curIdx, curCorrect in enumerate(self.correctWordList):
                    for curSynonym in curCorrect:
                        if curSynonym in allWords:
                            #if the word is in sequence you get two points if it is out of sequence
                            #you get only one point
                            if parameters['SequenceScoring'] and curIdx == allWords.index(curSynonym) and sequenceCorrect:
                                curScore += 2
                            else:
                                sequenceCorrect = False
                                curScore +=1
                            break
                
            scores.append(curScore)
            newAnswers.extend( list( set(allWords) - self.allKnownWords))
        
        #write out the new words
        with open(self.settings["Memory"]['New Words File'], 'wb') as fp:
            fp.write(linesep.join(list(set(newAnswers))))

        return scores, {}    
    
class detectionTaskEvaluator:
    def __init__( self, settings ):
        #store the settings and load the gridScores
        self.settings = settings
        self.gridScores = gridScores(settings)

    def computeScores( self, sessions, parameters ):
        #extract the task name and the task prefix from the xmlNode
        taskName = parameters['TaskName']
        itemPrefix = parameters['ItemPrefix']
        
        scores = []
        newAnswers = {}
        
        #cycle the sessions
        for curSession in sessions:
            #open the gridfile and cycle the answers
            curGridAnswers = GridAnswers(curSession['GridItems'])
            taskScore = 0
            specialItemAnswers = []
            specialItemFrequencies = []
            
            for curGridItem in curGridAnswers:
                if curGridItem.startswith(itemPrefix.lower().strip()):
                    #get the item score
                    itemScore = self.gridScores.getScore(curGridItem, curGridAnswers[curGridItem])

                    #check if it is one of the special items (i.e. items where you have to find two objects with the same frequency)
                    if curGridItem.startswith(parameters['SpecialItemPrefix'].lower().strip()):
                        specialItemAnswers.append(curGridAnswers[curGridItem])
                        specialItemFrequencies.append(itemScore)
                    else:
                        #add it to the task score if it isn't a -1
                        #We ignore new answers for this task since this is here for legacy reasons only
                        if not itemScore == -1:
                            taskScore += itemScore
            
            #compute the score for the special item
            if not len(specialItemAnswers) == 2:
                pass
            #if they answered the same object for 1 and 2 they get 0 points
            elif specialItemAnswers[0].lower().strip() == specialItemAnswers[1].lower().strip():
                pass
            else:
                #you get a maximum of 3 points and a minimum of 0 points and otherwise the number of points of the difference
                #between the frequencies of the objects you chose
                #e.g. if you picked two different objects with the same frequencies you get 3 points
                taskScore += np.maximum( np.minimum(3,3-abs(specialItemFrequencies[0]-specialItemFrequencies[1])),0)
            scores.append(taskScore)
        return scores, newAnswers


class brainstormTaskEvaluator:
    #TODO add docstring and doctest
    def __init__( self, settings ):
        #store the settings and load the gridScores
        self.settings = settings
        self.loaderFunctions = {'brainstormObject': importBrainstormBrickFile,
								'brainstormBrick': importBrainstormBrickFile,
                                'brainstormWords': importBrainstormWordsFile,
                                'brainstormEquations': importBrainstormEquationsFile}

    def computeScores( self, sessions, parameters ):
        #extract the task name and init the results
        taskName = parameters['TaskName']
        scores = []
        newAnswers = set()
        
        #cycle the sessions
        for curSession in sessions:
            #load the current session with the designated loader
            loaderFunc = self.loaderFunctions[parameters['IniFileSelector']]
            curFilename = curSession[parameters['IniFileSelector']]
            answers = loaderFunc(curFilename)
            
            #score with the designated scoring function
            scorer = ScoreBrainstorm(self.settings, parameters['IniFileSelector'], parameters['ScoreGraded'])
            curScores, curNewAnswers = scorer.getScore(answers)
            scores.append(curScores)
            for curAnswer in curNewAnswers:
                newAnswers.add(curAnswer)
        
        #export the new answers if wanted
        if self.settings['Brainstorming'][parameters['IniFileSelector'] + ' New Answers']:
            exportNewBrainstormItems(list(newAnswers), parameters['IniFileSelector'], self.settings)
        return scores, {}
    
class gameTaskEvaluator:
    #TODO add docstring and doctest
    def __init__( self, settings ):
        self.settings = settings

    def computeScores( self, sessions, parameters ):
        #extract the task name and init the results
        taskName = parameters['TaskName']
        scores = []
        
        #cycle the sessions
        for curSession in sessions:
            #load the metadata file
            curFilename = curSession['metaData']
            with open(curFilename, 'r') as fp:
                csvReader = csv.reader(fp)
                
                #init an indicator to see if the task we are in the metadata section of the task we are looking for
                taskStarted = False
                
                #we also need to keep tracks of how each individual scored on the picked metric
                subScores = []
                
                for curLine in csvReader:
                    #skip empty lines since this is horribly mal formed csv file
                    if len(curLine) < 2:
                        continue
                    #check if we are at the start of the task (the second column has to be the TaskStartIndicator)
                    #if we found it set taskStarted to true and pick the index of the column where the score we want is
                    if curLine[1] == parameters['TaskStartIndicator']:
                        taskStarted = True
                        scoreColumnIndex = curLine.index(parameters['ScoreColumnIndicator'])
                        continue
                    
                    #we are only looking for the row that says totals for now
                    #after we've found the score we break from the loop since we only want the first hit
                    if taskStarted:
                        #if the line start with 'Totals' we#ve reached the end of the task and can
                        #either summarize the individual scores or return the operation on the subscores
                        if curLine[0] == 'Totals':
                            #decide what operation we want to do to compute the score for this team
                            #supported are Totals (the total as computed by the system), mean, min, max, std
                            if parameters['Operation'].lower() == 'totals':
                                scores.append( float(curLine[scoreColumnIndex]) )
                            elif parameters['Operation'].lower() == 'mean':
                                scores.append( np.mean(subScores) )
                            elif parameters['Operation'].lower() == 'std':
                                scores.append( np.std(subScores) )
                            elif parameters['Operation'].lower() == 'max':
                                scores.append( max(subScores) )
                            elif parameters['Operation'].lower() == 'min':
                                scores.append( min(subScores) )
                            else:
                                print 'Operation '  + parameters['Operation'] + ' not supported by gameTaskEvaluator. Returning 0.0'
                                scores.append(0.0)
                            break
                        #otherwise we'll just keep adding the indvidual subscores to the list
                        else:
                            subScores.append(float(curLine[scoreColumnIndex]))
        return scores, {}

class typingTaskEvaluator:
    #TODO add docstring and doctest
    def __init__( self, settings ):
        self.settings = settings

        #init the typing scorer classes
        self.scoringFunctions = {'typingText': typingTextMatcher(settings),
                                'typingNumbers': typingNumbersMatcher(settings)}

    def computeScores( self, sessions, parameters ):
        #extract the task name and init the results
        taskName = parameters['TaskName']
        scores = []
        
        #pick the scoring function
        scoringClass = self.scoringFunctions[parameters['TypingTaskType']]
        
        #cycle the sessions
        for curSession in sessions:
            #load the current session with the designated loader
            curFilename = curSession[parameters['IniFileSelector']]
            
            if parameters['ScoreGraded'] == 'True':
                #score with the designated scoring function
                curScore = scoringClass.getMatchingScore( curFilename )
            else:
                curScore = getsize( curFilename )
            scores.append(curScore)
        return scores, {}

class orderedGridTaskEvaluator:
    #TODO add docstring and doctest
    def __init__( self, settings ):
        #store the settings and load the gridScores
        self.settings = settings
        self.gridScores = gridScores(settings)

    def computeScores( self, sessions, parameters ):
        #extract the task name and the task prefix from the xmlNode
        taskName = parameters['TaskName']
        itemPrefix = parameters['ItemPrefix']
        orderGridPrefix = parameters['OrderItemPrefix']
        
        scores = []
        newAnswers = {}
        
        #cycle the sessions
        for curSession in sessions:
            #open the gridfile and cycle the answers
            curGridAnswers = GridAnswers(curSession['GridItems'])
            taskScore = 0
            orderedItemScores = {}
            
            for curGridItem in curGridAnswers:
                if curGridItem.startswith(itemPrefix.lower().strip()):
                    itemScore = self.gridScores.getScore(curGridItem, curGridAnswers[curGridItem])
                    
                    #check if the item is part of the ordered item
                    if curGridItem.startswith(orderGridPrefix.lower().strip()):
                        if itemScore == -1:
                            orderedItemScores[curGridItem] = ''
                        else:
                            orderedItemScores[curGridItem] = itemScore
                    else:
                        #decide between new and known items
                        if itemScore == -1:
                            if not curGridItem in newAnswers:
                                newAnswers[curGridItem] = set(curGridAnswers[curGridItem])
                            else:
                                newAnswers[curGridItem].add(curGridAnswers[curGridItem])
                        else:
                            taskScore += itemScore
            
            #compute the score for the ordered grid item
            answeredString = ''
            correctString = parameters['CorrectOrder']
            for curOrderedItem in sorted(orderedItemScores):
                answeredString +=orderedItemScores[curOrderedItem]
                
            if len(answeredString) == len(correctString):
                earthMoverDistance = 0
                for curIndex, curAnswer in enumerate(answeredString):
                    earthMoverDistance += abs(curIndex - correctString.index(curAnswer))
 
                #one flip of adjacent items gives 1 point correct answer gives 2 points
                if earthMoverDistance == 0:
                    taskScore += 1
                elif earthMoverDistance == 2:
                    taskScore += 0.5
            scores.append(taskScore)
        return scores, newAnswers


class judgementPagesTaskEvaluator:
    #TODO add docstring and doctest
    def __init__( self, settings ):
        #store the settings and load the gridScores
        self.settings = settings
        self.gridScores = gridScores(settings)

    def computeScores( self, sessions, parameters ):
        #extract the task name and the task prefix from the xmlNode
        taskName = parameters['TaskName']
        itemPrefix = parameters['ItemPrefix']
        scores = []
        newAnswers = {}
        
        #cycle the sessions
        for curSession in sessions:
            #open the gridfile and cycle the answers
            curGridAnswers = GridAnswers(curSession['GridItems'])
            taskScore = 0
            allAnswers = [0,0,0,0]
            
            for curGridItem in curGridAnswers:
                if curGridItem.startswith(itemPrefix.lower().strip()):
                    itemScore = self.gridScores.getScore(curGridItem, curGridAnswers[curGridItem])
                    try:
                        taskScore += 1 - (abs(itemScore - int(curGridAnswers[curGridItem])) / itemScore)
                    except:
                        continue
            scores.append(taskScore)
        return scores, newAnswers

class judgementTaskEvaluator:
    #TODO add docstring and doctest
    def __init__( self, settings ):
        #store the settings and load the gridScores
        self.settings = settings
        self.gridScores = gridScores(settings)

    def computeScores( self, sessions, parameters ):
        #extract the task name and the task prefix from the xmlNode
        taskName = parameters['TaskName']
        itemPrefix = parameters['ItemPrefix']
        taskType = parameters['JudgementType']
        
        #correctAnswers
        correctAnswers = {'Pictures':np.array([6.53, 7.07, 4.91, 8.61, 7.37]),
                            'Slogans': np.array([4.39, 7.24, 7.55, 2.06, 5.92, 6.24]),
                            'Trial': np.array([4.92, 6.5, 4.42, 7.41, 5.16, 4.13])}

        normalizedCorrectAnswers = {'Pictures':np.array([-0.17779216, -0.00625737, -0.5383718, 0.58512163, 0.13729973]),
                            'Slogans': np.array([-0.16106099,  0.2834278,   0.3095566,  -0.55312234,  0.01688634,  0.10431258]),
                            'Trial': np.array([-0.18096256,  0.2374209,  -0.22189502,  0.44637445, -0.06895973, -0.211978])}
        
        scores = []
        newAnswers = {}
        
        #cycle the sessions
        for curSession in sessions:
            #open the gridfile and cycle the answers
            curGridAnswers = GridAnswers(curSession['GridItems'])
            taskScore = 0
            if taskType == 'Pictures':
                allAnswers = [1,1,1,1,1]
            else:
                allAnswers = [1,1,1,1,1,1]
                
            
            for curGridItem in curGridAnswers:
                if curGridItem.startswith(itemPrefix.lower().strip()):
                    itemIndex = int(curGridItem.strip()[-4])
                    if itemIndex > 4 and not taskType == 'Pictures':
                        itemIndex -= 1
                    try:
                        allAnswers[itemIndex-1] = int(curGridAnswers[curGridItem])
                    except:
                        continue
            if parameters['Normalize'] == 'True':
                allAnswers -= np.mean(allAnswers)
                allAnswers /= np.var(allAnswers)
                taskScore = sum(1-abs(np.array(allAnswers)- normalizedCorrectAnswers[taskType]))
            else:
                taskScore = sum(4-abs(np.array(allAnswers)- correctAnswers[taskType]))
            
            scores.append(taskScore)
        return scores, newAnswers
