from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        pegs = []
        i = 0
        #loop through pegs
        while (i < 3):
            i = i + 1
            #check for disks on current peg
            request = parse_input('fact: (on ?disk peg' + str(i) + ')')
            bndings = self.kb.kb_ask(request)
            order = []
            if bndings:
                for bnding in bndings:
                    num = (str(bnding.bindings_dict['?disk']))[-1]
                    order.append(int(num))
            order = sorted(order)
            pegs.append(tuple(order))
        return tuple(pegs)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if(movable_statement.predicate == 'movable'):
            terms = movable_statement.terms
            gamedata = self.getGameState()
            diskn = str(terms[0])
            peg1 = str(terms[1])
            peg2 = str(terms[2])
            numpeg1 = int(peg1[-1]) - 1
            numpeg2 = int(peg2[-1]) - 1
            #deal with changes to first peg aka peg1
            self.kb.kb_retract(parse_input('fact: (on '+diskn+' '+peg1+')'))
            self.kb.kb_retract(parse_input('fact: (ontop '+diskn+' '+peg1+')'))
            if len(gamedata[numpeg1])<=1:
                self.kb.kb_add(parse_input('fact: (empty '+peg1+')'))
            else:
                self.kb.kb_add(parse_input('fact: (ontop disk'+str(gamedata[numpeg1][1])+' '+ peg1 +')'))
            
            #deal with changes to second peg aka peg2
            self.kb.kb_add(parse_input('fact: (on '+diskn+' '+peg2+')'))
            if not(gamedata[numpeg2]):
                self.kb.kb_retract(parse_input('fact: (empty '+peg2+')'))
            else:
                self.kb.kb_retract(parse_input('fact: (ontop disk' + str(gamedata[numpeg2][0]) + ' ' + peg2 + ')'))
            self.kb.kb_add(parse_input('fact: (ontop '+diskn+' '+ peg2 +')'))




    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        rows = []
        i = 0
        while (i < 3):
            j = 0
            i = i + 1
            row = []    
            while j < 3:
                j = j + 1
                bnding = self.kb.kb_ask(parse_input("fact: (pos ?tile pos" + str(j) + " " + "pos" + str(i) + ")"))
                if bnding == False: break
                tilen =str(bnding[0].bindings_dict['?tile'])[-1]
                if tilen == 'y':
                    tilen = -1
                else:
                    tilen = int(tilen)
                row.append(tilen)
            rows.append(tuple(row))
        return tuple(rows)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if(movable_statement.predicate == 'movable'):
            terms = movable_statement.terms
            #takes care of the pos, and rule for empty takes care of movables
            remov = parse_input('fact: (pos empty '+str(terms[3])+' '+str(terms[4])+')')
            renew = parse_input('fact: (pos '+str(terms[0])+' '+str(terms[3])+' '+str(terms[4])+')')
            self.kb.kb_retract(remov)
            self.kb.kb_assert(renew)
            remov2 = parse_input('fact: (pos '+str(terms[0])+' '+str(terms[1])+' '+str(terms[2])+')')
            renew2 = parse_input('fact: (pos empty '+str(terms[1])+' '+str(terms[2])+')')
            self.kb.kb_retract(remov2)
            self.kb.kb_assert(renew2)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
