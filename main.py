from random import choice;
from math import sqrt, log;


class Node:

    def __init__(self, currentBoard, turn = -1, parent = None):

        self.board = copy2Darray(currentBoard);
        self.possibleMoves = getPossibleMoves(self.board);
        self.unvisitedNodes = copy2Darray(self.possibleMoves);
        self.visitedNodes = [];
        self.turn = turn;
        self.parent = parent;

        self.isLeaf = len(self.unvisitedNodes) == 0;

        self.visits = 0;
        self.wins = 0;



    def calculateUTC(self, parent):

        # larger values of c lead to more exploratory agents
        c = sqrt(2);

        return (self.wins / self.visits) + c * sqrt(log(parent.visits) / self.visits);


    def getBestUCT(self):

        bestNode = None;
        bestUCT = -1;

        for node in self.visitedNodes:

            UCT = node.calculateUTC(self);

            if (UCT > bestUCT):
                bestUCT = UCT;
                bestNode = node;

        return bestNode;

    # select best node to explore
    def selectNode(self):
        
        node = self;
        
        while ((not node.isLeaf) and len(node.unvisitedNodes) == 0):
            node = node.getBestUCT();

        if (node.isLeaf):
            return node;
            
        return node.expand();


    def makeNodeFromMove(self, move):
        return Node(makeMoveOther(self.board, move, self.turn), -self.turn, self);

    # removes a random unvisited child from the unvisited list (and adds it to the visited list) and returns it
    def expand(self):
        newNode = choice(self.unvisitedNodes);
        self.unvisitedNodes.remove(newNode);

        self.visitedNodes.append(self.makeNodeFromMove(newNode));

        return self.visitedNodes[-1];


    def backpropagate(self, result):
        self.visits += 1;
        self.wins += result;
        
        if (self.parent):
            self.parent.backpropagate(-result);
        

    # make random moves untill game terminates, and go back up updating the nodes
    def simulateGame(self):

        if (self.isLeaf):
            self.backpropagate(getState(self.board) * self.turn);
            return;

        randomMove = choice(self.possibleMoves);

        self.makeNodeFromMove(randomMove).simulateGame();


    def bestChild(self):

        bestChild = None;
        mostVisits = 0;

        for node in self.visitedNodes:
            if (node.wins / node.visits < mostVisits):
                bestChild = node;
                mostVisits = node.wins / node.visits;

        print("Oi:", bestChild.wins);
        return bestChild;


    def MCTS(self, n):
        for i in range(n):
            node = self.selectNode();
            node.simulateGame();

        return self.bestChild();








def copy2Darray(array):
    return [row[:] for row in array];


def makeMoveOther(board, move, player):
    newBoard = copy2Darray(board);
    newBoard[move[0]][move[1]] = player;

    return newBoard;

def makeMove(board, move, player):
    board[move[0]][move[1]] = player;

def unmakeMove(board, move):
    board[move[0]][move[1]] = 0;


# this is the most terrible piece of code ever, but it should work
# -1 is X wins, +1 if O wins, and 0 if neither of those
def getState(board):
    players = [-1, 1];

    for i in range(2):

        player = players[i];

        isDiag1 = True;
        isDiag2 = True;
        isHorizontal = [True, True, True];
        isVertical = [True, True, True];

        for j in range(3):
            isDiag1 = isDiag1 and (board[j][j] == player);
            isDiag2 = isDiag2 and (board[j][2 - j] == player);

            for k in range(3):
                isHorizontal[j] = isHorizontal[j] and (board[j][k] == player);
                isVertical[j] = isVertical[j] and (board[k][j] == player);

        isWin = isDiag1 or isDiag2;
        for j in range(3):
            isWin = isWin or isHorizontal[j] or isVertical[j];

        if (isWin):
            return player;

    return 0;


def getPossibleMoves(board):
    moves = [];

    if (getState(board) != 0):
        return moves;

    for i in range(3):
        for j in range(3):

            # a move can be made only in an empty place
            if (board[i][j] == 0):
                moves.append((i, j));

    return moves;


def printBoard(board):

    b = "";

    for i in range(3):

        for j in range(3):

            if (board[i][j] == 0):
                b += "   ";
            elif (board[i][j] == -1):
                b += " X ";
            else:
                b += " O ";

            b += ("|" if j < 2 else "")

        b += ("\n-----------\n" if i < 2 else "");

    print(b);




# 0 -> empty
# -1 -> X
# 1 -> O
# initiate an empty board
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
];

if (input("Quer começar? ")):
    printBoard(board);
    move = tuple(map(int, input("\nYour move: ").split(",")));
    if (move not in getPossibleMoves(board)):
        print("Você é burro mesmo");
    else:
        makeMove(board, move, -1);

while True:
    
    if (len(getPossibleMoves(board)) == 0):
        printBoard(board);
        print("Você empatou!");
        break;

    agent = Node(board, 1);
    board = agent.MCTS(50).board;
    
    if (getState(board)):
        printBoard(board);
        print("Você perdeu burrão!");
        break;
        
    if (len(getPossibleMoves(board)) == 0):
        printBoard(board);
        print("Você empatou!");
        break;

    printBoard(board);
    move = tuple(map(int, input("\nYour move: ").split(",")));
    if (move not in getPossibleMoves(board)):
        print("Você é burro mesmo");
        break;
        
    makeMove(board, move, -1);
    
    if (getState(board)):
        printBoard(board);
        print("Você venceu espertão!");
        break;
