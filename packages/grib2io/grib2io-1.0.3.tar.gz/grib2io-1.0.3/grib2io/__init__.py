from ._grib2io import *
from ._grib2io import __doc__

try:
    from . import __config__
    __version__ = __config__.grib2io_version
except(ImportError):
    pass

__all__ = ['open','Grib2Message','Grib2Metadata','show_config','tables','utils']

def show_config():
    """
    Print grib2io build configuration information.
    """
    from g2clib import __version__ as g2clib_version
    have_jpeg = True if 'jasper' in __config__.libraries or 'openjp2' in __config__.libraries else False
    have_png = True if 'png' in __config__.libraries else False
    jpeglib = 'OpenJPEG' if 'openjp2' in __config__.libraries else ('Jasper' if 'jasper' in __config__.libraries else None)
    pnglib = 'libpng' if 'png' in __config__.libraries else None
    print("grib2io version %s Configuration:\n"%(__version__))
    print("\tg2c library version:".expandtabs(4),g2clib_version)
    print("\tJPEG compression support:".expandtabs(4),have_jpeg)
    if have_jpeg: print("\t\tLibrary:".expandtabs(4),jpeglib)
    print("\tPNG compression support:".expandtabs(4),have_png)
    if have_png: print("\t\tLibrary:".expandtabs(4),pnglib)
