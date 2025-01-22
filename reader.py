import os
import sys
from bidict import bidict
import psycopg2
import random
import ast

card_version_dict = bidict({"0xFFFF": "4", "0x5210": "5", "0x6013": "6 AA", "0x7012": "7 AAX", "0x8015": "8 Infinity"})
model_dict = {"Toyota": ["TRUENO GT-APEX (AE86)", "LEVIN GT-APEX (AE86)", "LEVIN SR (AE85)", "86 GT (ZN6)", "ALTEZZA RS200 (SXE10)", "MR-S (ZZW30)", "MR2 G-Limited (SW20)", "SUPRA RZ (JZA80)", "PRIUS (ZVW30)", "SPRINTER TRUENO 2door GT-APEX (AE86)", "CELICA GT-FOUR (ST205)"],
              "Nissan": ["SKYLINE GT-R (BNR32)", "SKYLINE GT-R (BNR34)", "SILVIA K's (S13)", "Silvia Q's (S14)", "Silvia spec-R (S15)", "180SX TYPE II (RPS13)", "FAIRLADY Z (Z33)", "GT-R NISMO (R35)", "GT-R (R35)", "SKYLINE 25GT TURBO (ER34)"],
              "Honda": ["Civic SiR・II (EG6)", "CIVIC TYPE R (EK9)", "INTEGRA TYPE R (DC2)", "S2000 (AP1)", "NSX (NA1)"],
              "Mazda": ["RX-7 ∞III (FC3S)", "RX-7 Type R (FD3S)", "RX-7 Type RS (FD3S)", "RX-8 Type S (SE3P)", "ROADSTER (NA6CE)", "ROADSTER RS (NB8C)"],
              "Subaru": ["IMPREZA STi Ver.V (GC8)", "IMPREZA STi (GDBA)", "IMPREZA STI (GDBF)", "BRZ S (ZC6)"],
              "Mitsubishi": ["LANCER Evolution III (CE9A)", "LANCER EVOLUTION IV (CN9A)", "LANCER Evolution VII (CT9A)", "LANCER Evolution IX (CT9A)", "LANCER EVOLUTION X (CZ4A)", "LANCER GSR EVOLUTION VI T.M.EDITION (CP9A)", "LANCER RS EVOLUTION V (CP9A)"],
              "Suzuki": ["Cappuccino (EA11R)"],
              "Initial D": ["SILEIGHTY", "TRUENO 2door GT-APEX (AE86)"],
              "Complete": ["G-FORCE SUPRA (JZA80-kai)", "MONSTER CIVIC R (EK9)", "S2000 GT1 (AP1)", "RE Amemiya Genki-7 (FD3S)", "NSX-R GT (NA2)", "ROADSTER C-SPEC (NA8C Kai)"]
              }
story_list = ['1-1', '1-2', '1-3', '1-4', '1-5', '1-6', '1-7', '1-8', '1-9', '1-10',
              '2-1', '2-2', '2-3', '2-4', '2-5', '2-6', '2-7',
              '3-1', '3-2', '3-3', '3-4', '3-5', '3-6', '3-7', '3-8',
              '4-1', '4-2', '4-3', '4-4', '4-5', '4-6', '4-7', '4-8', '4-9',
              '5-1', '5-2', '5-3', '5-4', '5-5', '5-6',
              '6-1', '6-2', '6-3', '6-4', '6-5',
              '7-1', '7-2', '7-3', '7-4', '7-5', '7-6', '7-7',
              '8-1', '8-2', '8-3', '8-4',
              '9-1', '9-2', '9-3', '9-4', '9-5',
              '10-1', '10-2',
              '11-1', '11-2', '11-3', '11-4', '11-5',
              '12-1', '12-2', '12-3', '12-4', '12-5',
              '13-1', '13-2', '13-3', '13-4', '13-5', '13-6',
              '14-1', '14-2', '14-3', '14-4', '14-5', '14-6', '14-7', '14-8',
              '15-1', '15-2']
rival_list = ['9', '11', 'EX_4', '1', '4', '12', 'EX_1', '14', '47', '1',
              '13', 'EX_5', '10', '47', '1', '17', '4',
              '15', '11', 'EX_6', '4', '18', 'EX_5', '16', '16',
              '14', 'EX_6', '4', '19', '42', 'EX_5', '21', '28', '1',
              '42', '23', 'EX_5', '49', '2', '5',
              '22', '21', 'EX_6', '7', '2',
              '43', '24', 'EX_6', 'EX_5', '44', '18', '2',
              '50', 'EX_6', '51', '5',
              '26', '21', '22', '25', '5',
              'EX_6', '29',
              '31', '20', 'EX_5', '33', '2',
              '30', 'EX_6', '32', '35', '6',
              '36', '33', 'EX_5', '35', '37', '3',
              '34', '35', '41', 'EX_6', '53', 'EX_6', '52', '8',
              '40', '4']
