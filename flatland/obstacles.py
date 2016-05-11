
import planar
import random
import numpy as np
import math
import polytope
import scipy.spatial as spatial


class RandomObstacleGen(object):

    def __init__(self, **kwargs):
        self.bound_low = kwargs.get("bound_low", -10)
        self.bound_high = kwargs.get("bound_high", 10)
        self.rad_mean = kwargs.get("rad_mean", 5)
        self.rad_std = kwargs.get("rad_std", 0.5)
        self.dim = kwargs.get("dim", 2)
        self.sample_pts_mean = kwargs.get("sample_pts_mean", self.dim ** 2)
        self.sample_pts_std = kwargs.get("sample_pts_std", 0.1)

    def sample_n_sphere(self, rad, center):
        pt = np.zeros((self.dim,))
        angles = np.random.uniform(0, 2 * math.pi, [self.dim - 1])
        sin_angles = np.sin(angles)
        cos_angles = np.cos(angles)
        for i in xrange(0, self.dim - 1):
            sin_prod = 1
            for j in xrange(i):
                sin_prod *= sin_angles[j]
            pt[i] = center[i] + rad * cos_angles[i] * sin_prod
            if i == self.dim - 2:
                pt[i + 1] = center[i + 1] + rad * sin_prod * sin_angles[i]
        return pt

    def generate_random_points(self, num, rad, center):
        pts = np.zeros((num, self.dim))
        for i in xrange(num):
            pts[i] = self.sample_n_sphere(rad, center)
        return pts

    def generate(self, num):
        obs = list()
        for i in xrange(num):
            center = np.random.uniform(
                self.bound_low, self.bound_high, [self.dim])
            n_smpls = int(random.gauss(self.sample_pts_mean,
                                       self.sample_pts_std))
            radius = random.gauss(self.rad_mean, self.rad_std)
            pts = self.generate_random_points(n_smpls, radius, center)
            ch = spatial.ConvexHull(pts)
            eqs = ch.equations
            poly = polytope.Polytope(
                eqs[:, : - 1], -eqs[:, -1], minrep=True)
            obs.append((poly, ch.points))
        return obs
