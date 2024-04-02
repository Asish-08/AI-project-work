# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #define the number of iterations
        iterations=self.iterations
        for _ in range(iterations):
            #make copies of each iteration
            values_copy=self.values.copy()
            #get the states from the MDP
            mdp_states=self.mdp.getStates()

            #iterating over each state to get the best value
            for state in mdp_states:
                terminal_state=self.mdp.isTerminal(state)
                # checking if the state is terminal or not, if terminal, exit and update the copy of the values taken.
                if terminal_state != True:
                    possible_actions=self.mdp.getPossibleActions(state)
                    # calculating the max Q vlaue for the state by setting the deafult to -infinity
                    max_value = max([self.getQValue(state, action) for action in possible_actions], default=float('-inf'))
                    # updating the values that we took the coopy of with the max values that we got from above.
                    values_copy[state]=max_value
            # retruning the updated copy of values
            self.values=values_copy



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
    
        # get transition states and their probabilities
        transition_state = self.mdp.getTransitionStatesAndProbs(state, action)

        result = 0
        
        # iterate over each transition state and its probability
        for t in transition_state:
            # retrieve immediate reward to transition to the next state
            reward = self.mdp.getReward(state, action, t[0])
            
            # calculate the discounted future value using the next state's value
            future_value = self.discount * self.getValue(t[0])
            
            # Compute the Q-value for the current transition state
            q_value = t[1] * (reward + future_value)
            
            # Accumulate the Q-value
            result += q_value
        
        # Return the total Q-value
        return result


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
#        util.raiseNotDefined()
        terminal_state=self.mdp.isTerminal(state)
        # checking if the current state is terminal state
        if terminal_state != True:
            pass
            possible_actions=self.mdp.getPossibleActions(state)
            # if no actions are present return none
            if possible_actions==[]:
                return None
            # initialize variables to store the best action and its corresponding q-value to -infinity
            best_action = None
            max_val = float('-inf')
            
            # iterate over possible actions to find the one with the highest Q-value
            for action in possible_actions:
                # compute the q-value for the current action
                q_value = self.computeQValueFromValues(state, action)
                
                # update the best action and its corresponding q-value if necessary
                if q_value >= max_val:
                    best_action = action
                    max_val = q_value
            
            # Return the best action
            return best_action
        else:
            return None
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        # getting the list of states from MDP
        get_states=self.mdp.getStates()
        # getting the number of iterations 
        iteratrions=self.iterations
        # iterating over specified number of iterations just like mentioned in the description
        for i in range(iteratrions):
            # calculating the index for updating the index in a cyclic manner
            index = divmod(i, len(get_states))[1]
            #retreiving the states to be updated
            state_update = get_states[index]
            #assigning the current state to "terminal state"; to check if it is a terminal state or not
            terminal_state=self.mdp.isTerminal(state_update)
            # checking if the reteived state is terminal state or not
            if not terminal_state:
                # retreiving the actions from the current state
                ret_actions = self.mdp.getPossibleActions(state_update)
                # implementing the formula
                max_val = max([self.getQValue(state_update, a) for a in ret_actions], default=float('-inf'))

                # updating the val of current state witht he max of q-value
                self.values[state_update] = max_val

        return self.values


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