data_dict = dict()

def read_txt(filename):
    if not filename:
        raise Exception(f"file {filename} not found")
    with open(filename, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file]
    return lines

def pretty_bytes(byte_data, byte_order='big'):
    if byte_order not in ('big', 'little'):
        raise Exception("Byte order must be big or little")
    num = int.from_bytes(byte_data, byteorder=byte_order)
    hex_str = hex(num)[2:]
    expected_length = len(byte_data) * 2
    hex_str = hex_str.zfill(expected_length)
    return '0x' + hex_str

def safe_bytes(byte_data, size, byteorder='little', signed=False):
    if not byte_data:
        return b'\x00' * size
    if byteorder not in ('little', 'big'):
        raise ValueError("Invalid byte order")
    if isinstance(byte_data, str):
        if byte_data.startswith('0x'):
            byte_data = byte_data[2:]
        if len(byte_data) % 2 != 0:
            byte_data = '0' + byte_data
        byte_data = bytes.fromhex(byte_data)
    elif isinstance(byte_data, int):
        return byte_data.to_bytes(size, byteorder=byteorder, signed=signed)
    if byteorder == 'big':
        byte_data = byte_data[::-1]
    if byteorder == 'little':
        byte_data = byte_data.ljust(size, b'\x00')
    else:
        byte_data = byte_data.rjust(size, b'\x00')
    return byte_data[:size]

def ms_to_time(ms):
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    remaining_milliseconds = (ms % 60000) % 1000
    return f"{minutes}'{seconds:02}\"{remaining_milliseconds:03}"

def time_to_ms(time_str):
    minutes, rest = time_str.split("'")
    seconds, milliseconds = rest.split('"')
    minutes = int(minutes)
    seconds = int(seconds)
    milliseconds = int(milliseconds)
    total_ms = (minutes * 60000) + (seconds * 1000) + milliseconds
    return total_ms

#def skip(distance):
    #return .seek(distance, .tell)
def bytes_to_2bit_strings(byte_data):
    result = []
    for byte in byte_data:
        binary_str = format(byte, '08b')
        for i in range(0, 8, 2):
            result.append(binary_str[i:i+2])

    return result

def get_avatar_from_card(avatar_list_bytes):
    part_list = [0] * 7
    part_list[0] = (avatar_list_bytes[1] & 0xF) << 8 | avatar_list_bytes[0]
    part_list[1] = (avatar_list_bytes[1] >> 4) | (16 * avatar_list_bytes[2])
    part_list[2] = (avatar_list_bytes[4] & 0xF) << 8 | avatar_list_bytes[3]
    part_list[3] = (avatar_list_bytes[4] >> 4) | (16 * avatar_list_bytes[5])
    part_list[4] = (avatar_list_bytes[7] & 0xF) << 8 | avatar_list_bytes[6]
    part_list[5] = (avatar_list_bytes[7] >> 4) | (16 * avatar_list_bytes[8])
    part_list[6] = (avatar_list_bytes[10] & 0xF) << 8 | avatar_list_bytes[9]
    print(f"Avatar parts: {part_list[0]},{part_list[1]},{part_list[2]},{part_list[3]},{part_list[4]},{part_list[5]},{part_list[6]}")
    return part_list

def convert_part_list_to_bytes(part_list):
    byte_list = [0] * 11
    part1 = safe_bytes(part_list[0], 2)
    byte_list[0] = part1[0]
    byte_list[1] = part1[1]
    byte_list[1] = (byte_list[1] & 0xF) | (byte_list[1] & 0xF0)
    part2_helper = (byte_list[1] & 0xF) | (16 * part_list[1])
    part2_bytes = safe_bytes(part2_helper, 2)
    byte_list[1] = part2_bytes[0]
    byte_list[2] = part2_bytes[1]
    part3 = safe_bytes(part_list[2], 2)
    byte_list[3] = part3[0]
    byte_list[4] = part3[1]
    byte_list[4] = (byte_list[4] & 0xF) | (byte_list[4] & 0xF0)
    part4_helper = (byte_list[4] & 0xF) | (16 * part_list[3])
    part4_bytes = safe_bytes(part4_helper, 2)
    byte_list[4] = part4_bytes[0]
    byte_list[5] = part4_bytes[1]
    part5 = safe_bytes(part_list[4], 2)
    byte_list[6] = part5[0]
    byte_list[7] = part5[1]
    byte_list[7] = (byte_list[7] & 0xF) | (byte_list[7] & 0xF0)
    part6_helper = (byte_list[7] & 0xF) | (16 * part_list[5])
    part6_bytes = safe_bytes(part6_helper, 2)
    byte_list[7] = part6_bytes[0]
    byte_list[8] = part6_bytes[1]
    part7 = safe_bytes(part_list[6], 2)
    byte_list[9] = part7[0]
    byte_list[10] = part7[1]
    byte_list[10] = (byte_list[10] & 0xF) | (byte_list[10] & 0xF0)
    print(f"Avatar parts: {''.join(f'{byte:02X}' for byte in byte_list)}")
    return safe_bytes('0x' + ''.join(f'{byte:02X}' for byte in byte_list), 12)


