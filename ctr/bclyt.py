import json

from ctr.util.data_stream import DataStream
from ctr.util.serialize import JsonSerialize

from ctr.lib.lyt.layoutbase import LayoutBase
from ctr.lib.lyt.lyt1 import Lyt1
from ctr.lib.lyt.txl1 import Txl1
from ctr.lib.lyt.fnl1 import Fnl1
from ctr.lib.lyt.mat1 import Mat1
from ctr.lib.lyt.pan1 import Pan1, Bnd1
from ctr.lib.lyt.pic1 import Pic1
from ctr.lib.lyt.txt1 import Txt1
from ctr.lib.lyt.usd1 import Usd1
from ctr.lib.lyt.wnd1 import Wnd1
from ctr.lib.lyt.grp1 import Grp1
from ctr.clyt import Clyt

class Bclyt(LayoutBase):
    """A class to represent a BCLYT file."""

    filepath: str = None

    byteOrderMark: str = None
    headerLength: int = None
    revision: int = None
    fileSize: int = None
    sectionCount: int = None
    padding: int = None

    layoutParams: Lyt1 = None

    textureList: Txl1 = None
    fontList: Fnl1 = None
    materialList: Mat1 = None
    layout = None
    rootPane = None
    rootGroup = None

    def __init__(self, filepath: str = None):
        self.type = 'Layout'
        if filepath is not None:
            self.parse(filepath)

    def parse(self, filepath: str):
        self.filepath = filepath

        # Read the BCLYT file
        with open(filepath, 'rb') as d:

            print("Parsing BCLYT file...")

            # Create a data stream object
            data = DataStream(d)

            # Read the first 4 bytes of the file as a string to check for a valid signature
            signature = data.read_string(4)
            if signature != 'CLYT':
                raise ValueError("Input file specified has an invalid signature! (Expected 'CLYT', got '" + str(self.signature) + "')")
            
            # Read the next 2 bytes to get the byte order mark
            bom = data.read_bytes(2)
            if not (bom == b'\xFE\xFF' or bom == b'\xFF\xFE'):
                raise ValueError("Input file specified has an invalid byte order mark! (Expected b'\\xFE\\xFF' or b'\\xFF\\xFE', got " + str(bom) + ")")
            bom = 'little' if bom == b'\xFE\xFF' else 'big'
            self.byteOrderMark = bom

            # Set the byte order of the data stream
            data.byteOrder = bom

            # Read the next 2 bytes to get the header length
            self.headerLength = data.read_uint16()

            # Read the next 4 bytes to the get the revision
            self.revision = data.read_uint32()

            # Read the next 4 bytes to get the file size
            self.fileSize = data.read_uint32()

            # Read the next 4 bytes to get the number of sections
            self.sectionCount = data.read_uint32()

            # Read the next 4 bytes to check for valid magic
            magic = data.read_string(4)
            if magic != 'lyt1':
                raise ValueError("Input file specified has an invalid magic! (Expected 'lyt1', got '" + str(magic) + "')")
            
            # Pass the data a new Lyt1 class to determine the layout parameters
            self.layoutParams = Lyt1()
            data = self.layoutParams.read(data)

            # Set some variables
            layoutPrevious: LayoutBase = None
            layoutParent: LayoutBase = None
            groupPrevious: LayoutBase = None
            groupParent: LayoutBase = None
            isRootPaneSet = False
            isRootGroupSet = False

            # Clear the children of the layout
            self.children = []

            # Loop through each section
            for i in range(self.sectionCount-1):
                # Read the next 4 bytes to get the magic
                magic = data.read_string(4)
                match magic:
                    case 'txl1':
                        # Pass the data to a new Txl1 class to determine the texture list
                        self.textureList = Txl1()
                        data = self.textureList.read(data)
                    case 'fnl1':
                        # Pass the data to a new Fnl1 class to determine the font list
                        self.fontList = Fnl1()
                        data = self.fontList.read(data)
                    case 'mat1':
                        # Pass the data to a new Mat1 class to determine the material list
                        self.materialList = Mat1()
                        data = self.materialList.read(data)
                    case 'pan1':
                        # Pass the data to a new Pan1 class to create a new pane
                        pane = Pan1()
                        data = pane.read(data)
                        
                        # Set the root pane if it hasn't been set already
                        if not isRootPaneSet:
                            self.rootPane = pane
                            isRootPaneSet = True
                        
                        if layoutParent is not None:
                            layoutParent.add_child(pane)
                        
                        layoutPrevious = pane
                    case 'pic1':
                        # Pass the data to a new Pic1 class to create a new picture
                        pic = Pic1()
                        data = pic.read(data)

                        if layoutParent is not None:
                            layoutParent.add_child(pic)
                        
                        layoutPrevious = pic
                    case 'bnd1':
                        # Pass the data to a new Bnd1 class to create a new bounding box
                        bnd = Bnd1()
                        data = bnd.read(data)

                        if layoutParent is not None:
                            layoutParent.add_child(bnd)
                        
                        layoutPrevious = bnd
                    case 'txt1':
                        # Pass the data to a new Txt1 class to create a new text
                        txt = Txt1()
                        data = txt.read(data)

                        if layoutParent is not None:
                            layoutParent.add_child(txt)
                        
                        layoutPrevious = txt
                    case 'usd1':
                        # Pass the data to a new Usd1 class to create a new user data
                        usd = Usd1()
                        data = usd.read(data)

                        if layoutPrevious is not None:
                            layoutPrevious.add_user_data(usd)
                    case 'wnd1':
                        # Pass the data to a new Wnd1 class to create a new window
                        wnd = Wnd1(self.materialList)
                        data = wnd.read(data)

                        if layoutParent is not None:
                            layoutParent.add_child(wnd)
                        
                        layoutPrevious = wnd
                    case 'pas1':
                        if layoutPrevious is not None:
                            layoutParent = layoutPrevious
                        
                        data.read_uint32() # Unknown?
                    case 'pae1':
                        layoutPrevious = layoutParent
                        layoutParent = layoutPrevious.parent

                        data.read_uint32() # Unknown?
                    case 'pts1':
                        print("PTS1 found! These are seemingly unknown/undocumented... Please let one of the contributors know about this!")
                    case 'grp1':
                        # Pass the data to a new Grp1 class to create a new group
                        grp = Grp1()
                        data = grp.read(data)

                        if not isRootGroupSet:
                            self.rootGroup = grp
                            isRootGroupSet = True
                        
                        if groupParent is not None:
                            groupParent.add_child(grp)
                        
                        groupPrevious = grp
                    case 'grs1':
                        if groupPrevious is not None:
                            groupParent = groupPrevious

                        data.read_uint32() # Padding?
                    case 'gre1':
                        groupPrevious = groupParent
                        groupParent = groupPrevious.parent

                        data.read_uint32() # Padding?
                    case _:
                        print("Unknown section magic '" + str(magic) + "' at offset " + str(data.tell() - 4) + "!")

    def export(self, outpath=None):
        """Exports the BCLYT class as a BCLYT file."""

        # Set the output path to the input path if it's not specified.
        if outpath is None:
            outpath = self.filepath

        # TODO: Implement a BCLYT exporter


    def convertToClyt(self) -> Clyt:
        """Converts the BCLYT class to a CLYT class."""

        # TODO: Implement a BCLYT to CLYT converter once the Clyt class is implemented
    
    def __str__(self) -> str:
        j = JsonSerialize()

        # Add header information
        j.add("byteOrderMark", self.byteOrderMark)
        j.add("headerLength", self.headerLength)
        j.add("revision", self.revision)
        j.add("fileSize", self.fileSize)
        j.add("sectionCount", self.sectionCount)
        j.add("layoutParams", self.layoutParams)

        # Add the texture list if it exists
        if self.textureList is not None:
            j.add("textureList", self.textureList)
        else:
            j.add("textureList", [])
        
        # Add the font list if it exists
        if self.fontList is not None:
            j.add("fontList", self.fontList)
        else:
            j.add("fontList", [])
        
        # Add the material list if it exists
        if self.materialList is not None:
            j.add("materialList", self.materialList)
        else:
            j.add("materialList", [])
        
        # Add the root pane if it exists
        if self.rootPane is not None:
            j.add("rootPane", self.rootPane)
        else:
            j.add("rootPane", [])
        
        # Add the root group if it exists
        if self.rootGroup is not None:
            j.add("rootGroup", self.rootGroup)
        else:
            j.add("rootGroup", [])

        return j.serialize()