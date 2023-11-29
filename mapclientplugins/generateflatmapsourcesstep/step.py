
"""
MAP Client Plugin Step
"""
import json
import os

from PySide6 import QtGui

from cmlibs.exporter.flatmapsvg import ArgonSceneExporter
from cmlibs.zinc.context import Context

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.generateflatmapsourcesstep.configuredialog import ConfigureDialog


class GenerateFlatmapSourcesStep(WorkflowStepMountPoint):

    def __init__(self, location):
        super(GenerateFlatmapSourcesStep, self).__init__('Generate Flatmap Sources', location)
        self._configured = False  # A step cannot be executed until it has been configured.
        self._category = 'Morphometric'
        # Add any other initialisation code here:
        self._icon = QtGui.QImage(':/generateflatmapsourcesstep/images/morphometric.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#exf_file'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#directory_location'))
        # Port data:
        self._portData0 = None  # http://physiomeproject.org/workflow/1.0/rdf-schema#exf_file
        self._portData1 = None  # http://physiomeproject.org/workflow/1.0/rdf-schema#directory_location
        # Config:
        self._config = {
            'identifier': '',
            'prefix': 'flatmap',
        }

    def execute(self):
        """
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        """
        # Put your execute step code here before calling the '_doneExecution' method.
        self._portData1 = os.path.join(self._location, f"{self._config['identifier']}-generated")
        if not os.path.isdir(self._portData1):
            os.mkdir(self._portData1)

        c = Context('generate_flatmapsvg')
        root_region = c.getDefaultRegion()
        root_region.readFile(self._portData0)

        exporter = ArgonSceneExporter(self._portData1, self._config['prefix'])
        exporter.export_from_scene(root_region.getScene())

        self._doneExecution()

    def setPortData(self, index, dataIn):
        """
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.

        :param index: Index of the port to return.
        :param dataIn: The data to set for the port at the given index.
        """
        self._portData0 = dataIn  # http://physiomeproject.org/workflow/1.0/rdf-schema#exf_file

    def getPortData(self, index):
        """
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.

        :param index: Index of the port to return.
        """
        return self._portData1  # http://physiomeproject.org/workflow/1.0/rdf-schema#directory_location

    def configure(self):
        """
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        """
        dlg = ConfigureDialog(self._main_window)
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.getConfig()

        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        """
        The identifier is a string that must be unique within a workflow.
        """
        return self._config['identifier']

    def setIdentifier(self, identifier):
        """
        The framework will set the identifier for this step when it is loaded.
        """
        self._config['identifier'] = identifier

    def serialize(self):
        """
        Add code to serialize this step to string.  This method should
        implement the opposite of 'deserialize'.
        """
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        """
        Add code to deserialize this step from string.  This method should
        implement the opposite of 'serialize'.

        :param string: JSON representation of the configuration in a string.
        """
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()
