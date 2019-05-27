#!/usr/bin/env python
# Standard Library imports
import json
import csv
import argparse
import sys
from datetime import date

# Local imports
from columns import get_col_names
from rows import get_row_data


def parse_args():
    parser = argparse.ArgumentParser(description='converts a DBISAM .dat file to JSON format')
    parser.add_argument('filename', help='the .dat file you want to extract data from')
    parser.add_argument('-j', '--json', help='print output in JSON format', action='store_true')
    parser.add_argument('-c', '--csv', help='create a csv file containing the output')
    parser.add_argument('-o', '--out', help='instead of printing to stdout, save data to file.')
    parser.add_argument('-s', '--stream', help='print data row by row while it\'s being read', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()

    form = 'json'
    outfile = False
    # READ args
    if(args.json and args.csv):
        print('cannot use -j and -c options together')
        sys.exit(1)
    elif args.csv:
        form = 'csv'
        outfile = args.csv
    if args.out:
        outfile = args.out

    # READ .DAT file
    FILENAME = args.filename

    dataset = []

    with open(FILENAME, 'rb') as file:
        # GET file size
        file.seek(0, 2)
        num_bytes = file.tell()

        # GET column names
        cols, last_offset = get_col_names(file)

        # GET byte offsets for each row (row length is located little endian at 0x2D & 0x2E)
        file.seek(45)
        length = file.read(2)
        print(length)
        length_arr = bytearray(length)[::-1]
        row_length = int(bytes(length_arr).hex(), 16)
        print(row_length)

        # Make list of offsets for cols
        offsets = []
        while(last_offset < num_bytes):
            offsets.append(last_offset)
            last_offset += row_length

        # print(offsets)
        print(cols)
        # GET data from rows
        for i in range(0, len(offsets)-1):  # len(offsets)-1
            dataset.append(get_row_data(file, cols, offsets[i], args.stream))

    # EXPORT
    if args.stream:
        return
    else:
        # Make a list of keys for csv export
        keys = []
        for col in cols:
            keys.append(col['name'])
        # Make a list of arguments for exporting
        arguments = {}
        arguments['form'] = form
        arguments['file'] = outfile
        export(dataset, keys, arguments)


def export(dataset, keys, args):
    if args['form'] == 'json':
        def default(o):
            if isinstance(o, date):
                return o.isoformat()

        output = json.dumps(
            dataset,
            sort_keys=True,
            default=default
        )
    if args['file']:
        with open(args['file'], 'w') as file:
            if args['form'] == 'csv':
                # EXPORT TO CSV
                writer = csv.DictWriter(file, fieldnames=keys)

                writer.writeheader()
                for d in dataset:
                    writer.writerow(d)
            else:
                file.write(output)
                return
    else:
        # return
        print(output)

if __name__ == '__main__':
    main()
