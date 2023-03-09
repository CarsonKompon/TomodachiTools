class lmsInvalidHeader(Exception):
    """An exception that occurs when the header of a file is invalid"""
    pass


class lmsInvalidRevision(Exception):
    """An exception that occurs when the version number is invalid"""
    pass


class lmsInvalidEncoding(Exception):
    """An exception that occurs when the encoding of a file is invalid"""
    pass


class lmsInvalidBOM(Exception):
    """An exception that occurs when the BOM of a file is invalid"""
    pass
