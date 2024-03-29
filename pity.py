import genshinstats as gs
import genshin as gs_
import os, time, json, sys
from dotenv import load_dotenv
from time import sleep

load_dotenv(dotenv_path='settings.env')

with open(f'lang/{os.getenv("lan")}.json', 'r', encoding='utf-8') as lang:
    lang = json.load(lang)
    ID = lang['id']
    ERROR = lang['error_banner']
    PITY5 = lang['5*pity']
    PITY4 = lang['4*pity']
    REPEAT_ERROR = lang['repeat_error']
    REPEAT_ERROR2 = lang['repeat_error2']
    REPEAT = lang['repeat']
    REPEAT_W = lang['repeat_w']
    AUTH_ERROR = lang['auth_error']
    AUTH_TIMEOUT = lang['auth_timeout']
    QUIT_ = lang['quit']
    LAST = lang['last']
    NO_WISH_HISTORY_ERROR = lang['no_wish_history_error']
    NO_WISH_HISTORY_ERROR2 = lang['no_wish_history_error2']
    SOFT = lang['soft']
    TSOFT = lang['tsoft']
    CACHE = lang['cache']
    LCACHE = lang['load_cache']
    NOCACHE = lang['no_cache']
    NEXT = lang['next']
    PERMS_ERROR = lang['perms_error']

def search_string_in_file(file_name, string_to_search):
    line_number = 0
    list_of_results = []
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            line_number += 1
            if string_to_search in line:
                list_of_results.append((line_number, line.rstrip()))
    read_obj.close()
    return list_of_results

if os.getenv('cache') == "True":
    if os.path.exists(f'{os.environ["APPDATA"]}/nitolar play') == False:
        os.mkdir(f'{os.environ["APPDATA"]}/nitolar play')
        os.mkdir(f'{os.environ["APPDATA"]}/nitolar play/pity calc')
    else:
        if os.path.exists(f'{os.environ["APPDATA"]}/nitolar play/pity calc') == False:
            os.mkdir(f'{os.environ["APPDATA"]}/nitolar play/pity calc')

# https://webstatic-sea.hoyoverse.com/genshin/ - 44

global S_MSG
S_MSG = False

if os.getenv('authkey')[0:44] != 'https://webstatic-sea.hoyoverse.com/genshin/':
    if os.getenv('authkey') == 'auto':
        if os.getenv('gameloc') == "None":
            try:
                AUTH = gs_.utility.get_authkey()
            except PermissionError:
                print('\33[31m' + PERMS_ERROR + '\33[0m')
                AUTH = "sus"
                S_MSG = True
        else:
            try:
                AUTH = gs_.utility.get_authkey(os.getenv('gameloc'))
            except PermissionError:
                print('\33[31m' + PERMS_ERROR + '\33[0m')
                AUTH = "sus"
                S_MSG = True
    else:
        print('\33[31m' + AUTH_ERROR + '\33[0m')
        quit()
else:
    AUTH = gs.extract_authkey(os.getenv('authkey'))

REPEAT_FLAG = os.getenv('repeat')
r_a = ['ask', 'no', 'yes']

if REPEAT_FLAG not in r_a:
    print('\33[31m' + REPEAT_ERROR + '\33[0m')
    quit()

global BANNER
BANNER = 301

