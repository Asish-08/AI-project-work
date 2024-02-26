# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
#    print("Start:", problem.getStartState())
#    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
#    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    fringe=util.Stack()
#    function GRAPH-SEARCH(problem, fringe) return a solution, or failure
#    closed ← an empty set
    closed= set()
#    fringe ← INSERT(MAKE-NODE(INITIAL-STATE[problem]), fringe)
    fringe.push((problem.getStartState(),[]))
#    loop do
    while True:
#        if fringe is empty then return failure
        if fringe.isEmpty():
            raise Exception("Failed")
        else:
#        node ← REMOVE-FRONT(fringe)
            state,actions=fringe.pop()        
#        if GOAL-TEST(problem, STATE[node]) then return node
            if problem.isGoalState(state):
                return actions
#        if STATE[node] is not in closed then
            if state not in closed:
#            add STATE[node] to closed
                closed.add(state)
                successor=problem.getSuccessors(state)
#            for child-node in EXPAND(STATE[node], problem) do 
                for child in successor:
                    position=child[0]
                    direction=child[1]
                    if position not in closed:
#                fringe ← INSERT(child-node, fringe)
                        new_actions=actions + [direction]
                        fringe.push((position,new_actions))
#    end
    return None
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    fringe=util.Queue()
#    function GRAPH-SEARCH(problem, fringe) return a solution, or failure
#    closed ← an empty set
    closed= set()
#    fringe ← INSERT(MAKE-NODE(INITIAL-STATE[problem]), fringe)
    fringe.push((problem.getStartState(),[]))
#    loop do
    while True:
#        if fringe is empty then return failure
        if fringe.isEmpty():
            raise Exception("Failed")
        else:
#        node ← REMOVE-FRONT(fringe)
            state,actions=fringe.pop()        
#        if GOAL-TEST(problem, STATE[node]) then return node
            if problem.isGoalState(state):
                return actions
#        if STATE[node] is not in closed then
            if state not in closed:
#            add STATE[node] to closed
                closed.add(state)
                successor=problem.getSuccessors(state)
#            for child-node in EXPAND(STATE[node], problem) do 
                for child in successor:
                    position=child[0]
                    direction=child[1]
                    if position not in closed:
#                fringe ← INSERT(child-node, fringe)
                        new_actions=actions + [direction]
                        fringe.push((position,new_actions))
#    end
    return None
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first."
    start = problem.getStartState()
    visited = set()
    fringe = util.PriorityQueue()
    fringe.push((start, []), 0)

    while not fringe.isEmpty():
        state, actions = fringe.pop()
        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state)
            successors = problem.getSuccessors(state)
            for next_state, action, cost in successors:
                if next_state not in visited:
                    new_actions = actions + [action]
                    total_cost = problem.getCostOfActions(new_actions)
                    fringe.push((next_state, new_actions), total_cost)

    return []

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
#closed ← an empty set
    closed = set()
    fringe = util.PriorityQueue()
#fringe ← INSERT(MAKE-NODE(INITIAL-STATE[problem]), fringe) with priority f(n) = g(n) + h(n)
    fringe.push((problem.getStartState(), []), nullHeuristic(problem.getStartState(), problem))
#loop do
#        if fringe is empty then return failure
    while True:
        if fringe.isEmpty():
            raise Exception("Failed")
        
        else:
#node ← REMOVE-FRONT(fringe)
            state, actions = fringe.pop()
#if GOAL-TEST(problem, STATE[node]) then return node
            if problem.isGoalState(state):
                return actions
#if STATE[node] is not in closed then
            if state not in closed:
#add STATE[node] to closed
                closed.add(state)
                successors = problem.getSuccessors(state)
#for each action, successor in SUCCESSORS(STATE[node], problem) do
                for successor in successors:
                    position, direction = successor[0], successor[1]
#if STATE[successor] is not in closed then
                    if position not in closed:
                        newActions = actions + [direction]
#fringe ← INSERT(MAKE-NODE(STATE[successor], node, action, PATH-COST[node] + STEP-COST(node, action)), fringe)....
# ...with priority f(successor) = PATH-COST[node] + STEP-COST(node, action) + h(STATE[successor])
                        fringe.push((position, newActions), problem.getCostOfActions(newActions) + heuristic(position, problem))

    return actions
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
