import cups

# Подключение к серверу CUPS
conn = cups.Connection()

# Получение информации о задании печати
job_id = "print9.metalab.ifmo.ru-13"  # ID задания печати
job = conn.getJobs()


job_info = conn.getJobAttributes(3)
# Проверка статуса задания
# Проверка статуса задания печати
if job_info['job-state'] == 9:  # 9 означает "completed" (завершено)
    print("Файл успешно распечатан.")
else:
    print("Файл еще не был распечатан.")

# import subprocess

# # Запустите команду lpstat и захватите ее вывод
# output = subprocess.Popen(['lpstat'], stdout=subprocess.PIPE).communicate()[0]

# # Найдите строку, соответствующую вашему заданию печати
# for line in output.decode().splitlines():
#     if "JOBID" in line:
#         job_id = line.split()[0]
#         # Найдите статус задания печати по job_id
#         status = get_job_status(job_id)
#         if status == "completed":
#             print("Файл распечатан")
#         else:
#             print("Файл еще не распечатан")



# Функция get_job_status должна быть реализована вами
def get_job_status(job_id):

    # Реализуйте логику для получения статуса задания печати по job_id
    # (например, используя команду cups-query-job)
    pass

# import subprocess

# stat = subprocess.call(["systemctl", "is-active", "--quiet", "cups"])
# if(stat == 0):  # if 0 (active), print "Active"
#     print("Active")

# import os 

# qwe = os.system("ping -c 3 172.16.39.23",  flush=True)

# print(len( qwe))


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