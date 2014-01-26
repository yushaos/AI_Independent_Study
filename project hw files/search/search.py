"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
     Returns the start state for the search problem
     """
     util.raiseNotDefined()

  def isGoalState(self, state):
     """
       state: Search state

     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state

     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()


def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 74].

  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.18].
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 74]"
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  #initialize queue
  node_visited = []
  finalStateList = []
  travelPath = {}
  travelPathCost = {}
  need_to_search = util.PriorityQueue()

  startNodeFull = (problem.getStartState(),'STOP' , 0)
  need_to_search.push(startNodeFull, 0)
  #Start node have travel cost of 0
  travelPathCost[problem.getStartState()] = 0

  #while queue is not empty
  while (not need_to_search.isEmpty()):
    currentNodeFull = need_to_search.pop()
    #store position
    currentNode = currentNodeFull[0]

    #Add visited node to closed set
    node_visited.append(currentNode)

    # if node reached goal, terminate, else, continue expand children node
    if( problem.isGoalState(currentNode) ):

      #print "This is goal state"
      path = _reconstruct(travelPath, currentNodeFull)
      for i in range(0, len(path), 3):
        eachNodeState = [path[i], path[i+1], path[i+2]]
        finalStateList.append(eachNodeState)
      pathDirection = [x[1] for x in finalStateList]
      #remove first item
      pathDirection.pop(0)
      return(pathDirection)

    #expand all chilren state of current node
    ChildNodeList = problem.getSuccessors(currentNode)
    #only add the non-visited node to search list
    for node in ChildNodeList:
      if node[0] not in node_visited:
          #Find travel cost of node from orgin node
          # = previsou node travel cost + cost to current node
          travelPathCost[node[0]] = travelPathCost[currentNode] + node[2]

          #Add the node and its heristic value = previous cost + future estimate
          FCost = travelPathCost[node[0]] + heuristic(node[0],problem)
          need_to_search.push( node, FCost )
          travelPath[node] = currentNodeFull

def _reconstruct( travelPath, currentstate):
    if( currentstate in travelPath ):
        pp = _reconstruct( travelPath, travelPath[currentstate])
        return( pp + currentstate )
    else:
        return (currentstate)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


