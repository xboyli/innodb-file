# innodb文件分析，今日头条，零一研究院提供

import sys
import common

# 默认页大小
page_size = 16384

ibd = open(sys.argv[1], 'rb')

FIL_HEADER_DATA = 38
PAGE_HEADER_DATA = 56
PAGE_BODY_DATA = FIL_HEADER_DATA + PAGE_HEADER_DATA

pointer = 0

while True:
    page_bytes = ibd.read(page_size)

    size = len(page_bytes)
    if size == 0:
        break

    file_header = page_bytes[:FIL_HEADER_DATA]

    file_header_struct = {
        'check_sum': 4,
        'page_number': 4,
        'pre_page': 4,
        'next_page': 4,
        'lsn': 8,
        'page_type': 2,
        'flush_lsn': 8,
        'space_id': 4
    }

    common.translate_bytes_struct(file_header, file_header_struct)

    print('page offset:{}, page type:{}({})'.format(hex(pointer),
                                                      file_header_struct['page_type'],
                                                      hex(file_header_struct['page_type'])))
    pointer += size

    # print('File Header:')
    # print('\tcheck sum:', file_header_struct['check_sum'])
    # print('\toffset(page number):', file_header_struct['page_number'])
    # print('\tprevious page:', file_header_struct['pre_page'])
    # print('\tnext page:', file_header_struct['next_page'])
    # print('\tlsn:', file_header_struct['lsn'])
    # print('\tpage type:', file_header_struct['page_type'])
    # print('\tflush lsn:', file_header_struct['flush_lsn'])
    # print('\tspace id:', file_header_struct['space_id'])
    # print('-' * 50, '\n')


ibd.close()
