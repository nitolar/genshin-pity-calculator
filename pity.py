import genshinstats as gs
import genshin as gs_
import os, time, json
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
  
# https://webstatic-sea.hoyoverse.com/genshin/ - 44
    
if os.getenv('authkey')[0:44] != 'https://webstatic-sea.hoyoverse.com/genshin/':
    if os.getenv('authkey') == 'auto':
        AUTH = gs_.utility.get_authkey()
    else:
        print('\33[31m' + AUTH_ERROR + '\33[0m')
        quit()
else:
    AUTH = gs_.utility.extract_authkey(os.getenv('authkey'))

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
    
    for s in gs.get_wish_history(BANNER, 90, authkey=AUTH):
        with open('log.txt', "a+", encoding='utf-8') as file:
            file.write(f"{s['rarity']}* - {s['name']}, {s['type']}" + '\n')
            file.close()
            
    print(time.strftime('%H:%M:%S'))
    
    star5_ = search_string_in_file('log.txt', '5* - ')
    
    for star5 in star5_:
        print(f'{PITY5}' + f'{90 - int(star5[0]) + 1}' + f'\n{LAST} 5*: ' + star5[1][5:])
        break
        
    star4_ = search_string_in_file('log.txt', '4* - ')
    
    for star4 in star4_:
        print(f'{PITY4}' + f'{10 - int(star4[0]) + 1}' + f'\n{LAST} 4*: ' + star4[1][5:])
        break
        
    if REPEAT_FLAG == 'yes':
        print('----------------------------------------')
        sleep(int(os.getenv('sleep')))
        check_()
    elif REPEAT_FLAG == 'no':
        print('----------------------------------------' + '\33[0m')
        user_input()
    
def user_input():
    global REPEAT_FLAG
    REPEAT_FLAG = os.getenv('repeat')
    try:
        banner = gs.get_banner_types(AUTH)
    except gs.errors.AuthkeyTimeout:
        print('\33[31m' + AUTH_TIMEOUT + '\33[0m')
        quit()
    print(f'\33[0m{banner}')
    print('\33[33m' + QUIT_ + '\33[0m')
    
    global BANNER
    BANNER = input(ID)
    
    try:
        BANNER = int(BANNER)

        if banner.get(BANNER) == None:
            print('----------------------------------------')
            print('\33[31m' + ERROR + '\33[0m')
            print('----------------------------------------')
            user_input()
        else:
            print('----------------------------------------')
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