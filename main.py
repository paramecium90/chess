from operator import le
from tkinter import *
from move_types import *
import copy


#  performs the castle changes
def castle(side, x):

    if side == "right":
        rookold = [x, 7]
        kingnew = [x, 6]
        rooknew = [x, 5]
    else:
        rookold = [x, 0]
        kingnew = [x, 2]
        rooknew = [x, 3]
    kingold = [x, 4]

    # reset old square color
    if (kingold[0] + kingold[1]) % 2 == 1:
        game.board[selected["x"]][selected["y"]].label.configure(
            background="black")
    else:
        game.board[selected["x"]][selected["y"]].label.configure(
            background="white")
    #move and reset
    # king
    reseted_piece = reset_piece(kingold[0], kingold[1], game.board)
    place_piece(kingnew[0], kingnew[1], reseted_piece, game.board)

    # rook
    reseted_piece = reset_piece(rookold[0], rookold[1], game.board)
    place_piece(rooknew[0], rooknew[1], reseted_piece, game.board)

# check if there is a checkmaete


def checkmate(player):
    print(pieces[player])
    # for every piece of the player trie every possible move to see if the king is still after check
    for piece in pieces[player]:
        for move in piece.available_squares(game.board):
            print(move)
            if blessing_of_kings(piece.x, piece.y, move[0], move[1], player):
                # you found one move and you return true
                return True
    # there is no available move
    print("checkmate")
    # reset the piece list

    checkmate_menu()
    return False


def restart_game(menu):
    selected = {
        "is_selected": False,
        "x": -1,
        "y": -1



    }
    pieces["black"].clear()
    pieces["white"].clear()
    game.set_board()
    set_pieces()
    game.current_player = "white"
    menu.destroy()


def checkmate_menu(dummie=None):
    print(pieces)
    menu = Frame(root, width=200, height=200, bg="red")
    menu.grid(row=0, column=0)

    restart = Button(menu, text="restart", height=5,
                     width=20, command=lambda: restart_game(menu))
    restart.grid(
        row=2, column=3, columnspan=2)
    end = Button(menu, text="quit", height=5, width=20,
                 command=root.destroy)
    end.grid(
        row=3, column=3, columnspan=2)


# checks if you can perfom castle, if you can it perfoms it
def can_castle(selx, sely, targetx, targety):
    # if you have selected the king
    if game.board[selected["x"]][selected["y"]].piece.type == "king":
        squares_under_attack = []
        # find pieces under attack
        player = game.change_player()
        for piece in pieces[player]:
            squares_under_attack = squares_under_attack + \
                piece.available_squares(game.board)
        player = game.change_player()

        # check the king was moved
        if game.board[selx][sely].has_moved == True:
            return False
        if selx == targetx:
            left_castle = [0, 1, 2]

            right_castle = [6, 7]
            if targety in left_castle:
                # if all X convert to O then you can castle
                checklist = ["X", "X", "X", "X"]
                # checks if the between squares are under free
                for y in range(3):

                    if game.board[selx][y+1].piece == "free":
                        print("not here")
                        checklist[y] = "O"
                # checks if the rook has moved
                if game.board[selx][0].has_moved == False:
                    checklist[3] = "O"
                # if on of the above is false you cant castl
                if "X" in checklist:
                    print(checklist)
                    return False
                else:
                    # checks it the squares you area about to castle are under attack
                    left_castle = [[selx, 1], [selx, 2], [selx, 3]]
                    for cell in left_castle:
                        if cell in squares_under_attack:
                            return False
                    print("castle left")
                    castle("left", selx)
                    return True
            # right casater
            elif targety in right_castle:
                # if all X convert to O then you can castle
                checklist = ["X", "X", "X"]
                # checks if the between squares are under free
                for y in range(2):
                    print(y)
                    print(game.board[selx][y+5].piece)
                    if game.board[selx][y+5].piece == "free":
                        checklist[y] = "O"
                # checks if the rook has moved
                if game.board[selx][7].has_moved == False:
                    checklist[2] = "O"
                # if on of the above is false you cant castle
                if "X" in checklist:
                    print(checklist)
                    return False
                else:
                    # checks it the squares you area about to castle are under attack
                    right_castle = [[selx, 5], [selx, 6]]
                    for cell in right_castle:
                        if cell in squares_under_attack:
                            return False
                    print("castle right")
                    castle("right", selx)
                    return True
    return False

