bb#!/usr/bin/env python

import math, matrix, numpy as np
from scipy import linalg


class SigmaPTS():

    def __init__(self):
        self.chi = [] # matrix ptc x n
        self.state_weights = []
        self.cov_weights = []


    def calc_sigma_pts(self, mu, cov, alpha, beta, lamb):
        self.clear()
        self.get_chi(mu, cov, lamb)
        self.get_weights(mu, cov, alpha, beta, lamb)


    def get_chi(self, mu, cov, lamb):
        dim = len(mu)
        nlam = dim * self.lamb
        inner_term = [matrix.constant_multiply_vector(cov[i], nlam[i]) for i in range(dim)]
        root_cov = linalg.sqrtm(inner_term)

        self.chi.append(mu)
        for i in range(1, dim + 1):
            self.chi.append(matrix.add_vector(mu, root_cov[i]))
        for j in range(self.n + 1, 2 * dim + 2):
            self.chi.append(matrix.subtract_vector(mu, root_cov[j]))
        


    def get_weights(self, mu, cov, alpha, beta, lamb):
        dim = len(mu)

        self.state_weights.append(self.lamb / (dim + self.lamb))
        self.cov_weights.append(self.state_weights[0] + (1 - self.a**2 + self.b))

        val = 1 / (2 * (dim + self.lamb))
        for i in range(2 * dim + 1):
            self.state_weights.append(val)
            self.cov_weights.append(val)
        
        self.state_weights = np.array(state)
        self.cov_weights = np.array(cov)

    
    def transform(self, fxn):
        for i in range(len(self.chi)):
            self.chi = fxn(self.chi)


    def reconstruct(self):
        mean = [0 for x in range(len(self.chi))]
        for i in range(len(self.chi)):
            for j in range(len(self.chi[i])):
                mean[i] += self.state_weights[i] * self.chi[i] 
        
        temp = []

        for i in range(len(self.chi)):
            temp.append(matrix.subtract_vector(self.chi[i], mean))
        outer = matrix.outer_product(temp, temp)
        covariance = []
        for j in range(len(self.chi)):
            covariance.append(matrix.constant_multiply_vector(outer[i], self.cov_weights[j]))

        return (mean, covariance)


    def clear(self):
        self.chi = None
        self.state_weights = None
        self.cov_weights = None