def check_():
    if os.path.exists('log.txt') == True:
        os.remove('log.txt')

    list_rec = 90
    if BANNER == 302:
        list_rec = 80

    for s in gs.get_wish_history(BANNER, 200, authkey=AUTH):
        with open('log.txt', "a+", encoding='utf-8') as file:
            file.write(f"{s['rarity']}* - {s['name']}, {s['type']}" + '\n')
            file.close()

    print(time.strftime('%H:%M:%S'))

    star5_ = search_string_in_file('log.txt', '5* - ')

    dict_prc = {74: '6.6%', 75: '12.6%', 76: '18.6%', 77: '24.6%', 78: '30.6%', 79: '36.6%', 80: '42.6%', 81: '48.6%', 82: '54.6%', 83: '60.6%', 84: '66.6%', 85: '72.6%', 86: '78.6%', 87: '84.6%', 88: '90.6%', 89: '96.6%', 90: '100%'}

    load = False

    if str(star5_) == '[]':
        if os.path.exists(f'{os.environ["APPDATA"]}/nitolar play/pity calc/{BANNER}.json') == True:
            with open(f'{os.environ["APPDATA"]}/nitolar play/pity calc/{BANNER}.json', "r", encoding='utf-8') as data_:
                data = json.load(data_)
            print('\33[93m' + CACHE + '\33[0m')
            isoft = int(data['5*'][0]['soft'])
            if list_rec == 80:
                if isoft >= 63:
                    isoft = isoft + 11
                    print(f'\33[92m{SOFT.replace("?num?", "64")} {dict_prc[isoft]}\33[34m')
                else:
                    print(f'\33[92m{TSOFT.replace("?num?", f"{63 - isoft}")}\33[34m')
            else:
                if isoft >= 73:
                    isoft = isoft + 1
                    print(f'\33[92m{SOFT.replace("?num?", "74")} {dict_prc[isoft]}\33[34m')
                else:
                    print(f'\33[92m{TSOFT.replace("?num?", f"{73 - isoft}")}\33[34m')
                    
            print(f'{PITY5}' + f'{data["5*"][0]["pity"]}' + f'\n{LAST} 5*: ' + f'{data["5*"][0]["last"]}')
            if data["5*"][0]["next"] != None:
                print(f'{NEXT.replace("?star?", "5*")}' + f'{data["5*"][0]["next"]}')
            data_.close()
            load = True
        else:
            print(f'{PITY5}' + f'{NO_WISH_HISTORY_ERROR} 5*' + f'\n{LAST} 5*: ' + NO_WISH_HISTORY_ERROR2)
            load = True

    n5star = None

    for star5 in star5_:
        n_star5 = list_rec - int(star5[0]) + 1
        if n_star5 <= 0:
            n_star5 = 1

        isoft = list_rec - n_star5
        if list_rec == 90:
            if isoft >= 73:
                isoft = isoft + 1
                print(f'\33[92m{SOFT.replace("?num?", "74")} {dict_prc[isoft]}\33[34m')
            else:
                print(f'\33[92m{TSOFT.replace("?num?", f"{73 - isoft}")}\33[34m')
        else:
            if isoft >= 63:
                isoft = isoft + 11
                print(f'\33[92m{SOFT.replace("?num?", "64")} {dict_prc[isoft]}\33[34m')
            else:
                print(f'\33[92m{TSOFT.replace("?num?", f"{63 - isoft}")}\33[34m')

        print(f'{PITY5}' + f'{n_star5} / {list_rec}' + f'\n{LAST} 5*: ' + star5[1][5:])
        if BANNER == 200:
            if f'{star5_[0]}'[-3] == 'r' and f'{star5_[1]}'[-3] == 'r':
                print(f'{NEXT.replace("?star?", "5*")}' + 'Weapon')
                n5star = 'Weapon'
            elif f'{star5_[0]}'[-3] == 'n' and f'{star5_[1]}'[-3] == 'n':
                print(f'{NEXT.replace("?star?", "5*")}' + 'Character')
                n5star = 'Character'
        break

    star4_ = search_string_in_file('log.txt', '4* - ')

    if str(star4_) == '[]':
        if os.path.exists(f'{os.environ["APPDATA"]}/nitolar play/pity calc/{BANNER}.json') == True:
            with open(f'{os.environ["APPDATA"]}/nitolar play/pity calc/{BANNER}.json', "r", encoding='utf-8') as data_:
                data = json.load(data_)
            print(f'{PITY4}' + f'{data["4*"][0]["pity"]}' + f'\n{LAST} 4*: ' + f'{data["4*"][0]["last"]}')
            if data["4*"][0]["next"] != None:
                print(f'{NEXT.replace("?star?", "4*")}' + f'{data["4*"][0]["next"]}')
            data_.close()
            load = True
        else:
            print(f'{PITY4}' + f'{NO_WISH_HISTORY_ERROR} 4*' + f'\n{LAST} 4*: ' + NO_WISH_HISTORY_ERROR2)
            load = True

    n4star = None

    for star4 in star4_:
        n_star4 = 10 - int(star4[0]) + 1
        if n_star4 <= 0:
            n_star4 = 1
        print(f'{PITY4}' + f'{n_star4} / 10' + f'\n{LAST} 4*: ' + star4[1][5:])
        if f'{star4_[0]}'[-3] == 'r' and f'{star4_[1]}'[-3] == 'r':
            print(f'{NEXT.replace("?star?", "4*")}' + 'Weapon')
            n4star = 'Weapon'
        elif f'{star4_[0]}'[-3] == 'n' and f'{star4_[1]}'[-3] == 'n':
            print(f'{NEXT.replace("?star?", "4*")}' + 'Character')
            n4star = 'Character'
        break

    if load != True:
        if os.getenv('cache') == "True":
            with open(f'{os.environ["APPDATA"]}/nitolar play/pity calc/{BANNER}.json', 'w+', encoding='utf-8') as cach:
                ap = {}
                ap['5*'] = []
                ap['4*'] = []

                ap['5*'].append({
                    'last': star5[1][5:],
                    'pity': f'{n_star5} / {list_rec}',
                    'soft': isoft,
                    'next': n5star
                })

                ap['4*'].append({
                    'last': star4[1][5:],
                    'pity': f'{n_star4} / 10',
                    'next': n4star
                })
                json.dump(ap, cach, indent=4)
                cach.close()

    if REPEAT_FLAG == 'yes':
        print('----------------------------------------')
        sleep(int(os.getenv('sleep')))
        check_()
    elif REPEAT_FLAG == 'no':
        print('----------------------------------------' + '\33[0m')
        user_input()

