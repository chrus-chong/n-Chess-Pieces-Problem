import sys

from copy import deepcopy
from random import shuffle
from typing import List

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

creationId = 0  # global variable to facilitate comparison of chess pieces

alphabetDict = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9,
    "k": 10,
    "l": 11,
    "m": 12,
    "n": 13,
    "o": 14,
    "p": 15,
    "q": 16,
    "r": 17,
    "s": 18,
    "t": 19,
    "u": 20,
    "v": 21,
    "w": 22,
    "x": 23,
    "y": 24,
    "z": 25,
}


def parse(filename):

    # read file
    file = open(filename)
    endOfFile = False

    listOfPieces = []
    board = Board()

    numKing = None
    numQueen = None
    numBishop = None
    numRook = None
    numKnight = None

    while not endOfFile:
        line = file.readline()
        line = line.rstrip()  ##remove newline
        if "Rows:" in line:
            arrOfWords = line.split(":")
            rowValue = (int)(arrOfWords[1])
            board.rows = rowValue

        if "Cols:" in line:
            arrOfWords = line.split(":")
            colValue = (int)(arrOfWords[1])
            board.columns = colValue
            board.initialiseMatrix()

        if "Number of Obstacles:" in line:
            arrOfWords = line.split(":")
            num_obstacles = (int)(arrOfWords[1])
            board.numObstacles = num_obstacles

        if "Position of Obstacles (space between):" in line:
            if line.split(":")[1] == "-":
                continue
            line = line.split(":")[1]
            arrOfChessNotation = line.split(" ")
            board.placeObstacles(arrOfChessNotation)

        if "Number of King, Queen, Bishop, Rook, Knight (space between):" in line:
            line = line.split(":")[1]
            arrOfPieceNumbers = line.split(" ")

            numKing = (int)(arrOfPieceNumbers[0])
            numQueen = (int)(arrOfPieceNumbers[1])
            numBishop = (int)(arrOfPieceNumbers[2])
            numRook = (int)(arrOfPieceNumbers[3])
            numKnight = (int)(arrOfPieceNumbers[4])

            appendPiece = listOfPieces.append

            for i in range(numKing):
                appendPiece(King(None, None))

            for i in range(numQueen):
                appendPiece(Queen(None, None))

            for i in range(numBishop):
                appendPiece(Bishop(None, None))

            for i in range(numRook):
                appendPiece(Rook(None, None))

            for i in range(numKnight):
                appendPiece(Knight(None, None))

        if not line:
            endOfFile = True

    file.close()

    # Done parsing text file. need to fill in default 0 (empty)
    for i in range(board.rows):
        for j in range(board.columns):
            if board.matrix[i][j] is None:
                board.matrix[i][j] = 0

    state = State(listOfPieces, board)
    return state


class Move:
    def __init__(self, start_coords, end_coords):
        self.startCoords = start_coords
        self.endCoords = end_coords
        self.withinBoard = None

    def __str__(self):
        return "Move from " + str(self.startCoords) + " to " + str(self.endCoords)


class Piece:
    def __init__(self, x_coord, y_coord):
        self.isAlive = True
        self.coordinates = [x_coord, y_coord]
        self.type = None

        global creationId
        self.cId = creationId
        creationId += 1

    def generateAllMoves(self, pieceCoords: List[int], state):
        return None

    def __eq__(self, other):
        if isinstance(other, Piece):
            return self.cId == other.cId
        return False

    def isEqual(self, other):
        if isinstance(other, Piece):
            equal = True
            if self.isAlive != other.isAlive:
                equal = False
            if self.coordinates[0] != other.coordinates[0]:
                equal = False
            if self.coordinates[1] != other.coordinates[1]:
                equal = False
            if self.type != other.type:
                equal = False
            if self.cId == other.cId:
                if equal is False:
                    return False
                return True
            else:
                return False
        else:
            return False


class Obstacle(Piece):
    def __init__(self, x_coord, y_coord):
        super().__init__(x_coord, y_coord)
        self.type = "Obstacle"

    def generateAllMoves(self, pieceCoords: List[int], state):
        return None


