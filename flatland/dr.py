
import time
import planner
import numpy as np
import polytope
import sklearn.cluster as cluster
import sklearn.decomposition as decomp
import scipy.spatial as spatial
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
        for obst, verts in self.obstacles:
            X.append(verts)
        X = np.vstack(X)
        try:
            return self.trans(n_clusters=self.low_dim).fit(X)
        except TypeError:
            return self.trans(n_components=self.low_dim).fit(X)

    def low_dim_obstacles(self, tr):
        ld_obsts = list()
        for obst, verts in self.obstacles:
            ld_verts = tr.transform(verts)
            ch = spatial.ConvexHull(ld_verts)
            eqs = ch.equations
            poly = polytope.Polytope(
                A=eqs[:, : - 1], b=-eqs[:, -1], minrep=True)
            ld_obsts.append((poly, ch.points))
        return ld_obsts

    def path_to_arr(self, path):
        k = path.getStateCount()
        arr = np.zeros((k, self.low_dim))
        for i in xrange(k):
            s = path.getState(i)
            for j in xrange(self.low_dim):
                arr[i][j] = s[j]
        return arr

    def is_state_valid(self, state):
        for obst, _ in self.obstacles:
            if state in obst:
                return False
        return True

    def crow_flies(self, start, end, step):
        dr = (end - start) / np.linalg.norm(end - start)
        cur = start.copy()
        while np.linalg.norm(cur - end) > step:
            cur += step * dr
            yield cur

    def check_path(self, path):
        collision_count = 0
        for i in xrange(path.shape[0] - 1):
            for pt in self.crow_flies(path[i], path[i + 1], 0.2):
                if not self.is_state_valid(pt):
                    collision_count += 1
        return collision_count

    def solve(self, st, gl, timeout=1.0):
        if self.low_dim < self.high_dim:
            tr = self.fit(st, gl)
            ld_obsts = self.low_dim_obstacles(tr)
            ld_st_gl = tr.transform(np.array([st, gl]))
            flpl = planner.FLPlanner(
                dim=self.low_dim,
                planner=self.pl,
                obstacles=ld_obsts,
                low_bound=self.low_bound,
                high_bound=self.high_bound)
            start = time.time()
            res = flpl.solve(ld_st_gl[0], ld_st_gl[1], timeout)
            end = time.time()
            ld_path = res.get_solution()
            hd_path = tr.inverse_transform(self.path_to_arr(ld_path))
            hd_path = np.vstack((st, hd_path, gl))
            return hd_path, end - start
        else:
            flpl = planner.FLPlanner(
                dim=self.high_dim,
                planner=self.pl,
                obstacles=self.obstacles,
                low_bound=self.low_bound,
                high_bound=self.high_bound)
            start = time.time()
            res = flpl.solve(st, gl, timeout)
            end = time.time()
            res.write_to_file("sandbox/prmpath.txt")
            flpl.save_obstacles()
            path = res.get_solution()
            route = self.path_to_arr(path)
            return route, end - start
