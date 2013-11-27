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

baseUrl = "https://script.google.com/macros/s/AKfycbxxfc58z2Yp2DDvtlE1uVAkVSHDV80WXfIQ7oSvy8JghrtcOLZE/exec";

rand1 = random.random()
temp = round(rand1*100, 2)

rand2 = random.random()
hum = round(rand2*35, 2)

now = datetime.datetime.now();

print (read_temp())
deg_c, deg_f = read_temp()
args = "timestamp=" + str(now) + "&tempc=" + str(deg_c) + "&tempf=" + str(deg_f)

r = requests.get(baseUrl + "?" + args);

print(r.text);