class Rook(Piece):
    def __init__(self, x_coord, y_coord):
        super().__init__(x_coord, y_coord)
        self.type = "Rook"

    def allPossibleMovesLeft(self, pieceCoords: List[int], state):
        ## Keep x-coordinate the same. Change y-coordinate to keep decreasing until 0
        currentY = pieceCoords[1]
        allLeftMoves = []
        currentY = currentY - 1
        while currentY >= 0 and currentY < state.board.columns:
            if state.hasObstacleAt([pieceCoords[0], currentY]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [pieceCoords[0], currentY],
            )
            allLeftMovesAppend = allLeftMoves.append
            allLeftMovesAppend(move)
            currentY = currentY - 1
        return allLeftMoves

    def allPossibleMovesRight(self, pieceCoords: List[int], state):
        ## Keep x-coordinate the same. Change y-coordinate to keep increasing until equal (columns - 1)
        currentY = pieceCoords[1]
        allRightMoves = []
        currentY = currentY + 1
        while currentY >= 0 and currentY < state.board.columns:
            if state.hasObstacleAt([pieceCoords[0], currentY]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [pieceCoords[0], currentY],
            )

            allRightMovesAppend = allRightMoves.append
            allRightMovesAppend(move)
            currentY = currentY + 1
        return allRightMoves

    def allPossibleMovesUp(self, pieceCoords: List[int], state):
        ## Keep y-coordinate the same. Change x-coordinate to keep decreasing until 0
        currentX = pieceCoords[0]
        allUpMoves = []
        currentX = currentX - 1
        while currentX >= 0 and currentX < state.board.rows:
            if state.hasObstacleAt([currentX, pieceCoords[1]]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [currentX, pieceCoords[1]],
            )

            allUpMovesAppend = allUpMoves.append
            allUpMovesAppend(move)

            currentX = currentX - 1
        return allUpMoves

    def allPossibleMovesDown(self, pieceCoords: List[int], state):
        ## Keep y-coordinate the same. Change x-coordinate to keep increasing until equal (rows - 1)
        currentX = pieceCoords[0]
        allDownMoves = []
        currentX = currentX + 1
        while currentX >= 0 and currentX < state.board.rows:
            if state.hasObstacleAt([currentX, pieceCoords[1]]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [currentX, pieceCoords[1]],
            )

            allDownMovesAppend = allDownMoves.append
            allDownMovesAppend(move)

            currentX = currentX + 1
        return allDownMoves

    def generateAllMoves(self, pieceCoords: List[int], state):
        left = self.allPossibleMovesLeft(pieceCoords, state)
        right = self.allPossibleMovesRight(pieceCoords, state)
        up = self.allPossibleMovesUp(pieceCoords, state)
        down = self.allPossibleMovesDown(pieceCoords, state)
        allMoves = [
            *up,
            *right,
            *down,
            *left,
        ]
        return allMoves


