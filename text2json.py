import os
import re
import argparse

def read_document(input_dir):
    data = []
    if input_dir[-1] != '/':
        input_dir = input_dir + '/'
    file_names = os.listdir(input_dir)
    for file in file_names:
        with open(input_dir + file) as f:
            data.append(f.readlines())
    return data


def remove_ending_empty_lines_from_page(page):
    while page[1] == '\n':
        del page[-1]

def remove_ending_empty_lines_from_document(data):
    for page in data:
        remove_ending_empty_lines_from_page(page)
    return data


def remove_footnotes_from_document(data):
    for page in data:
        fully_scanned = False
        while not fully_scanned:
            fully_scanned = True
            counter = 0
            for line in reversed(page):
                counter += 1
                if '\n' == line:
                    break
                elif re.match('^\d\s', line):
                    del page[-counter:]
                    remove_ending_empty_lines_from_page(page)
                    fully_scanned = False
                    break


def remove_footnotes_with_star(data):
    for page in data:
        counter = 0
        for line in page:
            if re.match('^\*\s', line):
                break
            counter += 1
        del page[counter:]
        remove_ending_empty_lines_from_page(page)


def remove_headers_from_document(data):
    for page in data:
        counter = 0
        for line in page:
            counter += 1
            if '\n' == line:
                del page[:counter]
                break


def join_pages(data):
    result = []
    for page in data:
        result = result + page
    return result


def clean_document(document):
    remove_ending_empty_lines_from_document(document)
    remove_footnotes_from_document(document)
    remove_headers_from_document(document)
    remove_footnotes_with_star(document)
    document_as_one_page = join_pages(document)
    return document_as_one_page


def save_document(document, output_file):
    f = open(output_file, 'w')
    f.writelines(document)
    f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', required=True)
    parser.add_argument('-o', '--output_file', required=True)
    args = parser.parse_args()

    document = read_document(args.input_dir)
    document_as_one_page = clean_document(document)
    save_document(document_as_one_page, args.output_file)
    print('File cleaned and saved!')


if __name__ == '__main__':
    main()
