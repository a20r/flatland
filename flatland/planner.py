
from matplotlib.path import Path
from ompl import base as ob
from ompl import geometric as og


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

    def __init__(self, dim=2, planner=og.PRMstar, obstacles=list()):
        self.dim = dim
        self.planner = planner
        self.obstacles = obstacles

    def is_state_valid(self, state):
        for i in xrange(self.dim / 2):
            for obst in self.obstacles:
                poly = Path(obst)
                if poly.contains_point((state[2 * i], state[2 * i + 1])):
                    return False
        return True

    def solve(self, st, gl):
        space = ob.RealVectorStateSpace(self.dim)
        bounds = ob.RealVectorBounds(self.dim)
        bounds.setLow(-10)
        bounds.setHigh(10)
        space.setBounds(bounds)
        si = ob.SpaceInformation(space)
        si.setStateValidityChecker(
            ob.StateValidityCheckerFn(self.is_state_valid))
        start = ob.State(space)
        start[0] = st[0]
        start[1] = st[1]
        goal = ob.State(space)
        goal.random()
        goal[0] = gl[0]
        goal[1] = gl[1]
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
