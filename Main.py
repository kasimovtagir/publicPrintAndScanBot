#from cgitb import text
from email import message
from platform import python_branch
#import requests
from hashlib import sha1
import telebot 
from telebot import types
from PyPDF2 import PdfFileReader
import re
import time
from datetime import datetime
import os
import os.path, time
import string
import subprocess
#from PIL import Imagex  
import user
from user import  NoTidError, BadRoleError, ServerError
from requests.exceptions import Timeout
import random

import CallBackTG
import UploadTG
import Printing
import Scanning
import Additional


#os.system ("service cups restart")

def return_time():
    dt = datetime.now()
    dt_string = dt.strftime("%d.%m %H:%M")
    return dt_string

  
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States

from telebot.storage import StateMemoryStorage
ADMINS= ""
BOT_TOKEN = ""
RESTAPI_ACCESS_TOKEN = ""
state_storage = StateMemoryStorage() 
 
# import keys
# ADMINS = keys.ADMINS
# BOT_TOKEN = keys.BOT_TOKEN
# RESTAPI_ACCESS_TOKEN = keys.RESTAPI_ACCESS_TOKEN


if ADMINS == "" and BOT_TOKEN == "" and RESTAPI_ACCESS_TOKEN=="":
    ADMINS = str( os.environ["ADMINS"])
    BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    RESTAPI_ACCESS_TOKEN = os.environ["REST_API_TOKEN"]

USER_API = user.UserAPI(token=RESTAPI_ACCESS_TOKEN)


bot  = telebot.TeleBot(BOT_TOKEN,state_storage=state_storage)



@bot.message_handler(func=lambda message: not filter_Tg( bot, message.chat.id ))
def Send_instruction(message):
   bot.send_document(message.chat.id ,open("instruction.jpg", 'rb'))

    
@bot.message_handler(content_types=["photo"]) 
def sends_photo(message):
    
    data = bot.current_states.get_data(message.chat.id, message.chat.id )
    if data is not None:
        choose_printer = data.get("choose_printer")
        #file_name = data.get("file_name")
    else:
        choose_printer = None
        #file_name = None

     #bot.send_message(message.chat.id, "Файл нужно отправить без сжатия.")
    photo = message.photo[-1]
    file_id = photo.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    # Здесь вы можете обработать картинку, используя file_path
    # Например, можно ее скачать:
    downloaded_file = bot.download_file(file_path)

    # Затем можно сохранить скачанную картинку на диск:
    file_name = renameFile()+".jpg"
    bot.current_states.set_data(message.chat.id, message.from_user.id, "file_name", file_name)
    with open(f'/mnt/File/{file_name}', 'wb') as file:
        file.write(downloaded_file)
    bot.send_message(message.chat.id,"Имя файла: - "+ format(str(file_name))+"\nПринтер: - "+ str(choose_printer), reply_markup=CallBackTG.pre_printing())


def renameFile():
    return ''.join(random.choice("qwertyyuuiiop[lkjhgfdsmnbvcxzme") for _ in range(6))

    

def get_printers():
    list_printers = []
    try:
        # Выполняем команду lpstat для получения списка принтеров
        result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True, check=True)

        # Разбиваем вывод команды на строки
        lines = result.stdout.splitlines()

        # Извлекаем имена принтеров из строк
        printers = [line.split()[1] for line in lines]

        #printers = printers.split("[]'")
        #printers = printers.remove("'[")
        cleaned_text =''.join(char for char in printers if char not in "[]'")

        list_printers.append(cleaned_text)
        return list_printers

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        return []    

@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id == 815850294:
        #print("adsd")
        CallBackTG.callback_start(bot, message, "ADMINS" )
    else: 
        CallBackTG.callback_start(bot, message, "user")


#Доступ через сайт      
def filter_Tg(bot, tg_id):
    print(tg_id)
    try:
        try:
            user = USER_API.get_user_by_tid(tg_id)
            print (user.roles)
            return True
        except (Timeout, ServerError) as e:
            bot.send_message(tg_id, f"1.Чтобы получить доступ к телеграм боту вам необходимо добавить ваш TG ID в личный кабинет на сайте physics.itmo.ru.\nВаш TG ID - {tg_id}\n")
            #print(e)
        except (BadRoleError, NoTidError) as e:
            bot.send_message(tg_id, f"2.Чтобы получить доступ к телеграм боту вам необходимо добавить ваш TG ID в личный кабинет на сайте physics.itmo.ru.\nВаш TG ID - {tg_id}\n")
            #print(e)
        except Exception as e:
            bot.send_message(tg_id, f"3.Чтобы получить доступ к телеграм боту вам необходимо добавить ваш TG ID в личный кабинет на сайте physics.itmo.ru.\nВаш TG ID - {tg_id}\n")
            #print(e)
        return False 
    except :
         bot.send_message(tg_id,f"4.Чтобы получить доступ к телеграм боту вам необходимо добавить ваш TG ID в личный кабинет на сайте physics.itmo.ru.\nВаш TG ID - {tg_id}\n")

