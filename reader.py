import json
import os
import random
from io import BytesIO

import psycopg2
from bidict import bidict
from typing_extensions import Any

card_version_dict = bidict({b"\xFF\xFF": "4", b"\x10\x52": "5", b"\x13\x60": "6 AA", b"\x12\x70": "7 AAX", b"\x15\x80": "8 Infinity"})

def read_txt(filename: str) -> list[str]:
    if not filename:
        raise Exception(f"file {filename} not found")
    with open(filename, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file]
    return lines

def safe_bytes(byte_data, size: int, byteorder='little', signed=False) -> bytes:
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

def ms_to_time(ms: int) -> str:
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    remaining_milliseconds = (ms % 60000) % 1000
    return f"{minutes}'{seconds:02}\"{remaining_milliseconds:03}"

def time_to_ms(time_str: str) -> int:
    minutes, rest = time_str.split("'")
    seconds, milliseconds = rest.split('"')
    minutes, seconds, milliseconds = int(minutes), int(seconds), int(milliseconds)
    total_ms = (minutes * 60000) + (seconds * 1000) + milliseconds
    return total_ms

def bytes_to_2bit_strings(byte_data: bytes) -> list[str]:
    result = []
    for byte in byte_data:
        binary_str = format(byte, '08b')
        for i in range(0, 8, 2):
            result.append(binary_str[i:i+2])
    return result

def read_avatar_parts(avatar_list_bytes: bytes) -> list[int]:
    part_list = [0] * 7
    part_list[0] = (avatar_list_bytes[1] & 0xF) << 8 | avatar_list_bytes[0]
    part_list[1] = (avatar_list_bytes[1] >> 4) | (16 * avatar_list_bytes[2])
    part_list[2] = (avatar_list_bytes[4] & 0xF) << 8 | avatar_list_bytes[3]
    part_list[3] = (avatar_list_bytes[4] >> 4) | (16 * avatar_list_bytes[5])
    part_list[4] = (avatar_list_bytes[7] & 0xF) << 8 | avatar_list_bytes[6]
    part_list[5] = (avatar_list_bytes[7] >> 4) | (16 * avatar_list_bytes[8])
    part_list[6] = (avatar_list_bytes[10] & 0xF) << 8 | avatar_list_bytes[9]
    return part_list

def read_dcoin_info(f: BytesIO) -> list[dict[str, int|bytes]]:
    dcoins = []
    for i in range(2):
        dcoin_data = dict()
        dcoin_data["DCoin0"] = int.from_bytes(f.read(2), byteorder="little")
        dcoin_data["DCoin1"] = int.from_bytes(f.read(2), byteorder="little")
        dcoin_data["DCoin2"] = int.from_bytes(f.read(2), byteorder="little")
        dcoin_data["Year"] = f.read(2)
        dcoin_data["Month"] = f.read(2)
        dcoin_data["D.Net Stamp"] = f.read(2)
        dcoin_data["Error Count"] = f.read(2)
        dcoin_data["Checksum"] = f.read(2)
        dcoins.append(dcoin_data)
    return dcoins

def read_cars(f: BytesIO, car_count: int, make_list: list[str], car_prefectures: list[str], car_hirigana: list[str], model_dict: dict[str, list[str]]) -> list[dict[str, int|bytes|str]]:
    cars = []
    for i in range(car_count):
        car_dict = dict()
        model = int.from_bytes(f.read(1), byteorder="little")
        make = make_list[int.from_bytes(f.read(1), byteorder="little")]
        car_dict["Make"] = make
        car_dict["Model"] = model_dict[make][model]
        car_dict["Color"] = int.from_bytes(f.read(2), byteorder="little")
        car_dict["Tuning"] = f.read(2)
        car_dict["Option Flag"] = f.read(2)
        car_dict["Car Flag"] = f.read(2)
        _ = f.read(2)
        for j in range(4):
            car_dict[f"Event Sticker {j+1}"] = int.from_bytes(f.read(1), byteorder="little", signed=True)
        car_dict["Battle Wins"] = int.from_bytes(f.read(2), byteorder="little")
        car_dict["Bought Sequence ID"] = int.from_bytes(f.read(2), byteorder="little")
        car_dict["Infinity Tune"] = int.from_bytes(f.read(2), byteorder="little")
        _ = f.read(2)
        car_dict["Numplate Prefecture"] = car_prefectures[int.from_bytes(f.read(1), byteorder="little")]
        car_dict["Numplate Hirigana"] = car_hirigana[int.from_bytes(f.read(1), byteorder="little")]
        car_dict["Numplate Class Code"] = int.from_bytes(f.read(2), byteorder="little")
        car_dict["Numplate Plate Number"] = int.from_bytes(f.read(4), byteorder="little")
        car_dict["Customizations"] = f.read(64)
        cars.append(car_dict)
    for i in range(3 - car_count):
        f.read(96)
    return cars

