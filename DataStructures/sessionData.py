"""
Data structures to capsulate all data of a specific session

:Author: David Engel
:Email: entrymissing@gmail.com
"""

from os import listdir
from os.path import isdir, basename, exists
import csv

class sessionData:
    """
    Serves as an abstraction of all the data associated with a specific session
    Specifically it offers a standardized way to access the files for each task
    
    >>> import settingsStruct
    >>> settings = settingsStruct.settingsStruct('Test Study/settings.ini')
    >>> data = sessionData( 'XVal Session 21 - Group 1', settings)
    >>> data['logfile'].endswith('XVal Session 21 - Group 1/XVal Session 21 - Group 1 - LogFile.csv')
    True
    >>> data.sessionName
    'XVal Session 21 - Group 1'
    >>> data = sessionData( 'XVal Session 2 - Group 1', settings)
    Traceback (most recent call last):
    .
    IOError
    """
    def __init__(self, sessionName, settings):
        """
        Just pass the constructor on to the load Folder function
        """
        self.loadFolder(sessionName, settings)
    
    def loadFolder(self, sessionName, settings):
        """
        Check that the folder exists and create a dict that maps the expected files to actual filenames
        If the folder does not exist raise an exception
        But we don't ensure that all files actually exist
        """
        self.folder = settings['General']['datafolder'] + sessionName
        if not exists(self.folder):
            print 'Error in sessionData: Folder {} does not exist'.format(self.folder)
            raise IOError
        self.sessionName = sessionName
        self.datafolder = settings['General']['datafolder']
        self.parameters = {'sessionname':sessionName}
        
        for curParam in settings['FilePrefix']:
            self.parameters[curParam.lower().strip()] = self.datafolder + self.sessionName + '/' + self.sessionName + ' - ' + settings['FilePrefix'][curParam] + '.' + settings['FileExtension'][curParam]

    def __getitem__(self, key):
        """
        Access to the filenames is provided via the [] operator
        """
        return self.parameters[key.lower().strip()]

def readStudy( settings ):
    """
    Read study returns all the sessions as a list of sessionData
    The sessions will be in alphabetical order in the returned list
    
    >>> import settingsStruct
    >>> settings = settingsStruct.settingsStruct('Test Study/settings.ini')
    >>> sessions = readStudy( settings )
    >>> len(sessions)
    5
    >>> [curSession.sessionName for curSession in sessions]
    ['XVal Session 21 - Group 1', 'XVal Session 23 - Group 1', 'XVal Session 24 - Group 1', 'XVal Session 25 - Group 1', 'XVal Session 26 - Group 1']
    >>> settings = settingsStruct.settingsStruct('Test Study/settingsSubset.ini')
    >>> sessions = readStudy( settings )
    >>> len(sessions)
    3
    >>> [curSession.sessionName for curSession in sessions]
    ['XVal Session 21 - Group 1', 'XVal Session 23 - Group 1', 'XVal Session 26 - Group 1']
    """
    #if the sessionDataFile is false we are taking everything in the data folder
    if not settings['General']['sessionDataFile']:
        allSessions = [curFolder for curFolder in listdir(settings['General']['datafolder']) if isdir(settings['General']['datafolder'] + curFolder)]
    #otherwise we load the spreadsheet and load only the folders that have the flag set
    else:
        allSessions = []
        with open(settings['General']['sessionDataFile'], 'rU') as fp:
            csvReader = csv.reader(fp)
            headers = csvReader.next()
            selectionIndex = headers.index(settings['General']['sessionSelector'])
            
            for curLine in csvReader:
                if curLine[selectionIndex] == '1' and curLine[0]:
                    allSessions.append(curLine[0])

    #read in the folders
    return [sessionData(curFolder, settings) for curFolder in sorted(allSessions)]

if __name__ == '__main__':
    import settingsStruct
    settings = settingsStruct.settingsStruct('../Test Study/settings.ini')
    sessions = readStudy( settings )
    data = sessionData( 'XVal Session 21 - Group 1', settings)
    print data['logfile']