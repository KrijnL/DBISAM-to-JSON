# Standard Library imports
import sys
import struct
import json
import binascii
import csv
from datetime import date, timedelta

# Local imports
from columns import get_col_names

# def get_col_type(file, offset):
#     file.seek(offset + 164)
#     byte = file.read(1)
#     col_type = ''
#     if byte == '\x02':
#         col_type = 'date'
#         col_length = 5
#     if byte == '\x06':
#         col_type = 'int'
#         col_length = 5
#     if byte == '\x07':
#         col_type = 'float'
#         col_length = 9
#     if byte == '\x01':
#         col_type = 'string'
#         file.seek(offset + 166)
#         byte = file.read(1)
#         col_length = int(binascii.hexlify(byte), 16)+2

#     return col_type, col_length


# def get_col(file, offset, next_byte):
#     col = {}

#     num_cols = 0
#     file.seek(offset)
#     byte = file.read(1)
#     if byte == next_byte:
#         # print(next_byte)
#         num_cols += 1
#     else:
#         return '__DONE__'
#         # print(binascii.hexlify(byte))
#     next = offset+2

#     buf = ''
#     # file.seek(next)
#     # byte = file.read(1)

#     # Get col type
#     col['type'], col['length'] = get_col_type(file, offset)
#     # print(col['type'], col['length'])

#     # Get col name
#     while(True):
#         if(byte == b'\x00'):
#             break
#         # print('read: ' + binascii.hexlify(file.read(1)))
#         file.seek(next)
#         byte = file.read(1)
#         buf += byte.decode()
#         # print(byte)
#         next += 1
#     col['name'] = buf[1:-1]

#     return col


# def get_col_names(file):
#     # SET values to find first col
#     done = False
#     offset = 512  # first col has offset 0x200
#     nxt = 1

#     cols = []

#     # GET cols
#     while(not done):
#         next_byte = chr(nxt)
#         col = get_col(file, offset, next_byte)

#         if col != '__DONE__':
#             cols.append(col)
#             nxt += 1
#         else:
#             done = True
#             last_offset = offset

#         offset += 768  # next col has offset 0x300

#     # print(cols)
#     return cols, last_offset


def get_row_data(file, cols, offset):

    # First data appears after 26 bytes into the row
    offset = offset + 25
    file.seek(offset)
    data = {}
    for col in cols:
        # print(col['name'])
        byts = file.read(col['length'])
        offset += col['length']
        # print(binascii.hexlify(byts))

        if col['type'] == 'string':
            buf = ''
            for b in byts:
                if b not in ['\x00', '\x01']:
                    buf += b.decode('utf-8', 'ignore')
            val = buf
        if col['type'] == 'float':
            # print(binascii.hexlify(byts[1:]))
            val = struct.unpack('d', byts[1:])[0]
        if col['type'] == 'int':
            val = struct.unpack('i', byts[1:])[0]
        if col['type'] == 'date':
            # print(binascii.hexlify(byts[1:]))
            num = struct.unpack('i', byts[1:])[0]
            if not num == 0:
                d0 = date(1, 1, 1)
                days = timedelta(days=num-1)
                delta = d0 + days
                val = delta
            else:
                val = None

        data[col['name']] = val
    return data


def main():
    # READ args
    FILENAME = 'data.dat'
    OUTFILE = 'data.csv'
    if sys.argv[1]:
        if sys.argv[1] == '-h':
            print('converts a Samba .dat file to json format. Currently only works with BHIS*.dat files.')
            print('usage: python read.py <filename> <outfile>')
            exit()
        FILENAME = sys.argv[1]
    # try:
    #     OUTFILE = sys.argv[2]
    # except:
    #     OUTFILE = 'data.csv'

    dataset = []

    with open(FILENAME, 'rb') as file:
        # GET file size
        file.seek(0, 2)
        num_bytes = file.tell()

        # GET column names
        cols, last_offset = get_col_names(file)
        # print(cols, last_offset)

        # GET byte offsets for each row (length is little endian at 0x2D & 0x2E)
        file.seek(45)
        length = file.read(2)
        length_arr = bytearray(length)[::-1]
        row_length = int(bytes(length_arr).encode('hex'), 16)

        # Make list of offsets for cols (every row is 0x50 bytes long )
        offsets = []
        while(last_offset < num_bytes):
            offsets.append(last_offset)
            last_offset += row_length

        # GET data from rows
        for i in range(0, 1):  # len(offsets)-1
            dataset.append(get_row_data(file, cols, offsets[i]))

    # Export to JSON
    def default(o):
        if isinstance(o, date):
            return o.isoformat()

    print(json.dumps(
        dataset,
        sort_keys=True,
        default=default
    ))

    # print(json.dumps(dataset))

if __name__ == '__main__':
    main()
