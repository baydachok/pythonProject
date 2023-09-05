import struct


def main(data):
    signature = b'\xe5\x53\x49\x53\x55'
    s = {}
    offset = len(signature)

    # Int32
    s['A1'], s['A2'] = struct.unpack_from("ii", data, offset)
    offset += 8

    # uint16
    s['A3'] = struct.unpack_from('H', data, offset)
    offset += 2

    # Адресс (uint32) структуры B
    b_offset = struct.unpack_from('I', data, offset)
    offset += 4
    s['A4'] = parse_struct_b(data, b_offset)

    # int32
    s['A4'] = struct.unpack_from("i", data, offset)
    offset += 4

    # uint8
    s['A5'] = struct.unpack_from("B", data, offset)
    offset += 1

    return s


def parse_struct_b(data, offset):
    s = {}


    # int64
    s['B1'] = struct.unpack_from("q", data, offset)

    # Структура C
    s['B2'], offset = parse_struct_c(data, offset)

    # Адрес (uint16) структуры G
    g_offset = struct.unpack_from('H', data, offset)
    offset += 2
    s['B3'] = parse_struct_g(data, g_offset)

    return s, offset


def parse_struct_c(data, offset):
    s = {}

    b2_size, offs = struct.unpack_from('H', data, offset)
    b2_offset, offs = struct.unpack_from('H', data, offset)
    b2 = []
    for _ in range(b2_size):
        d_offs, b2_offset = struct.unpack_from('I', b2_offset, data)
        val, _ = parse_struct_d(data, d_offs)
        b2.append(val)

    # uint8
    s['C2'] = struct.unpack_from("B", data, offset)
    offset += 1

    # Структура C
    s['C3'], offset = parse_struct_e(data, offset)

    # Структура F
    s['C4'], offset = parse_struct_f(data, offset)

    s['C5'] = struct.unpack_from("d", data, offset)
    offset += 8

    # Размер (uint16) и адрес (uint32) массива int8
    c_size = struct.unpack_from('H', data, offset)
    offset += 2
    c_offset = struct.unpack_from('I', data, offset)
    offset += 4
    s['C6'] = list(struct.unpack_from(f'<{c_size}B', data, c_offset))

    # int16
    s['C7'] = struct.unpack_from('h', data, offset)
    offset += 2


    return s, offset


def parse_struct_d(data, offset):
    s = {}
    # int32, int16, int16
    s['D1'], s['D2'], s['D3'] = struct.unpack_from('ihh', data, offset)
    offset += 4 + 2 + 2

    # Массив int8, размер 3
    s['D3'] = []
    for i in range(3):
        d3_item, = struct.unpack_from('b', data, offset)
        offset += 1
        s['D3'].append(d3_item)

    # uint16 double
    s['D4'], s['D5'] = struct.unpack_from('Hd', data, offset)
    offset += 2 + 8

    return s

def parse_struct_e(data, offset):
    s = {}
    # int32
    s['E1']= struct.unpack_from('i', data, offset)
    offset += 4

    # Массив int32, размер 6
    s['E2'] = []
    for i in range(6):
        d3_item, = struct.unpack_from('I', data, offset)
        offset += 4
        s['D3'].append(d3_item)

    # Массив int16, размер 4
    s['E3'] = []
    for i in range(4):
        d3_item, = struct.unpack_from('h', data, offset)
        offset += 2
        s['D3'].append(d3_item)

    # uint16, int16
    s['E4'], s['E5'] = struct.unpack_from('Hh', data, offset)
    offset += 2 + 2

    return s

def parse_struct_f(data, offset):
    s = {}
    # int8 int8
    s['F1'], s['F2'] = struct.unpack_from('bb', data, offset)
    offset += 1 + 1

    return s

def parse_struct_g(data, offset):
    s = {}
    # uint16 int8 uint64 uint8
    s['G1'], s['G2'], s['G3'], s['G4'] = struct.unpack_from('HbQB', data, offset)
    offset += 2 + 1 + 4 + 1

    return s


if __name__ == '__main__':
    import json

    x = b'UXXV\x9d\xfd\x1e\xb3`\xbfwA\xb4DZ\x00\x00\x00g+\xcf\xda\x16\x16~,\xdf\x1b'b'n 6\xf9W\xe0\x87\xc5\x08\xd5"H\xe3I\xc1\xbf\xb9\x82\x0b\xa7\x95\xf0\xb4-'b'\xd1\x88\xd6\x12?\x80\x9f\x86>\xad\xb8\xb2?\x17\x00\x00\x00,\x00\x00'b'\x00\xd4\xe9\xf5\x84\xfc\xae\xd0\xec\xa5+mHt,1N\xd6\xa3+$\xef_\xdc'b"\xc5H\x02\x00A\x006`Q\xa0\x1cNM\x02-xj\x80\xc8>\x96'\xd0\xdc\x00\x8f\xd6s"b'\xff\xc5\xa6\x86\xb7\xdd\xc9\x9d\xe2:\xbcA\x13C\xfa\x97\xc4\xcb?V\x90~\x0fA'b'9\xcfI\xe7?\x05\x00I\x00\x00\x007\xbcN\x00'

    res = main(x)
    print(json.dumps(res, sort_keys=True, indent=4))
    print(res)
