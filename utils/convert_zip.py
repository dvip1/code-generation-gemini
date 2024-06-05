import shutil
import os
def ConvertZip(directory, archive_name):
    output_format = 'zip'
    shutil.make_archive(archive_name, output_format, directory)
    print(f'The archive {archive_name}.{output_format} has been created.')
