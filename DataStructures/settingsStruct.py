"""
Parser and classes to provide access to settings files
Extends ConfigParser by adding simplified access to key value pairs
and typed and case-insenstive access to key-value pairs in the sections

:Author: David Engel
:Email: entrymissing@gmail.com
"""

from ConfigParser import ConfigParser
from os.path import dirname, exists, realpath, dirname

class settingsSectionDict():
    """
    A subclass of the settingsStruct that provides case insensitive and typed access to key value pairs
    
    >>> d = settingsSectionDict({'a':'Hello', 'C':'YEs  ', 'd':' nO', 'E':' TRUE  ', 'f':' FaLse  ', 'G':'   100  ', 'H':'  -42.123 '})
    >>> d['a']
    'Hello'
    >>> d['c']
    True
    >>> d['D']
    False
    >>> d['E']
    True
    >>> d['f']
    False
    >>> d['g']
    100
    >>> d['h']
    -42.123
    >>> len(d)
    7
    """
    def __init__(self, d):
        """
        Make sure all keys are lower case to allow case insenstive access to the dict
        """
        self._d = {key.lower():d[key] for key in d }

    def __iter__(self):
        """
        Provide an iterator over the items
        This function is not tested
        """
        return iter(self._d)

    def __len__(self):
        """
        Provide the len function
        """
        return len(self._d)

    def __getitem__(self, key):
        """
        Provide case insentive access to the key value pairs
        Beyond this yes, no, true and false are returned as booleans
        Integers are returned as integers
        Floats are returned as floats
        Everything else is returned as strings (see test coverage on class level)
        """
        #retrieve the value
        curValue = self._d[key.lower().strip()]
        
        #check if the value is a bool
        if curValue.strip().lower() in ['yes','true']:
            return True
        if curValue.strip().lower() in ['no','false']:
            return False
        
        #check if value is a int
        if curValue.strip().isdigit():
            return int(curValue)
        
        #try to convert it to a float
        try:
            curValue = float(curValue)
            return curValue
        except ValueError:
            pass
        
        #return it as a string
        return curValue
    
    def __str__(self):
        """
        Return a string representation of the dict.
        Mainly for debugging reasons
        """
        return str(self._d)
        
class settingsStruct(ConfigParser):
    """
    settingsStruct is derived from ConfigParser, the general settings file parser from Python
    It expects to get passed a setting.ini file that adheres to the standard settings file structure
    We derive it to have easier access to specific settings via two bracket operators. The second
    one is a case insenstive dict to provide stability against some legacy code.
    
    >>> settings = settingsStruct('Test Study/settings.ini')
    >>> settings['FilePrefix']['logFile']
    'LogFile'
    >>> settings['FileExtension']['ChAtLoG']
    'csv'
    """
    #TODO add doctest for basepath and scriptPath

    def __init__(self, filename):
        """
        Since we derive SettingsStruct from ConfigParser which is at the time of writing an old-style class
        we can't use the super method to call the base class constructor. We check with isinstance if it is
        an old-type class. This should provide safety for future improvements of ConfigParser
        """
        if not isinstance(ConfigParser, type):
            ConfigParser.__init__(self)
        else:
            super(settingsStruct, self).__init__()
        self.parseFile(filename)


    def parseFile(self, filename):
        """
        Parse the file that was given. It goes beyond the baseclass function by raising an
        error if the file doesn't exist and furthermore adding the 'basePath' parameter to
        all sections so that you can always use %basePath in the configFile to give relative
        paths on different systems
        """
        if not exists(filename):
            print 'Settings File not found!'
            raise IOError
        
        #read the settings file
        self.read(filename)
        
        #set the variable basePath to the path the settings file is in
        #and the variable scriptPath to the basepath of the script
        for curSection in self.sections():
            self.set(curSection, 'basePath', dirname(filename))
            self.set(curSection, 'scriptPath', dirname(__file__) + '/..')
        
    def __getitem__(self, section):
        """
        Returns a Case insenstive Dict that returns correct types not just values
        Can be accessed via the [] operator.
        This is the way key value pairs should be accessed
        It isn't fast or space efficient since every lookup requires a new dict to be created
        but with the file sizes we are working with this isn't an issue
        """
        parameters = {}
        for curKey in self.options(section):
            parameters[curKey] = self.get(section, curKey)
        return settingsSectionDict(parameters)
    
if __name__ == '__main__':
    settings = settingsStruct('../Test Study/settings.ini')
    print settings['FilePrefix']['logFile']