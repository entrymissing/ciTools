from DataStructures.sessionData import readStudy
import pandas
import numpy as np
import jinja2
from createReportGraphs import renderBarFigure, renderRadarFigure
import os

def createReports(settings):
    #we need a custom envirnoment to deal with latex templates
    report_renderer = jinja2.Environment(
      block_start_string = '%{',
      block_end_string = '%}',
      variable_start_string = '%{{',
      variable_end_string = '%}}',
      comment_start_string = '((=',
      comment_end_string = '=))',
      loader = jinja2.FileSystemLoader(settings['Reporting']['Reporting Template Folder'])
        )

    #load the sessions and the dataFrame
    sessions = readStudy( settings )
    dFrame = pandas.DataFrame.from_csv(settings['ResultFiles']['scoresFilename'])
    dFrame2 = pandas.DataFrame.from_csv(settings['Reporting']['Additional Scores File'])
    dFrame = dFrame.join(dFrame2)
    dFrame.index = [str(curIdx) for curIdx in dFrame.index]
    
    #open the template and read it
    template = report_renderer.get_template(settings['Reporting']['Reporting Template Filename'])

    #create the dict with all the summary parameters
    summaryDict = {}
    for curTask in dFrame:
        try:
            summaryDict[curTask.replace(' ','_') + '_Mean'] = np.mean(dFrame[curTask])
            summaryDict[curTask.replace(' ','_') + '_Median'] = np.median(dFrame[curTask])
            summaryDict[curTask.replace(' ','_') + '_Max'] = max(dFrame[curTask])
            summaryDict[curTask.replace(' ','_') + '_Min'] = min(dFrame[curTask])
            summaryDict[curTask.replace(' ','_') + '_Std'] = np.std(dFrame[curTask])
            summaryDict[curTask.replace(' ','_') + '_Var'] = np.var(dFrame[curTask])
        except:
            continue
        
    #cycle the session
    for curSession in sessions:
        print curSession.sessionName
        #the index of the current team in the dataFrame is needed to access the scores quickly
        teamIndex = list(dFrame.index).index(curSession.sessionName)
        
        #render the graphs
        reportingTaskNames = ['Typing', 'Sudoku Solving', 'Matrix Reasoning',
                              'Unscrambling', 'Memory', 'Brainstorming',
                              'Games']
        renderBarFigure(dFrame, curSession.sessionName, reportingTaskNames, settings['Reporting']['Reporting Folder'] + 'Images/Bar-' + curSession.sessionName.replace(' ','_') + '.pdf' )
        reportingTaskNames = ['Executing','Generating','Memorizing','Choosing']
        renderRadarFigure(dFrame, curSession.sessionName, reportingTaskNames, settings['Reporting']['Reporting Folder'] + 'Images/Radar-' + curSession.sessionName.replace(' ','_') + '.pdf' )
        
        #create the valueDict for jinja starting from a copy of the summary statistics
        valueDict = summaryDict.copy()
        
        #add session name and the file names of the created figures
        valueDict['sessionName'] = curSession.sessionName
        valueDict['barFigureFilename'] = 'Bar-' + curSession.sessionName.replace(' ','_') + '.pdf'
        valueDict['radarFigureFilename'] = 'Radar-' + curSession.sessionName.replace(' ','_') + '.pdf'
        for curTask in dFrame:
            valueDict[curTask.replace(' ','_')] = dFrame[curTask][teamIndex]
        
        #write the output file
        with open(settings['Reporting']['Reporting Folder'] + curSession.sessionName + '.' + settings['Reporting']['Reporting Template Filename'].split('.')[-1], 'w+') as fp:
            fp.write(template.render(valueDict))
            
            
            