class Bishop(Piece):
    def __init__(self, x_coord, y_coord):
        super().__init__(x_coord, y_coord)
        self.type = "Bishop"

    def allPossibleMovesUpLeft(self, pieceCoords: List[int], state):
        ## Change both x and y coordinates to keep decreasing until either reaches 0
        currentX = pieceCoords[0]
        currentY = pieceCoords[1]
        allUpLeftMoves = []
        currentX = currentX - 1
        currentY = currentY - 1
        while (
            currentY >= 0
            and currentX >= 0
            and currentY < state.board.columns
            and currentX < state.board.rows
        ):
            if state.hasObstacleAt([currentX, currentY]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [currentX, currentY],
            )

            allUpLeftMovesAppend = allUpLeftMoves.append
            allUpLeftMovesAppend(move)

            currentX = currentX - 1
            currentY = currentY - 1
        return allUpLeftMoves

    def allPossibleMovesUpRight(self, pieceCoords: List[int], state):
        ## Change x-coordinate to keep decreasing until 0. Change y-coordinate to keep increasing until equal (columns - 1)
        currentX = pieceCoords[0]
        currentY = pieceCoords[1]
        allUpRightMoves = []
        currentX = currentX - 1
        currentY = currentY + 1
        while (
            currentY >= 0
            and currentX >= 0
            and currentY < state.board.columns
            and currentX < state.board.rows
        ):
            if state.hasObstacleAt([currentX, currentY]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [currentX, currentY],
            )

            allUpRightMovesAppend = allUpRightMoves.append
            allUpRightMovesAppend(move)

            currentX = currentX - 1
            currentY = currentY + 1
        return allUpRightMoves

    def allPossibleMovesDownLeft(self, pieceCoords: List[int], state):
        ## Change x-coordinate to keep increasing until (rows - 1). Change y-coordinate to keep decreasing until 0.
        currentX = pieceCoords[0]
        currentY = pieceCoords[1]
        allDownLeftMoves = []
        currentX = currentX + 1
        currentY = currentY - 1
        while (
            currentY >= 0
            and currentX >= 0
            and currentY < state.board.columns
            and currentX < state.board.rows
        ):
            if state.hasObstacleAt([currentX, currentY]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [currentX, currentY],
            )

            allDownLeftMovesAppend = allDownLeftMoves.append
            allDownLeftMovesAppend(move)

            currentX = currentX + 1
            currentY = currentY - 1
        return allDownLeftMoves

    def allPossibleMovesDownRight(self, pieceCoords: List[int], state):
        ## Change x-coordinate to keep increasing until (rows - 1). Change y-coordinate to keep increasing until (columns -1).
        currentX = pieceCoords[0]
        currentY = pieceCoords[1]
        allDownRightMoves = []
        currentX = currentX + 1
        currentY = currentY + 1
        while (
            currentY >= 0
            and currentX >= 0
            and currentY < state.board.columns
            and currentX < state.board.rows
        ):
            if state.hasObstacleAt([currentX, currentY]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [currentX, currentY],
            )

            allDownRightMovesAppend = allDownRightMoves.append
            allDownRightMovesAppend(move)

            currentX = currentX + 1
            currentY = currentY + 1
        return allDownRightMoves

    def generateAllMoves(self, pieceCoords: List[int], state):
        upLeft = self.allPossibleMovesUpLeft(pieceCoords, state)
        upRight = self.allPossibleMovesUpRight(pieceCoords, state)
        downLeft = self.allPossibleMovesDownLeft(pieceCoords, state)
        downRight = self.allPossibleMovesDownRight(pieceCoords, state)
        allMoves = [
            *upRight,
            *downRight,
            *downLeft,
            *upLeft,
        ]
        return allMoves


class Knight(Piece):
    def __init__(self, x_coord, y_coord):
        super().__init__(x_coord, y_coord)
        self.type = "Knight"

    def generateAllMoves(self, pieceCoords: List[int], state):
        UpUpLeft = [pieceCoords[0] - 2, pieceCoords[1] - 1]
        UpUpRight = [pieceCoords[0] - 2, pieceCoords[1] + 1]
        DownDownLeft = [pieceCoords[0] + 2, pieceCoords[1] - 1]
        DownDownRight = [pieceCoords[0] + 2, pieceCoords[1] + 1]
        LeftLeftUp = [pieceCoords[0] - 1, pieceCoords[1] - 2]
        LeftLeftDown = [pieceCoords[0] + 1, pieceCoords[1] - 2]
        RightRightUp = [pieceCoords[0] - 1, pieceCoords[1] + 2]
        RightRightDown = [pieceCoords[0] + 1, pieceCoords[1] + 2]
        allMoves = [
            UpUpRight,
            RightRightUp,
            RightRightDown,
            DownDownRight,
            DownDownLeft,
            LeftLeftDown,
            LeftLeftUp,
            UpUpLeft,
        ]
        allValidMoves = []

        for coordinates in allMoves:
            if (
                coordinates[0] >= 0
                and coordinates[1] >= 0
                and coordinates[0] < state.board.rows
                and coordinates[1] < state.board.columns
            ):
                if state.hasObstacleAt(coordinates):
                    continue
                move = Move(
                    [pieceCoords[0], pieceCoords[1]],
                    [coordinates[0], coordinates[1]],
                )
                allValidMovesAppend = allValidMoves.append
                allValidMovesAppend(move)
        return allValidMoves


