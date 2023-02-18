import json

from ctr.util.data_stream import DataStream

from ctr.lib.lyt.layoutbase import LayoutBase
from ctr.lib.lyt.lyt1 import Lyt1
from ctr.lib.lyt.txl1 import Txl1
from ctr.lib.lyt.fnl1 import Fnl1
from ctr.lib.lyt.mat1 import Mat1
from ctr.lib.lyt.pan1 import Pan1, Bnd1
from ctr.lib.lyt.pic1 import Pic1
from ctr.lib.lyt.txt1 import Txt1
from ctr.lib.lyt.usd1 import Usd1
from ctr.clyt import Clyt

class Bclyt(LayoutBase):
    """A class to represent a BCLYT file."""

    filepath: str = None

    signature: str = None
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
    rootGroup = None
    userDataEntries = None

    def __init__(self, filepath: str = None):
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
            self.signature = data.read_string(4)
            if self.signature != 'CLYT':
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
            isRootPaneSet = False
            isRootGroupSet = False

            # Loop through each section
            for i in range(self.sectionCount):
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
                            self.rootPane = self.layout
                            isRootPaneSet = True
                        
                        if layoutParent is not None:
                            layoutParent.add_child(pane)
                            pane.parent = layoutParent
                        
                        layoutPrevious = pane
                    case 'pic1':
                        # Pass the data to a new Pic1 class to create a new picture
                        pic = Pic1()
                        data = pic.read(data)

                        if layoutParent is not None:
                            layoutParent.add_child(pic)
                            pic.parent = layoutParent
                        
                        layoutPrevious = pic
                    case 'bnd1':
                        # Pass the data to a new Bnd1 class to create a new bounding box
                        bnd = Bnd1()
                        data = bnd.read(data)

                        if layoutParent is not None:
                            layoutParent.add_child(bnd)
                            bnd.parent = layoutParent
                        
                        layoutPrevious = bnd
                    case 'txt1':
                        # Pass the data to a new Txt1 class to create a new text
                        txt = Txt1()
                        data = txt.read(data)

                        if layoutParent is not None:
                            layoutParent.add_child(txt)
                            txt.parent = layoutParent
                        
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
                            wnd.parent = layoutParent
                        
                        layoutPrevious = wnd
                    # TODO: Add usd1, wnd1, pas1, pae1, pts1, grp1, grs1, and gre1 support
                    case _:
                        print("Unknown section magic '" + str(magic) + "' at offset " + str(data.tell() - 4) + "!")

            print(str(self))

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
        string = "{"
        string += f"filepath: {self.filepath}, "
        string += f"signature: {self.signature}, "
        string += f"byteOrderMark: {self.byteOrderMark}, "
        string += f"headerLength: {self.headerLength}, "
        string += f"revision: {self.revision}, "
        string += f"fileSize: {self.fileSize}, "
        string += f"sectionCount: {self.sectionCount}, "
        string += f"padding: {self.padding}, "
        string += f"layoutParams: {str(self.layoutParams)}, "
        string += f"textureList: {str(self.textureList)}, "
        string += f"fontList: {str(self.fontList)}, "
        string += f"materialList: {str(self.materialList)}, "
        string += f"layout: {self.layout}, "
        string += f"rootGroup: {self.rootGroup}, "
        string += f"userDataEntries: {self.userDataEntries}"
        string += "}"
        return string