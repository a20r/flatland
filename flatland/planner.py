
import numpy as np
from matplotlib.path import Path
from ompl import base as ob


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

    def __init__(self, dim, planner):
        self.dim = dim
        self.planner = planner

    def is_state_valid(self, state):
        poly = Path(np.array([[0, 0],
                              [1, 0],
                              [1, 1]]))
        return not poly.contains_point((state[0], state[1]))

    def solve(self):
        space = ob.RealVectorStateSpace(8)
        bounds = ob.RealVectorBounds(8)
        bounds.setLow(-10)
        bounds.setHigh(10)
        space.setBounds(bounds)
        si = ob.SpaceInformation(space)
        si.setStateValidityChecker(
            ob.StateValidityCheckerFn(self.is_state_valid))
        start = ob.State(space)
        start.random()
        start()[0] = -5
        goal = ob.State(space)
        goal.random()
        goal()[0] = 5
        planner_def = ob.ProblemDefinition(si)
        planner_def.setStartAndGoalStates(start, goal)
        ompl_planner = self.planner(si)
        ompl_planner.setProblemDefinition(planner_def)
        ompl_planner.setup()
        planner_solved = ompl_planner.solve(1.0)

        if planner_solved:
            return FLSolution(planner_def)
        else:
            raise ValueError("No Solution Found")
