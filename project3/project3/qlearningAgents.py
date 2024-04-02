# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        #initializing a counter
        self.QValues = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"

        return self.QValues.setdefault((state, action), 0)



    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        

        legal_actions = self.getLegalActions(state)

        if not legal_actions:
          return 0.0  # if there are no legal actions, return 0.0
        else:
          max_value = max(self.getQValue(state, action) for action in legal_actions)  # find the maximum Q-value
          return max_value




    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        # get legal actions for the given state
        legal_actions = self.getLegalActions(state)

        # initialize the maximum Q-value to negative infinity and an empty list to store better actions
        max_value = float('-inf')
        better_actions = []

        # check if there are legal actions available
        if len(legal_actions) != 0:
            # iterate over each legal action
            for action in legal_actions:
                # get the Q-value for the current action
                q_value = self.getQValue(state, action)
                
                # if the Q-value is greater than or equal to the current maximum Q-value
                if q_value >= max_value:
                    # if the Q-value is strictly greater, update the list of better actions
                    if q_value > max_value:
                        better_actions = [action]
                    # if the Q-value is equal, append the action to the list of better actions
                    else:
                        better_actions.append(action)
                    
                    # update the maximum Q-value
                    max_value = q_value

        # return a random choice from the list of better actions if it's not empty, otherwise return None
        return random.choice(better_actions) if better_actions else None



    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        #check if there are legal actions available
        if len(legalActions) != 0:
          # compute the probability of exploration
          probability = self.epsilon
          # flip a coin to decide whether to explore randomly or exploit the policy
          if util.flipCoin(probability) == True:
               #if exploration, choose a random action from the list of legal actions
              action_random = random.choice(legalActions)
          else:
              ## if exploitation, choose the best policy action
              action_random = self.getPolicy(state)
          return action_random
        else:
          #if no legal actions available (terminal state), return None
          return None

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        # Q(s, a) = (1-alpha)*Q(s, a) + (alpha)*(Reward + discount*Q_max(s', a'))
        current_QValue = self.getQValue(state, action)
        maximum_next_QValue = self.getValue(nextState)

        # Q(s, a) = (1 - alpha) * Q(s, a) + alpha * (reward + discount * maximum_next_QValue)
        new_QValue = (1 - self.alpha) * current_QValue  # non-updated portion of Q-value
        reward_component = self.alpha * (reward + self.discount * maximum_next_QValue)  # reward component
        current_QValue = new_QValue + reward_component  # updated Q-value

        self.QValues[(state, action)] = current_QValue



    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        #initializing
        Q_value=0
        feature_vector=self.featExtractor.getFeatures(state, action)
        # computing Q-value as the dot product of feature vector and weight vector
        Q_value = sum(feature_vector[f] * self.weights[f] for f in feature_vector)

        return Q_value



    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        #get the feature vector or the state action pair
        feature_vector = self.featExtractor.getFeatures(state, action)

        # get the rrent q values
        current_QValue = self.getQValue(state, action) # Q(s, a)

        #get the max q-values
        max_next_QValue = self.getValue(nextState) # Q_max(s', a')
#self.weights = {f: self.weights[f] + self.alpha * difference * feature_vector[f] for f in feature_vector}
        #update the weights using q-learning and update accordingly
        for feature in feature_vector: 
            #update the weight of the current feature
            self.weights[feature] += self.alpha*(reward + (self.discount*max_next_QValue) - current_QValue)*feature_vector[feature]


    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