# takes a square, checks if it free and appends the available squares list, if it is free it allows the searching process to continue, else it ends it


def is_free(x, y, color, available_squares, board):

    if board[x][y].piece == "free":
        available_squares.append([x, y])
        return True
    else:
        if color == board[x][y].piece.color:
            return False
        else:
            available_squares.append([x, y])
            return False

# if a pawn reaches the end it automaticaly promotes to a Queen


def promote(piece, x, y, old_x, old_y):
    # print(piece)
    if piece == "pawn":
        if x == 0 or x == 7:
            piece = place_piece(x, y, Queen(game.current_player), game.board)
            pieces[game.current_player].append(piece)
            game.board[old_x][old_y].piece = piece
            # remove pawn
            for i in range(len(pieces[game.current_player])):
                if old_x == pieces[game.current_player][i].x and old_y == pieces[game.current_player][i].y:
                    pieces[game.current_player].pop(i)
                    print(pieces[game.current_player])
                    break


def buttonfunction(e):
    # finds the clicked square
    for i in range(8):
        for j in range(8):
            if game.board[i][j].label == e.widget:
                # if you dont have a selected square it selects it
                if selected["is_selected"] == False:
                    if game.board[i][j].piece != "free":
                        # otan balw seira
                        if game.board[i][j].piece.color == game.current_player:
                            selected["x"] = i
                            selected["y"] = j
                            selected["is_selected"] = True
                            game.board[i][j].label.configure(bg="red")
                # if you have a square selected
                else:
                    # if the square you clicked is in the available moves
                    if [i, j] in game.board[selected["x"]][selected["y"]
                                                           ].piece.available_squares(game.board):
                        # check if the move is legal (king check)
                        if not blessing_of_kings(
                                selected["x"], selected["y"], i, j, game.current_player):
                            return 0
                        # backround color reset, very important to be done before the reasignments
                        if (selected["x"] + selected["y"]) % 2 == 1:
                            game.board[selected["x"]][selected["y"]].label.configure(
                                background="black")
                        else:

                            game.board[selected["x"]][selected["y"]].label.configure(
                                background="white")
                        # promote pawn
                        promote(game.board[selected["x"]]
                                [selected["y"]].piece.type, i, j, selected["x"], selected["y"])

                        # reset old square
                        reseted_piece = reset_piece(
                            selected["x"], selected["y"], game.board)
                        game.board[selected["x"]
                                   ][selected["y"]].has_moved = True

                        # move piece
                        place_piece(i, j, reseted_piece, game.board)
                        # update piece list
                        update_pieces(
                            selected["x"], selected["y"], i, j, game.current_player)
                        selected["is_selected"] = False
                        # check for check
                        check(game.current_player)
                        game.change_player()
                        checkmate(game.current_player)
                    # if it is not in the available squares is check fo castle
                    else:

                        print("cant go there")
                        can_castle(selected["x"], selected["y"], i, j)

# unselects the square


def rightclick(e):
    selected["is_selected"] = False
    # remove red background
    i = selected["x"]
    j = selected["y"]
    # only for the first turn where nothing is selected
    if i == -1:
        return 0
    if (i + j) % 2 == 1:
        game.board[i][j].label.configure(background="black")
    else:
        game.board[i][j].label.configure(background="white")


