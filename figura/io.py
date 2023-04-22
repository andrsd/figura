import OCC.Core.STEPControl as step
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.Interface import Interface_Static
import unicodedata
import string
import figura


class STEPFile:

    def __init__(self, file_name):
        """
        STEP file

        :param file_name: The name of the STEP file
        """
        self._file_name = file_name

    def read(self):
        """
        Read the file

        :return: The shape that is contained on the STEP file
        """
        step_reader = step.STEPControl_Reader()
        if step_reader.ReadFile(self._file_name) != IFSelect_RetDone:
            raise SystemExit("Unable to load '{}'".format(self._file_name))
        step_reader.NbRootsForTransfer()
        step_reader.TransferRoot()
        return step_reader.OneShape()

    def write(self, shapes):
        """
        Write shapes into the file

        :param shapes: List of shapes
        """
        step_writer = step.STEPControl_Writer()
        Interface_Static.SetCVal("write.step.unit", figura.model.units.upper())
        for shp in shapes:
            step_writer.Transfer(shp.shape(), step.STEPControl_AsIs)
        step_writer.Write(self._file_name)


class STLFile:

    def __init__(self, file_name, binary=True):
        """
        STL file

        :param file_name:  The name of the STL file
        :param binary: True for binary format, False for ASCII
        """
        if file_name.endswith('.stl'):
            self._file_name = file_name[:-4]
        else:
            self._file_name = file_name
        self._binary = binary
        # meshing params
        self._linear_deflection = 0.9
        self._angular_deflection = 0.1

    def write(self, shapes):
        """
        Write shapes into the file

        :param shapes: List of shapes
        """
        writer = StlAPI_Writer()
        writer.SetASCIIMode(not self._binary)
        for idx, shp in enumerate(shapes):
            mesh = BRepMesh_IncrementalMesh(shp.shape(), self._linear_deflection, False, self._angular_deflection, True)
            mesh.Perform()
            if not mesh.IsDone():
                raise SystemExit("Mesh is not done.")  # pragma: no cover
            if shp.name is None:
                fn = "{}.{}.stl".format(self._file_name, idx)
            else:
                fn = "{} - {}.stl".format(self._file_name, self._clean_shape_name(shp.name))
            success = writer.Write(shp.shape(), fn)
            if not success:
                raise SystemExit("Failed to write STL file")  # pragma: no cover

    def _clean_shape_name(self, file_name):
        valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        cleaned_file_name = unicodedata.normalize('NFKD', file_name).encode('ASCII', 'ignore').decode('ascii')
        return ''.join(c for c in cleaned_file_name if c in valid_filename_chars)
