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

from game import Directions
import util
from util import Stack
from util import Queue
from util import PriorityQueueWithFunction
from util import PriorityQueue

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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    stack = Stack()
    visited = []
    action = []
    stack.push((problem.getStartState(), action))
    while not stack.isEmpty():
        u, now_act = stack.pop()
        if problem.isGoalState(u):
            return now_act
        if u not in visited:
            successors = problem.getSuccessors(u)
            visited.append(u)
            for state, direct, cost in successors:
                if state not in visited:
                    stack.push((state, now_act + [direct]))
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = Queue()
    visited = []
    action = []
    queue.push((problem.getStartState(), action))
    while not queue.isEmpty():
        u, now_act = queue.pop()
        if problem.isGoalState(u):
            return now_act
        if u not in visited:
            successors = problem.getSuccessors(u)
            visited.append(u)
            for state, direct, cost in successors:
                if state not in visited:
                    queue.push((state, now_act + [direct]))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    global now_element
    "*** YOUR CODE HERE ***"
    start_point = problem.getStartState()
    pqueue = PriorityQueueWithFunction(lambda x: x[2])
    path = []
    visited = []
    pqueue.push((start_point, None, 0))
    parent_state = {(start_point, None, 0): None}
    while not pqueue.isEmpty():
        now_element = pqueue.pop()
        if problem.isGoalState(now_element[0]):
            break
        if now_element[0] not in visited:
            now_state = now_element[0]
            visited.append(now_state)
            next_state = problem.getSuccessors(now_state)
            for state in next_state:
                if state[0] not in visited:
                    cost = now_element[2]+state[2]
                    pqueue.push((state[0],state[1],cost))
                    parent_state[(state[0], state[1])] = now_element
    child_state = now_element
    while child_state is not None:
        path.append(child_state[1])
        child_state = None if child_state[0] == start_point else parent_state[(child_state[0], child_state[1])]
    path.reverse()
    return path[1:]


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


    pqueue = PriorityQueue()
    visited = []
    action = []
    pqueue.push((problem.getStartState(),action),0)
    while not pqueue.isEmpty():
        now_node, now_action = pqueue.pop()
        if problem.isGoalState(now_node):
            break
        if now_node not in visited:
            next_node = problem.getSuccessors(now_node)
            visited.append(now_node)
            for state , direct, cost in next_node:
                cost = problem.getCostOfActions(now_action + [direct]) + heuristic(state,problem)
                if (state  not in visited):
                    pqueue.push((state, (now_action + [direct])),cost)
    return now_action
    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