class Queen(Piece):
    def __init__(self, x_coord, y_coord):
        super().__init__(x_coord, y_coord)
        self.type = "Queen"

    def allPossibleMovesLeft(self, pieceCoords: List[int], state):
        ## Keep x-coordinate the same. Change y-coordinate to keep decreasing until 0
        currentY = pieceCoords[1]
        allLeftMoves = []
        currentY = currentY - 1
        while currentY >= 0 and currentY < state.board.columns:
            if state.hasObstacleAt([pieceCoords[0], currentY]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [pieceCoords[0], currentY],
            )

            allLeftMovesAppend = allLeftMoves.append
            allLeftMovesAppend(move)

            currentY = currentY - 1
        return allLeftMoves

    def allPossibleMovesRight(self, pieceCoords: List[int], state):
        ## Keep x-coordinate the same. Change y-coordinate to keep increasing until equal (columns - 1)
        currentY = pieceCoords[1]
        allRightMoves = []
        currentY = currentY + 1
        while currentY >= 0 and currentY < state.board.columns:
            if state.hasObstacleAt([pieceCoords[0], currentY]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [pieceCoords[0], currentY],
            )

            allRightMovesAppend = allRightMoves.append
            allRightMovesAppend(move)

            currentY = currentY + 1
        return allRightMoves

    def allPossibleMovesUp(self, pieceCoords: List[int], state):
        ## Keep y-coordinate the same. Change x-coordinate to keep decreasing until 0
        currentX = pieceCoords[0]
        allUpMoves = []
        currentX = currentX - 1
        while currentX >= 0 and currentX < state.board.rows:
            if state.hasObstacleAt([currentX, pieceCoords[1]]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [currentX, pieceCoords[1]],
            )

            allUpMovesAppend = allUpMoves.append
            allUpMovesAppend(move)

            currentX = currentX - 1
        return allUpMoves

    def allPossibleMovesDown(self, pieceCoords: List[int], state):
        ## Keep y-coordinate the same. Change x-coordinate to keep increasing until equal (rows - 1)
        currentX = pieceCoords[0]
        allDownMoves = []
        currentX = currentX + 1
        while currentX >= 0 and currentX < state.board.rows:
            if state.hasObstacleAt([currentX, pieceCoords[1]]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [currentX, pieceCoords[1]],
            )

            allDownMovesAppend = allDownMoves.append
            allDownMovesAppend(move)

            currentX = currentX + 1
        return allDownMoves

    def allPossibleMovesUpLeft(self, pieceCoords: List[int], state):
        ## Change both x and y coordinates to keep decreasing until either reaches 0
        currentX = pieceCoords[0]
        currentY = pieceCoords[1]
        allUpLeftMoves = []
        currentX = currentX - 1
        currentY = currentY - 1
        while (
            currentY >= 0
            and currentX >= 0
            and currentY < state.board.columns
            and currentX < state.board.rows
        ):

            if state.hasObstacleAt([currentX, currentY]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [currentX, currentY],
            )

            allUpLeftMovesAppend = allUpLeftMoves.append
            allUpLeftMovesAppend(move)

            currentX = currentX - 1
            currentY = currentY - 1
        return allUpLeftMoves

    def allPossibleMovesUpRight(self, pieceCoords: List[int], state):
        ## Change x-coordinate to keep decreasing until 0. Change y-coordinate to keep increasing until equal (columns - 1)
        currentX = pieceCoords[0]
        currentY = pieceCoords[1]
        allUpRightMoves = []
        currentX = currentX - 1
        currentY = currentY + 1
        while (
            currentY >= 0
            and currentX >= 0
            and currentY < state.board.columns
            and currentX < state.board.rows
        ):

            if state.hasObstacleAt([currentX, currentY]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [currentX, currentY],
            )

            allUpRightMovesAppend = allUpRightMoves.append
            allUpRightMovesAppend(move)

            currentX = currentX - 1
            currentY = currentY + 1
        return allUpRightMoves

    def allPossibleMovesDownLeft(self, pieceCoords: List[int], state):
        ## Change x-coordinate to keep increasing until (rows - 1). Change y-coordinate to keep decreasing until 0.
        currentX = pieceCoords[0]
        currentY = pieceCoords[1]
        allDownLeftMoves = []
        currentX = currentX + 1
        currentY = currentY - 1
        while (
            currentY >= 0
            and currentX >= 0
            and currentY < state.board.columns
            and currentX < state.board.rows
        ):

            if state.hasObstacleAt([currentX, currentY]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [currentX, currentY],
            )

            allDownLeftMovesAppend = allDownLeftMoves.append
            allDownLeftMovesAppend(move)

            currentX = currentX + 1
            currentY = currentY - 1
        return allDownLeftMoves

    def allPossibleMovesDownRight(self, pieceCoords: List[int], state):
        ## Change x-coordinate to keep increasing until (rows - 1). Change y-coordinate to keep increasing until (columns -1).
        currentX = pieceCoords[0]
        currentY = pieceCoords[1]
        allDownRightMoves = []
        currentX = currentX + 1
        currentY = currentY + 1
        while (
            currentY >= 0
            and currentX >= 0
            and currentY < state.board.columns
            and currentX < state.board.rows
        ):
            if state.hasObstacleAt([currentX, currentY]):
                break
            move = Move(
                [pieceCoords[0], pieceCoords[1]],
                [currentX, currentY],
            )

            allDownRightMovesAppend = allDownRightMoves.append
            allDownRightMovesAppend(move)

            currentX = currentX + 1
            currentY = currentY + 1
        return allDownRightMoves

    def generateAllMoves(self, pieceCoords: List[int], state):
        up = self.allPossibleMovesUp(pieceCoords, state)
        down = self.allPossibleMovesDown(pieceCoords, state)
        left = self.allPossibleMovesLeft(pieceCoords, state)
        right = self.allPossibleMovesRight(pieceCoords, state)

        upLeft = self.allPossibleMovesUpLeft(pieceCoords, state)
        upRight = self.allPossibleMovesUpRight(pieceCoords, state)
        downLeft = self.allPossibleMovesDownLeft(pieceCoords, state)
        downRight = self.allPossibleMovesDownRight(pieceCoords, state)
        allMoves = [
            *up,
            *upRight,
            *right,
            *downRight,
            *down,
            *downLeft,
            *left,
            *upLeft,
        ]
        return allMoves