global ISET
ISET = False

def user_input():
    global REPEAT_FLAG
    REPEAT_FLAG = os.getenv('repeat')
    try:
        banner = gs.get_banner_types(AUTH)
    except (gs.errors.AuthkeyTimeout, gs.errors.InvalidAuthkey):
        if S_MSG == False:
            print('\33[31m' + AUTH_TIMEOUT + '\33[0m')
        if str(os.listdir(f'{os.environ["APPDATA"]}/nitolar play/pity calc')) == '[]':
            print('\33[93m' + NOCACHE + '\33[0m')
            quit()
        while True:
            print('\33[93m' + LCACHE.replace('?nums?', str(os.listdir(f'{os.environ["APPDATA"]}/nitolar play/pity calc'))) + '\33[0m')

            global ID_CACHE
            ID_CACHE = input(ID)

            if ID_CACHE == 'quit':
                quit()

            if ID_CACHE not in os.listdir(f'{os.environ["APPDATA"]}/nitolar play/pity calc'):
                print('----------------------------------------')
                print('\33[31m' + ERROR + '\33[0m')
                print('----------------------------------------')
                continue
            else:
                dict_prc = {74: '6.6%', 75: '12.6%', 76: '18.6%', 77: '24.6%', 78: '30.6%', 79: '36.6%', 80: '42.6%', 81: '48.6%', 82: '54.6%', 83: '60.6%', 84: '66.6%', 85: '72.6%', 86: '78.6%', 87: '84.6%', 88: '90.6%', 89: '96.6%', 90: '100%'}

                list_rec = 90
                if ID_CACHE[0:3] == '302':
                    list_rec = 80

                print('\33[34m----------------------------------------\33[0m')
                with open(f'{os.environ["APPDATA"]}/nitolar play/pity calc/{ID_CACHE[0:3]}.json', "r", encoding='utf-8') as data_:
                    data = json.load(data_)
                isoft = int(data['5*'][0]['soft'])
                if list_rec == 80:
                    if isoft >= 63:
                        isoft = isoft + 11
                        print(f'\33[92m{SOFT.replace("?num?", "64")} {dict_prc[isoft]}\33[34m')
                    else:
                        print(f'\33[92m{TSOFT.replace("?num?", f"{63 - isoft}")}\33[34m')
                else:
                    if isoft >= 73:
                        isoft = isoft + 1
                        print(f'\33[92m{SOFT.replace("?num?", "74")} {dict_prc[isoft]}\33[34m')
                    else:
                        print(f'\33[92m{TSOFT.replace("?num?", f"{73 - isoft}")}\33[34m')

                print(f'{PITY5}' + f'{data["5*"][0]["pity"]}' + f'\n{LAST} 5*: ' + f'{data["5*"][0]["last"]}')
                if data["5*"][0]["next"] != None:
                    print(f'{NEXT.replace("?star?", "5*")}' + f'{data["5*"][0]["next"]}')
                print(f'{PITY4}' + f'{data["4*"][0]["pity"]}' + f'\n{LAST} 4*: ' + f'{data["4*"][0]["last"]}')
                if data["4*"][0]["next"] != None:
                    print(f'{NEXT.replace("?star?", "4*")}' + f'{data["4*"][0]["next"]}')
                data_.close()
                print('----------------------------------------')
                continue

    print(f'\33[0m{banner}')
    print('\33[33m' + QUIT_ + '\33[0m')

    global BANNER
    global ISET

    if len(sys.argv) < 2:
        BANNER = input(ID)
    else:
        if ISET == False:
            print(ID + str(sys.argv[1]))
            BANNER = int(sys.argv[1])
            ISET = True
        else:
            BANNER = input(ID)

    try:
        BANNER = int(BANNER)

        if banner.get(BANNER) == None:
            print('----------------------------------------')
            print('\33[31m' + ERROR + '\33[0m')
            print('----------------------------------------')
            user_input()
        else:
            if REPEAT_FLAG == 'ask':
                print('\33[31m' + REPEAT_W + '\33[0m')
                r_a = ['no', 'yes']
                while True:
                    REPEAT_FLAG = input(REPEAT)
                    if REPEAT_FLAG not in r_a:
                        print('\33[31m' + REPEAT_ERROR2 + '\33[0m')
                        print('----------------------------------------')
                        continue
                    else:
                        break
            print('\33[34m' + '----------------------------------------')
            check_()
    except: 
        if BANNER == 'quit':
            quit()
        print('----------------------------------------')
        print('\33[31m' + ERROR + '\33[0m')
        print('----------------------------------------')
        user_input()

user_input()