#!/usr/bin/env python3

import rospy
from lib.controller import Controller
from robosub2018.msg import MotorCommands, State


msg_state = None
msg_desired = None
msg_commands = None
pub_commands = None

def control():
    pass


def current_state_callback(msg):   
    msg_state = msg


def desired_state_callback(msg):
    msg_desired = msg


if __name__ == "__main__":
    # control()
    
    pub_commands = rospy.Publisher('command/motor', MotorCommands, queue_size=8)
    rospy.init_node('controller')

    rospy.Subscriber("borbcat/state", State, current_state_callback)
    rospy.Subscriber("borbcat/desired", State, desired_state_callback)

    msg_commands = MotorCommands()
    msg_commands.header.seq = 0
    msg_commands.header.stamp = rospy.get_rostime()

    controller = Controller(3, 0.8, 0, 0.75)

    rate = rospy.Rate(50)
    while not rospy.is_shutdown():
        msg_commands.command = controller.get_motor_commands(msg_state.state, msg_desired.state)
        msg_commands.header.seq += 1
        msg_commands.header.stamp=rospy.get_rostime()

        pub_commands.publish(msg_commands)
        
    
