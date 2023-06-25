from bs4 import BeautifulSoup as BS
import os

DEFAULT_INPUT_FILE_NAME = 'cams.htm'
DEFAULT_OUTPUT_FILE_NAME = 'cams.txt'
DEFAULT_SORTED_OUTPUT_FILE_NAME = 'cams_sort.txt'


def desc(ip):
    lst = [int(i) for i in ip.split('.')]
    return lst[0] * 256 ** 3 + lst[1] * 256 ** 2 + lst[2] * 256 + lst[3]


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
                if not ip or int(ip.split('.')[-1]) > 254:
                    continue
                result_dict[desc(ip)] = f'{ip} cam{name}'
        with open(DEFAULT_OUTPUT_FILE_NAME, 'w+', encoding='utf-8') as o_file:
            o_file.writelines('\n'.join(list(result_dict.values())))
        with open(DEFAULT_SORTED_OUTPUT_FILE_NAME, 'w+', encoding='utf-8') as o_file:
            o_file.writelines('\n'.join(list(sorted_dict(result_dict).values())))
            os.startfile(DEFAULT_SORTED_OUTPUT_FILE_NAME)
    except Exception:
        print(f'Нет файла {DEFAULT_INPUT_FILE_NAME} в корне программы!!!')


if __name__ == '__main__':
    print('Прога для конвертации html файла в txt\n'
          '-----------------------------------------------------------------\n'
          f'Для работы необходимо что бы файл {DEFAULT_INPUT_FILE_NAME} находился в той же дирректории\n'
          f'на выходе будет 2 файла {DEFAULT_OUTPUT_FILE_NAME} и отсортированый {DEFAULT_SORTED_OUTPUT_FILE_NAME}\n'
          'при зваершении работы автоматически откроется сортированный файл\n'
          '-------------------------- by CrassAir --------------------------\n')
    parser()
    input('Работа парсера закончена...')
