import binascii

from col_types import types


def get_col_type(file, offset):
    file.seek(offset + 164)
    byte = file.read(1)
    try:
        col_type = types[byte]['col_type']
        col_length = types[byte]['col_length']
    except:
        print('Unknown field type, can\'t extract data (yet)')
        exit()

    if col_type == 'string':
        file.seek(offset + 166)
        byte = file.read(1)
        col_length = int(binascii.hexlify(byte), 16)+2

    return col_type, col_length


def get_col(file, offset, next_byte):
    col = {}

    num_cols = 0
    file.seek(offset)
    byte = file.read(1)
    if byte == next_byte:
        num_cols += 1
    else:
        return '__DONE__'
    next = offset+2

    buf = ''
    # file.seek(next)
    # byte = file.read(1)

    # Get col type
    col['type'], col['length'] = get_col_type(file, offset)
    # print(col['type'], col['length'])

    # Get col name
    while(True):
        # When we reach \x00, we've reached the end of the title.
        if(byte == b'\x00'):
            break
        # print('read: ' + binascii.hexlify(file.read(1)))
        file.seek(next)
        byte = file.read(1)
        buf += byte.decode()
        # print(byte)
        next += 1
    # Strip beginning \x01 and ending \x00
    col['name'] = buf[1:-1]

    return col


def get_col_names(file):
    # SET values to find first col
    done = False
    offset = 512  # first col has offset 0x200
    nxt = 1

    cols = []

    # GET cols
    while(not done):
        next_byte = chr(nxt)
        col = get_col(file, offset, next_byte)

        if col != '__DONE__':
            cols.append(col)
            nxt += 1
        else:
            done = True
            last_offset = offset

        offset += 768  # next col has offset 0x300

    # print(cols)
    return cols, last_offset
