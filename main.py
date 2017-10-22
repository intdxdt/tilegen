import gdal
import sys
from gdal2tiles import GDAL2Tiles

#TODO:
__doc__globalmaptiles = """
In case you use this class in your product, translate it to another language
or find it useful for your project please let me know.
My email: klokan at klokan dot cz.
"""


if __name__=='__main__':
    argv = gdal.GeneralCmdLineProcessor( sys.argv )
    if argv:
        gdal2tiles = GDAL2Tiles( argv[1:] )
        gdal2tiles.process()
