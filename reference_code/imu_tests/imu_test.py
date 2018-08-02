#!/usr/bin/env python

# Run with sudo

import sys, math, time, serial, re, numpy as np


port = '/dev/tty.usbserial-FTHBZZLU' #Kirby's Mac
#port = '/dev/ttyUSB0' # Intel Nuc
baud = 115200

ser = serial.Serial(port, baud)
ser.flush()

def quaternion_to_euler(data):
    yz2 = 1 - (2 * (data[2]**2 + data[3]**2))
    pitch_p = 2 * (data[1] * data[2] - data[1] * data[3])
    roll_p = (2 * (data[0] * data[1] + data[2] * data[3])) / yz2
    yaw_p = (2 * (data[0] * data[3] + data[1] * data[2])) / yz2

    pitch_p = 1 if pitch_p > 1 else pitch_p
    pitch_p = -1 if pitch_p < -1 else pitch_p

    roll = math.atan(roll_p) / math.pi
    pitch = math.asin(pitch_p)  / math.pi
    yaw = math.atan(yaw_p) / math.pi

    #print("Roll: %s" % roll)
    #print("Pitch: %s" % pitch)
    #print("Yaw: %s" % yaw)

    return [roll, pitch, yaw]



def get_imu_data(command):
    global ser

    ser.write(command)
    data = ser.readline()
    values = np.array(re.findall('([-\d.]+)', data)).astype(np.float)
    return values


if __name__ == "__main__":    
    
    gyro = [] # x, y, z - angular velocity
    accel = [] # x, y, z - linear acceleration
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

        compass = quaternion_to_euler(mag)
    

        print("Data at Time: %s" % t)
        print("Magnetometer Quaternion Data: %s" % mag)
        print("Magnetometer Euler Data: %s" % compass)
        print("Gyrometer Data: %s" % gyro)
        print("Accelerometer Data: %s" % accel)
        print("Temperature Data: %s\n" % temp)

        t += 1
        time.sleep(1)
