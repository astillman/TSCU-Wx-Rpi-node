//The parts of this code for handling the temperature sensor were modified from a tutorial by Simon Monk, of Adafruit at 
//http://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20

//Replace with the URL of Apps Script web-app used to write to the spreadsheet
baseUrl = "https://script.google.com/macros/s/AKfycbxxfc58z2Yp2DDvtlE1uVAkVSHDV80WXfIQ7oSvy8JghrtcOLZE/exec";

import requests
import random
import datetime
import os
import glob
import time

os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():a
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0/5.0 + 32.0
        return temp_c, temp_f    

print 'starting';

now = datetime.datetime.now();

deg_c, deg_f = read_temp()
args = "timestamp=" + str(now) + "&tempc=" + str(deg_c) + "&tempf=" + str(deg_f)

r = requests.get(baseUrl + "?" + args);

print(r.text);
