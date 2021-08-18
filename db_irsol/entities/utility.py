# libraries dependencies
import gzip
import shutil
import os


def unzip_file(zip_file_path):

    dir_tmp_unzip = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tmp_unzip")
    file_name = os.path.basename(os.path.normpath(zip_file_path.replace(".gz", ""))) + ".fits"

    unzip_file_path = os.path.join(dir_tmp_unzip, file_name)

    with gzip.open(zip_file_path, 'rb') as f_in:
        with open(unzip_file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    return unzip_file_path