class King(Piece):
    def __init__(self, x_coord, y_coord):
        super().__init__(x_coord, y_coord)
        self.type = "King"

    def generateAllMoves(self, pieceCoords: List[int], state):
        Up = [pieceCoords[0] - 1, pieceCoords[1]]
        UpLeft = [pieceCoords[0] - 1, pieceCoords[1] - 1]
        UpRight = [pieceCoords[0] - 1, pieceCoords[1] + 1]
        Down = [pieceCoords[0] + 1, pieceCoords[1]]
        DownLeft = [pieceCoords[0] + 1, pieceCoords[1] - 1]
        DownRight = [pieceCoords[0] + 1, pieceCoords[1] + 1]
        Left = [pieceCoords[0], pieceCoords[1] - 1]
        Right = [pieceCoords[0], pieceCoords[1] + 1]
        allMoves = [
            Up,
            UpRight,
            Right,
            DownRight,
            Down,
            DownLeft,
            Left,
            UpLeft,
        ]
        allValidMoves = []

        for coordinates in allMoves:
            if (
                coordinates[0] >= 0
                and coordinates[1] >= 0
                and coordinates[0] < state.board.rows
                and coordinates[1] < state.board.columns
            ):
                # never acount for the situation where you move to a square where one of your pieces are already there

                if state.hasObstacleAt(coordinates):
                    continue
                move = Move(
                    [pieceCoords[0], pieceCoords[1]],
                    [coordinates[0], coordinates[1]],
                )
                allValidMovesAppend = allValidMoves.append
                allValidMovesAppend(move)
        return allValidMoves


class Arc:
    def __init__(self, unplaced: Piece, placed: Piece):
        self.unplaced = unplaced
        self.placed = placed