#Загрузка файл12ов      
@bot.message_handler(content_types=['document'])
def documents(message):
    UploadTG.Upload_files(bot,message)

      
#
@bot.callback_query_handler(func=lambda call: True)
def Actions (call):
    list_printers = []
    list_printers = get_printers()
    if call.data == "help_button":
        bot.send_message(call.from_user.id, text='Привет, я бот, который поможет тебе распечатать или отсканировать документ. \nЯ умею выбирать количество копий, формат бумаги (А3, А4, А5), печатать на обеих сторонах листа или включать режим постраничной печати. \nНажми start, чтобы начать.')

    if call.data == "back_button":
        Additional.Back_Button (bot,call)

    if call.data == "admin_button":
        CallBackTG.admin_buttons(bot,call)
        #print("admin")

    if call.data == "restart_cups":
        os.system("service cups restart")
        bot.send_message(call.message.chat.id, text='Служба перезапущена.')

    if call.data == "show_log":
        CallBackTG.admins(bot,call)
        #os.system("service cups restart")

    if call.data =="mount_store":
        path = "//mnt//Scan//print15"
        if os.path.exists(path) and os.path.isdir(path):
            bot.send_message(call.message.chat.id, text='Папка примонтирована.')
            #print("Сетевая папка примонтирована")
        else:
            #print("Сетевая папка не примонтирована")
            CallBackTG.admin_mount_store_yes_or_no(bot,call)
            #
            #print("Сетевая папка примонтирована")

    if call.data =="admin_mount_yes":
        try:
            os.system("mount -t nfs 192.168.5.49:/share/scan_bot /mnt/Scan/ -o nolock")
            bot.send_message(call.message.chat.id, text='Готово, папка примонтирована.')
        except: bot.send_message(call.message.chat.id, text='нет прав')


#-------------------------------------------------------------------------------------
    #show list scaner
    if call.data== "list_Scan":
        CallBackTG.callback_list_Print_for_scan(bot,call)

    scan_options = {
        "print21_scan": "print21",
        "print4318_scan": "print4318",
        "print17_scan": "print17",
        "print431_scan": "print431",
        "print7_scan": "print7",
        "print18_scan": None,
        "print19_scan": "print19",
        "print14_scan": None,
        "print15_scan": "print15",
        "print16_scan": "print16",
        "print10_scan": "print10",
        "print9_scan": "print9",
        "print22_scan": "print22",
        "print13_scan": "print13"
    }


    if call.data in scan_options:
        option = scan_options[call.data]
        if option is not None:
            CallBackTG.callback_print_scan(bot, call, option)
        else:
            bot.send_message(call.message.chat.id, text='В разработке.')


#-------------------------------------------------------------------------------------
    
    #show list printers
    if call.data == "list_Print":
        Printing.List_Print(bot, call)

    #action with printers
    print_options = {
            "print22_print": "print22.metalab.ifmo.ru",
            "print19_print": "print19.metalab.ifmo.ru",
            "print10_print": "print10.metalab.ifmo.ru",
            "print13_print": "print13.metalab.ifmo.ru",
            "print9_print": "print9.metalab.ifmo.ru",
            "print14_print": "print14.metalab.ifmo.ru",
            "print15_print": "print15.metalab.ifmo.ru",
            "print16_print": "print16.metalab.ifmo.ru",
            "print18_print": "print18.metalab.ifmo.ru",
            "print7_print": "print7.metalab.ifmo.ru",
            "print21_print": "print21.metalab.ifmo.ru",
            "print4318_print": "print4318.metalab.ifmo.ru",
            "print17_print": "print17.metalab.ifmo.ru",
            "print2426_print": "print2426.metalab.ifmo.ru"
        }


    if call.data in print_options:
        option = print_options[call.data]
        Printing.Show_Information(bot, call, option)
