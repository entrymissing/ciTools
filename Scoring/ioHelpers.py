#TODO: Docstring and tests
def importTextFile( filename ):
    #read the file, remove empty lines and strip everything
    with open(filename, 'r') as fp:
        lines = fp.read().splitlines()
        lines = [curLine.strip() for curLine in lines if curLine.strip()]

    return lines
