#!/usr/bin/env python3

import serial, rospy, re, math
import numpy as np
from sensor_msgs.msg import Imu


port = '/dev/ttyUSB0'
baud = 115200

class ImuReader():

    def __init__(self):
        self.publisher = rospy.Publisher('/sensors/imu' Imu, queue_size=10)
        self.ser = None

        rospy.init_node('imu')
        rate = rospy.Rate(100)

        imu_msg = Imu()
        imu_msg.header.seq = 0
        imu_msg.header.frame_id = "imu0"
        imu_msg.orientation_covariance = [0.000001, 0.0, 0.0, 0.0, 0.000001, 0.0, 0.0, 0.0, 0.000001]
        imu_msg.angular_velocity_covariance = [0.000001, 0.0, 0.0, 0.0, 0.000001, 0.0, 0.0, 0.0, 0.000001]
        imu_msg.linear_acceleration_covariance = [0.00117, 0.0, 0.0, 0.0, 0.00277, 0.0, 0.0, 0.0, 0.00034]

        try:
            self.ser = serial.Serial(port, baud)
        except serial.SerialException:
            rospy.logerr("Error Connceting to IMU")


    def get_imu_data(self, command):
        self.ser.write(command)
        data = ser.readline()
        values = np.array(re.findall('([-\d.]+)', data)).astype(np.float)
        return values

if __name__ == '__main__':
    try:
        imu = ImuReader()
        while not rospy.is_shutdown():
            if not imu.ser:
                continue
            imu.imu_msg

    except rospy.ROSInterruptException:
        pass
