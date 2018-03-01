#!/usr/bin/env python

import serial, re, math, time


northtek_file = 'forth/cal3d_and_converge.4th'
port = '/dev/ttyUSB0'
baud = 115200

ser = serial.Serial(port, baud)
ser.flush()


def write_imu(command):
    # global ser
    ser.write(command)
    print(ser.readline())


def read_imu():
    data = ser.readline()
    print("IMU SAYS: %s\n" % data)


if __name__ == "__main__":

    with open(northtek_file) as f:
        for line in f:
            if line.replace('\t', '')[0:2] != '//':
                print(line)
                write_imu(line)
                time.sleep(0.005) # sleep for 5 milliseconds

    while 1:
        #read_imu()
        ser.readline()

    


