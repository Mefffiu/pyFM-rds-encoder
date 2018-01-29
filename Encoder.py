import glob
import os
import math
from json import loads
from NewGenerator import parseToBin


def create_group0(i, PI, TP, PTY, TA, MS, AF1, AF2, PS1, PS2):
    block1 = PI
    block1 = block1 + control_word(block1, 1)

    group_type = '0000'
    group_version = '0'
    d = '1'
    counter = parseToBin(i/2, 2)
    block2 = group_type + group_version + TP + PTY + TA + MS + d + counter
    block2 = block2 + control_word(block2, 2)

    block3 = AF1 + AF2
    block3 = block3 + control_word(block3, 3)

    block4 = PS1 + PS2
    block4 = block4 + control_word(block4, 4)

    group0 = block1 + block2 + block3 + block4
    return group0


def create_group2(*arg):
    # (0, 1,  2,  3,   4,   5,   6,   7  )
    # (i, PI, TP, PTY, RT1, RT2, RT3, RT4)
    block1 = arg[1]
    block1 = block1 + control_word(block1, 1)

    group_type = '0010'
    group_version = '0'
    textAB = '1'
    counter = parseToBin(arg[0]/4, 4)
    block2 = group_type + group_version + arg[2] + arg[3] + textAB + counter
    block2 = block2 + control_word(block2, 2)
    block3 = ""
    block4 = ""

    n = len(arg) - 1
    if n == 4:
        block3 = arg[4] + '00000000'
        block3 = block3 + control_word(block3, 3)
        block4 = '00000000' + '00000000'
        block4 = block4 + control_word(block4, 4)
    elif n == 5:
        block3 = arg[4] + arg[5]
        block3 = block3 + control_word(block3, 3)
        block4 = '00000000' + '00000000'
        block4 = block4 + control_word(block4, 4)
    elif n == 6:
        block3 = arg[4] + arg[5]
        block3 = block3 + control_word(block3, 3)
        block4 = arg[6] + '00000000'
        block4 = block4 + control_word(block4, 4)
    elif n == 7:
        block3 = arg[4] + arg[5]
        block3 = block3 + control_word(block3, 3)
        block4 = arg[6] + arg[7]
        block4 = block4 + control_word(block4, 4)

    group2 = block1 + block2 + block3 + block4
    return group2


def control_word(bits, n):
    offsets = (
        0b0011111100,
        0b0110011000,
        0b0101101000,
        0b0110110100
    )
    G = (119, 743, 943, 779, 857, 880, 440, 220, 110, 55, 711, 959, 771, 861, 882, 441)
    crc = 0
    for i in range(len(bits)):
        if bits[i] == '1':
            crc ^= G[i]

    control_word = crc ^ offsets[n-1]
    return parseToBin(control_word, 10)



def aggregate(m):
    groups0 = ""
    groups2 = ""

    for i in range(0, 7, 2):
        # (i, PI, TP, PTY, TA, MS, AF1, AF2, PS1, PS2)
        groups0 += create_group0(i, m['PI'], m['TP'], m['PTY'], m['TA'], m['MS'],
                                 m['AF1'], m['AF2'], m['PS'][i], m['PS'][i + 1])

    rt_len = len(m['RT'])
    for index, i in enumerate(range(0, rt_len, 4)):
        if index == math.ceil(rt_len/4.0) - 1:  # if it is the last loop round
            if rt_len % 4 == 0:
                groups2 += create_group2(i, m['PI'], m['TP'], m['PTY'],
                                         m['RT'][i], m['RT'][i + 1], m['RT'][i + 2], m['RT'][i + 3])
            elif rt_len % 4 == 1:
                groups2 += create_group2(i, m['PI'], m['TP'], m['PTY'],
                                         m['RT'][i])
            elif rt_len % 4 == 2:
                groups2 += create_group2(i, m['PI'], m['TP'], m['PTY'],
                                         m['RT'][i], m['RT'][i + 1])
            elif rt_len % 4 == 3:
                groups2 += create_group2(i, m['PI'], m['TP'], m['PTY'],
                                         m['RT'][i], m['RT'][i + 1], m['RT'][i + 2])
        else:
            groups2 += create_group2(i, m['PI'], m['TP'], m['PTY'],
                                     m['RT'][i], m['RT'][i + 1], m['RT'][i + 2], m['RT'][i + 3])

    binary_message = groups0 + groups2
    return binary_message


# -------------------- MAIN FUNCTION --------------------

script_dir = os.path.dirname(os.path.abspath(__file__))
rel_path = "/data/*_b.json"
abs_file_path = script_dir + rel_path

files = glob.glob(abs_file_path)

binary_messages_json = []
for f in files:
    binary_messages_json.append(loads(open(f, 'r').read()))


binary_messages_groups = []
for m in binary_messages_json:
    binary_messages_groups.append(aggregate(m))

rel_path = "/data/"
abs_file_path = script_dir + rel_path
for m in binary_messages_groups:
    file = open(abs_file_path + str(binary_messages_groups.index(m)) + "_out.dat", 'w')
    file.write(m)
    file.close()

# -------------------- Data for prof. Zielinski Decoder --------------------
# print len(binary_messages_groups[0])
# file = open(abs_file_path + "FM_Radio_RDS.txt", 'a')
# for bit in binary_messages_groups[0]:
#     file.write(bit + "\n")
# file.close()
