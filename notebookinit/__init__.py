"""
breaking changes:
    0.0.3: 2023-04-07
        * the make_log() function now returns the log.info function instead of the log object itself.
            This means that one can now do `log('hello')` instead of `log.info('hello')`
"""
__version__ = "0.0.3"
from .notebookinit import *


def welcome():
    print('welcome -- notebookinit post-install function running from __init__.py')
