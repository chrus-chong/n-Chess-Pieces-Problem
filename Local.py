import sys

from random import randint
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

        if "K (Minimum number of pieces left in goal):" in line:
            if line.split(":")[1] == "-":
                continue
            kVal = (int)(line.split(":")[1])
            board.kValue = kVal

        if "Number of King, Queen, Bishop, Rook, Knight (space between):" in line:
            line = line.split(":")[1]
            arrOfPieceNumbers = line.split(" ")

            numKing = (int)(arrOfPieceNumbers[0])
            numQueen = (int)(arrOfPieceNumbers[1])
            numBishop = (int)(arrOfPieceNumbers[2])
            numRook = (int)(arrOfPieceNumbers[3])
            numKnight = (int)(arrOfPieceNumbers[4])

        if "Position of Pieces [Piece, Pos]:" in line:
            if line.split(":")[1] == "-":
                continue
            while True:
                line = file.readline()
                if not line:
                    endOfFile = True
                    break
                line = line[1:-2]  # Get rid of open and close brackets
                chessTypeChessNote = line.split(
                    ","
                )  # convert line into [chess_type, chess_notation]
                coordinates = Board.convertChessNotationToCoordinates(
                    chessTypeChessNote[1]
                )
                piece = State.createPiece(
                    chessTypeChessNote[0], coordinates[0], coordinates[1]
                )
                listOfPieces.append(piece)
            break

        if not line:
            endOfFile = True

    file.close()

    state = State(listOfPieces, board)
    state.numKing = numKing
    state.numQueen = numQueen
    state.numBishop = numBishop
    state.numRook = numRook
    state.numKnight = numKnight
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
            allLeftMoves.append(move)
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
            allRightMoves.append(move)
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
            allUpMoves.append(move)
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
            allDownMoves.append(move)
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
            allUpLeftMoves.append(move)
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
            allUpRightMoves.append(move)
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
            allDownLeftMoves.append(move)
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
            allDownRightMoves.append(move)
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
                allValidMoves.append(move)
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
            allLeftMoves.append(move)
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
            allRightMoves.append(move)
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
            allUpMoves.append(move)
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
            allDownMoves.append(move)
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
            allUpLeftMoves.append(move)
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
            allUpRightMoves.append(move)
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
            allDownLeftMoves.append(move)
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
            allDownRightMoves.append(move)
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
                allValidMoves.append(move)
        return allValidMoves


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

    def initialiseVisitedMatrix(self, rows, columns):
        # This should only be called after the variables self.rows and self.columns have been set
        # Prepares matrix for subsequent operations to track if the spot has been visited
        self.rows = rows
        self.columns = columns
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(False)
            self.matrix.append(row)

    def placeObstacles(self, arrOfChessNotation):
        for chessNotation in arrOfChessNotation:
            obstacleCoord = Board.convertChessNotationToCoordinates(chessNotation)
            self.matrix[obstacleCoord[0]][obstacleCoord[1]] = -1

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
        self.numKing = None
        self.numQueen = None
        self.numBishop = None
        self.numRook = None
        self.numKnight = None

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
        self, piecesRemaining
    ):  # generates all coordinates under threat from existing pieces
        threatenedCoords = []
        for piece in piecesRemaining:
            listOfMoves = piece.generateAllMoves(piece.coordinates, self)
            listOfCoords = map(lambda x: x.endCoords, listOfMoves)
            threatenedCoords.extend(listOfCoords)
        return threatenedCoords


class Node:  ## must keep track of nodes alr visited/piece coordinates already tested
    def __init__(self, pieces: List[Piece]):
        self.pieces = pieces  # List of remaining pieces for the current state. note that pieces attribute in State class only reflects initial state of pieces
        self.threatVal = (
            {}
        )  # Dictionary. Key is creationId, value is the sum of number of pieces that threaten and the number of pieces it threatens.
        self.threatValCreated = False

    def generateSuccessor(self, state: State):
        pieceToRemove = self.choosePieceToRemove(state)
        if pieceToRemove is None:
            return None
        newPieces = self.pieces.copy()
        newPieces.remove(pieceToRemove)
        successor = Node(newPieces)
        successor.generateThreatVals(state)  # generate threat vals on creation
        return successor

    def choosePieceToRemove(self, state: State):
        # look at all the remaining pieces. look at their threat val. select those with highest threat val. choose randomly amongst those
        # returns piece to remove. Else returns None.
        if len(self.pieces) <= state.board.kValue:
            return None
        listToRemove = []
        highestThreatVal = max(self.threatVal.values())
        for cId in self.threatVal.keys():
            if self.threatVal[cId] == highestThreatVal:
                pieceToRemove = self.findPieceWithId(cId)
                listToRemove.append(pieceToRemove)

        # len(listToRemove) == 0 should only happen when self.pieces has no more pieces/self.threatVal is empty
        if len(listToRemove) == 1:
            return listToRemove[0]

        chosenIndex = randint(0, len(listToRemove) - 1)
        return listToRemove[chosenIndex]

    def generateThreatVals(self, state: State):
        if self.threatValCreated:
            return False
        self.threatValCreated = True
        # for every piece. calculate the number of people that threaten you. then calculate the number of people that you threaten.
        threatenedCoords = state.generateListOfThreatenedCoords(self.pieces)
        for piece in self.pieces:
            numThreaten = 0
            numThreatened = 0
            listOfMoves = piece.generateAllMoves(piece.coordinates, state)
            listOfCoords = list(map(lambda x: x.endCoords, listOfMoves))
            for coords in threatenedCoords:
                if (
                    piece.coordinates[0] == coords[0]
                    and piece.coordinates[1] == coords[1]
                ):
                    numThreaten += 1
            for other in self.pieces:
                if piece.cId == other.cId:
                    continue
                if other.coordinates in listOfCoords:
                    numThreatened += 1
            self.threatVal[piece.cId] = numThreaten + numThreatened
        return True

    def isGoalNode(self, state: State):
        isGoal = True
        for cId in self.threatVal.keys():
            if self.threatVal[cId] != 0:
                isGoal = False
        return isGoal

    def findPieceWithId(self, id: int):
        for piece in self.pieces:
            if piece.cId == id:
                return piece
        return None

    def generateDict(self):
        dictionary = {}
        for piece in self.pieces:
            chessNotation = Board.convertCoordinatesToChessNotation(piece.coordinates)
            dictionary[chessNotation] = piece.type
        return dictionary


def randomRestarts(initialNode: Node, state: State):
    goalNode = None
    while goalNode == None:
        goalNode = search(initialNode, state)
    return goalNode


def search(initialNode: Node, state: State):
    current = initialNode
    while True:
        neighbour = current.generateSuccessor(state)
        if neighbour is None:
            break
        if neighbour.isGoalNode(state):
            return neighbour

        current = neighbour
    return None


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1]  # Do not remove. This is your input testfile.
    state = parse(testfile)
    initialNode = Node(state.pieces.copy())
    initialNode.generateThreatVals(state)
    goalNode = randomRestarts(initialNode, state)
    goalDict = goalNode.generateDict()
    return goalDict  # Format to be returned


print(run_local())
