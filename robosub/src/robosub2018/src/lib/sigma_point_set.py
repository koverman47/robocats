#!/usr/bin/env python

import math, matrix, numpy as np
from scipy import linalg


class SigmaPTS():

    def __init__(self, n, lam, alpha, beta):
        self.chi = None # matrix ptc x n
        self.state_weights = None
        self.cov_weights = None
        self.n = n # dimensionality
        self.a = alpha
        self.b = beta
        self.lam = lam


    def calc_sigma_pts(self, mu, cov):
        self.clear()
        self.get_chi(mu, cov)
        self.get_weights(mu, cov)


    def get_chi(self, mu, cov):
        nlam = self.n * self.lam
        inner_term = [matrix.constant_multiply_vector(cov[i], nlam[i]) for i in range(len(self.n))]
        root_cov = linalg.sqrtm(inner_term)

        self.chi.append(mu)
        for i in range(1, self.n + 1):
            self.chi.append(matrix.add_vector(mu, root_cov[i]))
        for j in range(self.n + 1, 2 * self.n + 2):
            self.chi.append(matrix.subtract_vector(mu, root_cov[j]))


    def get_weights(self, mu, cov):
        self.state_weights.append(self.lam / (self.n + self.lam))
        self.cov_weights.append(self.state_weights[0] + (1 - self.a**2 + self.b))

        for i in range(2 * self.n + 1):
            val = 1 / (2 * (self.n + self.lam))
            self.state_weights.append(val)
            self.cov_weights.append(val)
        

    # TODO: Refactor: now two sets of weights
    # TODO: Need to add the third case of validation
    def validate_pts(self, mu, cov):
        # validate weights
        for c in range(self.n): # c for component
            weight_sig = 0
            product_sig = 0
            for p in range(self.ptc): # p for point
                weight_sig += self.weights[p]
                product_sig += self.weights[p] * self.chi[p][c]
            if weight_sig != 1:
                pass # failure
            if mu[c] != product_sig:
                pass # failure


    def clear(self):
        self.chi = None
        self.state_weights = None
        self.cov_weights = None

