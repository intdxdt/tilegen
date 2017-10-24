import gdal
import sys
from gdal2tiles import single_threaded_tiling, \
    multi_threaded_tiling, process_args

# TODO:
__doc__globalmaptiles = """
In case you use this class in your product, translate it to another language
or find it useful for your project please let me know.
My email: klokan at klokan dot cz.
"""


def main():
    # TODO: gbataille - use mkdtemp to work in a temp directory
    # TODO: gbataille - debug intermediate tiles.vrt not produced anymore?
    # TODO: gbataille - Refactor generate overview tiles to not depend on self variables
    argv = gdal.GeneralCmdLineProcessor(sys.argv)
    input_file, output_folder, options = process_args(argv[1:])
    nb_processes = options.nb_processes or 1

    if nb_processes == 1:
        single_threaded_tiling(input_file, output_folder, options)
    else:
        multi_threaded_tiling(input_file, output_folder, options)


if __name__ == '__main__':
    main()
