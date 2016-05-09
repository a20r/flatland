
import planar
import random
import numpy as np


DIM = 2


class RandomObstacleGen(object):

    def __init__(self, **kwargs):
        self.low = kwargs.get("low", -10)
        self.high = kwargs.get("high", 10)
        self.vlow = kwargs.get("vlow", 3)
        self.vhigh = kwargs.get("vhigh", 10)
        self.radlow = kwargs.get("radlow", 0.3)
        self.radhigh = kwargs.get("radhigh", 0.8)

    def set_low(self, low):
        self.low = low
        return self

    def set_high(self, high):
        self.high = high
        return self

    def set_vertex_low(self, vlow):
        self.vlow = vlow
        return self

    def set_vertex_high(self, vhigh):
        self.vhigh = vhigh
        return self

    def set_radius_low(self, radlow):
        self.radlow = radlow
        return self

    def set_radius_high(self, radhigh):
        self.radhigh = radhigh
        return self

    def polygon_as_arr(self, poly):
        arr = np.zeros((len(poly), 2))
        for i, v in enumerate(poly):
            arr[i][0] = v.x
            arr[i][1] = v.y
        return arr

    def generate(self, num):
        obs = list()
        for i in xrange(num):
            x = random.uniform(self.low, self.high)
            y = random.uniform(self.low, self.high)
            vcount = random.randint(self.vlow, self.vhigh)
            radius = random.uniform(self.radlow, self.radhigh)
            center = planar.Vec2(x, y)
            ob = planar.Polygon.regular(vcount, radius, center=center)
            obs.append(self.polygon_as_arr(ob))
        return obs
