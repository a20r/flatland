#!/usr/bin/env python


from ompl import base as ob
from ompl import geometric as og


def isStateValid(state):
    # Some arbitrary condition on the state (note that thanks to
    # dynamic type checking we can just call getX() and do not need
    # to convert state to an SE2State.)
    return state[0] < 8


def planWithSimpleSetup():
    # create an SE2 state space
    space = ob.RealVectorStateSpace(8)

    # set lower and upper bounds
    bounds = ob.RealVectorBounds(8)
    bounds.setLow(-10)
    bounds.setHigh(10)
    space.setBounds(bounds)

    # create a simple setup object
    ss = og.SimpleSetup(space)
    ss.setStateValidityChecker(ob.StateValidityCheckerFn(isStateValid))

    start = ob.State(space)
    # we can pick a random start state...
    start.random()
    # ... or set specific values
    start()[0] = 5

    goal = ob.State(space)
    # we can pick a random goal state...
    goal.random()
    # ... or set specific values
    goal()[0] = -5

    ss.setStartAndGoalStates(start, goal)

    # this will automatically choose a default planner with
    # default parameters
    solved = ss.solve(5.0)

    if solved:
        # try to shorten the path
        #ss.simplifySolution()
        # print the simplified path
        print(ss.getSolutionPath().printAsMatrix())
        filename = 'path.txt'
        target = open(filename, 'w')
        target.write(ss.getSolutionPath().printAsMatrix())
        target.close()


def planTheHardWay():
    # create an SE2 state space
    space = ob.RealVectorStateSpace(8)
    # set lower and upper bounds
    bounds = ob.RealVectorBounds(8)
    bounds.setLow(-10)
    bounds.setHigh(10)
    space.setBounds(bounds)
    # construct an instance of space information from this state space
    si = ob.SpaceInformation(space)
    # set state validity checking for this space
    si.setStateValidityChecker(ob.StateValidityCheckerFn(isStateValid))
    # create a random start state
    start = ob.State(space)
    start.random()
    start()[0] = -5
    # create a random goal state
    goal = ob.State(space)
    goal.random()
    goal()[0] = 5
    # create a problem instance
    prmpdef = ob.ProblemDefinition(si)
    # set the start and goal states
    prmpdef.setStartAndGoalStates(start, goal)
    # create a planner for the defined space
    PRMplanner = og.PRMstar(si)
    # set the problem we are trying to solve for the planner
    PRMplanner.setProblemDefinition(prmpdef)
    # perform setup steps for the planner
    PRMplanner.setup()
    # print the settings for this space
    print(si.settings())
    # print the problem settings
    print(prmpdef)
    # attempt to solve the problem within one second of planning time
    PRMsolved = PRMplanner.solve(1.0)

    rrtpdef = ob.ProblemDefinition(si)
    rrtpdef.setStartAndGoalStates(start, goal)
    RRTplanner = og.RRTConnect(si)
    RRTplanner.setProblemDefinition(rrtpdef)
    RRTplanner.setup()
    RRTsolved = RRTplanner.solve(1.0)

    if PRMsolved:
        path = prmpdef.getSolutionPath()
        print("Found solution:\n%s" % path)
        filename = 'sandbox/prmpath.txt'
        target = open(filename, 'w')
        target.write(prmpdef.getSolutionPath().printAsMatrix())
        target.close()
    else:
        print("No solution found")

    if RRTsolved:
        path = rrtpdef.getSolutionPath()
        print("Found solution:\n%s" % path)
        filename = 'sandbox/rrtpath.txt'
        target = open(filename, 'w')
        target.write(rrtpdef.getSolutionPath().printAsMatrix())
        target.close()
    else:
        print("No solution found")


if __name__ == "__main__":
    #planWithSimpleSetup()
    #print("")
    planTheHardWay()
