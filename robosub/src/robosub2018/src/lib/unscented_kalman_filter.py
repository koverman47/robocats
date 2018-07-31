#!/usr/bin/env python

import math
import rospy
import time
import numpy as np

from sigma_point_set import SigmaPTS as SPT
from robosub2018.msg import State
from robosub2018.msg import Depth
from std_msgs.msg import Imu


class UKF():

    def __init__(self, dim, R, Q, G, H):
        self.x = []  # state mean belief
        self.P = []  # state covariance belief
        self.Q = Q   # state transition covariance
        self.R = R   # measurement covariance noise
        self.G = G   # state transition function
        self.H = H   # measurement transition function
        
        self.lam = 1
        self.alpha = 0.5
        self.beta = 2

    def get_belief():
