import OCC.Core.STEPControl as step
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh


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


class STLFile:

    def __init__(self, file_name, binary=True):
        self._file_name = file_name
        self._binary = binary
        # meshing params
        self._linear_deflection = 0.9
        self._angular_deflection = 0.1

    def write(self, shapes):
        writer = StlAPI_Writer()
        writer.SetASCIIMode(not self._binary)
        for idx, shp in enumerate(shapes):
            mesh = BRepMesh_IncrementalMesh(shp.shape(), self._linear_deflection, False, self._angular_deflection, True)
            mesh.Perform()
            if not mesh.IsDone():
                raise SystemExit("Mesh is not done.")  # pragma: no cover
            fn = "{}.{}.stl".format(self._file_name, idx)
            success = writer.Write(shp.shape(), fn)
            if not success:
                raise SystemExit("Failed to write STL file")  # pragma: no cover
