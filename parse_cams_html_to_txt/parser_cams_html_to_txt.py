from bs4 import BeautifulSoup as BS
import os
import re

DEFAULT_INPUT_FILE_NAME = 'cams.htm'
DEFAULT_OUTPUT_FILE_NAME = 'cams.txt'
DEFAULT_SORTED_OUTPUT_FILE_NAME = 'cams_sort.txt'


def desc(ip):
    lst = [int(i) for i in re.findall('\d+', ip)]
    return (lst[0] * 256 ** 3 + lst[1] * 256 ** 2 + lst[2] * 256 + lst[3]) * 100


def sorted_dict(dct):
    myKeys = list(dct.keys())
    myKeys.sort()
    sorted_dict = {i: dct[i] for i in myKeys}
    return sorted_dict


def parser():
    result_dict = {}
    try:
        with open(DEFAULT_INPUT_FILE_NAME, encoding='utf-8') as i_file:
            bs = BS(i_file, 'html.parser')
            table_cams = bs.select_one('#cameras-list')
            for camera in table_cams.select('tr.camera'):
                ip = camera.select_one('.ip').select_one('a').get_text()
                name = camera.select_one('.name').get_text()
                if not ip:
                    continue
                key = desc(ip)
                if result_dict.get(key) or int(ip.split('.')[-1]) > 254:
                    answer = input(f'{ip} - уже есть в списке оставить?(Enter or n): ')
                    if answer == 'n':
                        continue
                    else:
                        while result_dict.get(key):
                            key += 1
                result_dict[key] = f'{ip} cam{name},'
        with open(DEFAULT_OUTPUT_FILE_NAME, 'w+', encoding='utf-8') as o_file:
            o_file.writelines('\n'.join(list(result_dict.values())))
        with open(DEFAULT_SORTED_OUTPUT_FILE_NAME, 'w+', encoding='utf-8') as o_file:
            o_file.writelines('\n'.join(list(sorted_dict(result_dict).values())))
        return True
    except Exception as e:
        print(e)
        print(f'Нет файла {DEFAULT_INPUT_FILE_NAME} в корне программы!!!')
    return False


if __name__ == '__main__':
    print('Прога для конвертации html файла в txt\n'
          '-----------------------------------------------------------------\n'
          f'Для работы необходимо что бы файл {DEFAULT_INPUT_FILE_NAME} находился в той же дирректории\n'
          f'на выходе будет 2 файла {DEFAULT_OUTPUT_FILE_NAME} и отсортированый {DEFAULT_SORTED_OUTPUT_FILE_NAME}\n'
          'при зваершении работы автоматически откроется сортированный файл\n'
          '-------------------------- by CrassAir --------------------------\n')
    is_success = parser()
    if is_success:
        os.startfile(DEFAULT_SORTED_OUTPUT_FILE_NAME)
    input('Работа парсера закончена... для выхода нажмите Enter')
