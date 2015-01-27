"""
This module provides functions to export the chat logs

:Author: David Engel
:Email: entrymissing@gmail.com
"""

from DataStructures.sessionData import readStudy
from os.path import exists
import csv

def exportChatLogsForFile( logFilename, outFilename ):
	with open(logFilename,'rU') as f:
		chatreader=csv.reader(f)
		allchatline=[]
		for row in chatreader:
			if 'Chat' in row[1]: 
				chats = [row[9], row[4], row [2]]
				allchatline.append(chats)
	with open(outFilename, 'wb') as newf:
		chatwriter=csv.writer(newf, delimiter= ',')
		heading=['Date', 'UserID', 'Chat']
		chatwriter.writerow(heading)
		chatwriter.writerows(allchatline)

	
def exportChatLogs( settings ):
    #read the sessions
    sessions = readStudy(settings)

    #cycle the sessions
    for curSession in sessions:
        #call the functions that export the log file for that session
        exportChatLogsForFile(curSession['Logfile'], curSession['ChatLog'])
