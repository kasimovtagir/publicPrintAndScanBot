import os 
import CallBackTG
import telebot
from telebot import types

def list_printer_for_printing(bot, call ):
    if call.data == "list_Print":
        CallBackTG.callback_list_Print(bot,call)

    if call.data == "print22_print":
        CallBackTG.callback_print(bot,call, "print22.metalab.ifmo.ru")

    if call.data == "print19_print":
        CallBackTG.callback_print(bot,call, "print19.metalab.ifmo.ru")

    if call.data == "print10_print":
        CallBackTG.callback_print(bot,call, "print10.metalab.ifmo.ru")

    if call.data == "print13_print":
        CallBackTG.callback_print(bot,call, "print13.metalab.ifmo.ru")

    if call.data == "print9_print":
        CallBackTG.callback_print(bot,call, "print9.metalab.ifmo.ru")


    if call.data == "print14_print":
        CallBackTG.callback_print(bot,call, "print14.metalab.ifmo.ru")
                
    if call.data == "print15_print":
        CallBackTG.callback_print(bot,call, "print15.metalab.ifmo.ru")

    if call.data == "print16_print":
        CallBackTG.callback_print(bot,call, "print16.metalab.ifmo.ru")

    if call.data == "print18_print":
            CallBackTG.callback_print(bot,call, "print18.metalab.ifmo.ru")

    if call.data == "print7_print":
        CallBackTG.callback_print(bot,call, "print7.metalab.ifmo.ru")     

    if call.data == "print21_print":
        CallBackTG.callback_print(bot,call, "print21.metalab.ifmo.ru") 
        
    if call.data == "print4318_print":
        CallBackTG.callback_print(bot,call, "print4318.metalab.ifmo.ru")         

    if call.data == "print17_print":
        CallBackTG.callback_print(bot,call, "print17.metalab.ifmo.ru") 

    if call.data == "print2426_print":
        CallBackTG.callback_print(bot,call, "print2426.metalab.ifmo.ru")