class Pawn:
    def __init__(self, color):
        self.color = color
        self.x = None
        self.y = None
        self.type = "pawn"
        self.img = PhotoImage(file=f'img/{color}_pawn.png')

    def available_squares(self, board):
        available_squares = []
        if self.color == "black":
            # if free you can move 1 step forward
            if game.board[self.x+1][self.y].piece == "free":
                available_squares.append([self.x+1, self.y])
                # if you are in the starting position you can move 2 steps
                if self.x == 1:
                    if game.board[self.x+2][self.y].piece == "free":
                        available_squares.append([self.x+2, self.y])
            # side attacks
            if self.y-1 >= 0 and game.board[self.x+1][self.y-1].piece != "free":
                if game.board[self.x+1][self.y-1].piece.color == "white":
                    available_squares.append([self.x+1, self.y-1])
            if self.y+1 < 8 and game.board[self.x+1][self.y+1].piece != "free":
                if game.board[self.x+1][self.y+1].piece.color == "white":
                    available_squares.append([self.x+1, self.y+1])
        elif self.color == "white":
            # if free you can move 1 step forward
            if game.board[self.x-1][self.y].piece == "free":
                available_squares = [[self.x-1, self.y]]
                # if you are in the starting position you can move 2 steps
                if self.x == 6:
                    if game.board[self.x-2][self.y].piece == "free":
                        available_squares.append([self.x-2, self.y])
            # side attacks
            if self.y-1 >= 0 and game.board[self.x-1][self.y-1].piece != "free":
                if game.board[self.x-1][self.y-1].piece.color == "black":
                    available_squares.append([self.x-1, self.y-1])
            if self.y+1 < 8 and game.board[self.x-1][self.y+1].piece != "free":
                if game.board[self.x-1][self.y+1].piece.color == "black":
                    available_squares.append([self.x-1, self.y+1])

        return available_squares

    # pawn attacks is usefull to find which squares are under attack
    def pawn_attacks(self):

        if self.color == "black":
            attacks = [[self.x+1, self.y-1], [self.x+1, self.y+1]]
        elif self.color == "white":
            attacks = [[self.x-1, self.y-1], [self.x-1, self.y+1]]

        return attacks


class Rook:
    def __init__(self, color):
        self.color = color
        self.x = None
        self.y = None
        self.type = "rook"
        self.img = PhotoImage(file=f'img/{color}_rook.png')

    def available_squares(self, board):
        available_squares = []
        straight_paths = move_straight_cells(self.x, self.y)
        for path_direction in straight_paths:
            for square in path_direction:
                if is_free(square[0], square[1], self.color, available_squares, board):
                    pass
                else:
                    break
        return available_squares


class Knight:
    def __init__(self, color):
        self.color = color
        self.x = None
        self.y = None
        self.type = "knight"
        self.img = PhotoImage(file=f'img/{color}_knight.png')

    def available_squares(self, board):

        available_squares = []
        squares = move_knight_cells(self.x, self.y)
        for square in squares:
            is_free(square[0], square[1], self.color,
                    available_squares, board)

        return available_squares


class Bishop:
    def __init__(self, color):
        self.color = color
        self.x = None
        self.y = None
        self.type = "bishop"
        self.img = PhotoImage(file=f'img/{color}_bishop.png')

    def available_squares(self, board):
        available_squares = []
        diagonal_paths = move_diagonaly_cells(self.x, self.y)
        for path_direction in diagonal_paths:
            for square in path_direction:
                if is_free(square[0], square[1], self.color, available_squares, board):
                    pass
                else:
                    break
        return available_squares


class Queen:
    def __init__(self, color):
        self.color = color
        self.x = None
        self.y = None
        self.type = "queen"
        self.img = PhotoImage(file=f'img/{color}_queen.png')

    def available_squares(self, board):
        available_squares = []
        straight_paths = move_straight_cells(self.x, self.y)
        diagonal_paths = move_diagonaly_cells(self.x, self.y)
        for path_direction in straight_paths:
            for square in path_direction:
                if is_free(square[0], square[1], self.color, available_squares, board):
                    pass
                else:
                    break
        for path_direction in diagonal_paths:
            for square in path_direction:
                if is_free(square[0], square[1], self.color, available_squares, board):
                    pass
                else:
                    break
        return available_squares


