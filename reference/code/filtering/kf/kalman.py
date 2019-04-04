#!/usr/bin/env python

from random import gauss
import math


R = 0.00001
Q = 0.00001
A = 1.
B = 1.
C = 1.


def kf(state_t_1, covariance_t_1, z_t, u_t):
    mu_bar = A * state_t_1 + B * u_t
    cov_bar = A * covariance_t_1 * A + R

    gain = cov_bar * C * (1. / (C * cov_bar * C + Q))

    mu = mu_bar + gain * (z_t - C * mu_bar)
    cov = (1 - gain * C) * cov_bar

    return (mu, cov)


if __name__ == "__main__":

    delta_t 	    = 1.
    position 	    = 0.
    velocity 	    = 0.
    acceleration    = 0. # randomly set ~N(0, 1)
    variance        = 0.001
    measurement     = 0. # randomly set ~N(position, 1)

    true_acceleration = 1
    true_velocity   = 0
    true_position   = 0

   
    for i in range(1000):
        a = gauss(true_acceleration, 0.001) # measurement
        v0 = velocity
        v = velocity + (delta_t * a)
        #p = position + delta_t * ((v + velocity) / 2)

        ftv = true_velocity + (delta_t * true_acceleration)
        true_position = true_position + delta_t * ((true_velocity + ftv) / 2)

        true_velocity = ftv

        velocity, variance = kf(velocity, variance, v, true_acceleration)

        position = position + delta_t * ((velocity + v0) / 2)
        error = true_position - position
        
        print("Time: %s" % i)
        print("Measurement: %s m/s" % v)
        print("Position: %s m" % position)
        print("True Position: %s m" % true_position)
        print("Error: %s m" % error)
        print("Velocity: %s m/s" % velocity)
        print("True Velocity: %s m/s" % true_velocity)
        print("Acceleration: %s m/s^2" % a)
        print("Variance: %s m\n\n" % variance)

