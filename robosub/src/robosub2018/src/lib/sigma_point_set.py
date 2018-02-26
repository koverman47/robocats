#!/usr/bin/env python

import math, numpy as np


class SigmaPTS():

    def __init__(self, n, lam, alpha, beta):
        self.chi = None # matrix ptc x n
        self.state_weights = None # vector - ptc x 1
        self.cov_weights = None
        self.n = n # dimensionality
        self.ptc = 2 * n + 1 # point count
        self.a = alpha
        self.b = beta
        self.lam = lam


    def calc_sigma_pts(self, mu, cov):
        self.clear()
        self.get_chi(mu, cov)
        self.get_weights(mu, cov)


    def get_chi(self):
        pass


    def get_weights(self):
        pass


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
        self.weights = None