def read_story(f: BytesIO, card_data: dict[str, Any], story_dict: dict[str, str]):
    story_progress = f.read(23)
    story_progress_list = bytes_to_2bit_strings(story_progress)
    story_progress_list = []
    for byte in story_progress:
        binary_byte = format(byte, '08b')
        story_progress_list.extend([binary_byte[i:i+2] for i in range(0, len(binary_byte), 2)])
    story_progress_dict = {}
    for i, story in enumerate(story_dict):
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
        rival = story_dict[story]
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
    return grouped_dict

def read_course_cars(f: BytesIO, courses: list[str], make_list: list[str], model_dict: dict[str, list[str]]):
    course_data = dict()
    for i in range(len(courses)):
        course = courses[i]
        course_data[course] = {"Time": ms_to_time(int.from_bytes(f.read(3), byteorder="little"))}
        _ = f.read(1)
    for i in range(len(courses)):
        course = courses[i]
        model = int.from_bytes(f.read(1), byteorder="little", signed=True)
        make = make_list[int.from_bytes(f.read(1), byteorder="little", signed=True)]
        if model == -1:
            course_data[course]["Car Make"] = "Not Played"
            course_data[course]["Car Model"] = "Not Played"
        else:
            course_data[course]["Car Make"] = make
            course_data[course]["Car Model"] = model_dict[make][model]
    return course_data

def read_course_times(f: BytesIO, course_data, courses: list[str], course_count: int, course_times_list: list[str]) -> dict[str, int|str]:
    for i in range(course_count):
        course = courses[i]
        lap_1 = int.from_bytes(f.read(2), byteorder="big")
        lap_2 = int.from_bytes(f.read(2), byteorder="big")
        lap_3 = int.from_bytes(f.read(2), byteorder="big")
        total = time_to_ms(course_data[course]["Time"])
        lap_4 = total - (lap_1 + lap_2 + lap_3)
        course_data[course]["Lap 1"] = ms_to_time(lap_1)
        course_data[course]["Lap 2"] = ms_to_time(lap_2)
        course_data[course]["Lap 3"] = ms_to_time(lap_3)
        course_data[course]["Lap 4"] = ms_to_time(lap_4)
        course_builtin_times = course_times_list[i].split(',')
        course_data[course]["Time to Specialist"] = f'{ms_to_time(total - time_to_ms(course_builtin_times[1]))}\n({course_builtin_times[1]})'
        course_data[course]["Time to Platinum"] = f'{ms_to_time(total - time_to_ms(course_builtin_times[2]))}\n({course_builtin_times[2]})'
    return course_data

def read_course_proficiency(f: BytesIO, card_data: dict[str, Any], courses: list[str]):
    course_proficiency_dict = dict()
    for i in range(16):
        course = courses[i*2]
        course_proficiency_dict[course[:-5].rstrip()] = int.from_bytes(f.read(2), byteorder="little")
    return course_proficiency_dict

def read_tunings(f: BytesIO, card_data) -> dict[str, bytes]:
    tuning_dict = dict()
    for i in range(25):
        tuning_dict[f"Car {i}"] = f.read(1)
    return tuning_dict

