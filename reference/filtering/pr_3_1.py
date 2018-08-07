#!/usr/bin/env python

from random import gauss
import math


R = 0.01
Q = 0.01
A = 1.
B = 1.
C = 1.


def kf(state_t_1, covariance_t_1, z_t, u_t):
    mu_bar = A * state_t_1 + B * u_t
    cov_bar = A * covariance_t_1 * A + R

    gain = cov_bar * C * (1. / (C * cov_bar * C + Q))

    mu = mu_bar + gain * (measurement - C * mu_bar)
    cov = (1 - gain * C) * cov_bar

    return (mu, cov)


if __name__ == "__main__":

    delta_t 	    = 1.
    position 	    = 0.
    velocity 	    = 0.
    acceleration    = 0. # randomly set ~N(0, 1)
    variance        = 0.1
    measurement     = 0. # randomly set ~N(position, 1)

    true_position   = 0

   
    for i in range(1, 11):
        #acceleration = gauss(0, 1)
        #acceleration = 1
        #final_velocity = velocity + (delta_t * acceleration)
        #true_position = delta_t * ((final_velocity + velocity) / 2)
        velocity = 1
        true_position = velocity * i
        measurement = gauss(true_position, 0.1)
        #velocity = final_velocity

        position, variance = kf(position, variance, measurement, velocity)
        error = true_position - position
        
        print("Time: %s" % i)
        print("Position: %s" % position)
        print("True Position: %s" % true_position)
        print("Error: %s\n" % error)
        print("Velocity: %s" % velocity)
        print("Acceleration: %s" % acceleration)
        print("Measurement: %s" % measurement)
        print("Variance: %s\n\n" % variance)

