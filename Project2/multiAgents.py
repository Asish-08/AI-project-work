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


from typing import Self
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        min_fooddist = float('inf') # Initialize with infinity
        # utilizing the newfood() list for calculating the mindist from the agent to food
        for pellet in newFood.asList():
            dist_to_food=util.manhattanDistance(pellet, newPos)
            min_fooddist= min(min_fooddist, dist_to_food)
        # taking the reciprocal of mindist to food as mentioned in the hint
        if min_fooddist != 0:
        # If there is food nearby:
            food_Score = 1 / min_fooddist
        else:
        # If there is no food nearby:
            food_Score = float('inf')
        # initialziing the ghost penalty 
        ghost_penal=0
        min_ghost_dist = float('inf')  # Initialize with infinity
        for ghost in newGhostStates:
            ghost_pos = ghost.getPosition()
            dist_to_ghost = util.manhattanDistance(ghost_pos, newPos)
            min_ghost_dist = min(min_ghost_dist, dist_to_ghost)
        
        # implementing the ghost penalty when ghost is nearer to the agent
        if min_ghost_dist<=1 :
            ghost_penal=1
        
        # taking the reciprocal of mindist to ghosts 
        if min_ghost_dist != 0:
        # If there is food nearby:
            ghost_Score = 1 / min_ghost_dist
        else:
        # If there no ghost is nearby, consider ghost score to be 0
            ghost_Score = 0
    # calculating the overall score from the terms defined and implemented above
        eval_score= successorGameState.getScore()+ food_Score - ghost_penal - ghost_Score
        return eval_score
        

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        return self.minimax_decision(gameState)

    def minimax_decision(self, gameState):
        """
        Minimax decision function.
        """
        best_action, _ = self.minimax(gameState, 0, 0)
        return best_action

    def minimax(self, gameState, agentIndex, depth_agent):
        """
        Minimax algorithm.
        """
        # if all agents have completed their turn, reset agent index and increase depth
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth_agent += 1
            
        # if the agent goes too far such as exceeding the depth limit or has reached its final state
        if depth_agent == self.depth or gameState.isWin() or gameState.isLose():
            return None, self.evaluationFunction(gameState)

        #since the state of the game starts with 0; lets consider it ST pacman has to ab_max
        if agentIndex == 0:
            return self.max_value(gameState, agentIndex, depth_agent)
        else:
            #if not max then min only and hence the viceversa
            return self.min_value(gameState, agentIndex, depth_agent)

    """
        Max-value function.
    """
    def max_value(self, gameState, agentIndex, depth_agent):
        #initialize
        best_action = None
        best_value = float('-inf')
        # recursively call the minimax algorithm for the next agent (ghost) in the tree
        for action in gameState.getLegalActions(agentIndex):
            successor_state = gameState.generateSuccessor(agentIndex, action)
            _, value = self.minimax(successor_state, agentIndex + 1, depth_agent)
            if value > best_value:
            #update the best action and value if the value obtained from this action is better
                best_value = value
                best_action = action
        return best_action, best_value
    
    """
        Min-value function.
    """
    def min_value(self, gameState, agentIndex, depth_agent):
        #initialize
        best_action = None
        best_value = float('inf')
        # recursively call the minimax algorithm for the next agent (ghost) in the tree
        for action in gameState.getLegalActions(agentIndex):
            successor_state = gameState.generateSuccessor(agentIndex, action)
            _, value = self.minimax(successor_state, agentIndex + 1, depth_agent)
            if value < best_value:
                #update the best action and value if the value obtained from this action is better
                best_value = value
                best_action = action
        return best_action, best_value
                   
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
#similar to minmax but the pruning condition enters here.
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # passing alpha beta values now
        return self.alpha_beta_algo(gameState, 0, 0, float('-inf'), float('inf'))[0] 

    def alpha_beta_algo(self, gameState, agentIndex, depth_agent, alpha, beta):
        """
        Implements the alpha-beta search algorithm
        """
        # if all agents have completed their turn, reset agent index and increase depth
        if agentIndex >= gameState.getNumAgents(): 
            agentIndex = 0
            depth_agent += 1

        # if the agent goes too far such as exceeding the depth limit or has reached its final state
        if depth_agent == self.depth or gameState.isWin() or gameState.isLose():
            return None, self.evaluationFunction(gameState)

        #since the state of the game starts with 0; lets consider it ST pacman has to maximize
        if agentIndex == 0: 
            return self.ab_max(gameState, agentIndex, depth_agent, alpha, beta)
        else:
            return self.ab_min(gameState, agentIndex, depth_agent, alpha, beta)

    def ab_max(self, gameState, agentIndex, depth_agent, alpha, beta):
        """
        Implements the maximizing part of the alpha-beta algorithm
        """
        #initialize
        best_action = None
        best_value = float('-inf')
        # recursively call the alpha_beta_algo algorithm for the next agent (ghost) in the tree
        for action in gameState.getLegalActions(agentIndex):
            newState = gameState.generateSuccessor(agentIndex, action)
            _, value = self.alpha_beta_algo(newState, agentIndex + 1, depth_agent, alpha, beta)
            
            if value > best_value:
                #update the best action and value if the value obtained from this action is better
                best_action = action
                best_value = value
                
            # updating alpha if higher value is found in max node
            alpha = max(alpha, best_value) 
            if best_value > beta:
                break
        return best_action, best_value

    def ab_min(self, gameState, agentIndex, depth_agent, alpha, beta):
        """
        Implements the minimizing part of the alpha-beta algorithm
        """
        #initialize
        best_action = None
        best_value = float('inf')
        
        # recursively call the alpha_beta_algo algorithm for the next agent (ghost) in the tree
        for action in gameState.getLegalActions(agentIndex):
            newState = gameState.generateSuccessor(agentIndex, action)
            _, value = self.alpha_beta_algo(newState, agentIndex + 1, depth_agent, alpha, beta)
            
            if value < best_value:
                #update the best action and value if the value obtained from this action is better
                best_action = action
                best_value = value
                
            # updating beta if lower value is found in min node
            beta = min(beta, best_value) 
            if best_value < alpha:
                break
        return best_action, best_value

    
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        return self.Expectimax_decision(gameState)

    def Expectimax_decision(self, gameState):
        """
        Expectimax_decision decision function.
        """
        best_action, _ = self.Expectimax(gameState, 0, 0)
        return best_action

    def Expectimax(self, gameState, agentIndex, depth_agent):
        """
        Expectimax algorithm.
        """
        # if all agents have completed their turn, reset agent index and increase depth
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth_agent += 1
            
        # if the agent goes too far such as exceeding the depth limit or has reached its final state
        if depth_agent == self.depth or gameState.isWin() or gameState.isLose():
            return None, self.evaluationFunction(gameState)

        #since the state of the game starts with 0; lets consider it ST pacman has to ab_max
        if agentIndex == 0:
            return self.max_value(gameState, agentIndex, depth_agent)
        else:
            #if not max then min only and hence the viceversa
            return self.min_value(gameState, agentIndex, depth_agent)

    """
        Max-value function.
    """
    def max_value(self, gameState, agentIndex, depth_agent):
        #initialize
        best_action = None
        best_value = float('-inf')
        # recursively call the Expectimax algorithm for the next agent (ghost) in the tree
        for action in gameState.getLegalActions(agentIndex):
            successor_state = gameState.generateSuccessor(agentIndex, action)
            _, value = self.Expectimax(successor_state, agentIndex + 1, depth_agent)
            if value > best_value:
            #update the best action and value if the value obtained from this action is better
                best_value = value
                best_action = action
        return best_action, best_value
    
    """
        Min-value function.
    """
    def min_value(self, gameState, agentIndex, depth_agent):
        # initialize
        best_action = None
        best_value = 0
        
        # calculate the probability associated with each possible action at a chance node
        state_chance = len(gameState.getLegalActions(agentIndex)) ** -1.0
        
        # recursively call the Expectimax algorithm for the next agent (ghost) in the tree
        for action in gameState.getLegalActions(agentIndex):
            successor_state = gameState.generateSuccessor(agentIndex, action)
            _, value = self.Expectimax(successor_state, agentIndex + 1, depth_agent)
                #computing the expected value of the current state considering all possible successor states 
                # and their associated probabilities
            best_value+=(value*state_chance)
            # to introduce randomness into the decision-making process at chance nodes
            best_action=random.choice(gameState.getLegalActions(agentIndex))
        return best_action, best_value
                   
                   
                   
                   