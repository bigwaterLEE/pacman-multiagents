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
        # print zip(scores, legalMoves),
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        # print legalMoves[chosenIndex]
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
        # print currentGameState
        # print successorGameState
        # print newPos
        # print newFood
        # print newGhostStates[0]
        # print newScaredTimes
        # oldGhostPos = [oldGhostState.getPosition() for oldGhostState in currentGameState.getGhostStates()]
        newGhostPos = [newGhostState.getPosition() for newGhostState in newGhostStates]
        # print oldGhostPos == newGhostPos
        # print newPos, newGhostPos
            # print "*"*50
        scoreAdjust = 0.0
        scoreAdjust -= (500 if min([util.manhattanDistance(newPos, posItem) for posItem in newGhostPos]) < 2 else 0)

        # oldFoodPos = currentGameState.getFood()
        foodPos = newFood.asList()
        # print foodPos, successorGameState.isWin(), currentGameState.isWin()
        currentPos = currentGameState.getPacmanPosition()
        if successorGameState.isWin():
            scoreAdjust += 1
        else:
            currentClosestFood = min([util.manhattanDistance(currentPos, item) for item in foodPos])
            newClosestFood = min([util.manhattanDistance(newPos, item) for item in foodPos])
            scoreAdjust += 1*random.randint(0, 1) if newClosestFood < currentClosestFood else 0
        # print successorGameState.getScore() + scoreAdjust


        # result = 0.0 + util.manhattanDistance()
        return successorGameState.getScore() + scoreAdjust

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
        # util.raiseNotDefined()
        # print gameState.getNumAgents()
        v, a = MaxValue(self, gameState, self.depth)
        # print v, a
        return a

def MaxValue(minimaxAgent, gameState, leftDepth):
    # print "max",
    if CutoffTest(gameState, leftDepth):
        # print "stop"
        return (minimaxAgent.evaluationFunction(gameState), None)
    v = []
    for a in gameState.getLegalActions(0):
        # print "call min"
        v.append((MinValue(minimaxAgent, gameState.generateSuccessor(0, a), leftDepth, gameState.getNumAgents()-1)[0], a))
    return max(v)
    # pass

def MinValue(minimaxAgent, gameState, leftDepth, leftGhost):
    # print "min",
    if CutoffTest(gameState, leftDepth):
        # print "stop"
        return (minimaxAgent.evaluationFunction(gameState), None)
    v = []
    if leftGhost > 1:
        for a in gameState.getLegalActions(gameState.getNumAgents() - leftGhost):
            # print "call min"
            v.append((MinValue(minimaxAgent, gameState.generateSuccessor(gameState.getNumAgents() - leftGhost, a), leftDepth, leftGhost-1)[0], None))
    else:
        for a in gameState.getLegalActions(gameState.getNumAgents() - leftGhost):
            # print "call max"
            v.append((MaxValue(minimaxAgent, gameState.generateSuccessor(gameState.getNumAgents() - leftGhost, a), leftDepth - 1)[0], None))
    return min(v)
    # pass

def CutoffTest(gameState, leftDepth):
    # print gameState.isWin(), gameState.isLose()
    return leftDepth == 0 or gameState.isWin() or gameState.isLose()
    # pass
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        v, a = MaxValueAB(self, gameState, self.depth,-10000.0, 10000.0)
        # print v, a
        return a

def MaxValueAB(minimaxAgent, gameState, leftDepth, l, u):
    # print "max",
    if CutoffTest(gameState, leftDepth):
        # print "stop"
        return (minimaxAgent.evaluationFunction(gameState), None)
    v = []
    for a in gameState.getLegalActions(0):
        # print "call min"
        temp = MinValueAB(minimaxAgent, gameState.generateSuccessor(0, a), leftDepth, gameState.getNumAgents()-1, l, u)[0]
        if temp > u:
            return (temp, a)
        v.append((temp, a))
        l = max(max(v)[0], l)
    return max(v)
    # pass

def MinValueAB(minimaxAgent, gameState, leftDepth, leftGhost, l, u):
    # print "min",
    if CutoffTest(gameState, leftDepth):
        # print "stop"
        return (minimaxAgent.evaluationFunction(gameState), None)
    v = []
    if leftGhost > 1:
        for a in gameState.getLegalActions(gameState.getNumAgents() - leftGhost):
            # print "call min"
            temp = MinValueAB(minimaxAgent, gameState.generateSuccessor(gameState.getNumAgents() - leftGhost, a), leftDepth, leftGhost-1, l, u)[0]
            if temp < l:
                return (temp, None)
            v.append((temp, None))
            u = min(min(v)[0], u)
    else:
        for a in gameState.getLegalActions(gameState.getNumAgents() - leftGhost):
            # print "call max"
            temp = MaxValueAB(minimaxAgent, gameState.generateSuccessor(gameState.getNumAgents() - leftGhost, a), leftDepth - 1, l, u)[0]
            if temp < l:
                return (temp, None)
            v.append((temp, None))
            u = min(min(v)[0], u)
    return min(v)
    # pass