class King:
    def __init__(self, color):
        self.color = color
        self.x = None
        self.y = None
        self.type = "king"
        self.img = PhotoImage(file=f'img/{color}_king.png')

    def available_squares(self, board):

        available_squares = []
        squares = move_king_cells(self.x, self.y)
        for square in squares:
            is_free(square[0], square[1], self.color,
                    available_squares, board)

        return available_squares


def open_menu():
    menu = Frame(root, width=200, height=200, bg="red")
    menu.grid(row=0, column=0)
    piece = None

    start = Button(menu, text="Queen", height=5,
                   width=20, command=lambda: "queen")
    start.grid(
        row=2, column=3, columnspan=2)
    print(start
          )
    end = Button(menu, text="Rook", height=5, width=20)
    end.grid(
        row=3, column=3, columnspan=2)
    start = Button(menu, text="Bishop", height=5, width=20)
    start.grid(
        row=2, column=3, columnspan=2)
    end = Button(menu, text="Knight", height=5, width=20)
    end.grid(
        row=3, column=3, columnspan=2)


def promote_menu(piece, x, y, old_x, old_y):

    menu = Frame(root, width=200, height=200, bg="red")
    menu.grid(row=0, column=0)
    piece = None

    start = Button(menu, text="Queen", height=5,
                   width=20)
    start.grid(
        row=2, column=3, columnspan=2)
    end = Button(menu, text="Rook", height=5, width=20)
    end.grid(
        row=3, column=3, columnspan=2)
    start = Button(menu, text="Bishop", height=5, width=20)
    start.grid(
        row=4, column=3, columnspan=2)
    end = Button(menu, text="Knight", height=5, width=20)
    end.grid(

        row=5, column=3, columnspan=2)


class Game:

    current_player = "white"
    board = [[i for i in range(8)] for j in range(8)]
    # creates a black and white board

    def set_board(self):
        for i in range(8):
            for j in range(8):
                if (i+j) % 2 == 1:
                    color = "black"
                else:
                    color = "white"
                self.board[i][j] = Cell(i, j, color)

    # changes the current player
    def change_player(self):
        if self.current_player == "white":
            self.current_player = "black"
        else:
            self.current_player = "white"
        return(self.current_player)

# cells are the squares of the chessboards it contains the images and information about the pieces on them also the buttonfunctions


class Cell:
    def __init__(self, x, y, color="white"):
        self.x = x
        self.y = y
        self.has_moved = False
        self.img = None
        self.piece = "free"
        piece_pic = PhotoImage(file='img/black.png')
        self.label = Label(frame, bg=color, height=100,
                           width=100, image=piece_pic)
        self.label.grid(row=x, column=y)

        self.label.bind("<Button-1>", buttonfunction)
        self.label.bind("<Button-3>", rightclick)


# temp_cell is the simple version of Cell used only to temp boards which are used to check if the king is under attack if a move is perfomed
class temp_Cell:
    def __init__(self, x, y, color="white"):
        self.x = x
        self.y = y
        self.piece = "free"


# removes dead pieces after a move
def update_pieces(old_x, old_y, new_x, new_y, player):
    player = game.change_player()
    for i in range(len(pieces[player])):
        if new_x == pieces[player][i].x and new_y == pieces[player][i].y:
            pieces[player].pop(i)
            break
    player = game.change_player()


# def reset_cell
def reset_piece(x, y, board):
    piece = board[x][y].piece
    board[x][y].piece = "free"
    try:
        img = PhotoImage(file=f'img/black_king.png')
        board[x][y].label.configure(image=img, height=100,
                                    width=100)
    except:
        print("expect in reset")
    return piece


def place_piece(x, y, piece, board):
    piece.x = x
    piece.y = y
    board[x][y].piece = piece
    try:
        board[x][y].img = piece.img
        board[x][y].label.configure(image=board[x][y].img, height=100,
                                    width=100)
    except:
        pass
    return piece


