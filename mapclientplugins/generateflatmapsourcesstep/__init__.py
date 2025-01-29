
"""
MAP Client Plugin - Generated from MAP Client v0.20.0
"""

__version__ = '0.1.1'
__author__ = 'Hugh Sorby'
__stepname__ = 'Generate Flatmap Sources'
__location__ = 'https://github.com/mapclient-plugins/mapclientplugins.generateflatmapsourcesstep'

# import class that derives itself from the step mountpoint.
from mapclientplugins.generateflatmapsourcesstep import step

# Import the resource file when the module is loaded,
# this enables the framework to use the step icon.
from . import resources_rc
