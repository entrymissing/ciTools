"""
Scripts to check the integrity of a study, make sure all the files are downloaded and
produce alerts where duplicate files are found or where files are empty

:Author: David Engel
:Email: entrymissing@gmail.com
"""

from DataStructures.sessionData import readStudy
from os.path import exists, getsize
from os import linesep
from os import sep
from hashlib import md5

#TODO add docstrings and doctest
#TODO fix it to use sessionData instead of compiling filename by hand
def checkSessionIntegrity(session, settings, reportFP, md5Dict):
    for curExpectedFile in settings['FileExtension']:
        if curExpectedFile == 'basepath' or curExpectedFile == 'scriptpath':
            continue
        
        filename = settings['General']['dataFolder'] + session['sessionname'] + sep + session['sessionname'] + ' - ' + settings['FilePrefix'][curExpectedFile] + '.' + settings['FileExtension'][curExpectedFile]
        reportFP.write('<br> {}: '.format(curExpectedFile))

        #check for missing files
        if not exists(filename):
            reportFP.write('<font color = \'red\'>Error ' + filename + ' - File Missing</font>')
            continue

        #check for empty files but add some leeway in case there is just a newline char in there
        if getsize(filename) < 4:
            reportFP.write('<font color = \'orange\'>Warning - File Empty</font>')
            continue

        #open the file and compute the hexdigest
        md5Computer = md5()
        md5Computer.update( open(filename, 'r').read() )
        fileMD5 = md5Computer.hexdigest()
        if fileMD5 in md5Dict:
            reportFP.write('<font color = \'orange\'>Warning - File is a duplicate of {}</font>'.format(md5Dict[fileMD5]))
            continue

        md5Dict[fileMD5] = filename
        reportFP.write('<font color = \'Green\'>Passed - File seems ok</font>'.format(md5Dict[fileMD5]))                       
        
    return md5Dict

def checkStudyIntegrity(settings):
    #read the sessions
    sessions = readStudy(settings)
    
    #open the output file and write the header
    with open(settings['ResultFiles']['integrityCheckFilename'], 'w+') as fp:
        fp.write('<html><head><title>Integrity Checks</title></head><body>' + linesep)
        fp.write('<h2>Integrity Checks for Study {}</h2>'.format(settings['General']['studyName']) + linesep)
        fp.write('<h3>Study contains {} Sessions </h3>'.format(len(sessions)) + linesep)
        fp.write('<h3>Session Integrity Checks: </h3>' + linesep)
        
        #init the md5Dict to check for duplicate files
        md5Dict = {}
        
        #cycle the sessions
        for curSession in sessions:
            fp.write('<h4>Session Name: {}</hh><br>'.format(curSession['sessionname']) + linesep)
            
            #call the functions that export the log file for that session
            md5Dict = checkSessionIntegrity(curSession,settings, fp, md5Dict)