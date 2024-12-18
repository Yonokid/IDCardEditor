import os
import sys
from bidict import bidict

card_version_dict = bidict({"0xFFFF": "4", "0x5210": "5", "0x6013": "6 AA", "0x7012": "7 AAX", "0x8015": "8 Infinity"})
model_dict = {"Toyota": ["TRUENO GT-APEX (AE86)", "LEVIN GT-APEX (AE86)", "LEVIN SR (AE85)", "86 GT (ZN6)", "MR2 G-Limited (SW20)", "MR-S (ZZW30)", "ALTEZZA RS200 (SXE10)", "SUPRA RZ (JZA80)", "PRIUS (ZVW30)", "SPRINTER TRUENO 2door GT-APEX (AE86)", "CELICA GT-FOUR (ST205)"],
              "Nissan": ["SKYLINE GT-R (BNR32)", "SKYLINE GT-R (BNR34)", "SILVIA K's (S13)", "Silvia Q's (S14)", "Silvia spec-R (S15)", "180SX TYPE II (RPS13)", "FAIRLADY Z (Z33)", "GT-R NISMO (R35)", "GT-R (R35)", "SKYLINE 25GT TURBO (ER34)"],
              "Honda": ["Civic SiR・II (EG6)", "CIVIC TYPE R (EK9)", "INTEGRA TYPE R (DC2)", "S2000 (AP1)", "NSX (NA1)"],
              "Mazda": ["RX-7 ∞III (FC3S)", "RX-7 Type R (FD3S)", "RX-7 Type RS (FD3S)", "RX-8 Type S (SE3P)", "ROADSTER (NA6CE)", "ROADSTER RS (NB8C)"],
              "Subaru": ["IMPREZA STi Ver.V (GC8)", "IMPREZA STi (GDBA)", "IMPREZA STI (GDBF)", "BRZ S (ZC6)"],
              "Mitsubishi": ["LANCER Evolution III (CE9A)", "LANCER EVOLUTION IV (CN9A)", "LANCER Evolution VII (CT9A)", "LANCER Evolution IX (CT9A)", "LANCER EVOLUTION X (CZ4A)", "LANCER GSR EVOLUTION VI T.M.EDITION (CP9A)", "LANCER RS EVOLUTION V (CP9A)"],
              "Suzuki": ["Cappuccino (EA11R)"],
              "Initial D": ["SILEIGHTY", "TRUENO 2door GT-APEX (AE86)"],
              "Complete": ["G-FORCE SUPRA (JZA80-kai)", "MONSTER CIVIC R (EK9)", "NSX-R GT (NA2)", "RE Amemiya Genki-7 (FD3S)", "S2000 GT1 (AP1)", "ROADSTER C-SPEC (NA8C Kai)"]
              }
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

