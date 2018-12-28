# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        position = list(newPos)
        food_position = newFood.asList()
        food_list = [manhattanDistance(position, x) for x in food_position]
        inverse_pellet_dist = 1.0 / min(food_list) if len(food_list) > 0 and min(food_list) != 0 else 0
        ghost_list = [manhattanDistance(position, x.getPosition) for x in newGhostStates]
        nearest_ghost_dist = min(ghost_list)
        t_buff = 0
        time_score = sum([time for time in newScaredTimes])
        if time_score:
            t_buff = -1 * nearest_ghost_dist + 20
        return successorGameState.getScore() + time_score + (nearest_ghost_dist + t_buff) * inverse_pellet_dist + (0 if nearest_ghost_dist > 1 else -100000)


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def max_value(state, depth=1):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            result = []
            for direction in state.getLegalActions(0):
                result.append(min_value(state.generateSuccessor(0, direction), depth))
            return max(result)

        def min_value(state, depth, ghostNumber=1):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            values = []
            for direction in state.getLegalActions(ghostNumber):
                if ghostNumber < state.getNumAgents() - 1:
                    values.append(min_value(state.generateSuccessor(ghostNumber, direction), depth, ghostNumber + 1))
                if ghostNumber == state.getNumAgents() - 1:
                    values.append(max_value(state.generateSuccessor((state.getNumAgents() - 1), direction), depth + 1))
            return min(values)
        legal_moves = gameState.getLegalActions(1)
        scores = [max_value(gameState.generateSuccessor(1, action)) for action in legal_moves]
        best_score = min(scores)
        index = 0
        for i in range(len(scores)):
            if scores[i] == best_score:
                index = i
        return legal_moves[index]
        


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      An expectimax agent you can use or modify
    """
    def expectimax_value (self, gameState, agentIndex, nodeDepth):
        if(agentIndex >= gameState.getNumAgents()):
            agentIndex = 0
            nodeDepth += 1	
        if( nodeDepth == self.depth ):
            return self.evaluationFunction(gameState)
        if( agentIndex == self.index ):
            return self.max_value(gameState, agentIndex, nodeDepth)        
      
        else:
            return self.exp_value(gameState, agentIndex, nodeDepth)
        
        return 'None'

    def max_value (self, gameState, agentIndex, nodeDepth):
      if( gameState.isWin() or gameState.isLose() ):
        return self.evaluationFunction(gameState)

      value = float("-inf")
      actionValue = "Stop"

      for legalActions in gameState.getLegalActions(agentIndex) :
        if legalActions == Directions.STOP:
          continue
        successor = gameState.generateSuccessor(agentIndex, legalActions)
        temp = self.expectimax_value(successor, agentIndex+1, nodeDepth)
        if( temp > value):
          value = temp
          actionValue = legalActions

      if( nodeDepth == 0 ):
        return actionValue
      else:
        return value

    def exp_value(self, gameState, agentIndex, nodeDepth):
      if( gameState.isWin() or gameState.isLose() ):
        return self.evaluationFunction(gameState)
      value = 0
      pr = 1.0/len(gameState.getLegalActions(agentIndex))
      
      for legalActions in gameState.getLegalActions(agentIndex):
        if( legalActions == Directions.STOP):
          continue
        successor = gameState.generateSuccessor(agentIndex, legalActions)
        value = value + (self.expectimax_value(successor, agentIndex+1, nodeDepth) * pr)
      return value

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        return self.expectimax_value(gameState,0,0)    
    

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 3). 

      DESCRIPTION: In this part, I consider these factor to evaluate the performence. And add some factor to realize 
      ghost-hunting, pellet-nabbing, food-gobbling, unstoppable.
      1,nearest Pellet Distance: make pacman to eat the near food which is like the power to drive pacman to go. and it
      negative related to the score so we use the neagtive value.
      2,nearest Ghost Distance: warn pacman to keep ghost away. when the distance is less than one which means it is very 
      dangerous,a lifebuff ,a very small value,will work to decrease the score dramatically and minmax tree will throw this action.
      3,foodstuff : use to appeal pacman to go to the area where lots of food located in.
      4,big pellet: timescore is a factor which affect the pacman to eat big pellet, because timescore increase the score.
      5,Scared time: when pacman eat big pellet, game go into scared time and pacman do not scare ghost, so a timebuff will 
      offset the lifebuff and pacman will take food as the first place and increase the finnal gamescore.
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    pacman_pos = currentGameState.getPacmanPosition()
    food_pos = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()      
    
    food_list = []
    for food in food_pos:
        food_list.append(manhattanDistance(pacman_pos, food))
    nearest_pellet_dist = 0
    if len(food_list) > 0:
        nearest_pellet_dist = min(food_list)
    ghost_list = []
    for ghost in ghosts:
        ghost_list.append(manhattanDistance(pacman_pos, ghost.getPosition()))
    nearest_ghost_dist = min(ghost_list)  
    foodstuff = sum(food_list)
    life_buff = 0
    if nearest_ghost_dist <=1:
        life_buff = -100000
    scared_times = [ghostState.scaredTimer for ghostState in ghosts]  
    temp_1 = 0
    temp_2 = 0
    for time in scared_times:
        temp_2 = time + temp_2
    if temp_2 != 0:
        temp_1 = -1 * life_buff 
    score = score * 2 if nearest_pellet_dist < nearest_ghost_dist else score
    return score - nearest_pellet_dist + nearest_ghost_dist - 0.3 * foodstuff + life_buff + 50 * temp_2 + temp_1

# Abbreviation
better = betterEvaluationFunction

