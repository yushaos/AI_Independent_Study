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
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    #evaluate pacman manhaton distance from ghost
    #score is lower if pacman is closer to ghost
    FearScore = 0
    GoodScore = 0
    for i, ghost in enumerate( newGhostStates ):
        #heavy penalty if game is lsot
        if(successorGameState.isLose() ):
            FearScore = 99999

        #heavy reward is game is won
        if(successorGameState.isWin()):
            GoodScore = 88888

        #ignore the ghost if scaredtime is on & more than 1 sec left
        if( newScaredTimes[i] <= 1 ):
            dist = manhattanDistance(newPos, ghost.getPosition())
            #log formula that makes close ghost very fearful, and decay to non important
            #Scale: 1->100, 2->12.2, 3->3.6, 4->1.5, 5->0.8 ...
            #Don't do the calculation if ghost is on top of pacman, game is over
            if( dist != 0 ):
                FearScore += 100*pow(dist, -3.033)

    #It is good if this move is on a dot
    if( successorGameState.hasFood(newPos[0], newPos[1]) ):
        #scale to where ghost is more than 2 block away is worth to eat the dot
        GoodScore += 100*pow(2.3, -3.033)

    #evaluate pacman distance to food, closer the better
    #note: it should have less impact compare to closeby ghost
    MinDist= 9999
    for dot in oldFood.asList():
        dist = manhattanDistance(newPos, dot)
        if( dist < MinDist ):
            MinDist = dist

    #smaller the distance of closest dot, less subtraction from good score
    Const = 4
    GoodScore -= Const*MinDist

    #less number of dot left on the map the better
    GoodScore -= oldFood.count()


    #put some cost if pacman choose to stop, discourage this behavior
    if( action == 'Stop' ):
        GoodScore -= 5


    #set the final score, and round to nearest interger
    FinalScore = int(round(GoodScore - FearScore, 0))
    #FinalScore = GoodScore - FearScore

    #return ( successorGameState.getScore() + FinalScore )
    return(FinalScore)

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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"

    #Max Agent action
    def AlphaBetaFunc(state, alpha, beta, agentIndex):

        # Cut off criteria reaches when agentIndex level reached, game won, or lost
        if( agentIndex >= totalNumAng *self.depth - 1
           or state.isWin()
           or state.isLose() ):
            score = self.evaluationFunction( state )
            return (score)

        #Determine current agent and next agentIndex agent type: min or max
        if( agentIndex % totalNumAng < NumPacman ):
            currAgt = 'pacman'
        else:
            currAgt = 'ghost'

        # current node is pacman (max agent)
        if( currAgt == 'pacman' ):

            # get all possible move for current game state
            actionStateList = PossibleMove( state, agentIndex % totalNumAng )
            for item in actionStateList:
                action = item[0]
                state = item[1]

                alpha = max(alpha, AlphaBetaFunc(state, alpha, beta, agentIndex+1))

                # beta cutoff
                if beta <= alpha:
                    break
            return (alpha)

        # current node is ghost (min agent)
        else:
            # get all possible move for current game state
            actionStateList = PossibleMove( state, agentIndex % totalNumAng )
            for item in actionStateList:
                action = item[0]
                state = item[1]

                beta = min(beta, AlphaBetaFunc(state, alpha, beta, agentIndex+1))
                # alpha cut off
                if( beta <= alpha ):
                    break
            return(beta)

        raise Exception("Should not reach here")


    #----------------------------------------------------------------
    #generate possible moves
    def PossibleMove( state, agentIndex ):
        actions = state.getLegalActions(agentIndex)

        # remove 'stop' as one the the legal action
        if 'Stop' in actions:
            actions.remove('Stop')

        # actionStateList format: [(action, state, score), ...]
        actionStateList = []
        for action in actions:
            nextDepthState = state.generateSuccessor(agentIndex, action)
            actionStateList.append( [action, nextDepthState, None] )

        return( actionStateList )

    #--------------------------------------------------------------------
    depth = self.depth
    totalNumAng = gameState.getNumAgents()
    NumGhost = totalNumAng - 1
    NumPacman = 1
    action = None

    # get pacman current game agentIndex, and its possible actions
    agentIndex = 0
    actionStateList = PossibleMove( gameState, agentIndex )

    # Find the best evaluated result from root node's children actions
    MaxValue = -9999
    for item in actionStateList:
        action = item[0]
        state = item[1]
        score = AlphaBetaFunc(state, -99999, 99999, agentIndex+1)
        item[2] = score
        # Get the best action from the max score in the list
        if( MaxValue < score ):
            MaxValue = score
            BestAction = action

    return( BestAction )
    #util.raiseNotDefined()



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
    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