def read_card(filename):
    f = filename
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

    header = f.read(80)
    data_dict["Game Version"] = [card_version_dict[pretty_bytes(f.read(2), byte_order='little')], True]
    data_dict["Issued Store"] = [pretty_bytes(f.read(2)), False]
    data_dict["User ID"] = [int.from_bytes(f.read(4), byteorder="big", signed=True), False]
    data_dict["Home Area"] = [prefectures[int.from_bytes(f.read(2), byteorder="little")], True]
    data_dict["Avatar Gender"] = [avatar_gender_list[int.from_bytes(f.read(2), byteorder="little")], True]
    data_dict["Previous Card ID"] = [int.from_bytes(f.read(4), byteorder="little"), False]
    for i in range(3):
        dcoin = int.from_bytes(f.read(2), byteorder="little")
        data_dict[f"DCoin{i}"] = [dcoin, False]
    data_dict["Year"] = [pretty_bytes(f.read(2)), False]
    data_dict["Month"] = [pretty_bytes(f.read(2)), False]
    data_dict["D.Net Stamp"] = [pretty_bytes(f.read(2)), False]
    data_dict["Error Count"] = [pretty_bytes(f.read(2)), False]
    data_dict["Checksum"] = [pretty_bytes(f.read(2)), False]
    for i in range(3):
        dcoin = int.from_bytes(f.read(2), byteorder="little")
        data_dict[f"DCoin{i}_2"] = [dcoin, False]
    data_dict["Year_2"] = [pretty_bytes(f.read(2)), False]
    data_dict["Month_2"] = [pretty_bytes(f.read(2)), False]
    data_dict["D.Net Stamp_2"] = [pretty_bytes(f.read(2)), False]
    data_dict["Error Count_2"] = [pretty_bytes(f.read(2)), False]
    data_dict["Checksum_2"] = [pretty_bytes(f.read(2)), False]
    data_dict["Store Name"] = [(f.read(32).rstrip(b'\x00')).decode('shift-jis'), True]
    config_flag_1 = pretty_bytes(f.read(1))
    if config_flag_1[3] == 'a':
        data_dict["Wheel Sensitivity"] = [10, True]
    else:
        data_dict["Wheel Sensitivity"] = [int(config_flag_1[3]), True]
    data_dict["BGM Volume"] = [bgm_volume_list[int(config_flag_1[2])], True]
    config_flag_2 = pretty_bytes(f.read(1))
    config_flag_3 = bin(int.from_bytes(f.read(1), byteorder="little"))[2:].zfill(8)
    data_dict["Force Quit"] = [(int(config_flag_3[7])), True]
    data_dict["Cornering Guide"] = [(int(config_flag_3[6])), True]
    data_dict["Guide Line"] = [(int(config_flag_3[5])), True]
    data_dict["Cup"] = [(int(config_flag_3[4])), True]
    data_dict["Barricade"] = [(int(config_flag_3[3])), True]
    data_dict["Ghost Car"] = [(int(config_flag_3[2])), True]
    data_dict["Class"] = [class_list[int.from_bytes(f.read(1), byteorder="little")-1], True]
    data_dict["Class (Match)"] = [class_list[int.from_bytes(f.read(1), byteorder="little")], False]
    data_dict["Class (Tag Match)"] = [class_list[int.from_bytes(f.read(1), byteorder="little")], False]
    data_dict["Current Car"] = [int.from_bytes(f.read(1), byteorder="little"), True]
    data_dict["Number of Cars"] = [int.from_bytes(f.read(1), byteorder="little"), True]
    data_dict["Play Count"] = [int.from_bytes(f.read(2), byteorder="little"), True]
    data_dict["Pride Points"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Tag Pride Points"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Class Gauge"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Team ID"] = [int.from_bytes(f.read(4), byteorder="little", signed=True), False]
    data_dict["First Card ID"] = [pretty_bytes(f.read(4)), False]
    data_dict["Team Flag"] = [pretty_bytes(f.read(4)), False]
    data_dict["Driver Flags"] = [pretty_bytes(f.read(4)), False]
    data_dict["Driver Points"] = [int.from_bytes(f.read(4), byteorder="little"), True]
    data_dict["Avatar"] = [pretty_bytes(f.read(12)), True]
    padding = f.read(32)
    data_dict["Driver Name"] = [(f.read(14).rstrip(b'\x00')).decode('shift-jis'), True]
    data_dict["CRC01"] = [pretty_bytes(f.read(2)), False]
    for i in range(data_dict["Number of Cars"][0]):
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
        data_dict[f"Car {i+1}"] = [car_dict, True]
    for i in range(3 - data_dict["Number of Cars"][0]):
        f.read(96)
    data_dict["Avatar Points"] = [int.from_bytes(f.read(1), byteorder="little"), False]
    data_dict["My Frame"] = [int.from_bytes(f.read(1), byteorder="little"), True]
    data_dict["Selected Cup"] = [cup_list[int.from_bytes(f.read(1), byteorder="little")], True]
    data_dict["Tachometer"] = [tachometer_list[int.from_bytes(f.read(1), byteorder="little")], True]
    padding = f.read(1)
    data_dict["Battle Stance"] = [int.from_bytes(f.read(1), byteorder="little"), True]
    data_dict["CRC11"] = [pretty_bytes(f.read(2)), False]
    padding = f.read(2)
    data_dict["Story Losses"] = [int.from_bytes(f.read(2), byteorder="little"), True]
    data_dict["Story Wins"] = [int.from_bytes(f.read(2), byteorder="little"), True]
    padding = f.read(6)
    data_dict["Infinity Result Data 1"] = [pretty_bytes(f.read(1)), False]
    data_dict["Infinity Result Data 2"] = [pretty_bytes(f.read(1)), False]
    data_dict["Infinity Rank"] = [int.from_bytes(f.read(2), byteorder="little"), True]
    data_dict["Story Progress"] = [pretty_bytes(f.read(24)), True]
    padding = f.read(4)
    course_dict = dict()
    for i in range(len(courses)):
        course = courses[i]
        course_dict[course] = {"Time": ms_to_time(int.from_bytes(f.read(3), byteorder="little"))}
        termination = f.read(1)
    data_dict["Courses"] = [course_dict, False]
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
    data_dict["Net VS. Plays"] = [int.from_bytes(f.read(4), byteorder="little"), False]
    data_dict["Net Wins"] = [int.from_bytes(f.read(4), byteorder="little"), False]
    padding = f.read(4)
    data_dict["Net Now Count"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Net Now Count Wins"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Net Count Win Max"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Refuse Course Flag"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Total In-Store Plays"] = [int.from_bytes(f.read(4), byteorder="little"), True]
    data_dict["Total In-Store Wins"] = [int.from_bytes(f.read(4), byteorder="little"), True]
    data_dict["In-Store Now Count"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["In-Store Now Count Wins"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["In-Store Count Win Max"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    for i in range(len(courses)):
        course = courses[i]
        course_dict[course]["In-Store Wins"] = int.from_bytes(f.read(1), byteorder="little")
    padding = f.read(4)
    data_dict["Net Tag VS Plays"] = [int.from_bytes(f.read(4), byteorder="little"), False]
    data_dict["Net Tag VS Wins"] = [int.from_bytes(f.read(4), byteorder="little"), False]
    data_dict["Net Tag VS Now Count"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Net Tag VS Now Count Wins"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Net Tag VS Count Win Max"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    padding = f.read(6)
    data_dict["Tag Level EXP"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Total Bought"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["CRC12"] = [pretty_bytes(f.read(2)), False]
    padding = f.read(2)
    data_dict["Tag Story Level"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Tag Story Progress"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Tag Story Lose Count"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    padding = f.read(1)
    data_dict["Tag New Comer"] = [bool(int.from_bytes(f.read(1), byteorder="little")), False]
    data_dict["Tag Story Wins"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    course_proficiency_dict = dict()
    for i in range(16):
        course = courses[i*2]
        course_proficiency_dict[course[:-5].rstrip()] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Course Proficiency"] = [course_proficiency_dict, True]
    for i in range(3):
        data_dict[f"Pro D Mission Flag {i}"] = [pretty_bytes(f.read(2)), False]
    data_dict["Pro D Mission Page"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    for i in range(3):
        data_dict[f"Pro D Mission Flag Done {i}"] = [pretty_bytes(f.read(2)), False]
    data_dict["Pro D Mission Page Done"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Mileage"] = [int.from_bytes(f.read(4), byteorder="little"), True]
    data_dict["Aura"] = [aura_list[int.from_bytes(f.read(1), byteorder="little")], True]
    data_dict["Title Effect"] = [int.from_bytes(f.read(1), byteorder="little"), True]
    data_dict["Title"] = [title_list[int.from_bytes(f.read(2), byteorder="little")-1], True]
    for i in range(10):
        data_dict[f"Title Stocker {i}"] = [int.from_bytes(f.read(1), byteorder="little"), False]
    data_dict["CRC13"] = [pretty_bytes(f.read(2)), False]
    for i in range(3):
        data_dict[f"Parts Stocker Index {i}"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    for i in range(45):
        data_dict[f"Parts Stocker {i}"] = [int.from_bytes(f.read(2), byteorder="little", signed=True), False]
    data_dict["Parts Stocker Position 0"] = [int.from_bytes(f.read(1), byteorder="little", signed=True), False]
    data_dict["Parts Stocker Position 1"] = [int.from_bytes(f.read(1), byteorder="little", signed=True), False]
    data_dict["CRC21"] = [pretty_bytes(f.read(2)), False]
    for i in range(len(courses)):
        course = courses[i]
        course_dict[course]["Lap 1"] = ms_to_time(int.from_bytes(f.read(2), byteorder="little"))
        course_dict[course]["Lap 2"] = ms_to_time(int.from_bytes(f.read(2), byteorder="little"))
        course_dict[course]["Lap 3"] = ms_to_time(int.from_bytes(f.read(2), byteorder="little"))
    tuning_dict = dict()
    for i in range(25):
        tuning_dict[f"Car {i}"] = pretty_bytes(f.read(1))
    data_dict["Car Tunings"] = [tuning_dict, False]
    data_dict["Time Release Car Open Flag"] = [pretty_bytes(f.read(1)), False]
    padding = f.read(4)
    data_dict["CRC22"] = [pretty_bytes(f.read(2)), False]
    return data_dict

def write_card(filename, data_dict):
    f = filename
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
    f.write(safe_bytes(card_version_dict.inverse.get(data_dict["Game Version"][0]), 2, byteorder='big'))
    f.write(safe_bytes(data_dict["Issued Store"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["User ID"][0], 4, byteorder='big', signed=True))
    f.write(safe_bytes(prefectures.index(data_dict["Home Area"][0]), 2, byteorder='little'))
    f.write(safe_bytes(avatar_gender_list.index(data_dict["Avatar Gender"][0]), 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Previous Card ID"][0], 4, byteorder='little'))
    for i in range(3):
        dcoin = data_dict[f"DCoin{i}"][0]
        f.write(safe_bytes(dcoin, 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Year"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Month"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["D.Net Stamp"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Error Count"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Checksum"][0], 2, byteorder='little'))
    for i in range(3):
        dcoin = data_dict[f"DCoin{i}_2"][0]
        f.write(safe_bytes(dcoin, 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Year_2"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Month_2"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["D.Net Stamp_2"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Error Count_2"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Checksum_2"][0], 2, byteorder='little'))
    store_name = data_dict["Store Name"][0].encode('shift-jis')
    padded_store_name = store_name + b'\0' * (32 - len(store_name))  # Pad with null bytes to 32 bytes
    f.write(safe_bytes(padded_store_name, 32, byteorder='little'))

    config_flag_1 = ''
    config_flag_1 += str(bgm_volume_list.index(data_dict["BGM Volume"][0]))
    if int(data_dict["Wheel Sensitivity"][0]) == 10:
        config_flag_1 += 'a'
    else:
        config_flag_1 += str(data_dict["Wheel Sensitivity"][0])
    f.write(safe_bytes(config_flag_1, 1))
    config_flag_2 = f.read(1)

    config_flag_3 = '00'
    config_flag_3 += str(data_dict["Ghost Car"][0])
    config_flag_3 += str(data_dict["Barricade"][0])
    config_flag_3 += str(data_dict["Cup"][0])
    config_flag_3 += str(data_dict["Guide Line"][0])
    config_flag_3 += str(data_dict["Cornering Guide"][0])
    config_flag_3 += str(data_dict["Force Quit"][0])
    f.write(safe_bytes(int(config_flag_3, 2), 1))

    f.write(safe_bytes(class_list.index(data_dict["Class"][0])+1, 1))
    f.write(safe_bytes(class_list.index(data_dict["Class (Match)"][0]), 1))
    f.write(safe_bytes(class_list.index(data_dict["Class (Tag Match)"][0]), 1))
    f.write(safe_bytes(data_dict["Current Car"][0], 1))
    f.write(safe_bytes(data_dict["Number of Cars"][0], 1))
    f.write(safe_bytes(data_dict["Play Count"][0], 2))
    f.write(safe_bytes(data_dict["Pride Points"][0], 2))
    f.write(safe_bytes(data_dict["Tag Pride Points"][0], 2))
    f.write(safe_bytes(data_dict["Class Gauge"][0], 2))
    f.write(safe_bytes(data_dict["Team ID"][0], 4, signed=True))
    f.write(safe_bytes(data_dict["First Card ID"][0], 4))
    f.write(safe_bytes(data_dict["Team Flag"][0], 4))
    f.write(safe_bytes(data_dict["Driver Flags"][0], 4))
    f.write(safe_bytes(int(data_dict["Driver Points"][0]), 4))
    f.write(safe_bytes(data_dict["Avatar"][0], 12))
    f.write(b'\x00' * 32)
    encoded_name = data_dict["Driver Name"][0].encode('shift-jis')
    padded_name = encoded_name.ljust(14, b'\x00')
    f.write(safe_bytes(padded_name, 14))
    f.write(safe_bytes(data_dict["CRC01"][0], 2))
    for i in range(data_dict["Number of Cars"][0]):
        car_dict = data_dict[f"Car {i+1}"][0]
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
    for i in range(3 - data_dict["Number of Cars"][0]):
        f.read(96)
    f.write(safe_bytes(data_dict["Avatar Points"][0], 1))
    f.write(safe_bytes(int(data_dict["My Frame"][0]), 1))
    f.write(safe_bytes(cup_list.index(data_dict["Selected Cup"][0]), 1))
    f.write(safe_bytes(tachometer_list.index(data_dict["Tachometer"][0]), 1))
    padding = f.read(1)
    f.write(safe_bytes(data_dict["Battle Stance"][0], 1))
    f.write(safe_bytes(data_dict["CRC11"][0], 2))
    padding = f.read(2)
    f.write(safe_bytes(data_dict["Story Losses"][0], 2))
    f.write(safe_bytes(data_dict["Story Wins"][0], 2))
    padding = f.read(6)
    f.write(safe_bytes(data_dict["Infinity Result Data 1"][0], 1))
    f.write(safe_bytes(data_dict["Infinity Result Data 2"][0], 1))
    f.write(safe_bytes(int(data_dict["Infinity Rank"][0]), 2))
    f.write(safe_bytes(data_dict["Story Progress"][0], 24))
    padding = f.read(4)
    course_dict = data_dict["Courses"][0]
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
    f.write(safe_bytes(data_dict["Net VS. Plays"][0], 4))
    f.write(safe_bytes(data_dict["Net Wins"][0], 4))
    padding = f.read(4)
    f.write(safe_bytes(data_dict["Net Now Count"][0], 2))
    f.write(safe_bytes(data_dict["Net Now Count Wins"][0], 2))
    f.write(safe_bytes(data_dict["Net Count Win Max"][0], 2))
    f.write(safe_bytes(data_dict["Refuse Course Flag"][0], 2))
    f.write(safe_bytes(data_dict["Total In-Store Plays"][0], 4))
    f.write(safe_bytes(data_dict["Total In-Store Wins"][0], 4))
    f.write(safe_bytes(data_dict["In-Store Now Count"][0], 2))
    f.write(safe_bytes(data_dict["In-Store Now Count Wins"][0], 2))
    f.write(safe_bytes(data_dict["In-Store Count Win Max"][0], 2))
    for i in range(len(courses)):
        course = courses[i]
        f.write(safe_bytes(course_dict[course]["In-Store Wins"], 1))
    padding = f.read(4)
    f.write(safe_bytes(data_dict["Net Tag VS Plays"][0], 4))
    f.write(safe_bytes(data_dict["Net Tag VS Wins"][0], 4))
    f.write(safe_bytes(data_dict["Net Tag VS Now Count"][0], 2))
    f.write(safe_bytes(data_dict["Net Tag VS Now Count Wins"][0], 2))
    f.write(safe_bytes(data_dict["Net Tag VS Count Win Max"][0], 2))
    padding = f.read(6)
    f.write(safe_bytes(data_dict["Tag Level EXP"][0], 2))
    f.write(safe_bytes(data_dict["Total Bought"][0], 2))
    f.write(safe_bytes(data_dict["CRC12"][0], 2))
    padding = f.read(2)
    f.write(safe_bytes(data_dict["Tag Story Level"][0], 2))
    f.write(safe_bytes(data_dict["Tag Story Progress"][0], 2))
    f.write(safe_bytes(data_dict["Tag Story Lose Count"][0], 2))
    padding = f.read(1)
    f.write(safe_bytes(int(data_dict["Tag New Comer"][0]), 1))
    f.write(safe_bytes(data_dict["Tag Story Wins"][0], 2))
    course_proficiency_dict = data_dict["Course Proficiency"][0]
    for i in range(16):
        course = courses[i*2]
        f.write(safe_bytes(course_proficiency_dict[course[:-5].rstrip()], 2))
    for i in range(3):
        f.write(safe_bytes(data_dict[f"Pro D Mission Flag {i}"][0], 2))
    f.write(safe_bytes(data_dict["Pro D Mission Page"][0], 2))
    for i in range(3):
        f.write(safe_bytes(data_dict[f"Pro D Mission Flag Done {i}"][0], 2))
    f.write(safe_bytes(data_dict["Pro D Mission Page Done"][0], 2))
    f.write(safe_bytes(int(data_dict["Mileage"][0]), 4))
    f.write(safe_bytes(aura_list.index(data_dict["Aura"][0]), 1))
    f.write(safe_bytes(int(data_dict["Title Effect"][0]), 1))
    f.write(safe_bytes(title_list.index(data_dict["Title"][0]) + 1, 2))
    for i in range(10):
        f.write(safe_bytes(data_dict[f"Title Stocker {i}"][0], 1))
    f.write(safe_bytes(data_dict["CRC13"][0], 2))
    for i in range(3):
        f.write(safe_bytes(data_dict[f"Parts Stocker Index {i}"][0], 2))
    for i in range(45):
        f.write(safe_bytes(data_dict[f"Parts Stocker {i}"][0], 2, signed=True))
    f.write(safe_bytes(data_dict["Parts Stocker Position 0"][0], 1, signed=True))
    f.write(safe_bytes(data_dict["Parts Stocker Position 1"][0], 1, signed=True))
    f.write(safe_bytes(data_dict["CRC21"][0], 2))
    for i in range(len(courses)):
        course = courses[i]
        f.write(safe_bytes(time_to_ms(course_dict[course]["Lap 1"]), 2))
        f.write(safe_bytes(time_to_ms(course_dict[course]["Lap 2"]), 2))
        f.write(safe_bytes(time_to_ms(course_dict[course]["Lap 3"]), 2))
    tuning_dict = data_dict["Car Tunings"][0]
    for i in range(25):
        f.write(safe_bytes(tuning_dict[f"Car {i}"], 1))
    f.write(safe_bytes(data_dict["Time Release Car Open Flag"][0], 1))
    padding = f.read(4)
    f.write(safe_bytes(data_dict["CRC22"][0], 2))
