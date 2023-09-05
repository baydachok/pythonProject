import struct


class Reader:
    def __init__(self, data, offset):
        self.data = data
        self.offset = offset

    def read_struct_a(self):
        """
        1	Структура B
        2	Структура D
        :return:
        """
        # Чтение структуры B
        field1 = self.read_struct_b()

        # Чтение структуры D
        field2 = self.read_struct_d()

        # Возвращение объекта A
        return {
            'A1': field1,
            'A2': field2
        }

    def read_struct_b(self):
        """
        1	Массив char, размер 8
        2	Массив структур C, размер 4
        """
        # Чтение массива char, размер 8
        field1 = self.data[self.offset:self.offset + 8].decode('ascii')
        self.offset += 8

        # Чтение массива структур C, размер 4
        field2 = []
        for i in range(4):
            field2.append(self.read_struct_c())

        # Возвращение объекта B
        return {
            'B1': field1,
            'B2': field2
        }

    def read_struct_d(self):
        """
        1	double
        2	uint64
        3	uint64
        """
        # Чтение double
        field1, = struct.unpack_from('>d', self.data, self.offset)
        self.offset += 8

        # Чтение uint64
        field2, = struct.unpack_from('>Q', self.data, self.offset)
        self.offset += 8

        # Чтение uint64
        field3, = struct.unpack_from('>Q', self.data, self.offset)
        self.offset += 8

        # Возвращение объекта D
        return {
            'D1': field1,
            'D2': field2,
            'D3': field3
        }

    def read_struct_c(self):
        """
        1	Массив uint8, размер 5
        2	Массив int8, размер 8
        3	uint8
        4	Массив int16, размер 2
        """
        # Чтение массива uint8, размер 5
        field1 = list(struct.unpack_from('>5B', self.data, self.offset))
        self.offset += 5

        # Чтение массива int8, размер 8
        field2 = list(struct.unpack_from('>8b', self.data, self.offset))
        self.offset += 8

        # Чтение uint8
        field3 = struct.unpack_from('>B', self.data, self.offset)[0]
        self.offset += 1

        # Чтение массива int16, размер 2
        field4 = list(struct.unpack_from('>2h', self.data, self.offset))
        self.offset += 4

        # Возвращение объекта C
        return {
            'C1': field1,
            'C2': field2,
            'C3': field3,
            'C4': field4
        }


def main(data):
    s = b'\xf1\x55\x52\x53'
    if not data.startswith(s):
        raise ValueError('Error')
    return Reader(data, 4).read_struct_a()