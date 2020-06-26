
import sys


# 二进制/int转换方法
def byte2int(bytes, signed=True):
    return int().from_bytes(bytes, byteorder='big', signed=signed)


def translate_bytes_struct(bytes, obj):
    byte_offset = 0
    for key, value in obj.items():
        if type(value) == int:
            obj[key] = byte2int(bytes[byte_offset: byte_offset + value])
            byte_offset = byte_offset + value
        else:
            byte_size = value.get('size')
            callback = value.get('callback')
            signed = value.get('signed')

            if callback is not None:
                script = sys.modules[__name__]
                obj[key] = getattr(script, callback)(bytes[byte_offset: byte_offset + byte_size])
            elif signed is not None:
                obj[key] = byte2int(bytes[byte_offset: byte_offset + byte_size], signed)
            else:
                obj[key] = byte2int(bytes[byte_offset: byte_offset + byte_size])

            byte_offset = byte_offset + byte_size