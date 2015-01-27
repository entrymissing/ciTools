"""
This module provides functions for the log file analysis tool

:Author: David Engel
:Email: entrymissing@gmail.com
"""

import numpy as np

def getStdOfDict( counts, normalize = True ):
    """
    Get the standard deviation of a dictonary of edit counts. This function gets
    as count parameter a dictonary with keys of usernames and values the number of
    their edits and return the normalized or unnormalized standard deviation of
    those edits.
    
    >>> getStdOfDict({'a':100, 'b':100, 'c':100, 'd':100})
    0.0
    >>> getStdOfDict({'a':100, 'b':100, 'c':100, 'd':100}, False)
    0.0
    >>> getStdOfDict({'a':1, 'b':1, 'c':0, 'd':0})
    0.25
    >>> getStdOfDict({'a':1, 'b':1, 'c':0, 'd':0},False)
    0.5
    """
    
    #get the counts from the dict
    counts = np.array([counts[curKey] for curKey in counts], 'f')

    #check for zeros and no people
    if len(counts) == 0 or sum(counts) == 0:
        return 0

    #normalize if demanded
    if normalize:
        counts /= sum(counts)

    #return the variance
    return np.std(counts)
