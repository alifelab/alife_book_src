#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class T3(object):
    def __init__(self, omega0 = 0.9, omega1 = 0.3, epsilon = 0.345):
        self.omega0 = omega0
        self.omega1 = omega1
        self.epsilon = epsilon
        self.A = np.random.rand(8)
        self.B = np.random.rand(8)
        self.x, self.y = np.random.rand(2)

    def __iter__(self):
        return self

    def set_parameters(self, omega0 = None, omega1 = None, epsilon = None):
        self.omega0 = omega0 if omega0 is not None else self.omega0
        self.omega1 = omega1 if omega1 is not None else self.omega1
        self.epsilon = epsilon if epsilon is not None else self.epsilon

    def next(self):
        self.x, self.y = self.__circle_map(self.x, self.y, 0), self.__circle_map(self.x, self.y, 1)
        return self.x, self.y

    def __circle_map(self, x, y, z):
        s = np.sum([T3.__perturb(x, y, i, z, self.A, self.B) for i in range(4)])
        if z == 0:
            return (x + self.omega0 + self.epsilon*s/(2*np.pi)) % 1
        elif z == 1:
            return (y + self.omega1 + self.epsilon*s/(2*np.pi)) % 1
        else:
            return

    @staticmethod
    def __perturb(x, y, w, z, A, B):
        if z == 0:
            if w == 0:
                return A[0]*np.sin(2*np.pi*(x - y + B[0]));
            elif w == 1:
                return A[1]*np.sin(2*np.pi*(y + B[1]));
            elif w == 2:
                return A[2]*np.sin(2*np.pi*(x + B[2]));
            elif w == 3:
                return A[3]*np.sin(2*np.pi*(x + y + B[3]));
            else:
                return -100;
        elif z == 1:
            if w == 0:
                return A[4]*np.sin(2*np.pi*(x - y + B[4]));
            elif w == 1:
                return A[5]*np.sin(2*np.pi*(y + B[5]));
            elif w == 2:
                return A[6]*np.sin(2*np.pi*(x + B[6]));
            elif w == 3:
                return A[7]*np.sin(2*np.pi*(x + y + B[7]));
            else:
                return -100;
