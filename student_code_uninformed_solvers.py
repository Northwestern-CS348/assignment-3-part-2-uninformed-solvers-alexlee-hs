
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        ### look for unexplored child
        ### if none, go up to parent
        ### look for unexplored child
        
        if self.currentState.state == self.victoryCondition:
            return True
        moves = self.gm.getMovables()
        ind = self.currentState.nextChildToVisit
        while 1:
            while ind < len(moves):
                self.gm.makeMove(moves[ind])
                newState = GameState(self.gm.getGameState(), self.currentState.depth + 1, moves[ind])
                #if unexplored child...
                if newState not in self.visited:
                    self.currentState.nextChildToVisit = ind
                    newState.parent = self.currentState
                    self.currentState = newState #set new state
                    self.visited[self.currentState] = True
                    #return
                    if self.currentState.state == self.victoryCondition:
                        return True
                    else:
                        return False
                #if already explored child...
                else:
                    self.gm.reverseMove(moves[ind]) #go back
                    ind += 1
            #if there's parent node...
            if self.currentState.parent:
                self.currentState = self.currentState.parent
                return False
            else:
                break
        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.waitline = [self.currentState]

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        def reverseEv(sState):
            if sState.parent:
                self.gm.reverseMove(sState.requiredMovable)
                reverseEv(sState.parent)

        def getPath(sState,path):
            if sState.parent:
                path.append(sState.requiredMovable)
                path = getPath(sState.parent,path)
                self.gm.makeMove(path.pop(-1))
            return path
        
        #if already won, just stay
        if self.currentState.state == self.victoryCondition:
            return True
        
        #if not the first node, go to 
        if self.currentState.parent:
            if self.waitline[0] == self.currentState.parent:
                self.gm.reverseMove(self.currentState.requiredMovable)
            else:
                reverseEv(self.currentState)
                path = []
                getPath(self.waitline[0], path)
                
        self.currentState = self.waitline[0]
        
        moves = self.gm.getMovables()
        while(1):
            #tries out a branch
            self.gm.makeMove(moves[self.currentState.nextChildToVisit])
            newState = GameState(self.gm.getGameState(), self.currentState.depth + 1, moves[self.currentState.nextChildToVisit])
            #increments to test next branch in following loop
            self.currentState.nextChildToVisit += 1
            if self.currentState.nextChildToVisit >= len(moves):
                self.waitline.pop(0)


            #if unexplored...
            if newState not in self.visited:
                #plug into waitline list and visited dict
                self.waitline.append(newState)
                
                self.visited[newState] = True
                #set its parent
                newState.parent = self.currentState
                #print("Adding! " + str(newState.state))
                #print("")
                #set it as currentState to return response
                self.currentState = newState
                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    return False

            #if already explored or to be explored...
            else:
                #if done with this branch node
                self.gm.reverseMove(newState.requiredMovable)
                #if waitline was popped
                if self.waitline[0].nextChildToVisit == 0:
                    reverseEv(self.currentState)
                    path = []
                    getPath(self.waitline[0], path)
                    moves = self.gm.getMovables()
                self.currentState = self.waitline[0]
        return True
    
        