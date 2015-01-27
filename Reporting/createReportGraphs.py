import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams, rc
from radar_chart import radar_factory

def customaxis(ax, c_left='k', c_bottom='k', c_right='none', c_top='none',
               lw=3, size=12, pad=8):

    for c_spine, spine in zip([c_left, c_bottom, c_right, c_top],
                              ['left', 'bottom', 'right', 'top']):
        if c_spine != 'none':
            ax.spines[spine].set_color(c_spine)
            ax.spines[spine].set_linewidth(lw)
        else:
            ax.spines[spine].set_color('none')
    if (c_bottom == 'none') & (c_top == 'none'): # no bottom and no top
        ax.xaxis.set_ticks_position('none')
    elif (c_bottom != 'none') & (c_top != 'none'): # bottom and top
        ax.tick_params(axis='x', direction='out', width=lw, length=7,
                      color=c_bottom, labelsize=size, pad=pad)
    elif (c_bottom != 'none') & (c_top == 'none'): # bottom but not top
        ax.xaxis.set_ticks_position('bottom')
        ax.tick_params(axis='x', direction='out', width=lw, length=7,
                       color=c_bottom, labelsize=size, pad=pad)
    elif (c_bottom == 'none') & (c_top != 'none'): # no bottom but top
        ax.xaxis.set_ticks_position('top')
        ax.tick_params(axis='x', direction='out', width=lw, length=7,
                       color=c_top, labelsize=size, pad=pad)
    if (c_left == 'none') & (c_right == 'none'): # no left and no right
        ax.yaxis.set_ticks_position('none')
    elif (c_left != 'none') & (c_right != 'none'): # left and right
        ax.tick_params(axis='y', direction='out', width=lw, length=7,
                       color=c_left, labelsize=size, pad=pad)
    elif (c_left != 'none') & (c_right == 'none'): # left but not right
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='y', direction='out', width=lw, length=7,
                       color=c_left, labelsize=size, pad=pad)
    elif (c_left == 'none') & (c_right != 'none'): # no left but right
        ax.yaxis.set_ticks_position('right')
        ax.tick_params(axis='y', direction='out', width=lw, length=7,
                       color=c_right, labelsize=size, pad=pad)
        
def getStatsForTeam( dataSet, teamName, taskNames):
    taskScores = []
    for curTask in taskNames:
        curResults = {}
        allScores = dataSet.sliceData(curTask).data
        teamScore = dataSet.sliceData(curTask).getDataForSingleRow(teamName)
        curResults['taskName'] = curTask
        curResults['displayTaskName'] = curTask.replace(' Normalized','')
        curResults['score'] = np.around(teamScore[0],3)
        curResults['meanScore'] = np.around(np.mean(allScores),3)
        curResults['minScore'] = np.around(np.min(allScores),3)
        curResults['maxScore'] = np.around(np.max(allScores),3)
        taskScores.append(curResults)

    return taskScores

        
def renderBarFigure( dFrame, teamName, taskNames, outFileName ):
    #the index of the current team in the dataFrame is needed to access the scores quickly
    teamIndex = list(dFrame.index).index(teamName)
    
    figure = plt.figure()
    yTicks = []
    for curID, curTask in enumerate(taskNames):
        plt.barh(curID+0.5, dFrame[curTask][teamIndex], 0.5, color = 'b')
        plt.plot([np.mean(dFrame[curTask]),np.mean(dFrame[curTask])], [curID+0.4, curID+1.1], 'r', linewidth = 2)
        plt.plot([min(dFrame[curTask]),min(dFrame[curTask])], [curID+0.4, curID+1.1], 'k', linewidth = 2)
        plt.plot([max(dFrame[curTask]),max(dFrame[curTask])], [curID+0.4, curID+1.1], 'k', linewidth = 2)
        yTicks.append(curTask)
    
    plt.yticks([0.75+curVal for curVal in range(len(yTicks))],yTicks)
    customaxis(plt.gca())
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.savefig(outFileName)
    plt.close()

def renderRadarFigure( dFrame, teamName, taskNames, outFileName ):    
    #the index of the current team in the dataFrame is needed to access the scores quickly
    teamIndex = list(dFrame.index).index(teamName)
    scores = [dFrame[curTask][teamIndex] for curTask in taskNames]
    
    font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 25}

    rc('font', **font)

    theta = radar_factory(len(taskNames), frame='polygon')
    fig = plt.figure(figsize=(9, 9))
    plt.axes( projection='radar')
    plt.rgrids([0.1, 1, 2], ['0', '1', '2'])
    plt.plot(theta, scores, color='r', linewidth = 2)
    plt.ylim(-1.5,3)
    plt.gca().set_varlabels(taskNames)
    plt.gca().fill(theta, scores, facecolor='r', alpha=0.25)
    plt.tight_layout(pad=0.4, w_pad=0.8, h_pad=1.0)
    plt.savefig(outFileName)
    plt.close()