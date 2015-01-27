"""
Loader functions for the brainstorming tasks
Separated out to make it clean

:Author: David Engel
:Email: entrymissing@gmail.com
"""

def importBrainstormWordsFile(filename):
    """
    Import the brainstorming words results from one file and return the brainstormed words
    All returned words are lowercase
    If one line contains several words separated by commas or whitespaces they will returned as separate words
    Order is preserved as in the file
    
    >>> words = importBrainstormWordsFile('Test Study/Data/XVal Session 21 - Group 1/XVal Session 21 - Group 1 - Brainstorm - Words.txt')
    >>> len(words)
    26
    >>> words[0]
    'soon'
    >>> words[-2]
    'spain'
    """
    #init the list with all words in the file
    allWords = []
    
    #open the brainstorming words file and read the lines
    with open(filename, 'r') as fp:
        lines = fp.read().splitlines()
    
    #split the lines for the idiots that didn't read the instructions and add them to the output
    for curLine in lines:
        if curLine.startswith('Please type one'):
            continue
        cutLines = curLine.replace(',',' ').split()
    
        #cycle the word and add them
        for curWord in cutLines:
            allWords.append(curWord.strip().lower())
    
    return allWords


def importBrainstormBrickFile(filename):
    """
    Import the brainstorming brick results from one file
    Empty lines will be ignored
    All uses are lowercase
    Order is preserved as in the file
    
    >>> bricks = importBrainstormBrickFile('Test Study/Data/XVal Session 21 - Group 1/XVal Session 21 - Group 1 - Brainstorm Object - Brick.txt')
    >>> len(bricks)
    20
    >>> bricks[0]
    'build a wall'
    >>> bricks[-2]
    'catapult it'
    """
    #init the list with all bricks in the file
    allBricks = []
    
    #open the brainstorming words file and read the lines
    with open(filename, 'r') as fp:
        lines = fp.readlines()
    
    #cycle strip and clean the lines and add them to the set
    for curLine in lines:
        if curLine.startswith('Enter one user'):
            continue
        if curLine.strip():
            allBricks.append( curLine.strip().lower() )
    
    return allBricks

def importBrainstormEquationsFile(filename):
    """
    Import the brainstormed equations from one file
    Empty lines will be ignored
    All whitespaces will be stripped
    x and X is translated to *
    everything after the = is cut away
    Order is preserved as in the file
    
    >>> equations = importBrainstormEquationsFile('Test Study/Data/XVal Session 21 - Group 1/XVal Session 21 - Group 1 - Brainstorm - Equations.txt')
    >>> len(equations)
    3
    >>> equations[0]
    '6+4'
    >>> equations[-1]
    '2'
    """
    #init the list with all bricks in the file
    allEquations = []
    
    #open the brainstorming words file and read the lines
    with open(filename, 'r') as fp:
        lines = fp.readlines()
    
    #cycle strip and clean the lines and add them to the set
    for curLine in lines:
        if curLine.strip():
            curLine = curLine.strip().replace(' ','').replace('x','*').replace('X','*').split('=')[0]
            allEquations.append( curLine )
    
    return allEquations

def loadBrainstormingCorrectAnswersFile( filename ):
    """
    Load the files that contain correct answers for the brainstorming tasks.
    These files need to be in a human readable format.
    The function returns a synonym table which is a dict linking a category to all the
    words / uses / equations that are acceptable answers for this cateogry
    All categories and synonyms are stripped lower case
    All categories are synonyms for themselves
    
    >>> synonymTable = loadBrainstormingCorrectAnswersFile('Test Study/Scoring/Brainstorming Brick - Correct Answers.txt')
    >>> 'build a patio' in synonymTable['patio']
    True
    >>> all([(curKey in synonymTable[curKey]) for curKey in synonymTable])
    True
    """
    #read the file and init the output struct
    with open(filename, 'r') as fp:
        lines = fp.readlines()
    synonymTable = {}
    curCategory = ''
    
    for curLine in lines:
        #skip empty lines and lines that start with # as they are comments
        curLine = curLine.strip().lower()
        if not curLine or curLine.startswith('#'):
            continue
        
        #the > symbol indicates a new category all other lines are synonys for this cateogry
        if curLine.startswith('>'):
            curCategory = curLine[1:].strip()
            synonymTable[curCategory] = [curCategory]
            continue
        
        synonymTable[curCategory].append(curLine)
    
    return synonymTable

if __name__ == '__main__':
    words = importBrainstormWordsFile('../Test Study/Data/XVal Session 21 - Group 1/XVal Session 21 - Group 1 - Brainstorm - Words.txt')
    print words