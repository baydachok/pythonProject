from struct import *

FMT = dict(
    char='c',
    int8='b',
    uint8='B',
    int16='h',
    uint16='H',
    int32='i',
    uint32='I',
    int64='q',
    uint64='Q',
    float='f',
    double='d'
)


def parse(buf, offs, ty, order='<'):
    pattern = FMT[ty]
    size = calcsize(pattern)
    value = unpack_from(order + pattern, buf, offs)[0]
    return value, offs + size


def parse_g(buf, offs):
    g1, offs = parse(buf, offs, 'uint16')
    g2, offs = parse(buf, offs, 'int8')
    g3, offs = parse(buf, offs, 'uint64')
    g4, offs = parse(buf, offs, 'uint8')
    return dict(G1=g1, G2=g2, G3=g3, G4=g4), offs


def parse_e(buf, offs):
    e1, offs = parse(buf, offs, 'int32')
    e2 = []
    for _ in range(6):
        val, offs = parse(buf, offs, 'int32')
        e2.append(val)
    e3 = []
    for _ in range(4):
        val, offs = parse(buf, offs, 'int16')
        e3.append(val)
    e4, offs = parse(buf, offs, 'uint16')
    e5, offs = parse(buf, offs, 'int16')
    return dict(E1=e1, E2=e2, E3=e3, E4=e4, E5=e5), offs


def parse_f(buf, offs):
    f1, offs = parse(buf, offs, 'int8')
    f2, offs = parse(buf, offs, 'int8')

    return dict(F1=f1, F2=f2), offs


def parse_d(buf, offs):
    d1, offs = parse(buf, offs, 'int32')
    d2, offs = parse(buf, offs, 'int16')
    d3, offs = parse(buf, offs, 'int16')
    d4 = []
    for _ in range(3):
        val, offs = parse(buf, offs, 'int8')
        d4.append(val)
    d5, offs = parse(buf, offs, 'uint16')
    d6, offs = parse(buf, offs, 'double')
    return dict(D1=d1, D2=d2, D3=d3, D4=d4, D5=d5, D6=d6), offs


def parse_c(buf, offs):
    c1_size, offs = parse(buf, offs, 'uint16')
    c1_offset, offs = parse(buf, offs, 'uint16')
    c1 = []
    for _ in range(c1_size):
        d_offs, c1_offset = parse(buf, c1_offset, 'uint32')
        val, _ = parse_d(buf, d_offs)
        c1.append(val)
    c2, offs = parse(buf, offs, 'uint8')
    c3, offs = parse_e(buf, offs)
    c4, offs = parse_f(buf, offs)
    c5, offs = parse(buf, offs, 'double')

    c6_size, offs = parse(buf, offs, 'uint16')
    c6_offs, offs = parse(buf, offs, 'uint32')
    c6 = []
    for _ in range(c6_size):
        val, c6_offs = parse(buf, c6_offs, 'int8')
        c6.append(val)
    c7, offs = parse(buf, offs, 'int16')

    return dict(C1=c1, C2=c2, C3=c3, C4=c4, C5=c5, C6=c6, C7=c7), offs


def parse_b(buf, offs):
    b1, offs = parse(buf, offs, 'int64')
    b2, offs = parse_c(buf, offs)
    g_offset, offs = parse(buf, offs, 'uint16')
    b3, _ = parse_g(buf, g_offset)
    return dict(B1=b1, B2=b2, B3=b3), offs


def parse_a(buf, offs):
    a1, offs = parse(buf, offs, 'int32')
    a2, offs = parse(buf, offs, 'int32')
    a3, offs = parse(buf, offs, 'uint16')
    b_offset, offs = parse(buf, offs, 'uint32')
    a4, _ = parse_b(buf, b_offset)
    a5, offs = parse(buf, offs, 'int32')
    a6, offs = parse(buf, offs, 'uint8')
    return dict(A1=a1, A2=a2, A3=a3, A4=a4, A5=a5, A6=a6), offs


def main(stream):
    return parse_a(stream, 5)[0]


print(main(b'UXXV\x91n\xc6\xe6\xb7\xc3\xbf\x1c\xb5V]\x00\x00\x00\x8a\x1e\x8c\xfa\x81\xa8'
           b'u\xae\xe2\xe5%\xb8\xfc\x8bJ\x0bN\x1e\xb0\xc5-\xe1\x15w\xc3\xbfF\xfe\xab\xd6'
           b'\xc3\xa0w\xb9\xa0\x15\xf2Y\xc0\x18dYo\x8d\xd6\xdc?\x17\x00\x00\x00,\x00\x00'
           b'\x00\xf1\xbf\x9e\x17\xbem\xb9P\x93y\xa5\xbb5c\x96Y=\xee\x9e\x9f\xc8@\x99'
           b'\x83U\xde\xc3\x13\x02\x00A\x00.\x9a\x8d(\x00\x10\x92\x97\xc2 ##\x16\xfe\x92'
           b'\xeb\xeb\x04~\xb0\x12\xf7\x9b\t\x9f_X\xd38:\x06\x91\xd2\x7f#\x93\xb20J'
           b'S\x0c\x88\xe0\xf0\xe9\xd4#]\xe2\xde\xbf\x08\x00I\x00\x00\x00\xde\x15Q\x00'))
