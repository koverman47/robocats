#!/usr/bin/env python

import sys, math, time, serial, re, numpy as np


port = '/dev/tty.usbserial-FTHBZZLU'
baud = 115200

ser = serial.Serial(port, baud)
ser.flush()

def get_imu_data(command):
    global ser

    ser.write(command)
    data = ser.readline()
    values = np.array(re.findall('([-\d.]+)', data)).astype(np.float)
    return values


if __name__ == "__main__":    
    
    gyro = [] # x, y, z
    accel = [] # x, y, z
    mag = [] # w, x, y, z

    t = 0
    while 1:
        magnetometer = get_imu_data("$PSPA,QUAT\r\n")
        gyrometer = get_imu_data("$PSPA,G\r\n")
        accelerometer = get_imu_data("$PSPA,A\r\n")
        temp = get_imu_data("$PSPA,TEMP\r\n")
        
        mag = [magnetometer[i] for i in range(4)]
        gyro = [gyrometer[i] * math.pi / 180 / 1000 for i in range(3)]
        accel = [accelerometer[i] * 9.80665 / 1000 for i in range(3)]
    

        print("Data at Time: %s" % t)
        print("Magnetometer Data: %s" % mag)
        print("Gyrometer Data: %s" % gyro)
        print("Accelerometer Data: %s" % accel)
        print("Temperature Data: %s" % temp)

        t += 1
        time.sleep(1)
