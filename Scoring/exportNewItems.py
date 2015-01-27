from Scoring.brainstormFileInterface import importBrainstormBrickFile, importBrainstormEquationsFile, importBrainstormWordsFile
import json
from os import linesep

#TODO add docstring and doctest
def exportNewBrainstormItems( newAnswers, taskPrefix, settings ):
    loaderFunctions = { 'brainstormBrick': importBrainstormBrickFile,
						'brainstormObject': importBrainstormBrickFile,
                        'brainstormWords': importBrainstormWordsFile,
                        'brainstormEquations': importBrainstormEquationsFile}

    #load the items we already know to be wrong
    loadFunc = loaderFunctions[taskPrefix]
    wrongAnswers = loadFunc(settings['Brainstorming'][taskPrefix + ' Wrong Answers'])
    
    #create a list of new answers
    newAnswers = [curAnswer for curAnswer in newAnswers if not curAnswer in wrongAnswers]
    
    #open the file for the new answers and write new answers that aren't wrong in there
    with open(settings['Brainstorming'][taskPrefix + ' New Answers'], 'w+') as fp:
        fp.write(linesep.join(newAnswers))

#TODO Add docstring
def exportNewGridAnswers( newAnswers, settings ):
    #make sure all new Answers are lists
    for curTask in newAnswers:
        newAnswers[curTask] = list(newAnswers[curTask])
        
    #export the new answers as json
    with open(settings['Scoring']['New Grid Answers Json'], 'w+') as fp:
        json.dump(newAnswers, fp, indent = 4, sort_keys = True)

    #we also export them as txt file to make it more human readable
    with open(settings['Scoring']['New Grid Answers Txt'], 'w+') as fp:
        for curTask in sorted(newAnswers):
            fp.write(curTask + ':' + linesep)
            for curAnswer in newAnswers[curTask]:
                fp.write('\t' + curAnswer + linesep)
