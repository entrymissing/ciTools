"""
Provides the functionality for calculating the work and chat contribution of people
from the log files.

:Author: David Engel
:Email: entrymissing@gmail.com
"""

from os import listdir
from os.path import exists, isdir
from csv import reader, writer, QUOTE_ALL

from DataStructures.sessionData import readStudy
import csv
from logFileTools import getStdOfDict
from textblob import TextBlob

def analyzeLogMetrics( logIterable, eventCol = 1, dataCol = 2, subjectCol = 4):
    #init the counters
    chatCounter = 0
    wordCounter = 0
    gridCount = 0
    padCount = 0
    perPersonChatCount = dict()
    perPersonWordCount = dict()
    perPersonTextEdits = dict()
    perPersonGridEdits = dict()
    allChat = ''

    #cycle the log file
    for curLine in logIterable:
        #check if it is chat
        if curLine[eventCol] == 'Chat':
            #figure out who is talking
            curSubject = curLine[subjectCol]
            
            #add the chat line
            allChat += curLine[dataCol] + ' '

            #increment the chat counter and the per person Chat counter
            chatCounter += 1
            if not curSubject in perPersonChatCount:
                perPersonChatCount[curSubject] = 1
            else:
                perPersonChatCount[curSubject] += 1

            #add the number of words to the word counter and the per person word count
            wordCounter += len(curLine[dataCol].split(' '))
            if not curSubject in perPersonWordCount:
                perPersonWordCount[curSubject] = len(curLine[dataCol].split(' '))
            else:
                perPersonWordCount[curSubject] += len(curLine[dataCol].split(' '))

        #check if it is a grid edit line
        if curLine[eventCol] == 'Edit Grid':
            #increment
            gridCount += 1
            
            #figure out who is working
            curSubject = curLine[subjectCol]

            #increment the counter
            if not curSubject in perPersonGridEdits:
                perPersonGridEdits[curSubject] = 1
            else:
                perPersonGridEdits[curSubject] += 1

        #check if it is a grid edit line
        if curLine[eventCol].startswith('Edit pad'):
            #increment
            padCount += 1

            #figure out who is working
            curSubject = curLine[subjectCol]

            #increment the counter
            if not curSubject in perPersonTextEdits:
                perPersonTextEdits[curSubject] = 1
            else:
                perPersonTextEdits[curSubject] += 1
                
    #return the stuff
    return [chatCounter,
            wordCounter,
            gridCount,
            padCount,
            getStdOfDict(perPersonChatCount),
            getStdOfDict(perPersonWordCount),
            getStdOfDict(perPersonGridEdits),
            getStdOfDict(perPersonTextEdits),
            getStdOfDict(perPersonChatCount,False),
            getStdOfDict(perPersonWordCount,False),
            getStdOfDict(perPersonGridEdits,False),
            getStdOfDict(perPersonTextEdits,False),
            perPersonChatCount,
            perPersonWordCount,
            perPersonGridEdits,
            perPersonTextEdits,
            allChat]

def exportLogAnalysis( sessionNames, scores, outFilename ):
    #count the max subjects
    maxSubjects = 0
    for curScores in scores:
        maxSubjects = max([maxSubjects, len(curScores[12]), len(curScores[13]), len(curScores[14]), len(curScores[15])])
    
    resultData = ['Session', 'Number of Active Subjects', 'Total Chat Count', 'Total Chat Word Count', 'Total Grid Edit Count', 'Total Pad Edit Count',
                   'Normalized Std Chat Count', 'Normalized Std Chat Word Count', 'Normalized Std Grid Edits', 'Normalized Std Pad Edits',
                   'Std Chat Count', 'Std Chat Word Count', 'Std Grid Edits', 'Std Pad Edits',
                   'Sentiment Polarity', 'Sentiment Subjectivity']
    resultData += ['SubjectID' + str(curID+1) for curID in range(maxSubjects)]
    resultData += ['Chat Count' + str(curID+1) for curID in range(maxSubjects)]
    resultData += ['Chat Word Count' + str(curID+1) for curID in range(maxSubjects)]
    resultData += ['Pad Edits' + str(curID+1) for curID in range(maxSubjects)]

    resultData += ['Grid SubjectID' + str(curID+1) for curID in range(maxSubjects)]
    resultData += ['Grid Edits' + str(curID+1) for curID in range(maxSubjects)]
            
    resultData = [resultData]
    
    for curSession, curScores in zip(sessionNames, scores):
        curData = [curSession] \
                + [max([len(curVal) for curVal in curScores[12:16]])] \
                + curScores[:12]

        chatBlob = TextBlob(unicode(curScores[16], 'utf-8'))
        curData += [chatBlob.sentiment.polarity, chatBlob.sentiment.subjectivity]

        #find all the subjects
        allSubjects = []
        maxCurSubjects = 0
        for curMetric in [12, 13, 15]:
            if len(curScores[curMetric]) > maxCurSubjects:
                allSubjects = sorted(curScores[curMetric])
                maxCurSubjects = len(curScores[curMetric])

        while len(allSubjects) < maxSubjects:
            allSubjects += ['Missing']
        curData += allSubjects

        for curMetric in [12, 13, 15]:
            curData += [curScores[curMetric][curSbj] if curSbj in curScores[curMetric] else '' for curSbj in allSubjects]
        
        #find all the subjects for grid edits
        allSubjects = sorted(curScores[14])
        while len(allSubjects) < maxSubjects:
            allSubjects += ['Missing']
        curData += allSubjects

        curData += [curScores[14][curSbj] if curSbj in curScores[14] else '' for curSbj in allSubjects]

        resultData.append(curData)
    
    with open(outFilename, 'w+') as fp:
        resCSV = csv.writer(fp, delimiter = ',', quotechar='"', quoting=csv.QUOTE_ALL)
        resCSV.writerows(resultData)


def analyzeLogFiles( settings ):
    """
    Computes all the metrics for all the sessions in a study
    It writes out the metrics to a csv file
    """
    sessions = readStudy(settings)

    allScores = []
    sessionNames = []
    
    for curSession in sessions:
        #open the logfile and pass th csv reader to the analysis function
        with open(curSession['logfile'], 'rU') as fp:
            csvReader = csv.reader(fp)
            csvReader.next()
            
            curMetrics = analyzeLogMetrics( csvReader )
            allScores.append(curMetrics)
            sessionNames.append(curSession.sessionName)

    exportLogAnalysis(sessionNames, allScores, settings['ResultFiles']['logAnalysisFilename'])
    
    