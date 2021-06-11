import requests

a = requests.api

# ------Global Variables

list = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

board = ["-", "-", "-",
         "-", "-", "-",
         "-", "-", "-"]

# If game still going

game_still_going = True

winner = None

curent_player = 'x'


def display_board():
    print(board[0] + "|" + board[1] + "|" + board[2])
    print(board[3] + "|" + board[4] + "|" + board[5])
    print(board[6] + "|" + board[7] + "|" + board[8])


def play_game():
    display_board()

    while game_still_going:

        handle_turn(curent_player)

        check_if_game_over()

        flip_player()

    if winner == 'x' or winner == 'o':
        print(winner + ' won')
    elif winner == None:
        print("tie")


def handle_turn(player):

    print(player + "'s turn")
    position = input("Choose a pos from 1 to 9: ")

    valid = False
    while not valid:

        while position not in list:
            position = input("Invalid input.Choose a pos from 1 to 9: ")

        position = int(position) - 1

        if board[position] == "-":
            valid = True
        else:
            print('You cannot go there')

    board[position] = player
    display_board()


def check_if_game_over():
    check_if_win()
    check_if_tie()


def check_if_win():
    global winner
    row_winner = check_rows()
    col_winner = check_col()
    diog_winner = check_diog()
    if row_winner:
        winner = row_winner
    elif col_winner:
        winner = col_winner
    elif diog_winner:
        winner = diog_winner
    else:
        winner = None
    return


def check_rows():
    global game_still_going
    row_1 = board[0] == board[1] == board[2] != '-'
    row_2 = board[3] == board[4] == board[5] != '-'
    row_3 = board[6] == board[7] == board[8] != '-'

    if row_1 or row_2 or row_3:
        game_still_going = False
    if row_1:
        return board[0]
    elif row_2:
        board[3]
    elif row_3:
        board[6]
    return


def check_col():
    global game_still_going
    col_1 = board[0] == board[3] == board[6] != '-'
    col_2 = board[1] == board[4] == board[7] != '-'
    col_3 = board[2] == board[5] == board[8] != '-'

    if col_1 or col_2 or col_3:
        game_still_going = False
    if col_1:
        return board[0]
    elif col_2:
        board[1]
    elif col_3:
        board[2]
    return


def check_diog():
    global game_still_going
    diog_1 = board[0] == board[4] == board[8] != '-'
    diog_2 = board[2] == board[4] == board[6] != '-'

    if diog_1 or diog_2:
        game_still_going = False
    if diog_1:
        return board[0]
    elif diog_2:
        board[2]
    return


def check_if_tie():
    global game_still_going
    if '-' not in board:
        game_still_going = False
    return


def flip_player():
    global curent_player
    if curent_player == 'x':
        curent_player = 'o'
    elif curent_player == 'o':
        curent_player = 'x'
    return


play_game()
