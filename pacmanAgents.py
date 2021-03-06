# pacmanAgents.py
# ---------------
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


from pacman import Directions
from game import Agent
from heuristics import *
import random

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write BFS Algorithm instead of returning Directions.STOP
        frontier = []
        explored = []
        depth = 0
        # get next legal action from the root state
        nextActions = state.getLegalPacmanActions()
        depth += 1
        # add those actions and their corresponding successor states to frontier
        for action in nextActions:
            nextState = state.generatePacmanSuccessor(action)
            nextStateHeuristic = admissibleHeuristic(nextState)
            frontier.append({'state': nextState,
                             'depth': depth,
                             'totalCost': nextStateHeuristic+depth,
                             'rootAction': action})
        while len(frontier) > 0:
            currentNode = frontier.pop(0)
            explored.append(currentNode)
            legalActions = currentNode['state'].getLegalPacmanActions()
            if len(legalActions) > 0:
                depth = currentNode['depth'] + 1
            for action in legalActions:
                nextState = currentNode['state'].generatePacmanSuccessor(action)
                if nextState == None:
                    explored = sorted(explored, key=lambda exploredState:exploredState['totalCost'])
                    return explored.pop(0)['rootAction']
                elif nextState.isLose():
                    continue
                else:
                    totalCost = depth + admissibleHeuristic(nextState)
                    rootAction = currentNode['rootAction']
                    frontier.append({'state': nextState,
                                     'depth': depth,
                                     'totalCost': totalCost,
                                     'rootAction': rootAction})


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP
        frontier = []
        explored = []
        depth = 0
        # get next legal action from the root state
        nextActions = state.getLegalPacmanActions()
        depth += 1
        # add those actions and their corresponding successor states to frontier
        for action in nextActions:
            nextState = state.generatePacmanSuccessor(action)
            nextStateHeuristic = admissibleHeuristic(nextState)
            frontier.append({'state': nextState,
                             'depth': depth,
                             'totalCost': nextStateHeuristic + depth,
                             'rootAction': action})
        while len(frontier) > 0:
            currentNode = frontier.pop(0)
            explored.append(currentNode)
            legalActions = currentNode['state'].getLegalPacmanActions()
            if len(legalActions) > 0:
                depth = currentNode['depth'] + 1
            for action in legalActions:
                nextState = currentNode['state'].generatePacmanSuccessor(action)
                if nextState == None:
                    explored = sorted(explored, key=lambda exploredState: exploredState['totalCost'])
                    return explored.pop(0)['rootAction']
                elif nextState.isLose():
                    continue
                else:
                    totalCost = depth + admissibleHeuristic(nextState)
                    rootAction = currentNode['rootAction']
                    frontier.insert(0, {'state': nextState,
                                        'depth': depth,
                                        'totalCost': totalCost,
                                        'rootAction': rootAction})

class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        frontier = []
        explored = []
        depth = 0
        # get next legal action from the root state
        nextActions = state.getLegalPacmanActions()
        depth += 1
        # add those actions and their corresponding successor states to frontier
        for action in nextActions:
            nextState = state.generatePacmanSuccessor(action)
            nextStateHeuristic = admissibleHeuristic(nextState)
            frontier.append({'state': nextState,
                             'depth': depth,
                             'totalCost': nextStateHeuristic+depth,
                             'rootAction': action})
        while len(frontier) > 0:
            frontier = sorted(frontier, key=lambda state: state['totalCost'])
            currentNode = frontier.pop(0)
            legalActions = currentNode['state'].getLegalPacmanActions()
            if len(legalActions) > 0:
                depth = currentNode['depth']+1
            for action in legalActions:
                nextState = currentNode['state'].generatePacmanSuccessor(action)
                if nextState == None or nextState.isWin():
                    return currentNode['rootAction']
                elif nextState.isLose():
                    continue
                else:
                    totalCost = depth+admissibleHeuristic(nextState)
                    rootAction = currentNode['rootAction']
                    frontier.append({'state': nextState,
                                     'depth': depth,
                                     'totalCost': totalCost,
                                     'rootAction': rootAction})
