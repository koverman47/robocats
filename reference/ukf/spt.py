#!/usr/bin/env python

import numpy as np
from scipy import linalg


class SPT():
    
    def __init__(self):
        self.chi = None
        self.state_weights = None
        self.cov_weights = None


    def calc_sigma_pts(self, mu, cov, alpha, beta, lamb):
        self.clear()
        self.get_chi(mu, cov, lamb)
        self.get_weights(mu, cov, alpha, beta, lamb)


    def get_chi(self, mu, cov, lamb):
        dim = len(mu)
        self.chi = [mu]

        nlamb = dim + lamb
        inner_term = np.array([cov[i] * nlamb for i in range(dim)])
        root_cov = linalg.sqrtm(np.asmatrix(inner_term))

        for i in range(dim):
            self.chi.append(mu + root_cov[i])
        for j in range(dim):
            self.chi.append(mu - root_cov[j])
        self.chi = np.array(self.chi)


    def get_weights(self, mu, cov, alpha, beta, lamb):
        dim = len(mu)

        self.state_weights = [lamb / float(dim + lamb)]
        self.cov_weights = [self.state_weights[0] + (1 - alpha**2 + beta)]

        val = 1 / float(2 * (dim + lamb))
        for i in range(2 * dim):
            self.state_weights.append(val)
            self.cov_weights.append(val)

        self.state_weights = np.array(self.state_weights)
        self.cov_weights = np.array(self.cov_weights)


    def transform(self, fxn):
        for i in range(len(self.chi)):
            self.chi[i] = fxn(self.chi[i])


    def reconstruct(self):
        tpose_chi = np.transpose(self.chi)
        mean = np.array([0. for x in range(len(tpose_chi))])
        for i in range(len(tpose_chi)):
            mean[i] += np.inner(self.state_weights, tpose_chi[i])
        mean = np.array(mean)

        temp = []
        for i in range(len(self.chi)):
            temp.append(self.chi[i] - mean)
        temp = np.array(temp)
        outer = np.dot(np.transpose(temp), temp)
        
        covariance = []
        for j in range(len(tpose_chi)):
            covariance.append(outer[j] * self.cov_weights[j])
        covariance = np.array(covariance)
        
        return (mean, covariance)

    def clear(self):
        self.chi = None
        self.state_weights = None
        self.cov_weights = None
