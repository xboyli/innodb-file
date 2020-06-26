# innodb文件分析，今日头条，零一研究院提供

import sys
import common


def translate_bnode_page():
    print('BNode Page Header:')
    page_header = page_bytes[FIL_HEADER_DATA:PAGE_BODY_DATA]

    page_header_struct = {
        'n_slot': 2,
        'heap_top': 2,
        'n_heap': {'size':2, 'signed':False},
        'free': 2,
        'garbage': 2,
        'last_insert': 2,
        'direction': 2,
        'n_direction': 2,
        'n_recs': 2,
        'tx_id': 8,
        'level': 2,
        'index_id': 8,
        'btr_leaf': 10,
        'btr_top': 10
    }

    common.translate_bytes_struct(page_header, page_header_struct)

    print('\tn slot:', page_header_struct['n_slot'])
    print('\theap top:', page_header_struct['heap_top'])
    print('\tn heap:', page_header_struct['n_heap'])
    print('\tfree:', page_header_struct['free'])
    print('\tgarbage:', page_header_struct['garbage'])
    print('\tlast insert:', page_header_struct['last_insert'])
    print('\tdirection:', page_header_struct['direction'])
    print('\tn direction:', page_header_struct['n_direction'])
    print('\tn recs:', page_header_struct['n_recs'])
    print('\ttx id:', page_header_struct['tx_id'])
    print('\tlevel:', page_header_struct['level'])
    print('\tindex id:', page_header_struct['index_id'])
    print('\tbtr leaf:', page_header_struct['btr_leaf'])
    print('\tbtr top:', page_header_struct['btr_top'])
    print('-' * 50, '\n')
    print('Page Body:\n')
    print('Delete Records:')
    free = page_header_struct['free']
    if free > 0:
        while True:
            record_id = common.byte2int(page_bytes[free:free + 4], False)
            print("\n\toffset:", free)
            print("\trecord id:", record_id)

            record_head = page_bytes[free - 5:free]
            next_addr = common.byte2int(record_head[-2:])

            del_flag = record_head[0] >> 5 & 0x01
            print('\tdel_flag:', del_flag)

            if next_addr == 0:
                break

            free = free + next_addr
    record_offset = PAGE_BODY_DATA + 5
    print('+' * 50, '\n')
    print('Normal Records:')
    while True:
        record_head = page_bytes[record_offset - 5:record_offset]

        record_type = record_head[-3] & 0x03
        print('\n\trecord_type:', record_type)

        # infimum
        if record_type == 0b10:
            record_content = page_bytes[record_offset:record_offset + 7]
            print('\t' + record_content.decode(encoding='ASCII', errors='strict'))
        # supremum
        elif record_type == 0b11:
            record_content = page_bytes[record_offset:record_offset + 8]
            print('\t' + record_content.decode(encoding='ASCII', errors='strict'))
            break
        # btree pointer
        elif record_type == 0b1:
            record_id = common.byte2int(page_bytes[record_offset:record_offset + 4], False)
            print("\trecord id:", record_id)
            page_no = common.byte2int(page_bytes[record_offset + 4:record_offset + 8])
            print("\tpage no:", page_no)
        # btree node
        elif record_type == 0:
            record_id = common.byte2int(page_bytes[record_offset:record_offset + 4], False)
            print("\toffset:", record_offset)
            print("\trecord id:", record_id)

            del_flag = record_head[0] >> 5 & 0x01
            print('\tdel_flag:', del_flag)
        # 保留类型
        else:
            print('')

        record_offset = record_offset + common.byte2int(record_head[-2:])


# 默认页大小
PAGE_SIZE = 16384
# Fil Header长度
FIL_HEADER_DATA = 38
# Page Header长度
PAGE_HEADER_DATA = 56
# Page数据偏移位置
PAGE_BODY_DATA = FIL_HEADER_DATA + PAGE_HEADER_DATA


ibd = open(sys.argv[1], 'rb')

pointer = 0

while True:
    page_bytes = ibd.read(PAGE_SIZE)

    size = len(page_bytes)
    if size == 0:
        break

    pointer += size

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
    # print('*' * 20 + 'page start' + '*' * 20 + '\n')

    if file_header_struct['page_type'] != 0x45bf:
        continue

    print('page offset:{}, page type:{}({})'.format(hex(pointer - PAGE_SIZE),
                                                      file_header_struct['page_type'],
                                                      hex(file_header_struct['page_type'])))

    print('File Header:')
    print('\tcheck sum:', file_header_struct['check_sum'])
    print('\toffset(page number):', file_header_struct['page_number'])
    print('\tprevious page:', file_header_struct['pre_page'])
    print('\tnext page:', file_header_struct['next_page'])
    print('\tlsn:', file_header_struct['lsn'])
    print('\tpage type:', file_header_struct['page_type'])
    print('\tflush lsn:', file_header_struct['flush_lsn'])
    print('\tspace id:', file_header_struct['space_id'])
    print('-' * 50, '\n')

    translate_bnode_page()

ibd.close()


