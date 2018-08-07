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

        nlamb = dim * lamb
        inner_term = np.array([cov[i] * nlamb for i in range(dim)])
        root_cov = linalg.sqrtm(inner_term)

        np.append(self.chi, mu)
        for i in range(1, dim + 1):
            np.append(self.chi, mu + root_cov[i])
        for j in range(dim + 1, 2 * dim + 2):
            np.append(self.chi, mu - root_cov[i])


    def get_weights(self, mu, cov, alpha, beta, lamb):
        dim = len(mu)

        np.append(self.state_weights, (lamb / (dim + lamb)))
        np.append(self.cov_weights, (self.state_weights[0] + (1 - alpha**2 + beta)))

        val = 1 / (2 * (dim + lamb))
        for i in range(2 * dim + 1):
            np.append(self.state_weights, val)
            np.append(self.cov_weights, val)


    def transform(self, fxn):
        for i in range(len(self.chi)):
            self.chi[i] = fxn(self.chi[i])


    def reconstruct(self):
        mean = np.array([0 for x in range(len(self.chi))])
        for i in range(len(self.chi)):
            mean[i] += np.inner(self.state_weights, self.chi[i])

        temp = np.array([])
        for i in range(len(self.chi)):
            np.append(temp, self.chi[i] - mean)
        outer = np.outer(temp, temp)
        
        covariance = np.array([])
        for j in range(len(self.chi)):
            np.append(covariance, outer[j] * self.cov_weights[j])

        return (mean, cov)

    def clear(self):
        self.chi = None
        self.state_weights = None
        self.cov_weights = None
