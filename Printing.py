from glob import glob
from socket import PF_RDS
import os 
from datetime import datetime
import telebot
from telebot import types
from PyPDF2 import PdfFileReader
import string
from datetime import datetime
import time
from collections import deque
#import UploadTG
import CallBackTG
from ping3 import ping, verbose_ping
# import subprocess
# import socket
# import struct
# import time

def pinging(host):
    response_time = ping(host)
    if response_time is not None:
        if response_time is False:
            print(f'{host} недоступен', flush=True)
            return False
        else: 
            print(f'{host} доступен (Время отклика: {response_time} мс)', flush=True)
            return True
    else:
        print(f'{host} недоступен', flush=True)
        return False

def return_time():
    dt = datetime.now()
    dt_string = dt.strftime("%d.%m %H:%M")
    return dt_string

def checkPrint(choose_printer):
    if (pinging(choose_printer)):
        return "✅"
    else: return "❎"


def List_Print(bot,call):
    with open('/mnt/Logs/logs.txt', 'a') as logs:
            logs.write( f"{str(return_time())} - Пользователь: {str(call.from_user.first_name)} - выбрал ПЕЧАТЬ  " + "\n")

    keyboard_list_print_for_print_2520_2530 = types.InlineKeyboardMarkup(row_width=4)
    buttons_2520_2530 = [
        types.InlineKeyboardButton(text=f'print14 {checkPrint("print14.metalab.ifmo.ru")}', callback_data='print14_print' ),
        types.InlineKeyboardButton(text=f'print15 {checkPrint("print15.metalab.ifmo.ru")}', callback_data='print15_print'),
        types.InlineKeyboardButton(text=f'print16 {checkPrint("print16.metalab.ifmo.ru")}', callback_data='print16_print'),
        types.InlineKeyboardButton(text=f'print10 {checkPrint("print10.metalab.ifmo.ru")}', callback_data='print10_print'),
        types.InlineKeyboardButton(text=f'print9 {checkPrint("print9.metalab.ifmo.ru")}', callback_data='print9_print'),
        types.InlineKeyboardButton(text=f'print13 {checkPrint("print13.metalab.ifmo.ru")}', callback_data='print13_print'),
        types.InlineKeyboardButton(text=f'print19 {checkPrint("print19.metalab.ifmo.ru")}', callback_data='print19_print'),
        types.InlineKeyboardButton(text=f'print22 {checkPrint("print22.metalab.ifmo.ru")}', callback_data='print22_print')
    ]
    keyboard_list_print_for_print_2520_2530.add(*buttons_2520_2530)
    bot.send_message(call.from_user.id, text='На принтере есть этикетка с именем принтера.\nВыбери принтер для печати.\nПринтеры на Ломоносова, 9 на 6-ом этаже(2520)\n✅ - принтер включен\n❎ - принтер выключен.',reply_markup=keyboard_list_print_for_print_2520_2530)


    keyboard_list_print_for_print_cerkov = types.InlineKeyboardMarkup(row_width=4)
    buttons_cerkov = [
        types.InlineKeyboardButton(text=f'print18 {checkPrint("print18.metalab.ifmo.ru")}', callback_data='print18_print'),
        types.InlineKeyboardButton(text=f'print7 {checkPrint("print17.metalab.ifmo.ru")}', callback_data='print7_print'),
        types.InlineKeyboardButton(text=f'print4318 {checkPrint("print4318.metalab.ifmo.ru")}', callback_data='print4318_print'),
        types.InlineKeyboardButton(text=f'print21 {checkPrint("print21.metalab.ifmo.ru")}', callback_data='print21_print')
    ]
    keyboard_list_print_for_print_cerkov.add(*buttons_cerkov)
    bot.send_message(call.from_user.id, text='Принтеры на Ломоносова, 9 (церковь: Phoenix, ИЦ).',reply_markup=keyboard_list_print_for_print_cerkov)


    keyboard_list_print_for_print_4_flor = types.InlineKeyboardMarkup(row_width=4)
    buttons_4_flors = [
        types.InlineKeyboardButton(text=f'print2426 {checkPrint("172.16.35.75")}', callback_data='print2426_print')
    ]
    keyboard_list_print_for_print_4_flor.add(*buttons_4_flors)
    bot.send_message(call.from_user.id, text='Принтеры на Ломоносова, 9, 4й этаж.',reply_markup=keyboard_list_print_for_print_4_flor)



def Show_Information (bot:telebot.TeleBot,call:telebot.types.CallbackQuery,choose_printer):
    if pinging(choose_printer):
        try :
            bot.current_states.set_data(call.message.chat.id, call.message.chat.id, "choose_printer", choose_printer)
        except Exception as ex:
            bot.send_message(call.message.chat.id,f"{ex}\nПроизошла неизвестная ошибка, нажми на кнопку start")

        data = bot.current_states.get_data(call.message.chat.id, call.message.chat.id )
        if data is not None:
            file_name = data.get("file_name")
        else:
            file_name = None
        
        if file_name is not None:
            bot.send_message(call.message.chat.id, f"Файл: {file_name} \nВыбран принтер {choose_printer}. \nФормат файла А4 (по умолчанию)",  reply_markup=CallBackTG.pre_printing())
        else:
            bot.send_message(call.message.chat.id, f"Выбран принтер {choose_printer}. \nЗагрузи файл, который нужно распечатать: \nФормат файла А4 (по умолчанию)")
        with open('logs.txt', 'a') as logs:
            logs.write( f"{str(return_time())} - Пользователь: {str(call.from_user.first_name)} - выбрал {choose_printer}  " + "\n")
        logs.close()
    else: 
        bot.send_message(call.message.chat.id, f"Принтер {choose_printer} выключен или недоступен.\nПожалуйста, свяжитесь с IT-отделом.")