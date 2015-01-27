import argparse
from LogAnalyzer.logFileAnalyzer import analyzeLogFiles
from DataStructures.settingsStruct import settingsStruct
from LogAnalyzer.chatLogExporter import exportChatLogs
from Scoring.integrityChecks import checkStudyIntegrity
from Scoring.updateBrainstormScoringTables import updateScoringTable
from Scoring.scoreStudy import scoreStudy
from Scoring.computeCI import computeCI
from Reporting.createReports import createReports

def mainFunction( args ):
    #load the settings file
    settings = settingsStruct(args.settingsFile)
    
    #parse the command
    if args.command.lower().strip() == 'loganalysis':
        analyzeLogFiles( settings )

    elif args.command.lower().strip() == 'chatlogs':
        exportChatLogs( settings )

    elif args.command.lower().strip() == 'integritychecks':
        checkStudyIntegrity(settings)

    elif args.command.lower().strip() == 'updatescoringtables':
        updateScoringTable(settings)

    elif args.command.lower().strip() == 'scoring':
        scoreStudy(settings)

    elif args.command.lower().strip() == 'computeci':
        computeCI(settings)

    elif args.command.lower().strip() == 'reporting':
        createReports(settings)

    else:
        print 'Unsopported Command. Please use -h to see a list of all supported commands'    

#TODO add docstring
if __name__ == '__main__':
    #setup the argparser
    acceptedCommands = ['loganalysis', 'chatlogs', 'integritychecks', 'updatescoringtables', 'scoring']
    parser = argparse.ArgumentParser(description='The MCI Scoring and Evaluation Toolbox')
    parser.add_argument("command", help="Action to perform (readme for more details). Options are: " + ', '.join(acceptedCommands), action="store")
    parser.add_argument("settingsFile", help="Settings file that describes the study to perform the action on", action="store")
    args = parser.parse_args()

    #call the main function
    mainFunction( args )

