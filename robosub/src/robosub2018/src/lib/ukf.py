#!/usr/bin/env python

import math, rospy, time, numpy as np
from sigma_point_set import SigmaPTS as SPT
from robosub2018.msg import State, Depth
from std_msgs.msg import Imu


class UKF():

    def __init__(self, dim):
        self.x = [] # state vector
        self.p = [] # state covariance matrix
        self.Q = [] # motion noise
        self.R = [] # observation noise
        self.sigma_pts = SPT(dim, 1, 0.5, 2) # Need to parameters


    # zeta should come preprocessed
    def get_estimate(self, zeta):
        self.sigma_pts.calc_sigma_pts(self.x, self.p) 

        mu_bar = self.calc_mu_estimate()
        cov_bar = self.calc_cov_estimate(mu_bar)

        self.sigma_pts.calc_sigma_pts(self.mu_bar, self.cov_bar)

        prop = self.calc_propagation()
        zeta_bar = self.calc_zeta_estimate(prop)

        st = self.calc_s(prop, zeta) # check on zeta instead of zeta bar

        cov_xz = self.calc_cov_xz(mu_bar, prop, zeta_bar)

        kappa = self.calc_kalman_gain(cov_bar, st)

        self.x = self.calc_final_mu(mu_bar, kappa, zeta, zeta_bar)
        self.p = self.calc_final_cov(cov_bar, kappa, st)


    def get_state(self, zeta):
        pass


    def calc_mu_estimate(self):
        pass

    
    def calc_cov_estimate(self, mu_bar):
        pass

    
    def calc_propagation(self):
        pass


    def calc_zeta_estimate(self, prop):
        pass
    
    
    def calc_s(self, prop, zeta):
        pass


    def calc_cov_xz(self, mu_bar, prop, zeta_bar):
        pass


    def calc_kalman_gain(self, cov_bar, st):
        pass


    def calc_final_mu(self, mu_bar, kappa, zeta, zeta_bar):
        pass


    def calc_final_cov(self, cov_bar, kappa, st):
        pass

