# -*- coding: utf-8 -*-
#
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    # Lista de nodos visitados
    cerrados = []
    # En el DFS usamos la "Stack" como estructura
    frontera = util.Stack()
    # Almacenamos el "start" en la pila
    frontera.push((problem.getStartState(),[]) )
    # Comprobamos si nuestra "Stack" está vacía
    while not frontera.isEmpty():
        nodo = frontera.pop()
    # Comprobamos si dicho nodo es el "goal"    
        if problem.isGoalState(nodo[0]):
        # De así serlo, pedimos el camino (que vendría a ser la solución o final)
            final = nodo[1]
            return final
       # Comprobamos si está cerrado y lo añadimos a la lista de cerrados
        if nodo[0] not in cerrados:
            cerrados.append(nodo[0])    
            # Obtenemos los sucesores
            for i in problem.getSuccessors( nodo[0]):
        
                    # Sumamos los caminos para obtener el recorrido hasta el momento
                    recorrido = nodo[1] + [i[1]]
                    # Y, de nuevo, almacenamos la tupla en la stack
                    frontera.push((i[0], recorrido) )
        
            
                      

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
    # En el algortimo BFS usamos la queue como estructura, y el resto del proceso es casi idéntico al anterior
    cerrados=[]
    frontera = util.Queue()
    frontera.push((problem.getStartState(),[]))
    

    while not frontera.isEmpty():
        nodo = frontera.pop()

        
        if problem.isGoalState(nodo[0]):
            final = nodo[1]
            return final
        
        if nodo[0] not in cerrados:
            cerrados.append(nodo[0])
            
            for i in problem.getSuccessors( nodo[0]):
                    recorrido = nodo[1] + [i[1]]
                    frontera.push((i[0], recorrido))
                   
       

       

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
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
    
    cerrados = []
    frontera = util.PriorityQueue()
    # En el start el coste es 0 pero luego lo acumularemos sumando el del nodo y el de sus sucesores
    frontera.push((problem.getStartState(), [], 0), 0)
    
    while not frontera.isEmpty():
        nodo=frontera.pop()
       
        if problem.isGoalState(nodo[0]):
            final = nodo[1]
            return final
    
        if nodo[0] not in cerrados:
            cerrados.append(nodo[0])
            
            for sucesor in problem.getSuccessors(nodo[0]):
                recorrido = nodo[1] + [sucesor[1]]
                coste = nodo[2] + sucesor[2]
                frontera.push((sucesor[0], recorrido, coste), (coste + heuristic(sucesor[0], problem)))




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch