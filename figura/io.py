from OCC.Core.STEPControl import (STEPControl_AsIs, STEPControl_Reader)
from OCC.Core.STEPCAFControl import STEPCAFControl_Writer
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.Interface import Interface_Static
from OCC.Core.XCAFDoc import (XCAFDoc_DocumentTool, XCAFDoc_ColorGen)
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.TDataStd import TDataStd_Name
from OCC.Core.TCollection import TCollection_ExtendedString
from OCC.Core.Quantity import Quantity_Color, Quantity_TypeOfColor
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
        step_reader = STEPControl_Reader()
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
        doc = TDocStd_Document(TCollection_ExtendedString("figura-doc"))

        shape_tool = XCAFDoc_DocumentTool.ShapeTool(doc.Main())
        color_tool = XCAFDoc_DocumentTool.ColorTool(doc.Main())
        for shp in shapes:
            label = shape_tool.AddShape(shp.shape(), False)
            if shp.name is not None:
                TDataStd_Name.Set(label, TCollection_ExtendedString(shp.name))

            if shp.color is not None:
                r = shp.color[0]
                g = shp.color[1]
                b = shp.color[2]
                color = Quantity_Color(r, g, b, Quantity_TypeOfColor.Quantity_TOC_RGB)
                color_tool.SetColor(label, color, XCAFDoc_ColorGen)

        writer = STEPCAFControl_Writer()
        Interface_Static.SetCVal("write.step.unit", figura.model.units.upper())
        writer.SetNameMode(True)
        writer.Transfer(doc, STEPControl_AsIs)
        writer.Write(self._file_name)


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


def export(file_name, shapes, file_format='step'):
    """
    Export shapes into a file

    :param file_name: Name of the file
    :param shapes: List of shapes
    :param file_format: File format ['step', 'stl']
    """
    if (isinstance(shapes, list)):
        fmt = file_format.lower()
        if fmt == 'step':
            step = STEPFile(file_name)
            step.write(shapes)
        elif fmt == 'stl':
            stl = STLFile(file_name)
            stl.write(shapes)
        else:
            raise SystemExit("Unknown format {}.".format(file_format))
    else:
        raise TypeError("Parameter 'shapes' must be a list.")
