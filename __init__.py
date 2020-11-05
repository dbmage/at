'''Module to allow easy use of AT command'''
import sys
if not (sys.version_info[0] >= 3):
    raise EnvironmentError("This module only supports python3")

if sys.platform == 'win32':
    raise EnvironmentError("This module is not supported on Windows")

from .at import atsudo, runOsCmd, getJobsList, addJob, addJobFromFile, removeJob, clearJobs

''' Set default logging handler to avoid "No handler found" warnings.
Used code from requests 2.9.1, Copyright Kenneth Reitz'''
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

__version__ = '1.0.1'
__revision__ = ''
__author__ = 'Joe Ash (DBMage)'
__license__ = 'Apache 2.0'
__all__ = ['runOsCmd', 'getJobsList', 'addJob', 'addJobFromFile', 'removeJob', 'clearJobs', '__version__', '__revision__']


