import argparse
from subprocess import call
import os
import copy

TMP_FILE_NAME = 'tmp123.tiff'

COMMAND_CONVERT_PDF_2_TIFF = ['gswin64c', '-dNOPAUSE', '-dBATCH', '-r600', '-sDEVICE=tiffg4']
COMMAND_CONVERT_TIFF_2_HOCR = ['tesseract', '--oem', '2', TMP_FILE_NAME]


def convert(input_file_name, output_dir, first_page, last_page):

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for i in range(first_page, last_page + 1):
        print('\n\n###### Converting page: {0}'.format(i))

        print('\n### Converting PDF to TIFF...\n')

        tmp_command_step_one = copy.deepcopy(COMMAND_CONVERT_PDF_2_TIFF)
        tmp_command_step_one.append('-dFirstPage={0}'.format(i))
        tmp_command_step_one.append('-dLastPage={0}'.format(i))
        tmp_command_step_one.append('-sOutputFile={0}'.format(TMP_FILE_NAME))
        tmp_command_step_one.append(input_file_name)
        call(tmp_command_step_one)

        print('\n### Converting TIFF to hOCR...\n')
        tmp_command_step_two = copy.deepcopy(COMMAND_CONVERT_TIFF_2_HOCR)
        tmp_command_step_two.append('{0}/page_{1}'.format(output_dir, i))
        tmp_command_step_two.append('hocr')
        call(tmp_command_step_two)

        os.remove(TMP_FILE_NAME)

    print('\n\n###### Task finished! ######')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',  '--input_file_name', required=True)
    parser.add_argument('-o',  '--output_dir', required=True)
    parser.add_argument('-fp', '--first_page', type=int, required=True)
    parser.add_argument('-lp', '--last_page', type=int, required=True)
    args = parser.parse_args()

    convert(args.input_file_name, args.output_dir, args.first_page, args.last_page)

if __name__ == '__main__':
    main()

