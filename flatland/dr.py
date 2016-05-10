
import planner
import numpy as np
import polytope
import sklearn.cluster as cluster
from ompl import geometric as og


class DRPlanner(object):

    def __init__(self, **kwargs):
        self.high_dim = kwargs.get("high_dim", 10)
        self.low_dim = kwargs.get("low_dim", 2)
        self.pl = kwargs.get("planner", og.PRMstar)
        self.trans = kwargs.get("transform", cluster.FeatureAgglomeration)
        self.obstacles = kwargs.get("obstacles", list())
        self.low_bound = kwargs.get("low_bound", -10)
        self.high_bound = kwargs.get("high_bound", 10)

    def fit(self, st, gl):
        X = [st, gl]
        for obst in self.obstacles:
            vs = polytope.extreme(obst)
            X.append(vs)
        X = np.vstack(X)
        return self.trans(n_clusters=self.low_dim).fit(X)

    def low_dim_obstacles(self, tr):
        ld_obsts = list()
        for obst in self.obstacles:
            verts = polytope.extreme(obst)
            ld_verts = tr.transform(verts)
            ld_obsts.append(polytope.qhull(ld_verts, 0.1))
        return ld_obsts

    def path_to_arr(self, path):
        k = path.getStateCount()
        arr = np.zeros((k, self.low_dim))
        for i in xrange(k):
            s = path.getState(i)
            for j in xrange(self.low_dim):
                arr[i][j] = s[j]
        return arr

    def solve(self, st, gl, timeout=1.0):
        tr = self.fit(st, gl)
        ld_obsts = self.low_dim_obstacles(tr)
        ld_st_gl = tr.transform(np.array([st, gl]))
        flpl = planner.FLPlanner(
            dim=self.low_dim,
            planner=self.pl,
            obstacles=ld_obsts,
            low_bound=self.low_bound,
            high_bound=self.high_bound)
        ld_path = flpl.solve(ld_st_gl[0], ld_st_gl[1]).get_solution()
        hd_path = self.path_to_arr(ld_path)
        return tr.inverse_transform(hd_path)
