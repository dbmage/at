'''Module to allow easy use of AT command'''
import sys
if not (sys.version_info[0] >= 3):
    raise EnvironmentError("This module only supports python3")

if sys.platform == 'win32':
    raise EnvironmentError("This module is not supported on Windows")

from at import runOsCmd, getJobsList, addJob, addJobFromFile, removeJob, clearJobs

__version__ = '1.0.0'
__revision__ = ''
__all__ = ['runOsCmd', 'getJobsList', 'addJob', 'addJobFromFile', 'removeJob', 'clearJobs', '__version__', '__revision__']


