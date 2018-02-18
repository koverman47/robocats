#!/usr/bin/env python3

import math


def add_vector(a, b):
    c = []
    for i in range(len(a)):
        c.append(a[i] + b[i])
    return c


def add_matrix(a, b):
    c = []
    for i in range(len(a)):
        c.append(add_vector(a[i], b[i]))
    return c


def subtract_vector(a, b):
    c = []
    for i in range(len(a)):
        c.append( a[i] - b[i] )
    return c


def subtract_matrix(a, b):
    c = []
    for i in range(len(a)):
        c.append(subtract_vector(a[i], b[i]))
    return c


def inner_product(a, b):
    return sum(a[i] * b[i] for i in range(len(a)))


def convolution(a, b):
    pass


def cross_product(a, b):
    pass


def matrix_multiplication(a, b):
    pass


def constant_multiply_vector(a, k):
    c = []
    for i in range(len(a)):
        c.append(round(a[i] * k, 8))
        #c.append(a[i] * k)
    return c


def constant_multiply_matrix(a, k):
    c = []
    for v in a:
        c.append(constant_multiply_vector(v, k))
    return c


def invert(a, b):
    pass

def recursive_vector_sum(vector, n):
    if n == 1:
        return vector[-1]
    return add_vector(vector[-n], recursive_vector_sum(vector, n - 1))