def read_card_id6(f: BytesIO, card_data) -> dict[str, Any]:
    prefectures = read_txt('app/static/D6/prefectures.txt')
    avatar_gender_list = read_txt('app/static/D6/avatar_gender.txt')
    bgm_volume_list = read_txt('app/static/D8/bgm_volume.txt')
    class_list = read_txt('app/static/D8/class.txt')
    make_list = read_txt('app/static/D8/make.txt')
    car_prefectures = read_txt('app/static/D8/car_prefectures.txt')
    car_hirigana = read_txt('app/static/D8/car_hirigana.txt')
    with open('app/static/D6/cars.json', 'r') as j:
        model_dict = json.loads(j.read())

    card_data["Issued Store"] = f.read(2)
    card_data["User ID"] = int.from_bytes(f.read(4), byteorder="little", signed=True)
    card_data["Home Area"] = prefectures[int.from_bytes(f.read(2), byteorder="little")]
    card_data["Avatar Gender"] = avatar_gender_list[int.from_bytes(f.read(2), byteorder="little")]
    card_data["Previous Card ID"] = int.from_bytes(f.read(4), byteorder="little")
    _ = f.read(32)
    card_data["Store Name"] = (f.read(32).rstrip(b'\x00')).decode('shift-jis')
    config_flag_1 = int.from_bytes(f.read(1))
    card_data["Wheel Sensitivity"] = config_flag_1 % 16
    card_data["BGM Volume"] = bgm_volume_list[config_flag_1 // 16]
    config_flag_2 = f.read(1)  # noqa: F841
    config_flag_3 = int.from_bytes(f.read(1))
    card_data["Force Quit"] = config_flag_3 & 1
    card_data["Cornering Guide"] = (config_flag_3 >> 1) & 1
    card_data["Guide Line"] = (config_flag_3 >> 2) & 1
    card_data["Cup"] = (config_flag_3 >> 3) & 1
    card_data["Barricade"] = (config_flag_3 >> 4) & 1
    card_data["Ghost Car"] = (config_flag_3 >> 5) & 1
    card_data["Class"] = class_list[int.from_bytes(f.read(1), byteorder="little")-1]
    _ = f.read(2)
    card_data["Current Car"] = int.from_bytes(f.read(1), byteorder="little")
    card_data["Number of Cars"] = int.from_bytes(f.read(1), byteorder="little")
    card_data["Play Count"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Pride Points"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Tag Pride Points"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Class Gauge"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Team ID"] = int.from_bytes(f.read(4), byteorder="little", signed=True)
    card_data["First Card ID"] = f.read(4)
    card_data["Team Flag"] = f.read(4)
    card_data["Driver Flags"] = f.read(4)
    card_data["Driver Points"] = int.from_bytes(f.read(4), byteorder="little")
    card_data["Avatar"] = read_avatar_parts(f.read(12))
    card_data["API Request Header"] = f.read(6)
    card_data["User ID (HTTP)"] = f.read(4)
    card_data["Access Code"] = (f.read(22).rstrip(b'\x00')).decode('shift-jis')
    card_data["Driver Name"] = (f.read(14).rstrip(b'\x00')).decode('shift-jis')
    card_data["CRC01"] = f.read(2)
    card_data["Cars"] = read_cars(f, card_data["Number of Cars"], make_list, car_prefectures, car_hirigana, model_dict)
    return card_data

def read_card_id8(f: BytesIO, card_data) -> dict[str, Any]:
    prefectures = read_txt('app/static/D8/prefectures.txt')
    avatar_gender_list = read_txt('app/static/D8/avatar_gender.txt')
    bgm_volume_list = read_txt('app/static/D8/bgm_volume.txt')
    make_list = read_txt('app/static/D8/make.txt')
    car_prefectures = read_txt('app/static/D8/car_prefectures.txt')
    car_hirigana = read_txt('app/static/D8/car_hirigana.txt')
    courses = read_txt('app/static/D8/courses.txt')
    cup_list = read_txt('app/static/D8/cup.txt')
    tachometer_list = read_txt('app/static/D8/tachometer.txt')
    aura_list = read_txt('app/static/D8/aura.txt')
    class_list = read_txt('app/static/D8/class.txt')
    title_list = read_txt('app/static/D8/titles.txt')
    course_times_list = read_txt('app/static/D8/times.txt')
    with open('app/static/D8/cars.json', 'r') as j:
        model_dict = json.loads(j.read())
    with open('app/static/D8/Story/story.json', 'r') as j:
        story_dict = json.loads(j.read())

    card_data["Issued Store"] = f.read(2)
    card_data["User ID"] = int.from_bytes(f.read(4), byteorder="little", signed=True)
    card_data["Home Area"] = prefectures[int.from_bytes(f.read(2), byteorder="little")]
    card_data["Avatar Gender"] = avatar_gender_list[int.from_bytes(f.read(2), byteorder="little")]
    card_data["Previous Card ID"] = int.from_bytes(f.read(4), byteorder="little")
    card_data["DCoin Data"] = read_dcoin_info(f)
    card_data["Store Name"] = (f.read(32).rstrip(b'\x00')).decode('shift-jis')
    config_flag_1 = int.from_bytes(f.read(1))
    card_data["Wheel Sensitivity"] = config_flag_1 % 16
    card_data["BGM Volume"] = bgm_volume_list[config_flag_1 // 16]
    config_flag_2 = f.read(1)  # noqa: F841
    config_flag_3 = int.from_bytes(f.read(1))
    card_data["Force Quit"] = config_flag_3 & 1
    card_data["Cornering Guide"] = (config_flag_3 >> 1) & 1
    card_data["Guide Line"] = (config_flag_3 >> 2) & 1
    card_data["Cup"] = (config_flag_3 >> 3) & 1
    card_data["Barricade"] = (config_flag_3 >> 4) & 1
    card_data["Ghost Car"] = (config_flag_3 >> 5) & 1
    card_data["Class"] = class_list[int.from_bytes(f.read(1), byteorder="little")-1]
    card_data["Class (Match)"] = class_list[int.from_bytes(f.read(1), byteorder="little")-1]
    card_data["Class (Tag Match)"] = class_list[int.from_bytes(f.read(1), byteorder="little")-1]
    card_data["Current Car"] = int.from_bytes(f.read(1), byteorder="little")
    card_data["Number of Cars"] = int.from_bytes(f.read(1), byteorder="little")
    card_data["Play Count"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Pride Points"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Tag Pride Points"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Class Gauge"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Team ID"] = int.from_bytes(f.read(4), byteorder="little", signed=True)
    card_data["First Card ID"] = f.read(4)
    card_data["Team Flag"] = f.read(4)
    card_data["Driver Flags"] = f.read(4)
    card_data["Driver Points"] = int.from_bytes(f.read(4), byteorder="little")
    card_data["Avatar"] = read_avatar_parts(f.read(12))
    _ = f.read(10)
    card_data["Access Code"] = (f.read(22).rstrip(b'\x00')).decode('shift-jis')
    card_data["Driver Name"] = (f.read(14).rstrip(b'\x00')).decode('shift-jis')
    card_data["CRC01"] = f.read(2)
    card_data["Cars"] = read_cars(f, card_data["Number of Cars"], make_list, car_prefectures, car_hirigana, model_dict)
    card_data["Avatar Points"] = int.from_bytes(f.read(1), byteorder="little")
    card_data["My Frame"] = int.from_bytes(f.read(1), byteorder="little")
    card_data["Selected Cup"] = cup_list[int.from_bytes(f.read(1), byteorder="little")]
    card_data["Tachometer"] = tachometer_list[int.from_bytes(f.read(1), byteorder="little")]
    _ = f.read(1)
    card_data["Battle Stance"] = int.from_bytes(f.read(1), byteorder="little")
    card_data["CRC11"] = f.read(2)
    _ = f.read(2)
    card_data["Story Losses"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Story Wins"] = int.from_bytes(f.read(2), byteorder="little")
    _ = f.read(6)
    card_data["Infinity Result Data 1"] = f.read(1)
    card_data["Infinity Result Data 2"] = f.read(1)
    card_data["Infinity Rank"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Story Progress"] = read_story(f, card_data, story_dict)
    _ = f.read(5)
    card_data["Courses"] = read_course_cars(f, courses, make_list, model_dict)
    card_data["Net VS. Plays"] = int.from_bytes(f.read(4), byteorder="little")
    card_data["Net Wins"] = int.from_bytes(f.read(4), byteorder="little")
    _ = f.read(4)
    card_data["Net Now Count"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Net Now Count Wins"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Net Count Win Max"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Refuse Course Flag"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Total In-Store Plays"] = int.from_bytes(f.read(4), byteorder="little")
    card_data["Total In-Store Wins"] = int.from_bytes(f.read(4), byteorder="little")
    card_data["In-Store Now Count"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["In-Store Now Count Wins"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["In-Store Count Win Max"] = int.from_bytes(f.read(2), byteorder="little")
    for course in courses:
        card_data["Courses"][course]["In-Store Wins"] = int.from_bytes(f.read(1), byteorder="little")
    _ = f.read(4)
    card_data["Net Tag VS Plays"] = int.from_bytes(f.read(4), byteorder="little")
    card_data["Net Tag VS Wins"] = int.from_bytes(f.read(4), byteorder="little")
    card_data["Net Tag VS Now Count"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Net Tag VS Now Count Wins"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Net Tag VS Count Win Max"] = int.from_bytes(f.read(2), byteorder="little")
    _ = f.read(6)
    card_data["Tag Level EXP"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Total Bought"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["CRC12"] = f.read(2)
    _ = f.read(2)
    card_data["Tag Story Level"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Tag Story Progress"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Tag Story Lose Count"] = int.from_bytes(f.read(2), byteorder="little")
    _ = f.read(1)
    card_data["Tag New Comer"] = bool(int.from_bytes(f.read(1), byteorder="little"))
    card_data["Tag Story Wins"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Course Proficiency"] = read_course_proficiency(f, card_data, courses)
    card_data["Pro D Mission Flag 0"] = f.read(2)
    card_data["Pro D Mission Flag 1"] = f.read(2)
    card_data["Pro D Mission Flag 2"] = f.read(2)
    card_data["Pro D Mission Page"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Pro D Mission Flag Done 0"] = f.read(2)
    card_data["Pro D Mission Flag Done 1"] = f.read(2)
    card_data["Pro D Mission Flag Done 2"] = f.read(2)
    card_data["Pro D Mission Page Done"] = int.from_bytes(f.read(2), byteorder="little")
    card_data["Mileage"] = int.from_bytes(f.read(4), byteorder="little")
    card_data["Aura"] = aura_list[int.from_bytes(f.read(1), byteorder="little")]
    card_data["Title Effect"] = int.from_bytes(f.read(1), byteorder="little")
    card_data["Title"] = title_list[int.from_bytes(f.read(2), byteorder="little")-1]
    for i in range(10):
        card_data[f"Title Stocker {i}"] = int.from_bytes(f.read(1), byteorder="little")
    card_data["CRC13"] = f.read(2)
    for i in range(3):
        card_data[f"Parts Stocker Index {i}"] = int.from_bytes(f.read(2), byteorder="little")
    for i in range(45):
        card_data[f"Parts Stocker {i}"] = int.from_bytes(f.read(2), byteorder="little", signed=True)
    card_data["Parts Stocker Position 0"] = int.from_bytes(f.read(1), byteorder="little", signed=True)
    card_data["Parts Stocker Position 1"] = int.from_bytes(f.read(1), byteorder="little", signed=True)
    card_data["CRC21"] = f.read(2)
    card_data["Courses"] = read_course_times(f, card_data["Courses"], courses, len(courses), course_times_list)
    card_data["Car Tunings"] = read_tunings(f, card_data)
    card_data["Time Release Car Open Flag"] = f.read(1)
    _ = f.read(4)
    card_data["CRC22"] = f.read(2)
    card_data["Upload Scores"] = True
    return card_data

def read_card(f: BytesIO) -> dict[str, Any]:
    card_data = dict()
    _ = f.read(80)
    card_data["Game Version"] = card_version_dict[f.read(2)]
    game_ver = card_data["Game Version"]
    match game_ver:
        case '8 Infinity':
            return read_card_id8(f, card_data)
        case '6 AA':
            return read_card_id6(f, card_data)
        case _:
            raise Exception('Card Version not matched')


def write_avatar_parts(part_list: list[int]) -> bytes:
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
    return safe_bytes('0x' + ''.join(f'{byte:02X}' for byte in byte_list), 12)

def write_dcoin_info(dcoin_data) -> bytes:
    byte_data = b''
    for i in range(2):
        byte_data += safe_bytes(dcoin_data[i]["DCoin0"], 2, byteorder='little')
        byte_data += safe_bytes(dcoin_data[i]["DCoin1"], 2, byteorder='little')
        byte_data += safe_bytes(dcoin_data[i]["DCoin2"], 2, byteorder='little')
        byte_data += safe_bytes(dcoin_data[i]["Year"], 2, byteorder='little')
        byte_data += safe_bytes(dcoin_data[i]["Month"], 2, byteorder='little')
        byte_data += safe_bytes(dcoin_data[i]["D.Net Stamp"], 2, byteorder='little')
        byte_data += safe_bytes(dcoin_data[i]["Error Count"], 2, byteorder='little')
        byte_data += safe_bytes(dcoin_data[i]["Checksum"], 2, byteorder='little')
    return byte_data

def write_card(f, card_data: dict, user_id: int) -> None:
    prefectures = read_txt('app/static/D8/prefectures.txt')
    avatar_gender_list = read_txt('app/static/D8/avatar_gender.txt')
    bgm_volume_list = read_txt('app/static/D8/bgm_volume.txt')
    make_list = read_txt('app/static/D8/make.txt')
    car_prefectures = read_txt('app/static/D8/car_prefectures.txt')
    car_hirigana = read_txt('app/static/D8/car_hirigana.txt')
    courses = read_txt('app/static/D8/courses.txt')
    cup_list = read_txt('app/static/D8/cup.txt')
    tachometer_list = read_txt('app/static/D8/tachometer.txt')
    aura_list = read_txt('app/static/D8/aura.txt')
    class_list = read_txt('app/static/D8/class.txt')
    title_list = read_txt('app/static/D8/titles.txt')
    with open('app/static/D8/cars.json', 'r') as j:
        model_dict = json.loads(j.read())

    f.seek(80)
    f.write(safe_bytes(card_version_dict.inverse.get(card_data["Game Version"]), 2, byteorder='little'))
    f.write(safe_bytes(card_data["Issued Store"], 2, byteorder='little'))
    f.write(safe_bytes(user_id, 4, byteorder='little', signed=True))
    f.write(safe_bytes(prefectures.index(card_data["Home Area"]), 2, byteorder='little'))
    f.write(safe_bytes(avatar_gender_list.index(card_data["Avatar Gender"]), 2, byteorder='little'))
    f.write(safe_bytes(card_data["Previous Card ID"], 4, byteorder='little'))
    f.write(write_dcoin_info(card_data["DCoin Data"]))
    store_name = card_data["Store Name"].encode('shift-jis')
    padded_store_name = store_name + b'\0' * (32 - len(store_name))  # Pad with null bytes to 32 bytes
    f.write(safe_bytes(padded_store_name, 32, byteorder='little'))

    config_flag_1 = ''
    config_flag_1 += str(bgm_volume_list.index(card_data["BGM Volume"]))
    if int(card_data["Wheel Sensitivity"]) == 10:
        config_flag_1 += 'a'
    else:
        config_flag_1 += str(card_data["Wheel Sensitivity"])
    f.write(safe_bytes(config_flag_1, 1))
    _ = f.read(1)

    config_flag_3 = '00'
    config_flag_3 += str(card_data["Ghost Car"])
    config_flag_3 += str(card_data["Barricade"])
    config_flag_3 += str(card_data["Cup"])
    config_flag_3 += str(card_data["Guide Line"])
    config_flag_3 += str(card_data["Cornering Guide"])
    config_flag_3 += str(card_data["Force Quit"])
    f.write(safe_bytes(int(config_flag_3, 2), 1))

    f.write(safe_bytes(class_list.index(card_data["Class"])+1, 1))
    f.write(safe_bytes(class_list.index(card_data["Class (Match)"]), 1))
    f.write(safe_bytes(class_list.index(card_data["Class (Tag Match)"]), 1))
    f.write(safe_bytes(card_data["Current Car"], 1))
    f.write(safe_bytes(card_data["Number of Cars"], 1))
    f.write(safe_bytes(card_data["Play Count"], 2))
    f.write(safe_bytes(card_data["Pride Points"], 2))
    f.write(safe_bytes(card_data["Tag Pride Points"], 2))
    f.write(safe_bytes(card_data["Class Gauge"], 2))
    f.write(safe_bytes(card_data["Team ID"], 4, signed=True))
    f.write(safe_bytes(card_data["First Card ID"], 4))
    f.write(safe_bytes(card_data["Team Flag"], 4))
    f.write(safe_bytes(card_data["Driver Flags"], 4))
    f.write(safe_bytes(int(card_data["Driver Points"]), 4))
    f.write(write_avatar_parts(card_data["Avatar"]))
    f.write(b'\x00' * 32)
    encoded_name = card_data["Driver Name"].encode('shift-jis')
    padded_name = encoded_name.ljust(14, b'\x00')
    f.write(safe_bytes(padded_name, 14))
    f.write(safe_bytes(card_data["CRC01"], 2))
    for i in range(card_data["Number of Cars"]):
        car_dict = card_data["Cars"][i]
        f.write(safe_bytes(model_dict[car_dict["Make"]].index(car_dict["Model"]), 1))
        f.write(safe_bytes(make_list.index(car_dict["Make"]), 1))
        f.write(safe_bytes(car_dict["Color"], 2))
        f.write(safe_bytes(car_dict["Tuning"], 2))
        f.write(safe_bytes(car_dict["Option Flag"], 2))
        f.write(safe_bytes(car_dict["Car Flag"], 2))
        _ = f.read(2)
        for j in range(4):
            f.write(safe_bytes(car_dict[f"Event Sticker {j+1}"], 1, signed=True))
        f.write(safe_bytes(car_dict["Battle Wins"], 2))
        f.write(safe_bytes(car_dict["Bought Sequence ID"], 2))
        f.write(safe_bytes(car_dict["Infinity Tune"], 2))
        _ = f.read(2)
        f.write(safe_bytes(car_prefectures.index(car_dict["Numplate Prefecture"]), 1))
        f.write(safe_bytes(car_hirigana.index(car_dict["Numplate Hirigana"]), 1))
        f.write(safe_bytes(car_dict["Numplate Class Code"], 2))
        f.write(safe_bytes(car_dict["Numplate Plate Number"], 4))
        f.write(safe_bytes(car_dict["Customizations"], 64))
    for i in range(3 - card_data["Number of Cars"]):
        f.read(96)
    f.write(safe_bytes(card_data["Avatar Points"], 1))
    f.write(safe_bytes(int(card_data["My Frame"]), 1))
    f.write(safe_bytes(cup_list.index(card_data["Selected Cup"]), 1))
    f.write(safe_bytes(tachometer_list.index(card_data["Tachometer"]), 1))
    _ = f.read(1)
    f.write(safe_bytes(int(card_data["Battle Stance"]), 1))
    f.write(safe_bytes(card_data["CRC11"], 2))
    _ = f.read(2)
    f.write(safe_bytes(card_data["Story Losses"], 2))
    f.write(safe_bytes(card_data["Story Wins"], 2))
    _ = f.read(6)
    f.write(safe_bytes(card_data["Infinity Result Data 1"], 1))
    f.write(safe_bytes(card_data["Infinity Result Data 2"], 1))
    f.write(safe_bytes(int(card_data["Infinity Rank"]), 2))
    story_progress_list = []
    for chapter, episodes in card_data["Story Progress"].items():
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
    _ = f.read(6)
    course_data = card_data["Courses"]
    for i in range(len(courses)):
        course = courses[i]
        f.write(safe_bytes(time_to_ms(course_data[course]["Time"]), 3))
        _ = f.read(1)
    for i in range(len(courses)):
        course = courses[i]
        if course_data[course]["Car Model"] == 'Not Played':
            f.write(safe_bytes('0xFF', 1))
            f.write(safe_bytes('0xFF', 1))
        else:
            f.write(safe_bytes(model_dict[course_data[course]["Car Make"]].index(course_data[course]["Car Model"]), 1))
            f.write(safe_bytes(make_list.index(course_data[course]["Car Make"]), 1))
    f.write(safe_bytes(card_data["Net VS. Plays"], 4))
    f.write(safe_bytes(card_data["Net Wins"], 4))
    _ = f.read(4)
    f.write(safe_bytes(card_data["Net Now Count"], 2))
    f.write(safe_bytes(card_data["Net Now Count Wins"], 2))
    f.write(safe_bytes(card_data["Net Count Win Max"], 2))
    f.write(safe_bytes(card_data["Refuse Course Flag"], 2))
    f.write(safe_bytes(card_data["Total In-Store Plays"], 4))
    f.write(safe_bytes(card_data["Total In-Store Wins"], 4))
    f.write(safe_bytes(card_data["In-Store Now Count"], 2))
    f.write(safe_bytes(card_data["In-Store Now Count Wins"], 2))
    f.write(safe_bytes(card_data["In-Store Count Win Max"], 2))
    for i in range(len(courses)):
        course = courses[i]
        f.write(safe_bytes(course_data[course]["In-Store Wins"], 1))
    _ = f.read(4)
    f.write(safe_bytes(card_data["Net Tag VS Plays"], 4))
    f.write(safe_bytes(card_data["Net Tag VS Wins"], 4))
    f.write(safe_bytes(card_data["Net Tag VS Now Count"], 2))
    f.write(safe_bytes(card_data["Net Tag VS Now Count Wins"], 2))
    f.write(safe_bytes(card_data["Net Tag VS Count Win Max"], 2))
    _ = f.read(6)
    f.write(safe_bytes(card_data["Tag Level EXP"], 2))
    f.write(safe_bytes(card_data["Total Bought"], 2))
    f.write(safe_bytes(card_data["CRC12"], 2))
    _ = f.read(2)
    f.write(safe_bytes(card_data["Tag Story Level"], 2))
    f.write(safe_bytes(card_data["Tag Story Progress"], 2))
    f.write(safe_bytes(card_data["Tag Story Lose Count"], 2))
    _ = f.read(1)
    f.write(safe_bytes(int(card_data["Tag New Comer"]), 1))
    f.write(safe_bytes(card_data["Tag Story Wins"], 2))
    course_proficiency_dict = card_data["Course Proficiency"]
    for i in range(16):
        course = courses[i*2]
        f.write(safe_bytes(course_proficiency_dict[course[:-5].rstrip()], 2))
    for i in range(3):
        f.write(safe_bytes(card_data[f"Pro D Mission Flag {i}"], 2))
    f.write(safe_bytes(card_data["Pro D Mission Page"], 2))
    for i in range(3):
        f.write(safe_bytes(card_data[f"Pro D Mission Flag Done {i}"], 2))
    f.write(safe_bytes(card_data["Pro D Mission Page Done"], 2))
    f.write(safe_bytes(int(card_data["Mileage"]), 4))
    f.write(safe_bytes(aura_list.index(card_data["Aura"]), 1))
    f.write(safe_bytes(int(card_data["Title Effect"]), 1))
    f.write(safe_bytes(title_list.index(card_data["Title"]) + 1, 2))
    for i in range(10):
        f.write(safe_bytes(card_data[f"Title Stocker {i}"], 1))
    f.write(safe_bytes(card_data["CRC13"], 2))
    for i in range(3):
        f.write(safe_bytes(card_data[f"Parts Stocker Index {i}"], 2))
    for i in range(45):
        f.write(safe_bytes(card_data[f"Parts Stocker {i}"], 2, signed=True))
    f.write(safe_bytes(card_data["Parts Stocker Position 0"], 1, signed=True))
    f.write(safe_bytes(card_data["Parts Stocker Position 1"], 1, signed=True))
    f.write(safe_bytes(card_data["CRC21"], 2))
    for i in range(len(courses)):
        course = courses[i]
        f.write(safe_bytes(time_to_ms(course_data[course]["Lap 1"]), 2, byteorder="big"))
        f.write(safe_bytes(time_to_ms(course_data[course]["Lap 2"]), 2, byteorder="big"))
        f.write(safe_bytes(time_to_ms(course_data[course]["Lap 3"]), 2, byteorder="big"))
    tuning_dict = card_data["Car Tunings"]
    for i in range(25):
        f.write(safe_bytes(tuning_dict[f"Car {i}"], 1))
    f.write(safe_bytes(card_data["Time Release Car Open Flag"], 1))
    _ = f.read(4)
    f.write(safe_bytes(card_data["CRC22"], 2))

def create_leaderboard_table() -> None:
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

def upload_times(user_id: int, username: str, times) -> int:
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