class Board:
    def __init__(self):
        self.rows = None
        self.columns = None
        self.numObstacles = None
        self.matrix = []
        self.kValue = None

    def initialiseMatrix(
        self,
    ):  # This should only be called after the variables self.rows and self.columns have been set
        # Prepares matrix for subsequent operations to add step costs
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(None)
            self.matrix.append(row)

    def placeObstacles(self, arrOfChessNotation):
        for chessNotation in arrOfChessNotation:
            obstacleCoord = Board.convertChessNotationToCoordinates(chessNotation)
            self.matrix[obstacleCoord[0]][obstacleCoord[1]] = -1

    def generateEmptySpaces(self):
        emptySpaces = []
        for row in range(self.rows):
            for col in range(self.columns):
                if self.matrix[row][col] == 0:
                    emptySpacesAppend = emptySpaces.append
                    emptySpacesAppend((row, col))
        return emptySpaces

    def convertChessNotationToCoordinates(chess_notation):
        xCoord = (int)(chess_notation[1:])
        firstChar = chess_notation[0]
        yCoord = alphabetDict.get(
            firstChar, None
        )  # Get numeric representation of alphabet. Return None if not in alphabet dictionary.
        return [xCoord, yCoord]

    def convertCoordinatesToChessNotation(coords):
        xCoord = coords[0]
        yCoord = None
        for key in alphabetDict.keys():
            if alphabetDict[key] == coords[1]:
                yCoord = key
        chessNotation = (yCoord, xCoord)
        return chessNotation


class State:
    def __init__(self, pieces: List[Piece], board: Board):
        self.pieces = pieces
        self.board = board

    def hasObstacleAt(self, coordinates):
        hasObstacle = self.board.matrix[coordinates[0]][coordinates[1]] == -1
        return hasObstacle

    def createPiece(type, xCoord, yCoord):
        if type == "King":
            return King(xCoord, yCoord)
        elif type == "Queen":
            return Queen(xCoord, yCoord)
        elif type == "Bishop":
            return Bishop(xCoord, yCoord)
        elif type == "Rook":
            return Rook(xCoord, yCoord)
        elif type == "Knight":
            return Knight(xCoord, yCoord)
        else:
            return None

    def generateListOfThreatenedCoords(
        self, piecesPlacedDict: dict
    ):  # generates all coordinates under threat from existing pieces
        threatenedCoords = []
        for cId in piecesPlacedDict.keys():
            piece = self.findPieceWithId(cId)
            listOfMoves = piece.generateAllMoves(piecesPlacedDict[cId], self)
            listOfCoords = map(lambda x: x.endCoords, listOfMoves)
            threatenedCoords.extend(listOfCoords)
        return threatenedCoords

    def findPieceWithId(self, id: int):
        for piece in self.pieces:
            if piece.cId == id:
                return piece
        return None