#-------------------------------------------------------------------------------------

    #show access additionals 
    if call.data == "Additionally":
        Additional.Button_Additional(bot,call)

    if call.data == "duplex_print" :
        Additional.Button_Duplex_Print(bot,call)

    if call.data == "count_Copies" :
        Additional.Button_Choose_Count_Copies(bot, call)  

    count_copies_option = {
        "count_one": "1",
        "count_two": "2",
        "count_three": "3",
        "count_four": "4",
        "count_copies_n": None
        }    

    if call.data in count_copies_option:
        option = count_copies_option[call.data]
        if option is not None:
            Additional.Button_Count_Copies(bot,call,option)
        else:
            Additional.button_N_Copies(bot,call)


    
    if call.data == "pages" :
        Additional.Button_Choose_print_Pages(bot,call)


    if call.data == "format_pages":
        Additional.Show_size_paper(bot,call)


    size_option = {
        "sizeA3": "3",
        "sizeA4": "4",
        "sizeA5": "5"
    }

    if call.data in size_option:
        option = size_option[call.data]
        if option is not None:
             Additional.Button_Size_Papes(bot,call,option)


    if call.data == "cancel":
        CallBackTG.cansel_buttons(bot, call)

    if call.data == "call_yes":
        CallBackTG.call_yes(bot, call)

    if call.data == "call_no":
        CallBackTG.call_no(bot, call)      




#-----------------------------------------------------------START PRINTING--------------------------------
    if call.data=="Printing":
        data = bot.current_states.get_data(call.message.chat.id, call.message.chat.id )
        if data is not None:
            file_name = data.get("file_name")
            choose_printer = data.get ("choose_printer")
            duplex_print = data.get("duplex_print")
            count_copies = data.get("count_copies")
            pages_print = data.get ("pages_print")
            size_paper = data.get ("size_paper")
            pagess = data.get ("pagess")

        else:
            file_name = None
            choose_printer = None
            duplex_print = None
            count_copies= None
            pages_print = None
            size_paper = None
            pagess = None

        with open('/mnt/Logs/logs.txt', 'a') as logs:
            logs.write( f"{str(return_time())} - Пользователь: {str(call.from_user.first_name)} - отправил на печеть файл: {format(str(file_name))} На принтер {choose_printer} \n")

        if file_name == None:
            bot.send_message(call.message.chat.id,f"Зафиксировано повторное нажатие. \nНажми на кнопку START")       
        else:
            bot.send_message(call.message.chat.id,f"Идет печать файла: {format(str(file_name))} \nНа принтере: {choose_printer}\n")
            if pages_print==None:
                pages_print =""
            else: 
                pages_print=f" -o page-ranges={pages_print}"
            
            if duplex_print==None:
                duplex_print=""
            if count_copies == None:
                count_copies= ""    
            if size_paper==None:
                size_paper=""
                printing =  f"lp -d {choose_printer} /mnt/File/{file_name} -o media=A4 {duplex_print} {count_copies} {pages_print} {size_paper}"

            else: printing =  f"lp -d {choose_printer} /mnt/File/{file_name} {size_paper} {duplex_print} {count_copies} {pages_print}"
            
            print(f"{str(return_time())} - Пользователь: {str(call.from_user.first_name)} - отправил на печеть файл: {format(str(file_name))} На принтер {choose_printer}")
            print(printing)
            #убрать комент который ниже 
            os.system(printing)
            delete_files_in_folder("/mnt/File/")
            bot.current_states.set_state(call.message.chat.id, call.message.chat.id, None)
            bot.current_states.reset_data(call.message.chat.id, call.message.chat.id)


def delete_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"file {file_path} is deleted")
        except Exception as e:
            print(f'Ошибка при удалении файла {file_path}. {e}')


          
@bot.message_handler(content_types=['text'])
def repeat_all_message(message):
    data = bot.current_states.get_data(message.chat.id, message.chat.id )

    if data is not None:
        file_name = data.get("file_name")
        choose_printer = data.get("choose_printer")
        pagess =  data.get("pagess")
        count_copies = data.get("count_copies")
        tag_count_copies  = data.get("tag_count_copies")

    else:
        file_name = None 
        choose_printer - None
        pagess = None
        count_copies = None
        tag_count_copies= None

    print (tag_count_copies)
    print(pagess)
    if pagess is not None:
        print("печать страниц")
        Additional.Pages_Print(bot, message)
        try :
            pagess = None
            bot.current_states.set_data(message.chat.id, message.chat.id, "pagess", pagess)
        except:
            bot.send_message(message.chat.id,"ПРоизошла неизвестная ошибка, нажми на кнопку start")

        print(pagess)
    else:
        print("Страницы не указаны. ") 
            

    if tag_count_copies is not None:
        print("печать количества страниц")
        Additional.Button_Count_Copies_N(bot, message)
        print(count_copies)
        try :
            tag_count_copies = None
            bot.current_states.set_data(message.chat.id, message.chat.id, "tag_count_copies", tag_count_copies)
        except:
            bot.send_message(message.chat.id,"ПРоизошла неизвестная ошибка, нажми на кнопку start")


    else: print("Страниц не печать нет.") 
        
          

try:
    bot.infinity_polling()
except Exception as ex:  
    print (ex)
    os.system("python3 Main.py")