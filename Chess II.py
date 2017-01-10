import sys
import copy
import colorama
import random

colorama.init()

# Board Construction Function
def buildBoard():
    global mainBoard
    global outputBoard
    global castling
    mainBoard = {}
    outputBoard = {}

    for i in range(1, 9):
        for j in range(1, 9):
            squareName = i * 10 + j
            mainBoard[squareName] = 0

    placementSquares = [11, 21, 31, 41, 51, 61, 71, 81, 12, 22, 32, 42, 52, 62, 72, 82, 17, 27, 37, 47, 57, 67, 77, 87, 18, 28, 38, 48, 58, 68, 78, 88]
    placementPieces =  [14, 12, 13, 15, 16, 13, 12, 14, 11, 11, 11, 11, 11, 11, 11, 11, 21, 21, 21, 21, 21, 21, 21, 21, 24, 22, 23, 25, 26, 23, 22, 24]

    for i in range(0, len(placementSquares)):
        mainBoard[placementSquares[i]] = placementPieces[i]

    castling = {11 : True, 81 : True, 51 : True,
                18 : True, 88 : True, 58 : True}

def createListOfSquares():
    global listOfSquares
    listOfSquares = []
    for i in range(1, 9):
        for j in range(1, 9):
            listOfSquares.append(i * 10 + j)

# UI Representation of board data
pieceOutput = {21: "p", 22: "n", 23: "b", 24: "r", 25: "q", 26: "k",
               11: "P", 12: "N", 13: "B", 14: "R", 15: "Q", 16: "K",
               0: " "}

def king(position, board):
    availableMoves = []
    adjacentMoves = [1, 11, 10, 9, -1, -11, -10, -9]
    if board[position] < 17: # If the piece is white
        for i in range(0,8):
            try:
                if board[position + adjacentMoves[i]] == 0 or board[position + adjacentMoves[i]] > 17: # If the destination square is unoccupied or black
                    availableMoves.append(position + adjacentMoves[i])
                else:
                    pass
            except:
                pass
        if castling[51] and castling[11] and board[21] == 0 and board[31] == 0 and board[41] == 0 and board[58] == 16 and board[18] == 14: # If long castle is available
            availableMoves.append(31)
        else:
            pass
        if castling[51] and castling[81] and board[61] == 0 and board[71] == 0 and board[51] == 16 and board[81] == 14: # If short castling is available
            availableMoves.append(71)
        else:
            pass
    else: # If the piece is black

        for i in range(0,8):
            try:
                if board[position + adjacentMoves[i]] < 17: # If the destination square is unoccupied or white
                    availableMoves.append(position + adjacentMoves[i])
                else:
                    pass
            except:
                pass

        if castling[58] and castling[18] and board[28] == 0 and board[38] == 0 and board[48] == 0 and board[58] == 26 and board[18] == 24:  # If long castle is available
            availableMoves.append(38)
        else:
            pass
        if castling[58] and castling[88] and board[68] == 0 and board[78] == 0 and board[58] == 26 and board[88] == 24: # If short castling is available
            availableMoves.append(78)
        else:
            pass

    return(availableMoves)