class Node:  ## must keep track of nodes alr visited/piece coordinates already tested
    def __init__(
        self, piecesPlaced: dict, piecesRemaining: List[int], domainDict: dict
    ):
        self.piecesPlaced = piecesPlaced  # {3:(9,9), 4:(5,5)}
        self.piecesRemaining = piecesRemaining  # [1,2]
        self.domainDict = domainDict  # make sure that domain dict is updated when add a piece into pieces.placed
        # {1:[(1,2), (3,4)],  2:[(5,2), (5,5)]} tuples represent possible locations we can put

    def selectPieceToAssign(self, state: State):
        # Utilises the Degree heuristic. Choose Variable involved with most constraints on other unassigned variables
        # In this case, constraints are the squares that a piece can potentially threaten

        pieceToAssign = None
        listOfRemainingPieces = list(
            map(lambda x: state.findPieceWithId(x), self.piecesRemaining)
        )
        queens = list(filter(lambda x: x.type == "Queen", listOfRemainingPieces))
        if len(queens) != 0:
            pieceToAssign = queens[0]
            return pieceToAssign

        bishops = list(filter(lambda x: x.type == "Bishop", listOfRemainingPieces))
        if len(bishops) != 0:
            pieceToAssign = bishops[0]
            return pieceToAssign

        rooks = list(filter(lambda x: x.type == "Rook", listOfRemainingPieces))
        if len(rooks) != 0:
            pieceToAssign = rooks[0]
            return pieceToAssign

        kings = list(filter(lambda x: x.type == "King", listOfRemainingPieces))
        if len(kings) != 0:
            pieceToAssign = kings[0]
            return pieceToAssign

        knights = list(filter(lambda x: x.type == "Knight", listOfRemainingPieces))
        if len(knights) != 0:
            pieceToAssign = knights[0]
            return pieceToAssign

        return None

    def determineLocationOfPiece(self, piece: Piece):
        possibleLocations = self.domainDict[piece.cId]
        possibleLocations.reverse()

        for i in range(0, len(possibleLocations) - 5, 5):
            shuffledPortion = possibleLocations[i : i + 5]
            shuffle(shuffledPortion)
            possibleLocations[i : i + 5] = shuffledPortion  # overwrite the original

        return possibleLocations

    def revise(self, unplacedPiece: Piece, threatenedCoords):
        revised = False
        toRemove = []
        for coord in self.domainDict[unplacedPiece.cId]:
            if coord in threatenedCoords:
                toRemoveAppend = toRemove.append
                toRemoveAppend(coord)
                revised = True

        for coordToBeRemoved in toRemove:
            remov = self.domainDict[unplacedPiece.cId].remove
            remov(coordToBeRemoved)

        return revised

    def generateDict(self, state: State):
        dictionary = {}
        for cId in self.piecesPlaced.keys():
            coords = self.piecesPlaced[cId]
            chessNotation = Board.convertCoordinatesToChessNotation(coords)
            dictionary[chessNotation] = state.findPieceWithId(cId).type
        return dictionary

    def addToAssignment(self, pieceToAssign: Piece, location: tuple, state: State):
        self.piecesPlaced[pieceToAssign.cId] = location
        self.domainDict[pieceToAssign.cId] = [location]
        remov = self.piecesRemaining.remove
        remov(pieceToAssign.cId)

        hasNoInconsistencies = True

        placedPieceCoords = self.piecesPlaced[pieceToAssign.cId]
        listOfMoves = pieceToAssign.generateAllMoves(
            [placedPieceCoords[0], placedPieceCoords[1]], state
        )
        coordsThreatenedByPlacedPiece = list(
            map(lambda x: tuple(x.endCoords), listOfMoves)
        )

        # placement of this piece shld not threaten others on board
        for coord in self.piecesPlaced.values():
            if coord in coordsThreatenedByPlacedPiece:
                return False

        # The below is just to make sure that domains follow arc consistency between all unplaced and place pieces
        for remainingCid in self.piecesRemaining:
            if location in self.domainDict[remainingCid]:
                removLoc = self.domainDict[remainingCid].remove
                removLoc(location)

            self.revise(
                state.findPieceWithId(remainingCid),
                coordsThreatenedByPlacedPiece,
            )
            if len(self.domainDict[remainingCid]) == 0:
                hasNoInconsistencies = False

        return hasNoInconsistencies

    def removeFromAssignment(self, pieceToAssign: Piece, originalDomainDict: dict):
        del self.piecesPlaced[pieceToAssign.cId]
        appen = self.piecesRemaining.append
        appen(pieceToAssign.cId)
        self.domainDict = originalDomainDict


def search(node: Node, state: State):
    # Uses backtracking algorithm
    if len(node.piecesRemaining) == 0:
        return node

    pieceToAssign = node.selectPieceToAssign(state)  # select variable
    possibleLocationsOfPiece = node.determineLocationOfPiece(pieceToAssign)
    # selecting values to assign to var

    if possibleLocationsOfPiece is None:
        return None

    for location in possibleLocationsOfPiece:
        currentNode = Node(
            node.piecesPlaced.copy(),
            list(node.piecesRemaining),
            deepcopy(node.domainDict),
        )
        inferences = currentNode.addToAssignment(pieceToAssign, location, state)

        if inferences:
            result = search(currentNode, state)
            if result != None:
                return result
    return None


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1]  # Do not remove. This is your input testfile.
    state = parse(testfile)

    piecesPlaced = {}
    piecesRemaining = []
    domainDict = {}

    for piece in state.pieces:
        pieceId = piece.cId
        piecesRemaining.append(pieceId)
        domainDict[pieceId] = state.board.generateEmptySpaces()

    initialNode = Node(piecesPlaced, piecesRemaining, domainDict)

    goalNode = search(initialNode, state)
    goalDict = goalNode.generateDict(state)

    return goalDict  # Format to be returned


print(run_CSP())
