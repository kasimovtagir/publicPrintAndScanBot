from email import message
from telebot import types
import telebot
import os
import subprocess
from PIL import Image
import random
#\from telegram import ReplyMarkup
#from PyPDF2 import PdfFileReader

file_name=""
file_rename=""
save_dir=""
file_extension = ""

import CallBackTG
  

import sys
#from pydocx import PyDocX

#from docx2pdf import convert

def convert_to(input_file):
    docx_file = input_file
    # Путь к выходному файлу PDF
    #pdf_files = docx_file+ ".pdf"
    # Выполнить конвертацию с помощью LibreOffice
    subprocess.call(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', '/mnt/File/', docx_file])
    return docx_file
    #convert(doc_path, path)
    # subprocess.call(['soffice',
    #                          # '--headless',
    #                          '--convert-to',
    #                          'pdf',
    #                          '--outdir',
    #                          path,
    #                          doc_path])
    #print(doc_path)
    #return doc_path
                             
    # cmd = ['unoconv', '--format', 'pdf', '--output', doc_path+".pdf", doc_path]
    # subprocess.run(cmd)
    # #print(doc_path) 
    # return doc_path+".pdf"


def resize_image(input_image_path,
                 output_image_path,
                 size):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    print('The original image size is {wide} wide x {height} '
          'high'.format(wide=width, height=height))
 
    resized_image = original_image.resize(size)
    width, height = resized_image.size
    print('The resized image size is {wide} wide x {height} '
          'high'.format(wide=width, height=height))
    resized_image.show()
    resized_image.save(output_image_path)

def rename_file_name (bot, path, file, message):
    global file_extension
    file_rename = (file.replace(" ", "-"))
    file_rename = (file_rename.replace("(", "-"))
    file_rename = (file_rename.replace(")", "-"))

    os.rename(path + "/" +file, path + "/" +file_rename)

    split_tup = os.path.splitext(file_rename)

    file_extension = split_tup[1]

    data = bot.current_states.get_data(message.chat.id, message.chat.id )
    if data is not None:
        choose_printer = data.get("choose_printer")

    else:
        choose_printer = None

    if str(file_extension) in [".doc", ".docx", ".odt", ".rtf"]:
        print(convert_to(path + "/"+file_rename))
        print(path + "/"+file_rename)
        #convert_name = convert_to(path + "/"+file_rename)
        #convert_name = convert_name + ".pdf"
        convert_name = split_tup[0]+".pdf"
        bot.current_states.set_data(message.chat.id, message.from_user.id, "file_name", convert_name)

        bot.send_message(message.chat.id,"Имя файла: - "+ format(str(convert_name))+"\nПринтер: - "+ str(choose_printer), reply_markup=CallBackTG.pre_printing())
        #return convert_name

    elif str(file_extension) in  [".jpg", ".png", ".jpeg"]:
        file_size = os.path.getsize(path + "/"+file_rename)
        if file_size >=2000000:
            resize_image(input_image_path=path + "/"+file_rename,
                output_image_path=path +"/Resize_"+file_rename ,
                size=(1920, 1080))
            #CallBackTG.file_name="Resize_"+file_rename
            f_n="/Resize_"+ file_rename
            file_rename = path +"/Resize_"+file_rename
            bot.current_states.set_data(message.chat.id, message.from_user.id, "file_name", f_n)

            print(file_rename)

            bot.send_message(message.chat.id,"Имя файла: - "+ f_n+"\nПринтер: - "+ str(choose_printer), reply_markup=CallBackTG.pre_printing())
        else: 
            #CallBackTG.file_name=file_rename
            if choose_printer =="":
                 CallBackTG.callback_list_Print(bot,message)
            else:     
                #CallBackTG.file_name=file_rename
                bot.send_message(message.chat.id,"Имя файла: - "+ file_rename +"\nПринтер: - "+ str(choose_printer), reply_markup=CallBackTG.pre_printing())
    
    elif str(file_extension) == ".pdf": 
        #CallBackTG.file_name=file_rename
        bot.current_states.set_data(message.chat.id, message.from_user.id, "file_name", file_rename)

       # CallBackTG.count_pages= number_of_pages        
        #= number_of_pages
        #bot.current_states.set_data(message.chat.id, message.from_user.id, "pages_print",pages_print)
        #print(pages_print)
        if choose_printer is None:
            CallBackTG.callback_list_Print(bot,message)
            #bot.send_message(message.chat.id,"Выбери принтер ")
        else:
            bot.send_message(message.chat.id,"Имя файла: - "+ format(str(file_rename))+"\nПринтер: - "+ str(choose_printer), reply_markup=CallBackTG.pre_printing())

    else :
        bot.send_message(message.chat.id,"Формат файла не поддерживается\nБот поддерживает файлы формата pdf, doc, docx, odt, jpg, jpeg, png, rtf.\nНажми на кнопку START")
        print(f"Файл {file_rename} удален")
        os.remove(path + "/"+file_rename)





def Upload_files(bot:telebot.TeleBot,message:telebot.types.Message):
    try:
        try:
            save_dir = "/mnt/File"
            # save_dir = message.caption
        except:
            save_dir = "/mnt/File"
            # save_dir = os.getcwd()
            s = "[!] you aren't entered directory, saving to {}".format(save_dir)
            bot.send_message(message.chat.id, str(s))
        file_name = message.document.file_name

        file_id = message.document.file_name
        file_id_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        print(f"Пользователь {str(message.from_user.first_name)} загрузил файл: {str(file_name)}" )
        
        with open('logs.txt', 'a') as logs:
            logs.write( f"{str(CallBackTG.return_time())} - Пользователь: {str(message.from_user.first_name)} - загрузил файл: {str(file_name)}\n")



        with open(save_dir + "/" + file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
        try :
            bot.current_states.set_data(message.chat.id, message.from_user.id, "file_name", file_name)
        except:
            bot.current_states.set_state(message.chat.id, message.from_user.id, None)
            bot.current_states.reset_data(message.chat.id, message.chat.id)
            bot.current_states.set_data(message.chat.id, message.from_user.id, "file_name", file_name)
        rename_file_name(bot, save_dir, file_name, message)


        # os.remove(tagir)
    except Exception as ex:
        bot.send_message(message.chat.id, f"{ex}Неизвестная ошибка\nНажми на кнопку START")