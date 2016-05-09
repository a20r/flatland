
from matplotlib.path import Path
from ompl import base as ob
from ompl import geometric as og
import os
import numpy as np


class FLSolution(object):

    def __init__(self, planner_def):
        self.planner_def = planner_def

    def write_to_file(self, filename):
        path = self.planner_def.getSolutionPath()
        with open(filename, "w") as f:
            f.write(path.printAsMatrix())
        return self

    def get_planner_def(self):
        return self.planner_def

    def get_solution(self):
        return self.planner_def.getSolutionPath()


class FLPlanner(object):

    def __init__(self, **kwargs):
        self.dim = kwargs.get("dim", 2)
        self.planner = kwargs.get("planner", og.PRMstar)
        self.obstacles = kwargs.get("obstacles", list())
        self.low_bound = kwargs.get("low_bound", -10)
        self.high_bound = kwargs.get("high_bound", 10)
        self.save_obstacles()

    def save_obstacles(self):
        obstacleFolder = 'sandbox/obstacles/'
        obstacle_tmp = obstacleFolder + "obstacle{}.txt"
        for i in os.listdir(obstacleFolder):
            obstaclePath = obstacleFolder + i
            os.remove(obstaclePath)
        for i, obst in enumerate(self.obstacles):
            filename = obstacle_tmp.format(i)
            np.savetxt(filename, obst, '%f')

    def is_state_valid(self, state):
        for i in xrange(self.dim / 2):
            for obst in self.obstacles:
                poly = Path(obst)
                if poly.contains_point((state[2 * i], state[2 * i + 1])):
                    return False
        return True

    def set_state(self, state, arr):
        for i in xrange(self.dim):
            state()[i] = arr[i]
        return self

    def solve(self, st, gl, timeout=1.0):
        space = ob.RealVectorStateSpace(self.dim)
        bounds = ob.RealVectorBounds(self.dim)
        bounds.setLow(self.low_bound)
        bounds.setHigh(self.high_bound)
        space.setBounds(bounds)
        si = ob.SpaceInformation(space)
        si.setStateValidityChecker(
            ob.StateValidityCheckerFn(self.is_state_valid))
        start = ob.State(space)
        goal = ob.State(space)
        self.set_state(start, st)
        self.set_state(goal, gl)
        planner_def = ob.ProblemDefinition(si)
        planner_def.setStartAndGoalStates(start, goal)
        ompl_planner = self.planner(si)
        ompl_planner.setProblemDefinition(planner_def)
        ompl_planner.setup()
        planner_solved = ompl_planner.solve(timeout)

        if planner_solved:
            return FLSolution(planner_def)
        else:
            raise ValueError("No Solution Found")