def rook(position, board):
    availableMoves = []
    lattitude = position - (position//10)*10
    longitude = position//10
    higher = 8 - lattitude
    lower = lattitude - 1
    left = longitude - 1
    right = 8 - longitude

    for i in range(1, higher + 1):
        if board[position + i] == 0:
            availableMoves.append(position + i)
        elif board[position + i]//10 != board[position]//10:
            availableMoves.append(position + i)
            break
        else:
            break

    for i in range(1, lower + 1):
        if board[position - i] == 0:
            availableMoves.append(position - i)
        elif board[position - i] // 10 != board[position]//10:
            availableMoves.append(position - i)
            break
        else:
            break

    for i in range(1, right + 1):
        if board[position + i*10] == 0:
            availableMoves.append(position + i*10)
        elif board[position + i*10]//10 != board[position]//10:
            availableMoves.append(position + i*10)
            break
        else:
            break

    for i in range(1, left + 1):
        if board[position - i*10] == 0:
            availableMoves.append(position - i*10)
        elif board[position - i*10]//10 != board[position]//10:
            availableMoves.append(position - i*10)
            break
        else:
            break

    return(availableMoves)

def bishop(position, board):
    availableMoves = []

    # Moving upwards and leftwards
    for i in range(1, 8):
        try:
            if board[position - i * 9] == 0:
                availableMoves.append(position - i * 9)
            elif board[position - i * 9] // 10 != board[position] // 10:
                availableMoves.append(position - i * 9)
                break
            else:
                break
        except:
            break

    # Moving upwards and rightwards
    for i in range(1, 8):
        try:
            if board[position + i * 11] == 0:
                availableMoves.append(position + i * 11)
            elif board[position + i * 11] // 10 != board[position] // 10:
                availableMoves.append(position + i * 11)
                break
            else:
                break
        except:
            break

    # Moving downwards and leftwards
    for i in range(1, 8):
        try:
            if board[position - i * 11] == 0:
                availableMoves.append(position - i * 11)
            elif board[position - i * 11] // 10 != board[position] // 10:
                availableMoves.append(position - i * 11)
                break
            else:
                break
        except:
            break

    # Moving downwards and rightwards
    for i in range(1, 8):
        try:
            if board[position + i * 9] == 0:
                availableMoves.append(position + i * 9)
            elif board[position + i * 9] // 10 != board[position] // 10:
                availableMoves.append(position + i * 9)
                break
            else:
                break
        except:
            break

    return(availableMoves)

def knight(position, board):
    availableMoves = []
    adjacentMoves = [12, 21, 19, 8, -12, -21, -19, -8]
    if board[position] < 17: # If the piece is white
        for i in range(0,8):
            try:
                if board[position + adjacentMoves[i]] == 0 or board[position + adjacentMoves[i]] > 17: # If the destination square is unoccupied or black
                    availableMoves.append(position + adjacentMoves[i])
                else:
                    pass
            except:
                pass
    else: # If the piece is black

        for i in range(0,8):
            try:
                if board[position + adjacentMoves[i]] < 17: # If the destination square is unoccupied or white
                    availableMoves.append(position + adjacentMoves[i])
                else:
                    pass
            except:
                pass
    return(availableMoves)

def queen(position, board):
    availableMoves = bishop(position, board) + rook(position, board)
    return(availableMoves)

def pawn(position, board):
    availableMoves = []
    if board[position]//10 == 1: # Pawn is white
        try:
            if board[position + 1] == 0:
                availableMoves.append(position + 1)
            else:
                pass
        except:
            pass
        try:
            if board[position + 2] == 0 and board[position + 1] == 0 and position - (position//10)*10 == 2:
                availableMoves.append(position +2)
            else:
                pass
        except:
            pass
        try:
            if board[position + 11]//10 == 2:
                availableMoves.append(position + 11)
            else:
                pass
        except:
            pass
        try:
            if board[position - 9]//10 == 2:
                availableMoves.append(position - 9)
            else:
                pass
        except:
            pass

    else:  # Pawn is black
        try:
            if board[position - 1] == 0:
                availableMoves.append(position - 1)
            else:
                pass
        except:
            pass
        try:
            if board[position - 2] == 0 and board[position - 1] == 0 and position - (position // 10) * 10 == 7:
                availableMoves.append(position - 2)
            else:
                pass
        except:
            pass
        try:
            if board[position + 9] // 10 == 1:
                availableMoves.append(position + 9)
            else:
                pass
        except:
            pass
        try:
            if board[position - 11] // 10 == 1:
                availableMoves.append(position - 11)
            else:
                pass
        except:
            pass

    return(availableMoves)

def kingSafety(move, board):
    futureBoard = copy.deepcopy(board)
    moveFunction(move, futureBoard)
    inCheck = 0
    for i in range(1, 9):
        if inCheck == 1:
            break
        else:
            pass
        for j in range(1, 9):
            if inCheck == 1:
                break
            else:
                pass
            if futureBoard[i + j * 10] // 10 != board[move[0]] // 10 and futureBoard[i + j * 10] != 0:
                for k in range(0, len(pieceFunction[futureBoard[i + j * 10]](i + j * 10, futureBoard))):
                    if futureBoard[pieceFunction[futureBoard[i + j * 10]](i + j * 10, futureBoard)[k]] - ((futureBoard[pieceFunction[futureBoard[i + j * 10]](i + j * 10, futureBoard)[k]]) // 10) * 10 == 6:
                        inCheck = 1
                        #print(i + j * 10)
                        #print(pieceFunction[futureBoard[i + j * 10]](i + j * 10, futureBoard))
                        break
                    else:
                        pass
            else:
                pass
    if inCheck == 0:
        return(True)
    else:
        return(False)

def playerInCheck(board, whiteTurn):
    inCheck = 0
    if whiteTurn == 1:
        for i in range(1, 9):
            if inCheck == 1:
                break
            else:
                pass
            for j in range(1, 9):
                if inCheck == 1:
                    break
                else:
                    pass
                if board[i + j * 10] // 10 == 2 and board[i + j * 10] != 0:
                    for k in range(0, len(pieceFunction[board[i + j * 10]](i + j * 10, board))):
                        if board[pieceFunction[board[i + j * 10]](i + j * 10, board)[k]] == 16:
                            inCheck = 1
                            break
                        else:
                            pass
                else:
                    pass
    else:
        for i in range(1, 9):
            if inCheck == 1:
                break
            else:
                pass
            for j in range(1, 9):
                if inCheck == 1:
                    break
                else:
                    pass
                if board[i + j * 10] // 10 == 1 and board[i + j * 10] != 0:
                    for k in range(0, len(pieceFunction[board[i + j * 10]](i + j * 10, board))):
                        if board[pieceFunction[board[i + j * 10]](i + j * 10, board)[k]] == 16:
                            inCheck = 1
                            break
                        else:
                            pass
                else:
                    pass
    if inCheck == 1:
        return(True)
    else:
        return(False)

def nothing(move, board):
    return([])

def findMoves(board, whoseTurn):

    availableMoves = []

    for i in range(1, 9):
        for j in range(1, 9):
            if board[i + j * 10] // 10 == whoseTurn:
                for k in range(0, len(pieceFunction[board[i + j * 10]](i + j * 10, board))):
                    availableMoves.append(pieceFunction[board[i + j * 10]](i + j * 10, board)[k] + (i + j * 10)*100)
            else:
                pass
    return(availableMoves)

# Board data and corresponding piece functions
pieceFunction = {11 : pawn, 21 : pawn,
                 12 : knight, 22 : knight,
                 13 : bishop, 23 : bishop,
                 14 : rook, 24 : rook,
                 15 : queen, 25 : queen,
                 16 : king, 26 : king,
                 0 : nothing}


# Function for manipulating board data
def moveFunction(move, board):
    board[move[1]] = board[move[0]]
    board[move[0]] = 0

pieceEval = {21 : 1, 22 : 3, 23 : 3, 24 : 5, 25 : 9, 26 : 999,
             11 : -1, 12 : -3, 13 : -3, 14 : -5, 15 : -9, 16 : -999,
             0 : 0}

def computerMove(board):
    temp = [0, -9999]
    temp2 = []
    availableMoves = []
    for i in range(1, 9):
        for j in range(1, 9):
            if board[i + j * 10] != 0:
                availableMovesTo = pieceFunction[board[i + j * 10]](i + j * 10, board)
                for k in range(0, len(availableMovesTo)):
                    availableMoves.append([i + j * 10, availableMovesTo[k]])
            else:
                pass
    for i in range(0, len(availableMoves)):

        futureBoard = copy.deepcopy(mainBoard)
        computerOutput = availableMoves[i]

        if mainBoard[computerOutput[0]] > 20:  # Is the right colour moving?
            if computerOutput[1] in pieceFunction[mainBoard[computerOutput[0]]](computerOutput[0], mainBoard):  # Is the moved valid for the piece being moved?
                if kingSafety(computerOutput, mainBoard):  # Is the king safe?
                    moveFunction(computerOutput, futureBoard)
                    if boardEval(futureBoard) == temp[len(temp) - 1]:
                        temp.append(boardEval(futureBoard))
                        temp2.append(computerOutput)
                    elif boardEval(futureBoard) > temp[len(temp) - 1]:
                        temp = [boardEval(futureBoard)]
                        temp2 = [computerOutput]
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass

    return(temp2[random.randrange(0, len(temp2))])

def boardEval(board):
    evaluation = 0
    for i in range(1, 9):
        for j in range(1, 9):
            evaluation = evaluation + pieceEval[board[i + j * 10]]
    return(evaluation)

def checkMate(board, whiteTurn):

    inCheckmate = True

    availableMoves = []

    if whiteTurn == 1:
        for i in range(1, 9):
            for j in range(1, 9):
                if board[i + j * 10] != 0 and board[i + j * 10] // 10 == 1:
                    availableMovesTo = pieceFunction[board[i + j * 10]](i + j * 10, board)
                    for k in range(0, len(availableMovesTo)):
                        availableMoves.append([i + j * 10, availableMovesTo[k]])
                else:
                    pass

        for i in range(0, len(availableMoves)):
            if kingSafety(availableMoves[i], mainBoard):
                inCheckmate = False
                break
            else:
                pass

    else:
        for i in range(1, 9):
            for j in range(1, 9):
                if board[i + j * 10] != 0 and (board[i + j * 10] // 10) == 2:
                    availableMovesTo = pieceFunction[board[i + j * 10]](i + j * 10, board)
                    for k in range(0, len(availableMovesTo)):
                        availableMoves.append([i + j * 10, availableMovesTo[k]])
                else:
                    pass

        for i in range(0, len(availableMoves)):
            if kingSafety(availableMoves[i], mainBoard):
                inCheckmate = False
                break
            else:
                pass
    return(inCheckmate)

def printBoard(board):
    for i in range(1, 9):
        for j in range(1, 9):
            squareName = i * 10 + j
            outputBoard[squareName] = pieceOutput[board[squareName]]

    sys.stdout.write("\033[1;1H")
    sys.stdout.write("\033[0J")
    print("")
    print("             -- C H E S S --                 ")
    print("")
    print("     Turn: ")
    print("")
    print("       A   B   C   D   E   F   G   H")
    print("     ---------------------------------")
    print("   8 | " + outputBoard[18] + " | " + outputBoard[28] + " | " + outputBoard[38] + " | " + outputBoard[48] + " | " + outputBoard[58] + " | " + outputBoard[68] + " | " + outputBoard[78] + " | " + outputBoard[88] + " | 8")
    print("     ---------------------------------")
    print("   7 | " + outputBoard[17] + " | " + outputBoard[27] + " | " + outputBoard[37] + " | " + outputBoard[47] + " | " + outputBoard[57] + " | " + outputBoard[67] + " | " + outputBoard[77] + " | " + outputBoard[87] + " | 7")
    print("     ---------------------------------")
    print("   6 | " + outputBoard[16] + " | " + outputBoard[26] + " | " + outputBoard[36] + " | " + outputBoard[46] + " | " + outputBoard[56] + " | " + outputBoard[66] + " | " + outputBoard[76] + " | " + outputBoard[86] + " | 6")
    print("     ---------------------------------")
    print("   5 | " + outputBoard[15] + " | " + outputBoard[25] + " | " + outputBoard[35] + " | " + outputBoard[45] + " | " + outputBoard[55] + " | " + outputBoard[65] + " | " + outputBoard[75] + " | " + outputBoard[85] + " | 5")
    print("     ---------------------------------")
    print("   4 | " + outputBoard[14] + " | " + outputBoard[24] + " | " + outputBoard[34] + " | " + outputBoard[44] + " | " + outputBoard[54] + " | " + outputBoard[64] + " | " + outputBoard[74] + " | " + outputBoard[84] + " | 4")
    print("     ---------------------------------")
    print("   3 | " + outputBoard[13] + " | " + outputBoard[23] + " | " + outputBoard[33] + " | " + outputBoard[43] + " | " + outputBoard[53] + " | " + outputBoard[63] + " | " + outputBoard[73] + " | " + outputBoard[83] + " | 3")
    print("     ---------------------------------")
    print("   2 | " + outputBoard[12] + " | " + outputBoard[22] + " | " + outputBoard[32] + " | " + outputBoard[42] + " | " + outputBoard[52] + " | " + outputBoard[62] + " | " + outputBoard[72] + " | " + outputBoard[82] + " | 2")
    print("     ---------------------------------")
    print("   1 | " + outputBoard[11] + " | " + outputBoard[21] + " | " + outputBoard[31] + " | " + outputBoard[41] + " | " + outputBoard[51] + " | " + outputBoard[61] + " | " + outputBoard[71] + " | " + outputBoard[81] + " | 1")
    print("     ---------------------------------")
    print("       A   B   C   D   E   F   G   H")
    print("")

while True: # Game Loop

    createListOfSquares()
    buildBoard()
    whiteTurn = 1

    while True: # Board Loop

        while True: # Input Loop
            if whiteTurn == 1:
                print(findMoves(mainBoard, 1))
            else:
                print(findMoves(mainBoard, 2))
            printBoard(mainBoard)
            if checkMate(mainBoard, whiteTurn):
                input("CHECKMATE")
                userInput = "menu"
            else:
                if playerInCheck(mainBoard, whiteTurn):
                    if whiteTurn == 1:
                        print("In Check\n")
                        userInput = input("White to move: ").lower()
                    else:
                        print("In Check\n")
                        userInput = computerMove(mainBoard)
                else:
                    if whiteTurn == 1:
                        userInput = input("White to move: ").lower()
                    else:
                        userInput = computerMove(mainBoard)

            if userInput == "menu":
                while True:
                    sys.stdout.write("\033[1;1H")
                    sys.stdout.write("\033[0J")
                    print(" ")
                    print("             -- C H E S S --                 ")
                    print("    ------------------------------------ ")
                    print("                  MENU ")
                    print("")
                    print("    To exit game type:           'exit'")
                    print("    To start a new game, type:   'new'")
                    print("    To go back, type:            'back'")
                    print("    ------------------------------------ ")
                    print("")
                    action = input("    INPUT: ").lower()
                    if action != "exit" and action != "new" and action != "back":
                        print("  INVALID RESPONSE")
                        pass
                    else:
                        break
            else:
                action = None
                if whiteTurn == 1:
                    if len(userInput) == 5: # Is the input five characters long?
                        if 96 < ord(userInput[0]) < 105 and 48 < ord(userInput[1]) < 57 and ord(userInput[2]) == 32 and 96 < ord(userInput[3]) < 105 and 48 < ord(userInput[4]) < 57: # Does the input correspond to existing squares on the board?
                            move = [int(str(ord(userInput[0])-96) + userInput[1]), int(str(ord(userInput[3])-96) + userInput[4])]
                            if (mainBoard[move[0]] < 17 and whiteTurn == 1) or (mainBoard[move[0]] > 20 and whiteTurn == -1):  # Is the right colour moving?
                                if move[1] in pieceFunction[mainBoard[move[0]]](move[0], mainBoard):  # Is the moved valid for the piece being moved?
                                    if kingSafety(move, mainBoard):  # Is the king safe?
                                        moveFunction(move, mainBoard)
                                        if whiteTurn == 1:
                                            if move[0] == 51:
                                                castling[51] = False
                                            else:
                                                pass
                                            if move[0] == 11:
                                                castling[11] = False
                                            else:
                                                pass
                                            if move[0] == 81:
                                                castling[81] = False
                                            else:
                                                pass
                                        else:
                                            if move[0] == 58:
                                                castling[58] = False
                                            else:
                                                pass
                                            if move[0] == 18:
                                                castling[18] = False
                                            else:
                                                pass
                                            if move[0] == 88:
                                                castling[88] = False
                                            else:
                                                pass
                                        if move == [51, 31]:
                                            moveFunction([11, 41], mainBoard)
                                        else:
                                            pass
                                        if move == [51, 71]:
                                            moveFunction([81, 61], mainBoard)
                                        else:
                                            pass
                                        if move == [58, 38]:
                                            moveFunction([18, 48], mainBoard)
                                        else:
                                            pass
                                        if move == [58, 78]:
                                            moveFunction([88, 68], mainBoard)
                                        else:
                                            pass
                                        whiteTurn = whiteTurn * -1
                                    else:
                                        print("King Not Safe")
                                else:
                                    print("Invalid Input: Invalid Piece Move")
                            else:
                                print("Invalid Input: Wrong Colour")
                        else:
                            print("Invalid Input: Outside board limits")
                    else:
                        print("Invalid Input: Incorrect Syntax")
                else:
                    move = userInput
                    moveFunction(move, mainBoard)
                    if whiteTurn == 1:
                        if move[0] == 51:
                            castling[51] = False
                        else:
                            pass
                        if move[0] == 11:
                            castling[11] = False
                        else:
                            pass
                        if move[0] == 81:
                            castling[81] = False
                        else:
                            pass
                    else:
                        if move[0] == 58:
                            castling[58] = False
                        else:
                            pass
                        if move[0] == 18:
                            castling[18] = False
                        else:
                            pass
                        if move[0] == 88:
                            castling[88] = False
                        else:
                            pass
                    if move == [51, 31]:
                        moveFunction([11, 41], mainBoard)
                    else:
                        pass
                    if move == [51, 71]:
                        moveFunction([81, 61], mainBoard)
                    else:
                        pass
                    if move == [58, 38]:
                        moveFunction([18, 48], mainBoard)
                    else:
                        pass
                    if move == [58, 78]:
                        moveFunction([88, 68], mainBoard)
                    else:
                        pass
                    whiteTurn = whiteTurn * -1

            if action == "exit" or action == "new" or action == "back":
                break
            else:
                pass

        if action == "back":
            pass
        else:
            break

    if action == "new":
        pass
    else:
        break
