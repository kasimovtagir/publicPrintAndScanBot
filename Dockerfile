FROM python:3.8-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt

RUN apt-get update -y
RUN apt-get install mc -y
RUN apt-get install nfs-common -y
RUN apt install -y unoconv 
RUN apt install -y cups 
RUN apt install -y sudo
RUN apt install -y cups-client 
RUN apt install -y cups-bsd 
RUN apt install -y cups-filters 
RUN apt install -y foomatic-db-compressed-ppds 
RUN apt install -y printer-driver-all 
RUN apt install -y openprinting-ppds 
RUN apt install -y hpijs-ppds 
RUN apt install -y hp-ppd 
RUN apt install -y hplip 
RUN apt install -y smbclient 
RUN apt install -y printer-driver-cups-pdf 
RUN apt install -y libreoffice 
RUN apt install -y iputils-ping
#RUN mount -t nfs  192.168.5.49:/share/scan_bot /mnt/

RUN pip3 install -r requirements.txt


RUN useradd \
  --groups=sudo,lp,lpadmin \
  --create-home \
  --home-dir=/home/print \
  --shell=/bin/bash \
  --password=$(mkpasswd print) \
  print \
&& sed -i '/%sudo[[:space:]]/ s/ALL[[:space:]]*$/NOPASSWD:ALL/' /etc/sudoers

COPY . .
COPY requirements.txt .
#RUN pip install -r requirements.txt


# Copy the default configuration file
# Copy the default configuration file
COPY --chown=root:lp cupsd.conf /etc/cups/cupsd.conf
# COPY --chown=root:lp /ppd/printers.conf /etc/cups/printers.conf
# COPY --chown=root:lp /ppd/ppd/print7.metalab.ifmo.ru.ppd /etc/cups/ppd/print7.metalab.ifmo.ru.ppd
# COPY --chown=root:lp /ppd/ppd/print7.metalab.ifmo.ru.ppd.O /etc/cups/ppd/print7.metalab.ifmo.ru.ppd.O
# COPY --chown=root:lp /ppd/ppd/print9.metalab.ifmo.ru.ppd /etc/cups/ppd/print9.metalab.ifmo.ru.ppd 
# COPY --chown=root:lp /ppd/ppd/print9.metalab.ifmo.ru.ppd.O /etc/cups/ppd/print9.metalab.ifmo.ru.ppd.O 
# COPY --chown=root:lp /ppd/ppd/print10.metalab.ifmo.ru.ppd /etc/cups/ppd/print10.metalab.ifmo.ru.ppd
# COPY --chown=root:lp /ppd/ppd/print10.metalab.ifmo.ru.ppd.O /etc/cups/ppd/print10.metalab.ifmo.ru.ppd.O 
# COPY --chown=root:lp /ppd/ppd/print13.metalab.ifmo.ru.ppd /etc/cups/ppd/print13.metalab.ifmo.ru.ppd 
# COPY --chown=root:lp /ppd/ppd/print13.metalab.ifmo.ru.ppd.O /etc/cups/ppd/print13.metalab.ifmo.ru.ppd.O
# COPY --chown=root:lp /ppd/ppd/print14.metalab.ifmo.ru.ppd /etc/cups/ppd/print14.metalab.ifmo.ru.ppd
# COPY --chown=root:lp /ppd/ppd/print14.metalab.ifmo.ru.ppd.O /etc/cups/ppd/print14.metalab.ifmo.ru.ppd.O
# COPY --chown=root:lp /ppd/ppd/print15.metalab.ifmo.ru.ppd /etc/cups/ppd/print15.metalab.ifmo.ru.ppd  
# COPY --chown=root:lp /ppd/ppd/print15.metalab.ifmo.ru.ppd.O /etc/cups/ppd/print15.metalab.ifmo.ru.ppd.O 
# COPY --chown=root:lp /ppd/ppd/print16.metalab.ifmo.ru.ppd /etc/cups/ppd/print16.metalab.ifmo.ru.ppd  
# COPY --chown=root:lp /ppd/ppd/print16.metalab.ifmo.ru.ppd.O /etc/cups/ppd/print16.metalab.ifmo.ru.ppd.O
# COPY --chown=root:lp /ppd/ppd/print18.metalab.ifmo.ru.ppd /etc/cups/ppd/print18.metalab.ifmo.ru.ppd 
# COPY --chown=root:lp /ppd/ppd/print18.metalab.ifmo.ru.ppd.O /etc/cups/ppd/print18.metalab.ifmo.ru.ppd.O 
# COPY --chown=root:lp /ppd/ppd/print19.metalab.ifmo.ru.ppd /etc/cups/ppd/print19.metalab.ifmo.ru.ppd 
# COPY --chown=root:lp /ppd/ppd/print19.metalab.ifmo.ru.ppd.O /etc/cups/ppd/print19.metalab.ifmo.ru.ppd.O 
# COPY --chown=root:lp /ppd/ppd/print22.metalab.ifmo.ru.ppd /etc/cups/ppd/print22.metalab.ifmo.ru.ppd 
# COPY --chown=root:lp /ppd/ppd/print22.metalab.ifmo.ru.ppd.O /etc/cups/ppd/print22.metalab.ifmo.ru.ppd.O 
# COPY --chown=root:lp /ppd/ppd/print21.metalab.ifmo.ru.ppd /etc/cups/ppd/print21.metalab.ifmo.ru.ppd 
# COPY --chown=root:lp /ppd/ppd/print21.metalab.ifmo.ru.ppd.O /etc/cups/ppd/print21.metalab.ifmo.ru.ppd.O 
# COPY --chown=root:lp /ppd/ppd/print2426.metalab.ifmo.ru.ppd /etc/cups/ppd/print2426.metalab.ifmo.ru.ppd

RUN mkdir  /mnt/Scan
RUN mkdir  /mnt/Logs
RUN mkdir  /mnt/File
RUN chmod -R o+w /mnt/

CMD [ "python3", "Main.py"]


#после создания контейнера, нужно: 
#1. примаунтить папку scan, через телеграм бота 
#2. поменять пароль пользователю print, командой passwd print 
#3. Скопирвоать файл printers.conf из /mnt/scan/ppd/printers.conf в папку /etc/cups
#4. скопировать всю папку /mnt/scan/ppd в /etc/cups
#5. поменять рекунсивно пользователь:группа в папке cups командой chown root:root -R /etc/cups
#6. перезапустить службу cups командой service cups restart 
#7. доабвить в portainer во вкладке Network поле Hosts file entries значение physics.itmo.ru:77.234.203.238
#