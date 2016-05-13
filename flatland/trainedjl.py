
import numpy as np
import scipy.optimize as opt
import random


class TrainedJL(object):

    def __init__(self, n_components=2):
        self.low_dim = n_components

    def fit(self, X):
        self.high_dim = X.shape[1]
        self.X = X
        x0 = np.ones((1, self.high_dim * self.low_dim))
        cons = ({"type": "ineq", "fun": lambda x: np.all(x != 0)})
        res = opt.minimize(self.objective, x0, constraints=cons,
                           method="SLSQP")
        print res
        return res.x

    def objective(self, x):
        err = 0
        mat = x.reshape((self.high_dim, self.low_dim))
        # # i = random.randint(0, self.X.shape[0])
        # # j = random.randint(0, self.X.shape[0])
        # i = 1
        # j = 1000
        # # print i, j
        for i in xrange(self.X.shape[0] / 2000):
            for j in xrange(self.X.shape[0] / 2000):
                lxi = np.dot(self.X[i], mat)
                lxj = np.dot(self.X[j], mat)
                h_dist = np.linalg.norm(self.X[i] - self.X[j])
                l_dist = np.linalg.norm(lxi - lxj)
                err += abs(h_dist - l_dist)
        return err
