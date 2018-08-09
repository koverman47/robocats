#!/usr/bin/env python

import copy
import numpy as np
from spt import SPT


class UKF():

    def __init__(self, R, Q, G, H):
        self.R = R # state transition covariance
        self.Q = Q # state measurement covariance
        self.G = G # state transition function
        self.H = H # measurement probability function

        self.lamb = 1
        self.alpha = 0.5
        self.beta = 2


    def get_belief(self, state_t_1, covariance_t_1, measurement, control):
        chi_t_1 = SPT()
        chi_t_1.calc_sigma_pts(state_t_1, covariance_t_1, self.alpha, self.beta, self.lamb)
        chi_t_1.transform(self.G, control)

        mu_bar, cov_bar = chi_t_1.reconstruct()
        cov_bar = cov_bar + self.R

        chi_bar = SPT()
        chi_bar.calc_sigma_pts(mu_bar, cov_bar, self.alpha, self.beta, self.lamb)

        zeta_bar = copy.deepcopy(chi_bar)
        zeta_bar.transform(self.H)

        zeta_hat, zeta_hat_cov = zeta_bar.reconstruct()
        zeta_hat_cov = zeta_hat_cov + self.Q

        cross_cov = self.get_cross_covariance(chi_bar, mu_bar, zeta_bar, zeta_hat)

        gain = self.get_kalman_gain(cross_cov, zeta_hat_cov)

        mu = self.get_mean_correction(mu_bar, gain, measurement, zeta_hat)
        cov = self.get_covariance_correction(cov_bar, gain, zeta_hat_cov)

        return (mu, cov)


    def get_cross_covariance(self, spt1, mean1, spt2, mean2):
        first_term = np.array([])
        second_term = np.array([])

        cross_cov = np.array([[0. for i in range(len(mean1))] for j in range(len(mean1))])
        
        for i in range(len(mean1)):
            cross_cov += spt1.cov_weights[i] * np.outer(spt1.chi[i] - mean1, np.transpose(spt2.chi[i] - mean2))

        return cross_cov

    
    def get_kalman_gain(self, cross_cov, zeta_cov):
        return np.dot(cross_cov, np.linalg.pinv(zeta_cov))


    def get_mean_correction(self, mu_bar, gain, measurement, zeta_mean):
        return mu_bar + np.dot(np.asarray(gain), (measurement - zeta_mean))


    def get_covariance_correction(self, cov_bar, gain, zeta_cov):
        return cov_bar - np.dot(gain, np.dot(zeta_cov, np.transpose(gain)))
