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


def parse_e(buf, offs):
    e1, offs = parse(buf, offs, 'double')
    e2_size, offs = parse(buf, offs, 'uint32')
    e2_offs, offs = parse(buf, offs, 'uint16')
    e2 = []
    for _ in range(e2_size):
        val, e2_offs = parse(buf, e2_offs, 'int32')
        e2.append(val)
    e3, offs = parse(buf, offs, 'int32')
    f_offset, offs = parse(buf, offs, 'uint32')
    e4, _ = parse_f(buf, f_offset)
    return dict(E1=e1, E2=e2, E3=e3, E4=e4), offs


def parse_f(buf, offs):
    f1, offs = parse(buf, offs, 'float')
    f2, offs = parse(buf, offs, 'int8')
    f3_size, offs = parse(buf, offs, 'uint16')
    f3_offset, offs = parse(buf, offs, 'uint32')
    f3 = []
    for _ in range(f3_size):
        val, f3_offset = parse(buf, f3_offset, 'double')
        f3.append(val)
    f4, offs = parse(buf, offs, 'int64')
    f5, offs = parse(buf, offs, 'double')
    f6 = []
    for _ in range(2):
        val, offs = parse(buf, offs, 'int32')
        f6.append(val)
    f7, offs = parse(buf, offs, 'int32')
    return dict(F1=f1, F2=f2, F3=f3, F4=f4, F5=f5, F6=f6, F7=f7), offs


def parse_d(buf, offs):
    d1, offs = parse(buf, offs, 'int8')
    d2, offs = parse(buf, offs, 'uint8')
    d3, offs = parse(buf, offs, 'uint16')
    return dict(D1=d1, D2=d2, D3=d3), offs


def parse_c(buf, offs):
    c1, offs = parse(buf, offs, 'int8')
    c2, offs = parse(buf, offs, 'float')
    c3 = []
    for _ in range(2):
        val, offs = parse(buf, offs, 'float')
        c3.append(val)
    c4, offs = parse(buf, offs, 'double')
    return dict(C1=c1, C2=c2, C3=c3, C4=c4), offs


def parse_b(buf, offs):
    b1, offs = parse_c(buf, offs)
    b2_size, offs = parse(buf, offs, 'uint32')
    b2_offset, offs = parse(buf, offs, 'uint32')
    b2 = []
    for _ in range(b2_size):
        d_offs, b2_offset = parse(buf, b2_offset, 'uint16')
        val, _ = parse_d(buf, d_offs)
        b2.append(val)
    b3, offs = parse(buf, offs, 'uint8')
    b4, offs = parse(buf, offs, 'int32')
    return dict(B1=b1, B2=b2, B3=b3, B4=b4), offs


def parse_a(buf, offs):
    a1, offs = parse_b(buf, offs)
    a2, offs = parse(buf, offs, 'int64')
    a3, offs = parse_e(buf, offs)
    a4, offs = parse(buf, offs, 'int16')
    a5, offs = parse(buf, offs, 'int64')
    a6, offs = parse(buf, offs, 'int64')
    return dict(A1=a1, A2=a2, A3=a3, A4=a4, A5=a5, A6=a6), offs


def main(stream):
    return parse_a(stream, 5)[0]