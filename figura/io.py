import OCC.Core.STEPControl as step
from OCC.Core.IFSelect import IFSelect_RetDone


class STEPFile:

    def __init__(self, file_name):
        self._file_name = file_name

    def read(self):
        step_reader = step.STEPControl_Reader()
        if step_reader.ReadFile(self._file_name) != IFSelect_RetDone:
            raise SystemExit("Unable to load '{}'".format(self._file_name))
        step_reader.NbRootsForTransfer()
        step_reader.TransferRoot()
        return step_reader.OneShape()

    def write(self, shapes):
        step_writer = step.STEPControl_Writer()
        for shp in shapes:
            step_writer.Transfer(shp.shape(), step.STEPControl_AsIs)
        step_writer.Write(self._file_name)
