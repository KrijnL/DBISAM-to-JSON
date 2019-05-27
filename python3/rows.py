import struct
import binascii
from datetime import date, timedelta


def get_row_data(file, cols, offset, stream):
    # print('here')

    # First data appears after 26 bytes in the row (first bytes are a hash)
    offset = offset + 25
    file.seek(offset)
    data = {}
    for col in cols:
        byts = file.read(col['length'])
        offset += col['length']
        # print('data')
        # print(binascii.hexlify(byts))

        if col['type'] == 'string':
            buf = ''
            for b in bytearray(byts):
                
                # print(b)
                if b not in [1, 0]:
                    # print(b)
                    buf += chr(b)
            # print(buf.strip())
            val = buf
        if col['type'] == 'float':
            val = struct.unpack('d', byts[1:])[0]
        if col['type'] == 'int':
            val = struct.unpack('i', byts[1:])[0]
        if col['type'] == 'date':
            num = struct.unpack('i', byts[1:])[0]
            if not num == 0:
                d0 = date(1, 1, 1)
                days = timedelta(days=num-1)
                delta = d0 + days
                val = delta
            else:
                val = None

        data[col['name']] = val
    if stream:
        print(data)
    return data
