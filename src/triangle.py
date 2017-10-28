#!/usr/bin/env python3

import numpy as np


class Triangle(object):

    def __init__(self, vx, vy, vz):
        self.vx = np.asarray(vx)
        self.vy = np.asarray(vy)
        self.vz = np.asarray(vz)
        self.v0 = np.asarray([v[0] for v in (vx, vy, vz)])
        self.v1 = np.asarray([v[1] for v in (vx, vy, vz)])
        self.v2 = np.asarray([v[2] for v in (vx, vy, vz)])

    def normal_unit_vector(self):
        u = self.v1 - self.v0
        v = self.v2 - self.v0
        ni = u[1] * v[2] - u[2] * v[1]
        nj = u[2] * v[0] - u[0] - v[2]
        nk = u[0] * v[1] - v[1] * v[0]
        n = np.asarray([ni, nj, nk])
        c = np.linalg.norm(n)
        return n / c
