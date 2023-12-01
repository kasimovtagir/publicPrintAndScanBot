import os 

qwe = os.system("ping -c 3 172.16.39.23",  flush=True)

print(len( qwe))


# import subprocess
# import re

# def get_printers():
#     try:
#         # Выполняем команду lpstat для получения списка принтеров
#         result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True, check=True)

#         # Разбиваем вывод команды на строки
#         lines = result.stdout.splitlines()

#         # Извлекаем имена принтеров из строк
#         printers = [line.split()[1] for line in lines]

#         #printers = printers.split("[]'")
#         #printers = printers.remove("'[")
#         cleaned_text =''.join(char for char in printers if char not in "[]'")


#         return cleaned_text

#     except subprocess.CalledProcessError as e:
#         print(f"Ошибка при выполнении команды: {e}")
#         return []

# # Получаем и выводим список принтеров
# printers = get_printers()
# print(printers)


# import datetime
# from datetime import datetime

# def return_time():
#     dt = datetime.now()
#     dt_string = dt.strftime("%d.%m %H:%M")
#     return dt_string



# dt = datetime.now()
# dt_string = dt.strftime("%H:%M")
# # timex = return_time()

# print (dt_string)
# if dt_string=="02:32":
#     print("sad")