# def MinValueAB(minimaxAgent, gameState, leftDepth, leftGhost, l, u):
#     # print "min",
#     if CutoffTest(gameState, leftDepth):
#         # print "stop"
#         return (minimaxAgent.evaluationFunction(gameState), None)
#     v = [(10000.0, None)]
#     if leftGhost == gameState.getNumAgents()-1:
#         if leftGhost > 1:
#             for a in gameState.getLegalActions(gameState.getNumAgents() - leftGhost):
#                 # print "call min"
#                 temp = MinValueAB(minimaxAgent, gameState.generateSuccessor(gameState.getNumAgents() - leftGhost, a), leftDepth, leftGhost-1, min(v))[0]
#                 if (temp, None) <= upperEtremum:
#                     return (temp, None)
#                 v.append((temp, None))
#         else:
#             for a in gameState.getLegalActions(gameState.getNumAgents() - leftGhost):
#                 # print "call max"
#                 temp = MaxValueAB(minimaxAgent, gameState.generateSuccessor(gameState.getNumAgents() - leftGhost, a), leftDepth - 1, min(v))[0]
#                 if (temp, None) <= upperEtremum:
#                     return (temp, None)
#                 v.append((temp, None))
#     else:
#         if leftGhost > 1:
#             for a in gameState.getLegalActions(gameState.getNumAgents() - leftGhost):
#                 # print "call min"
#                 v.append((MinValueAB(minimaxAgent, gameState.generateSuccessor(gameState.getNumAgents() - leftGhost, a), leftDepth, leftGhost-1, min(v))[0], None))
#         else:
#             for a in gameState.getLegalActions(gameState.getNumAgents() - leftGhost):
#                 # print "call max"
#                 v.append((MaxValueAB(minimaxAgent, gameState.generateSuccessor(gameState.getNumAgents() - leftGhost, a), leftDepth - 1, min(v))[0], None))
#     return min(v)
#     # pass

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
        # util.raiseNotDefined()
        # print gameState.getNumAgents()
        v, a = ExpectMax(self, gameState, self.depth)
        # print v, a
        return a

def ExpectMax(minimaxAgent, gameState, leftDepth):
    # print "max",
    if CutoffTest(gameState, leftDepth):
        # print "stop"
        return (minimaxAgent.evaluationFunction(gameState), None)
    v = []
    for a in gameState.getLegalActions(0):
        # print "call min"
        v.append((ChanceValue(minimaxAgent, gameState.generateSuccessor(0, a), leftDepth, gameState.getNumAgents()-1)[0], a))
    return max(v)
    # pass

def ChanceValue(minimaxAgent, gameState, leftDepth, leftGhost):
    # print "min",
    if CutoffTest(gameState, leftDepth):
        # print "stop"
        return (minimaxAgent.evaluationFunction(gameState), None)
    v = []
    if leftGhost > 1:
        for a in gameState.getLegalActions(gameState.getNumAgents() - leftGhost):
            # print "call min"
            v.append((ChanceValue(minimaxAgent, gameState.generateSuccessor(gameState.getNumAgents() - leftGhost, a), leftDepth, leftGhost-1)[0], None))
    else:
        for a in gameState.getLegalActions(gameState.getNumAgents() - leftGhost):
            # print "call max"
            v.append((ExpectMax(minimaxAgent, gameState.generateSuccessor(gameState.getNumAgents() - leftGhost, a), leftDepth - 1)[0], None))
    vSum = 0.0
    for value, item in v:
        vSum += value
    vAverage = vSum/len(v)
    return (vAverage, None)
    # pass

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    scoreAdjust = 0.0

    currentPos = currentGameState.getPacmanPosition()
    foodPos = currentGameState.getFood().asList()
    closestFood = [util.manhattanDistance(food, currentPos) for food in foodPos]
    scoreAdjust = ((0.5)**min(closestFood))*10 if len(closestFood) > 0  else 0

    capsulePos = currentGameState.getCapsules()
    closestCapsule = [util.manhattanDistance(capsule, currentPos) for capsule in capsulePos]
    scoreAdjust = ((0.5)**min(closestCapsule))*20 if len(closestCapsule) > 0  else 0

    ghostStates = currentGameState.getGhostStates()
    targetGhost = [(0.5**util.manhattanDistance(ghost.getPosition(), currentPos))*200 for ghost in ghostStates if util.manhattanDistance(ghost.getPosition(), currentPos) < ghost.scaredTimer]
    targetGhost.append(0)
    scoreAdjust += max(targetGhost)

    # scoreAdjust += currentPos[0] + currentPos[1]
    # maxManhattan = min(closestCapsule) if len(closestCapsule) > 0 else 0
    # random.seed()
    # scoreAdjust += (0.5**(maxManhattan + 3))*random.random()
    temp = [(0.5**util.manhattanDistance(ghost.getPosition(), currentPos))*2 for ghost in ghostStates if ghost.scaredTimer == 0]
    temp.append(0)
    scoreAdjust += max(temp)
    return currentGameState.getScore() + scoreAdjust

# Abbreviation
better = betterEvaluationFunction