def set_pieces():

    # pawns
    for i in range(0, 8):

        pieces["black"].append(place_piece(1, i, Pawn("black"), game.board))
        pieces["white"].append(place_piece(6, i, Pawn("white"), game.board))

    pieces["white"].append(place_piece(7, 3, Queen("white"), game.board))
    pieces["black"].append(place_piece(0, 3, Queen("black"), game.board))

    pieces["white"].append(place_piece(7, 7, Rook("white"), game.board))
    pieces["white"].append(place_piece(7, 0, Rook("white"), game.board))
    pieces["black"].append(place_piece(0, 7, Rook("black"), game.board))
    pieces["black"].append(place_piece(0, 0, Rook("black"), game.board))

    pieces["white"].append(place_piece(7, 2, Bishop("white"), game.board))
    pieces["white"].append(place_piece(7, 5, Bishop("white"), game.board))
    pieces["black"].append(place_piece(0, 2, Bishop("black"), game.board))
    pieces["black"].append(place_piece(0, 5, Bishop("black"), game.board))

    pieces["white"].append(place_piece(7, 1, Knight("white"), game.board))
    pieces["white"].append(place_piece(7, 6, Knight("white"), game.board))
    pieces["black"].append(place_piece(0, 1, Knight("black"), game.board))
    pieces["black"].append(place_piece(0, 6, Knight("black"), game.board))

    pieces["white"].append(place_piece(7, 4, King("white"), game.board))
    pieces["black"].append(place_piece(0, 4, King("black"), game.board))


def blessing_of_kings(x_old, y_old, x_new, y_new, player):
    temp_board = [[temp_Cell(0, 0)
                   for n in range(8)] for m in range(8)]
    # print(temp_board[1][1].x)
    # create a temp board
    for i in range(8):
        for j in range(8):

            if game.board[i][j].piece != "free":
                temp_board[i][j].piece = copy.copy(game.board[i][j].piece)
                temp_board[i][j].piece.x = game.board[i][j].piece.x
                temp_board[i][j].piece.y = game.board[i][j].piece.y
                temp_board[i][j].piece.type = game.board[i][j].piece.type
                temp_board[i][j].piece.color = game.board[i][j].piece.color
    # perfom the move in the temp board
    reseted_piece = reset_piece(
        x_old, y_old, temp_board)
    place_piece(x_new, y_new, reseted_piece, temp_board)
    # find the new king possition in the temp board
    for row in temp_board:
        for cell in row:
            if cell.piece != "free":
                if cell.piece.type == "king" and cell.piece.color == player:

                    king_cords = [cell.piece.x, cell.piece.y]
                    # print("temp king")
                    # print(king_cords)

    # find the squares under attack in the temp board
    player = game.change_player()
    squares_under_attack = []
    for piece in pieces[player]:
        # pawns attack differently than they move
        if piece.type == "pawn":
            squares_under_attack = squares_under_attack + \
                piece.pawn_attacks()
        else:
            squares_under_attack = squares_under_attack + \
                piece.available_squares(temp_board)
    # print(squares_under_attack)

    player = game.change_player()

    if king_cords in squares_under_attack:
        print("suicide")
        return False

    return True

# checks if king is under attack


def check(player):
    squares_under_attack = []
    for piece in pieces[player]:
        squares_under_attack = squares_under_attack + \
            piece.available_squares(game.board)
    player = game.change_player()

    for piece in pieces[player]:
        if piece.type == "king":
            enemy_king_cords = [piece.x, piece.y]

    if enemy_king_cords in squares_under_attack:
        print("enemy checks")
        game.board[enemy_king_cords[0]][enemy_king_cords[1]
                                        ].label.configure(bg="red")

    game.change_player()
    pass


pieces = {"black": [], "white": []}

selected = {
    "is_selected": False,
    "x": -1,
    "y": -1


}


root = Tk()

frame = Frame(root)
frame.grid(row=0, column=0)
root.bind('<Escape>', checkmate_menu)

game = Game()
game.set_board()
set_pieces()


# open_menu()

root.mainloop()