def read_card(f):
    prefectures = read_txt('app/static/prefectures.txt')
    avatar_gender_list = read_txt('app/static/avatar_gender.txt')
    bgm_volume_list = read_txt('app/static/bgm_volume.txt')
    make_list = read_txt('app/static/make.txt')
    car_prefectures = read_txt('app/static/car_prefectures.txt')
    car_hirigana = read_txt('app/static/car_hirigana.txt')
    courses = read_txt('app/static/courses.txt')
    cup_list = read_txt('app/static/cup.txt')
    tachometer_list = read_txt('app/static/tachometer.txt')
    aura_list = read_txt('app/static/aura.txt')
    class_list = read_txt('app/static/class.txt')
    title_list = read_txt('app/static/titles.txt')
    course_times_list = read_txt('app/static/times.txt')

    header = f.read(80)
    data_dict["Game Version"] = card_version_dict[pretty_bytes(f.read(2), byte_order='little')]
    data_dict["Issued Store"] = pretty_bytes(f.read(2))
    data_dict["User ID"] = int.from_bytes(f.read(4), byteorder="little", signed=True)
    data_dict["Home Area"] = prefectures[int.from_bytes(f.read(2), byteorder="little")]
    data_dict["Avatar Gender"] = avatar_gender_list[int.from_bytes(f.read(2), byteorder="little")]
    data_dict["Previous Card ID"] = int.from_bytes(f.read(4), byteorder="little")
    for i in range(3):
        dcoin = int.from_bytes(f.read(2), byteorder="little")
        data_dict[f"DCoin{i}"] = dcoin
    data_dict["Year"] = pretty_bytes(f.read(2))
    data_dict["Month"] = pretty_bytes(f.read(2))
    data_dict["D.Net Stamp"] = pretty_bytes(f.read(2))
    data_dict["Error Count"] = pretty_bytes(f.read(2))
    data_dict["Checksum"] = pretty_bytes(f.read(2))
    for i in range(3):
        dcoin = int.from_bytes(f.read(2), byteorder="little")
        data_dict[f"DCoin{i}_2"] = dcoin
    data_dict["Year_2"] = pretty_bytes(f.read(2))
    data_dict["Month_2"] = pretty_bytes(f.read(2))
    data_dict["D.Net Stamp_2"] = pretty_bytes(f.read(2))
    data_dict["Error Count_2"] = pretty_bytes(f.read(2))
    data_dict["Checksum_2"] = pretty_bytes(f.read(2))
    data_dict["Store Name"] = (f.read(32).rstrip(b'\x00')).decode('shift-jis')
    config_flag_1 = pretty_bytes(f.read(1))
    if config_flag_1[3] == 'a':
        data_dict["Wheel Sensitivity"] = 10
    else:
        data_dict["Wheel Sensitivity"] = int(config_flag_1[3])
    data_dict["BGM Volume"] = bgm_volume_list[int(config_flag_1[2])]
    config_flag_2 = pretty_bytes(f.read(1))
    config_flag_3 = bin(int.from_bytes(f.read(1), byteorder="little"))[2:].zfill(8)
    data_dict["Force Quit"] = int(config_flag_3[7])
    data_dict["Cornering Guide"] = int(config_flag_3[6])
    data_dict["Guide Line"] = int(config_flag_3[5])
    data_dict["Cup"] = int(config_flag_3[4])
    data_dict["Barricade"] = int(config_flag_3[3])
    data_dict["Ghost Car"] = int(config_flag_3[2])
    data_dict["Class"] = class_list[int.from_bytes(f.read(1), byteorder="little")-1]
    data_dict["Class (Match)"] = class_list[int.from_bytes(f.read(1), byteorder="little")]
    data_dict["Class (Tag Match)"] = class_list[int.from_bytes(f.read(1), byteorder="little")]
    data_dict["Current Car"] = int.from_bytes(f.read(1), byteorder="little")
    data_dict["Number of Cars"] = int.from_bytes(f.read(1), byteorder="little")
    data_dict["Play Count"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Pride Points"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Tag Pride Points"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Class Gauge"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Team ID"] = int.from_bytes(f.read(4), byteorder="little", signed=True)
    data_dict["First Card ID"] = pretty_bytes(f.read(4))
    data_dict["Team Flag"] = pretty_bytes(f.read(4))
    data_dict["Driver Flags"] = pretty_bytes(f.read(4))
    data_dict["Driver Points"] = int.from_bytes(f.read(4), byteorder="little")
    data_dict["Avatar"] = get_avatar_from_card(f.read(12))
    padding = f.read(32)
    data_dict["Driver Name"] = (f.read(14).rstrip(b'\x00')).decode('shift-jis')
    data_dict["CRC01"] = pretty_bytes(f.read(2))
    for i in range(data_dict["Number of Cars"]):
        car_dict = dict()
        model = int.from_bytes(f.read(1), byteorder="little")
        make = make_list[int.from_bytes(f.read(1), byteorder="little")]
        car_dict["Make"] = make
        car_dict["Model"] = model_dict[make][model]
        car_dict["Color"] = int.from_bytes(f.read(2), byteorder="little")
        car_dict["Tuning"] = pretty_bytes(f.read(2))
        car_dict["Option Flag"] = pretty_bytes(f.read(2))
        car_dict["Car Flag"] = pretty_bytes(f.read(2))
        padding = f.read(2)
        for j in range(4):
            car_dict[f"Event Sticker {j+1}"] = int.from_bytes(f.read(1), byteorder="little", signed=True)
        car_dict["Battle Wins"] = int.from_bytes(f.read(2), byteorder="little")
        car_dict["Bought Sequence ID"] = int.from_bytes(f.read(2), byteorder="little")
        car_dict["Infinity Tune"] = int.from_bytes(f.read(2), byteorder="little")
        padding = f.read(2)
        car_dict["Numplate Prefecture"] = car_prefectures[int.from_bytes(f.read(1), byteorder="little")]
        car_dict["Numplate Hirigana"] = car_hirigana[int.from_bytes(f.read(1), byteorder="little")]
        car_dict["Numplate Class Code"] = int.from_bytes(f.read(2), byteorder="little")
        car_dict["Numplate Plate Number"] = int.from_bytes(f.read(4), byteorder="little")
        car_dict["Customizations"] = pretty_bytes(f.read(64))
        data_dict[f"Car {i+1}"] = car_dict
    for i in range(3 - data_dict["Number of Cars"]):
        f.read(96)
    data_dict["Avatar Points"] = int.from_bytes(f.read(1), byteorder="little")
    data_dict["My Frame"] = int.from_bytes(f.read(1), byteorder="little")
    data_dict["Selected Cup"] = cup_list[int.from_bytes(f.read(1), byteorder="little")]
    data_dict["Tachometer"] = tachometer_list[int.from_bytes(f.read(1), byteorder="little")]
    padding = f.read(1)
    data_dict["Battle Stance"] = int.from_bytes(f.read(1), byteorder="little")
    data_dict["CRC11"] = pretty_bytes(f.read(2))
    padding = f.read(2)
    data_dict["Story Losses"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Story Wins"] = int.from_bytes(f.read(2), byteorder="little")
    padding = f.read(6)
    data_dict["Infinity Result Data 1"] = pretty_bytes(f.read(1))
    data_dict["Infinity Result Data 2"] = pretty_bytes(f.read(1))
    data_dict["Infinity Rank"] = int.from_bytes(f.read(2), byteorder="little")
    story_progress = f.read(23)
    story_progress_list = bytes_to_2bit_strings(story_progress)
    story_progress_list = []
    for byte in story_progress:
        binary_byte = format(byte, '08b')
        story_progress_list.extend([binary_byte[i:i+2] for i in range(0, len(binary_byte), 2)])
    story_progress_dict = {}
    for i, story in enumerate(story_list):
        progress = story_progress_list[i]
        if progress in ('0', '00'):
            story_progress_dict[story] = 'Not Played'
        elif progress in ('01', '1'):
            story_progress_dict[story] = 'A'
        elif progress == '10':
            story_progress_dict[story] = 'S'
        elif progress == '11':
            story_progress_dict[story] = 'SS'
        else:
            raise Exception('Story progress corrupted')
    grouped_dict = {}
    for i, (story, progress) in enumerate(story_progress_dict.items()):
        chapter = story.split('-')[0]  # Extract chapter name
        rival = rival_list[i] if i < len(rival_list) else '0'
        if chapter not in grouped_dict:
            grouped_dict[chapter] = []
        grouped_dict[chapter].append((story, progress, rival))
    for chapter, episodes in grouped_dict.items():
        rs, sc = False, False
        for episode in episodes:
            progress = episode[1]
            if progress in ('A', 'Not Played'):
                rs, sc = False, False
                break
            elif progress == 'S':
                rs, sc = True, False
                break
            elif progress == 'SS':
                rs, sc = True, True
        episodes.append((rs, sc))
    data_dict["Story Progress"] = grouped_dict
    padding = f.read(5)
    course_dict = dict()
    for i in range(len(courses)):
        course = courses[i]
        course_dict[course] = {"Time": ms_to_time(int.from_bytes(f.read(3), byteorder="little"))}
        termination = f.read(1)
    data_dict["Courses"] = course_dict
    for i in range(len(courses)):
        course = courses[i]
        model = int.from_bytes(f.read(1), byteorder="little", signed=True)
        make = make_list[int.from_bytes(f.read(1), byteorder="little", signed=True)]
        if model == -1:
            course_dict[course]["Car Make"] = "Not Played"
            course_dict[course]["Car Model"] = "Not Played"
        else:
            course_dict[course]["Car Make"] = make
            course_dict[course]["Car Model"] = model_dict[make][model]
    data_dict["Net VS. Plays"] = int.from_bytes(f.read(4), byteorder="little")
    data_dict["Net Wins"] = int.from_bytes(f.read(4), byteorder="little")
    padding = f.read(4)
    data_dict["Net Now Count"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Net Now Count Wins"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Net Count Win Max"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Refuse Course Flag"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Total In-Store Plays"] = int.from_bytes(f.read(4), byteorder="little")
    data_dict["Total In-Store Wins"] = int.from_bytes(f.read(4), byteorder="little")
    data_dict["In-Store Now Count"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["In-Store Now Count Wins"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["In-Store Count Win Max"] = int.from_bytes(f.read(2), byteorder="little")
    for i in range(len(courses)):
        course = courses[i]
        course_dict[course]["In-Store Wins"] = int.from_bytes(f.read(1), byteorder="little")
    padding = f.read(4)
    data_dict["Net Tag VS Plays"] = int.from_bytes(f.read(4), byteorder="little")
    data_dict["Net Tag VS Wins"] = int.from_bytes(f.read(4), byteorder="little")
    data_dict["Net Tag VS Now Count"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Net Tag VS Now Count Wins"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Net Tag VS Count Win Max"] = int.from_bytes(f.read(2), byteorder="little")
    padding = f.read(6)
    data_dict["Tag Level EXP"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Total Bought"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["CRC12"] = pretty_bytes(f.read(2))
    padding = f.read(2)
    data_dict["Tag Story Level"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Tag Story Progress"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Tag Story Lose Count"] = int.from_bytes(f.read(2), byteorder="little")
    padding = f.read(1)
    data_dict["Tag New Comer"] = bool(int.from_bytes(f.read(1), byteorder="little"))
    data_dict["Tag Story Wins"] = int.from_bytes(f.read(2), byteorder="little")
    course_proficiency_dict = dict()
    for i in range(16):
        course = courses[i*2]
        course_proficiency_dict[course[:-5].rstrip()] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Course Proficiency"] = course_proficiency_dict
    for i in range(3):
        data_dict[f"Pro D Mission Flag {i}"] = pretty_bytes(f.read(2))
    data_dict["Pro D Mission Page"] = int.from_bytes(f.read(2), byteorder="little")
    for i in range(3):
        data_dict[f"Pro D Mission Flag Done {i}"] = pretty_bytes(f.read(2))
    data_dict["Pro D Mission Page Done"] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Mileage"] = int.from_bytes(f.read(4), byteorder="little")
    data_dict["Aura"] = aura_list[int.from_bytes(f.read(1), byteorder="little")]
    data_dict["Title Effect"] = int.from_bytes(f.read(1), byteorder="little")
    data_dict["Title"] = title_list[int.from_bytes(f.read(2), byteorder="little")-1]
    for i in range(10):
        data_dict[f"Title Stocker {i}"] = int.from_bytes(f.read(1), byteorder="little")
    data_dict["CRC13"] = pretty_bytes(f.read(2))
    for i in range(3):
        data_dict[f"Parts Stocker Index {i}"] = int.from_bytes(f.read(2), byteorder="little")
    for i in range(45):
        data_dict[f"Parts Stocker {i}"] = int.from_bytes(f.read(2), byteorder="little", signed=True)
    data_dict["Parts Stocker Position 0"] = int.from_bytes(f.read(1), byteorder="little", signed=True)
    data_dict["Parts Stocker Position 1"] = int.from_bytes(f.read(1), byteorder="little", signed=True)
    data_dict["CRC21"] = pretty_bytes(f.read(2))
    for i in range(len(courses)):
        course = courses[i]
        lap_1 = int.from_bytes(f.read(2), byteorder="big")
        lap_2 = int.from_bytes(f.read(2), byteorder="big")
        lap_3 = int.from_bytes(f.read(2), byteorder="big")
        total = time_to_ms(course_dict[course]["Time"])
        lap_4 = total - (lap_1 + lap_2 + lap_3)
        course_dict[course]["Lap 1"] = ms_to_time(lap_1)
        course_dict[course]["Lap 2"] = ms_to_time(lap_2)
        course_dict[course]["Lap 3"] = ms_to_time(lap_3)
        course_dict[course]["Lap 4"] = ms_to_time(lap_4)
        course_builtin_times = course_times_list[i].split(',')
        course_dict[course]["Time to Specialist"] = f'{ms_to_time(total - time_to_ms(course_builtin_times[1]))}\n({course_builtin_times[1]})'
        course_dict[course]["Time to Platinum"] = f'{ms_to_time(total - time_to_ms(course_builtin_times[2]))}\n({course_builtin_times[2]})'
    tuning_dict = dict()
    for i in range(25):
        tuning_dict[f"Car {i}"] = pretty_bytes(f.read(1))
    data_dict["Car Tunings"] = tuning_dict
    data_dict["Time Release Car Open Flag"] = pretty_bytes(f.read(1))
    padding = f.read(4)
    data_dict["CRC22"] = pretty_bytes(f.read(2))
    data_dict["Upload Scores"] = True
    return data_dict

def write_card(f, data_dict, user_id):
    prefectures = read_txt('app/static/prefectures.txt')
    avatar_gender_list = read_txt('app/static/avatar_gender.txt')
    bgm_volume_list = read_txt('app/static/bgm_volume.txt')
    make_list = read_txt('app/static/make.txt')
    car_prefectures = read_txt('app/static/car_prefectures.txt')
    car_hirigana = read_txt('app/static/car_hirigana.txt')
    courses = read_txt('app/static/courses.txt')
    cup_list = read_txt('app/static/cup.txt')
    tachometer_list = read_txt('app/static/tachometer.txt')
    aura_list = read_txt('app/static/aura.txt')
    class_list = read_txt('app/static/class.txt')
    title_list = read_txt('app/static/titles.txt')

    f.seek(80)
    f.write(safe_bytes(card_version_dict.inverse.get(data_dict["Game Version"]), 2, byteorder='big'))
    f.write(safe_bytes(data_dict["Issued Store"], 2, byteorder='little'))
    data_dict["User ID"] = user_id
    f.write(safe_bytes(data_dict["User ID"], 4, byteorder='little', signed=True))
    f.write(safe_bytes(prefectures.index(data_dict["Home Area"]), 2, byteorder='little'))
    f.write(safe_bytes(avatar_gender_list.index(data_dict["Avatar Gender"]), 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Previous Card ID"], 4, byteorder='little'))
    for i in range(3):
        dcoin = data_dict[f"DCoin{i}"]
        f.write(safe_bytes(dcoin, 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Year"], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Month"], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["D.Net Stamp"], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Error Count"], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Checksum"], 2, byteorder='little'))
    for i in range(3):
        dcoin = data_dict[f"DCoin{i}_2"]
        f.write(safe_bytes(dcoin, 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Year_2"], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Month_2"], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["D.Net Stamp_2"], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Error Count_2"], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Checksum_2"], 2, byteorder='little'))
    store_name = data_dict["Store Name"].encode('shift-jis')
    padded_store_name = store_name + b'\0' * (32 - len(store_name))  # Pad with null bytes to 32 bytes
    f.write(safe_bytes(padded_store_name, 32, byteorder='little'))

    config_flag_1 = ''
    config_flag_1 += str(bgm_volume_list.index(data_dict["BGM Volume"]))
    if int(data_dict["Wheel Sensitivity"]) == 10:
        config_flag_1 += 'a'
    else:
        config_flag_1 += str(data_dict["Wheel Sensitivity"])
    f.write(safe_bytes(config_flag_1, 1))
    config_flag_2 = f.read(1)

    config_flag_3 = '00'
    config_flag_3 += str(data_dict["Ghost Car"])
    config_flag_3 += str(data_dict["Barricade"])
    config_flag_3 += str(data_dict["Cup"])
    config_flag_3 += str(data_dict["Guide Line"])
    config_flag_3 += str(data_dict["Cornering Guide"])
    config_flag_3 += str(data_dict["Force Quit"])
    f.write(safe_bytes(int(config_flag_3, 2), 1))

    f.write(safe_bytes(class_list.index(data_dict["Class"])+1, 1))
    f.write(safe_bytes(class_list.index(data_dict["Class (Match)"]), 1))
    f.write(safe_bytes(class_list.index(data_dict["Class (Tag Match)"]), 1))
    f.write(safe_bytes(data_dict["Current Car"], 1))
    f.write(safe_bytes(data_dict["Number of Cars"], 1))
    f.write(safe_bytes(data_dict["Play Count"], 2))
    f.write(safe_bytes(data_dict["Pride Points"], 2))
    f.write(safe_bytes(data_dict["Tag Pride Points"], 2))
    f.write(safe_bytes(data_dict["Class Gauge"], 2))
    f.write(safe_bytes(data_dict["Team ID"], 4, signed=True))
    f.write(safe_bytes(data_dict["First Card ID"], 4))
    f.write(safe_bytes(data_dict["Team Flag"], 4))
    f.write(safe_bytes(data_dict["Driver Flags"], 4))
    f.write(safe_bytes(int(data_dict["Driver Points"]), 4))
    f.write(convert_part_list_to_bytes(data_dict["Avatar"]))
    f.write(b'\x00' * 32)
    encoded_name = data_dict["Driver Name"].encode('shift-jis')
    padded_name = encoded_name.ljust(14, b'\x00')
    f.write(safe_bytes(padded_name, 14))
    f.write(safe_bytes(data_dict["CRC01"], 2))
    for i in range(data_dict["Number of Cars"]):
        car_dict = data_dict[f"Car {i+1}"]
        f.write(safe_bytes(model_dict[car_dict["Make"]].index(car_dict["Model"]), 1))
        f.write(safe_bytes(make_list.index(car_dict["Make"]), 1))
        f.write(safe_bytes(car_dict["Color"], 2))
        f.write(safe_bytes(car_dict["Tuning"], 2))
        f.write(safe_bytes(car_dict["Option Flag"], 2))
        f.write(safe_bytes(car_dict["Car Flag"], 2))
        padding = f.read(2)
        for j in range(4):
            f.write(safe_bytes(car_dict[f"Event Sticker {j+1}"], 1, signed=True))
        f.write(safe_bytes(car_dict["Battle Wins"], 2))
        f.write(safe_bytes(car_dict["Bought Sequence ID"], 2))
        f.write(safe_bytes(car_dict["Infinity Tune"], 2))
        padding = f.read(2)
        f.write(safe_bytes(car_prefectures.index(car_dict["Numplate Prefecture"]), 1))
        f.write(safe_bytes(car_hirigana.index(car_dict["Numplate Hirigana"]), 1))
        f.write(safe_bytes(car_dict["Numplate Class Code"], 2))
        f.write(safe_bytes(car_dict["Numplate Plate Number"], 4))
        f.write(safe_bytes(car_dict["Customizations"], 64))
    for i in range(3 - data_dict["Number of Cars"]):
        f.read(96)
    f.write(safe_bytes(data_dict["Avatar Points"], 1))
    f.write(safe_bytes(int(data_dict["My Frame"]), 1))
    f.write(safe_bytes(cup_list.index(data_dict["Selected Cup"]), 1))
    f.write(safe_bytes(tachometer_list.index(data_dict["Tachometer"]), 1))
    padding = f.read(1)
    f.write(safe_bytes(int(data_dict["Battle Stance"]), 1))
    f.write(safe_bytes(data_dict["CRC11"], 2))
    padding = f.read(2)
    f.write(safe_bytes(data_dict["Story Losses"], 2))
    f.write(safe_bytes(data_dict["Story Wins"], 2))
    padding = f.read(6)
    f.write(safe_bytes(data_dict["Infinity Result Data 1"], 1))
    f.write(safe_bytes(data_dict["Infinity Result Data 2"], 1))
    f.write(safe_bytes(int(data_dict["Infinity Rank"]), 2))
    story_progress_list = []
    for chapter, episodes in data_dict["Story Progress"].items():
        no_rs_sc = episodes[:-1]
        for episode in no_rs_sc:
            story, progress, rival = episode
            if progress == 'Not Played':
                binary_progress = '00'
            elif progress == 'A':
                binary_progress = '01'
            elif progress == 'S':
                binary_progress = '10'
            elif progress == 'SS':
                binary_progress = '11'
            else:
                raise Exception('Invalid progress state')
            story_progress_list.append(binary_progress)
    story_progress_bytes = []
    for i in range(0, len(story_progress_list), 4):
        binary_byte = ''.join(story_progress_list[i:i+4])
        if len(binary_byte) == 8:
            story_progress_bytes.append(int(binary_byte, 2))
    f.write(bytes(story_progress_bytes))
    padding = f.read(6)
    course_dict = data_dict["Courses"]
    for i in range(len(courses)):
        course = courses[i]
        f.write(safe_bytes(time_to_ms(course_dict[course]["Time"]), 3))
        termination = f.read(1)
    for i in range(len(courses)):
        course = courses[i]
        if course_dict[course]["Car Model"] == 'Not Played':
            f.write(safe_bytes('0xFF', 1))
            f.write(safe_bytes('0xFF', 1))
        else:
            f.write(safe_bytes(model_dict[course_dict[course]["Car Make"]].index(course_dict[course]["Car Model"]), 1))
            f.write(safe_bytes(make_list.index(course_dict[course]["Car Make"]), 1))
    f.write(safe_bytes(data_dict["Net VS. Plays"], 4))
    f.write(safe_bytes(data_dict["Net Wins"], 4))
    padding = f.read(4)
    f.write(safe_bytes(data_dict["Net Now Count"], 2))
    f.write(safe_bytes(data_dict["Net Now Count Wins"], 2))
    f.write(safe_bytes(data_dict["Net Count Win Max"], 2))
    f.write(safe_bytes(data_dict["Refuse Course Flag"], 2))
    f.write(safe_bytes(data_dict["Total In-Store Plays"], 4))
    f.write(safe_bytes(data_dict["Total In-Store Wins"], 4))
    f.write(safe_bytes(data_dict["In-Store Now Count"], 2))
    f.write(safe_bytes(data_dict["In-Store Now Count Wins"], 2))
    f.write(safe_bytes(data_dict["In-Store Count Win Max"], 2))
    for i in range(len(courses)):
        course = courses[i]
        f.write(safe_bytes(course_dict[course]["In-Store Wins"], 1))
    padding = f.read(4)
    f.write(safe_bytes(data_dict["Net Tag VS Plays"], 4))
    f.write(safe_bytes(data_dict["Net Tag VS Wins"], 4))
    f.write(safe_bytes(data_dict["Net Tag VS Now Count"], 2))
    f.write(safe_bytes(data_dict["Net Tag VS Now Count Wins"], 2))
    f.write(safe_bytes(data_dict["Net Tag VS Count Win Max"], 2))
    padding = f.read(6)
    f.write(safe_bytes(data_dict["Tag Level EXP"], 2))
    f.write(safe_bytes(data_dict["Total Bought"], 2))
    f.write(safe_bytes(data_dict["CRC12"], 2))
    padding = f.read(2)
    f.write(safe_bytes(data_dict["Tag Story Level"], 2))
    f.write(safe_bytes(data_dict["Tag Story Progress"], 2))
    f.write(safe_bytes(data_dict["Tag Story Lose Count"], 2))
    padding = f.read(1)
    f.write(safe_bytes(int(data_dict["Tag New Comer"]), 1))
    f.write(safe_bytes(data_dict["Tag Story Wins"], 2))
    course_proficiency_dict = data_dict["Course Proficiency"]
    for i in range(16):
        course = courses[i*2]
        f.write(safe_bytes(course_proficiency_dict[course[:-5].rstrip()], 2))
    for i in range(3):
        f.write(safe_bytes(data_dict[f"Pro D Mission Flag {i}"], 2))
    f.write(safe_bytes(data_dict["Pro D Mission Page"], 2))
    for i in range(3):
        f.write(safe_bytes(data_dict[f"Pro D Mission Flag Done {i}"], 2))
    f.write(safe_bytes(data_dict["Pro D Mission Page Done"], 2))
    f.write(safe_bytes(int(data_dict["Mileage"]), 4))
    f.write(safe_bytes(aura_list.index(data_dict["Aura"]), 1))
    f.write(safe_bytes(int(data_dict["Title Effect"]), 1))
    f.write(safe_bytes(title_list.index(data_dict["Title"]) + 1, 2))
    for i in range(10):
        f.write(safe_bytes(data_dict[f"Title Stocker {i}"], 1))
    f.write(safe_bytes(data_dict["CRC13"], 2))
    for i in range(3):
        f.write(safe_bytes(data_dict[f"Parts Stocker Index {i}"], 2))
    for i in range(45):
        f.write(safe_bytes(data_dict[f"Parts Stocker {i}"], 2, signed=True))
    f.write(safe_bytes(data_dict["Parts Stocker Position 0"], 1, signed=True))
    f.write(safe_bytes(data_dict["Parts Stocker Position 1"], 1, signed=True))
    f.write(safe_bytes(data_dict["CRC21"], 2))
    for i in range(len(courses)):
        course = courses[i]
        f.write(safe_bytes(time_to_ms(course_dict[course]["Lap 1"]), 2, byteorder="big"))
        f.write(safe_bytes(time_to_ms(course_dict[course]["Lap 2"]), 2, byteorder="big"))
        f.write(safe_bytes(time_to_ms(course_dict[course]["Lap 3"]), 2, byteorder="big"))
    tuning_dict = data_dict["Car Tunings"]
    for i in range(25):
        f.write(safe_bytes(tuning_dict[f"Car {i}"], 1))
    f.write(safe_bytes(data_dict["Time Release Car Open Flag"], 1))
    padding = f.read(4)
    f.write(safe_bytes(data_dict["CRC22"], 2))

def create_leaderboard_table():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leaderboard (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        times TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def upload_times(user_id, username, times):
    create_leaderboard_table()
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    times = str(times)
    if user_id == -1:
        user_id = random.randint(1, 2147483647)
        cursor.execute("INSERT INTO leaderboard (user_id, username, times) VALUES (%s, %s, %s)",
                               (user_id, username, times))
    else:
        cursor.execute("UPDATE leaderboard SET username = %s, times = %s WHERE user_id = %s",
                               (username, times, user_id))
    conn.commit()
    conn.close()
    return user_id
