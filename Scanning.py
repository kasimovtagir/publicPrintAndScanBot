import os 
import CallBackTG
import telebot
from telebot import types

def list_printer_for_scaning(bot, call ):
    if call.data== "list_Scan":
        bot.send_message(call.from_user.id, text="В разработке.")
        #CallBackTG.callback_list_Print_for_scan(bot,call)

    if call.data== "print21_scan":
        CallBackTG.callback_print_scan(bot,call, "print21")

    if call.data == "print4318_scan":
        CallBackTG.callback_print(bot,call, "print4318")         
        
    if call.data== "print17_scan":
        CallBackTG.callback_print_scan(bot,call, "print17")

    if call.data== "print431_scan":
        CallBackTG.callback_print_scan(bot,call, "print431")             

    if call.data== "print7_scan":
        CallBackTG.callback_print_scan(bot,call, "print7")
 
    if call.data== "print18_scan":
        bot.send_message(call.from_user.id, text='В разработке.')
        #CallBackTG.callback_print_scan(bot,call, "print18")

    if call.data== "print19_scan":
        CallBackTG.callback_print_scan(bot,call, "print19")

    if call.data== "print14_scan":
        bot.send_message(call.from_user.id, text='В разработке.')
        #CallBackTG.callback_print_scan(bot,call, "print14")

    if call.data== "print15_scan":
        CallBackTG.callback_print_scan(bot,call, "print15")

    if call.data== "print16_scan":
        CallBackTG.callback_print_scan(bot,call, "print16")

    if call.data== "print10_scan":
        CallBackTG.callback_print_scan(bot,call, "print10")

    if call.data== "print9_scan":
        CallBackTG.callback_print_scan(bot,call, "print9")
        
    if call.data== "print22_scan":
        CallBackTG.callback_print_scan(bot,call, "print22")        

    if call.data== "print13_scan":
        CallBackTG.callback_print_scan(bot,call, "print13")
        #CallBackTG.callback_print13_scan(bot,call, "2022")