#!/usr/bin/env python

import math, matrix, numpy as np
from scipy import linalg


class SigmaPTS():

    def __init__(self):
        self.chi = None # matrix ptc x n
        self.state_weights = None
        self.cov_weights = None


    def calc_sigma_pts(self, mu, cov, alpha, beta, lamb):
        self.clear()
        self.get_chi(mu, cov, lamb)
        self.get_weights(mu, cov, alpha, beta, lamb)


    def get_chi(self, mu, cov, lamb):
        dim = len(mu)
        nlam = dim * self.lam
        inner_term = [matrix.constant_multiply_vector(cov[i], nlam[i]) for i in range(dim)]
        root_cov = linalg.sqrtm(inner_term)

        self.chi.append(mu)
        for i in range(1, dim + 1):
            self.chi.append(matrix.add_vector(mu, root_cov[i]))
        for j in range(self.n + 1, 2 * dim + 2):
            self.chi.append(matrix.subtract_vector(mu, root_cov[j]))


    def get_weights(self, mu, cov, alpha, beta, lamb):
        dim = len(mu)

        self.state_weights.append(self.lam / (dim + self.lam))
        self.cov_weights.append(self.state_weights[0] + (1 - self.a**2 + self.b))

        val = 1 / (2 * (dim + self.lam))
        for i in range(2 * dim + 1):
            self.state_weights.append(val)
            self.cov_weights.append(val)

    
    def transform(self, fxn):
        pass


    def reconstruct_mean(self):
        pass
        

    def clear(self):
        self.chi = None
        self.state_weights = None
        self.cov_weights = None

