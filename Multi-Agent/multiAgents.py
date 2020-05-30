# multiAgents.py
# --------------
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
        comidaManhattan = 99999
        for food in newFood:
            u = util.manhattanDistance(newPos, food) 
            if u < comidaManhattan and u != 0:
                comidaManhattan= u #Distancia Manhattan entre pacman y la comida mas cercana
        fantasManhattan = 99999
        for ghostState in newGhostStates:
            fantasma = util.manhattanDistance(newPos, ghostState.getPosition())
            if fantasma < fantasManhattan:
                fantasManhattan = fantasma #Distancia Manhattan entre pacman y los fantasmas
            
        if fantasManhattan == 0 or fantasManhattan < 2: 
            fantasManhattan = -1000 #Quitandole muchos puntos si el fantasma esta a menos de 2 de distancia te aseguras de que no se acerce demasiado a este.
        else:
            fantasManhattan = 0
        
        if action == "Stop": #Asi se evita que pacman se quede quieto
            return -500
        
        return successorGameState.getScore() + fantasManhattan/comidaManhattan


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
        agents=gameState.getNumAgents()
        profundidad=agents*self.depth
        return max([(self.minimax(gameState.generateSuccessor(0,action),profundidad-1,1,agents),action) for action in gameState.getLegalActions(0)])[1] #0 = pacman y [1] #posicion a la que quieres ir
        # el algoritmo minimax recibe como parametros el estado del juego actual, el index actual(agente) y el numero de agentes
    def minimax(self,gameState, profundidad, index, agents):
        # si hemos llegado al final o hemos ganado o perdido, le preguntamos el estado del juego 
        if profundidad==0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState) #puntuacion de cada estado
        # como index 0 es Pacman, cuando le toque a Pacman cogeremos la puntuacion mas alta
        if index == 0:
            return max([self.minimax(gameState.generateSuccessor(index, i), profundidad - 1, (index+1)%agents, agents) for i in gameState.getLegalActions(index)])
        # si index no es 0, es decir, si le toca a un fantasma, buscaremos la puntuacion minima
        else:
            return min([self.minimax(gameState.generateSuccessor(index, i), profundidad - 1, (index+1)%agents,agents) for i in gameState.getLegalActions(index)])
   
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        agents=gameState.getNumAgents()
        alpha=-float('inf')
        beta=float('inf')
        m=-float('inf')
        # esta vez ademas añadimos alpha y beta con valores menos infinito e infinto
        profundidad=agents*self.depth
        for i in gameState.getLegalActions(0):
            valorAB=self.minimaxPoda(gameState.generateSuccessor(0,i),profundidad-1,1,agents,alpha,beta)
            if valorAB>m:
                action=i
                m=valorAB
            if valorAB>beta:
                return action
            alpha=max(valorAB, alpha)
        # si el valor obtenido es mayor que m, se reasigna el valor, ya que es la mejor opcion a tomar. Como beta tambien es menos infinito
        # el valor que evaluamos tambien es mayor que beta y, por tanto, se sustituye y se sale del bucle.
        return action

    def minimaxPoda(self,gameState, profundidad, index, agents,alpha,beta):
        # el primer if es igual que minimax
        if profundidad==0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        # si le toca a Pacman:
        if index ==0:
            # como valorAB almacenara el maximo, se le da valor menos infinito
            valorAB = -float('inf')
            for i in gameState.getLegalActions(index):
                valorAB = max(valorAB, self.minimaxPoda(gameState.generateSuccessor(index, i), profundidad - 1, (index+1)%agents, agents, alpha, beta))
                # cuando el valor sea mayor de beta se sustituye y, por tanto, se poda
                if valorAB>beta:
                    return valorAB
                # el valor maximo (valorAB) sera alpha
                alpha=max(valorAB,alpha)
            return valorAB
        else:
            # como ahora  valorAB debe ser el minimo, se le asigna el valor infinito
            
            valorAB = float('inf')
            for i in gameState.getLegalActions(index):
                valorAB = min(valorAB, self.minimaxPoda(gameState.generateSuccessor(index, i), profundidad - 1, (index+1)%agents,agents, alpha, beta))
                # si v es menos que alpha, se poda
                if valorAB<alpha:
                    return valorAB
                # el valor minimo (valorAB) sera beta
                beta=min(valorAB,beta)
            return valorAB

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
        agents=gameState.getNumAgents()
        profundidad=agents*self.depth
        return max([(self.expectiminimax(gameState.generateSuccessor(0,action),profundidad-1,1,agents),action) for action in gameState.getLegalActions(0)])[1]
        
    def expectiminimax(self, gameState, profundidad, index, agents):
        if profundidad == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        agente = (index + 1) % agents
        if index == 0:
            return max([self.expectiminimax(gameState.generateSuccessor(index, i), profundidad - 1, agente, agents) for i in gameState.getLegalActions(index)])
        else:
            # igual que minimax hasta aqui. A continuacion se hace una media de todos los posibles estados
            beta = sum([self.expectiminimax(gameState.generateSuccessor(index, i), profundidad - 1, agente, agents) for i in gameState.getLegalActions(index)])
            return float(beta/len(gameState.getLegalActions(index)))


    def betterEvaluationFunction(currentGameState):
        """ 
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>

        "*** YOUR CODE HERE ***"""
 
        newPos = currentGameState.getPacmanPosition()
        newFood = currentGameState.getFood().asList()
        newGhostStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
        # asi se puede saber donde estan todas las bolas de comida
        food = sum([manhattanDistance(food, newPos) for food in newFood])
    
        fantasma = 0
        # para todos los fantasmas:
        for i in range(len(newGhostStates)):
            d = manhattanDistance(newPos, newGhostStates[i].getPosition())
            # todos los fantasmas con sus respectivas posiciones
            # si el fantasma esta asustado, Pacman ira a por el
            if newScaredTimes[0] > 0:
                fantasma += 10.0
            # huir del fantasma si no esta asustado
            if newScaredTimes[i] == 0 and d < 1:
                fantasma -= 1. / (1-d)
            # si Pacman llega al fantasma mientras esta asustado, se lo comera
            elif newScaredTimes[i] < d:
                fantasma += 1. / d
        # devolvemos todos los valores
        return 1. / (1 + food * len(newFood)) + 10*fantasma + currentGameState.getScore()
    
    # Abbreviation
    better = betterEvaluationFunction

