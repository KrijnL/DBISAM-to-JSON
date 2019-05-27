import struct
from datetime import date, timedelta


def get_row_data(file, cols, offset):

    # First data appears after 26 bytes in the row (first bytes are a hash)
    offset = offset + 25
    file.seek(offset)
    data = {}
    for col in cols:
        byts = file.read(col['length'])
        offset += col['length']

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
