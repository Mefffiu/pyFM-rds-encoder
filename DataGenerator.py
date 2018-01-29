import string
from json import dumps
from random import randint, choice, getrandbits, uniform
import os


def parseToBin(x, length):
    x = bin(x)[2:]
    if len(x) == length:
        return x
    else:
        while len(x) != length:
            x = '0' + x
        return x


def generatePI():
    country = 'PL'
    areas = ('L', 'I', 'N', 'S',) + tuple('R' + str(i) for i in range(1, 13))
    ref_num = randint(1, 255)

    area = choice(areas)

    country_b = '0011'
    area_b = parseToBin(areas.index(area), 4)
    ref_num_b = parseToBin(ref_num, 8)

    pi = country + area + str(ref_num)
    pi_b = country_b + area_b + ref_num_b

    return pi, pi_b


def generateProgrammeType():
    types = (
        'Undefined1',
        'News',
        'News2',
        'Journals',
        'Sport',
        'Education',
        'Podcasts',
        'Culture',
        'Science',
        'Others',
        'POP Music',
        'Rock Music',
        'M.O.R Music',
        'Classical Peaceful Music',
        'Classical Music',
        'Undefined2',
        'Alarm'
    )
    type = choice(types)
    if type == 'Undefined2':
        return type, parseToBin(randint(16, 30), 5)
    elif type == 'Alarm':
        return type, parseToBin(31, 5)
    else:
        return type, parseToBin(types.index(type), 5)


def generateMS():
    mss = ('Music', 'Speech')
    ms = choice(mss)

    if ms == 'Music':
        return ms, 1
    else:
        return ms, 0


def generateAF(af_freq):
    choice = bool(getrandbits(1))
    if choice:
        af = round(uniform(87.6, 107.9), 1)
        af_code = af_freq.index(af) + 1
        af_b = parseToBin(af_code, 8)
        return af, af_b
    else:
        return 'No AF', parseToBin(224, 8)


def generatePS():
    ps = ''.join(choice(string.ascii_letters + string.digits) for _ in range(8))
    ps_b = []
    for x in ps:
        ps_b.append(parseToBin(ord(x), 8))

    return ps, ps_b


def generateRT():
    char_number = randint(1, 64)
    if char_number < 64:
        rt = ''.join(choice(string.ascii_letters + string.digits) for _ in range(char_number)) + '\r'
    else:
        rt = ''.join(choice(string.ascii_letters + string.digits) for _ in range(char_number))

    rt_b = []
    for x in rt:
        rt_b.append(parseToBin(ord(x), 8))

    return rt, rt_b


def generate_message(af_freq):
    PI = generatePI()
    TP_b = getrandbits(1)
    TP = bool(TP_b)
    PTY = generateProgrammeType()
    TA_b = getrandbits(1) if TP else 0
    TA = bool(TA_b)
    MS = generateMS()
    AF1 = generateAF(af_freq)
    AF2 = generateAF(af_freq)
    PS = generatePS()
    RT = generateRT()

    text_message = {
        'PI': PI[0],
        'TP': str(TP),
        'PTY': PTY[0],
        'TA': str(TA),
        'MS': MS[0],
        'AF1': AF1[0],
        'AF2': AF2[0],
        'PS': PS[0],
        'RT': RT[0]
    }

    binary_message_json = {
        'PI': PI[1],
        'TP': str(TP_b),
        'PTY': PTY[1],
        'TA': str(TA_b),
        'MS': str(MS[1]),
        'AF1': AF1[1],
        'AF2': AF2[1],
        'PS': PS[1],
        'RT': RT[1]
    }

    return text_message, binary_message_json


def af_freq():
    af_freq = []
    f = 87.5
    for i in range(1, 205):
        f = f + 0.1
        af_freq.append(round(f, 1))
    return af_freq


# -------------------------- 'MAIN' FUNCTION --------------------------
af_freq = af_freq()

text_messages = []
binary_messages_json = []
for i in range(1):
    message = generate_message(af_freq)
    text_messages.append(message[0])
    binary_messages_json.append(message[1])

script_dir = os.path.dirname(os.path.abspath(__file__))
rel_path = "/data/"
abs_file_path = script_dir + rel_path

for i in text_messages:
    file = open(abs_file_path + str(text_messages.index(i)) + ".json", 'w')
    file.write(dumps(i))
    file.close()

for j in binary_messages_json:
    file = open(abs_file_path + str(binary_messages_json.index(j)) + "_b.json", 'w')
    file.write(dumps(j))
    file.close()
