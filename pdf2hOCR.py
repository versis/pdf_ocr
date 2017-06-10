import argparse
from subprocess import call
import os

TMP_FILE_NAME = 'tmp123.tiff'


def convert(input_file_name, output_file_name, first_page=None, last_page=None):

    command_convert_pdf2tiff = ['gswin64c', '-dNOPAUSE', '-dBATCH', '-r600', '-sDEVICE=tiffg4', '-sOutputFile=' + TMP_FILE_NAME]
    command_convert_tiff2hocr = ['tesseract', '--oem', '2', TMP_FILE_NAME, output_file_name, 'hocr']

    if first_page is not None:
        command_convert_pdf2tiff.append('-dFirstPage=' + first_page)

    if last_page is not None:
        command_convert_pdf2tiff.append('-dLastPage=' + last_page)

    command_convert_pdf2tiff.append(input_file_name)

    print('\n\n### Converting PDF to TIFF...\n')
    call(command_convert_pdf2tiff)

    print('\n\n### Converting TIFF to hOCR...\n')
    call(command_convert_tiff2hocr)
    os.remove(TMP_FILE_NAME)

    print('\n\n### Task finished!')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',  '--input_file_name',  required=True)
    parser.add_argument('-o',  '--output_file_name', required=True)
    parser.add_argument('-fp', '--first_page',       required=False)
    parser.add_argument('-lp', '--last_page',        required=False)
    args = parser.parse_args()

    convert(args.input_file_name, args.output_file_name, args.first_page, args.last_page)

if __name__ == '__main__':
    main()
