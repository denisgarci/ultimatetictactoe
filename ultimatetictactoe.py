from itertools import product

def ask(board):
    """ Return a correct move else raise a ValueError. """
    authorized_moves = product(range(3), range(3))
    pair = raw_input('(a pair of numbers between 1 and 3 separated by a comma):')
    pair = pair.split(',')
    try:
        pair = (int(pair[0]) - 1, int(pair[1]) - 1) # Pair between 0 and 2 and player will be between 1 and 3
    except:
        raise ValueError('{0} is not a correct input'.format(','.join(pair)))
    if pair not in authorized_moves:
        raise ValueError('({0}, {1}) is out of bounds.'.format(pair[0] + 1, pair[1] + 1))
    elif pair in board:
        raise ValueError('({0}, {1}) was already played.'.format(pair[0] + 1, pair[1] + 1))
    else:
        return pair

def draw_small(small_board, numbers=False):
    """
    Returns a list of strings representing each small_board lines.
    If number is True, coordinate are added at the beginning of each line.
    Loop left to right starting in the top left corner.
    """
    lines = []
    for j in range(2, -1, -1):
        draw_line = ''
        if numbers:
            draw_line += str(j + 1) + ' '
        for i in range(3):
            cell = small_board.get((i,j), 0)
            if cell == 0:
                draw_line += '.'
            elif cell == 1:
                draw_line += 'X'
            elif cell == 2:
                draw_line += 'O'
            draw_line += ' '
        lines.append(draw_line)
    if numbers:
        lines.append('  1 2 3')
    return lines


def draw_big(big_board, big_board_status):
    """
    Draw the big_board directly calling print statements.
    The drawing is made 3 lines at a time. This function is a bit hackish but doing ASCII by hand is not very fun ^ ^
    The following signs are used to help the players:
    if player 1 wins one of the small boards, a big X is drawn instead of the actual small board.
    if player 2 wins one of the small boards, a big O is drawn instead of the actual small board.
    if a small board is draw it will be shown as a board filled with '*'.
    """
    print('  ____________________')
    for j in range(2, -1, -1):
        line0 = '|'
        line1 = '|'
        line2 = '|'
        for i in range(3):
            # Drawing sugar in case a board is won are stale
            if (i,j) in big_board_status:
                if big_board_status[(i,j)] == 0:
                    line0 += '* * * |'
                    line1 += '* * * |'
                    line2 += '* * * |'
                elif big_board_status[(i,j)] == 1:
                    line0 += 'X   X |'
                    line1 += '  X   |'
                    line2 += 'X   X |'
                elif big_board_status[(i,j)] == 2:
                    line0 += ' OOO  |'
                    line1 += 'O   O |'
                    line2 += ' OOO  |'
            else:
                line0 += draw_small(big_board[(i,j)])[0] + '|'
                line1 += draw_small(big_board[(i,j)])[1] + '|'
                line2 += draw_small(big_board[(i,j)])[2] + '|'
        print(' ' + line0)
        print(str(j + 1) + line1)
        print(' ' + line2)
        if j == 0:
            print(' |______|______|______|')
            print('    1      2      3')
        else:
            print(' |______|______|______|')


def rows(board):
    """
    Generator used in end_game, return first horizontal
    then vertical and finaly the diagonal rows.
    """
    for k in range(3):
        row_k = [board.get((i, k), 0) for i in range(3)]
        yield row_k
    for k in range(3):
        col_k = [board.get((k,j), 0) for j in range(3)]
        yield col_k
    dia1 = [board.get((i,i), 0) for i in range(3)]
    yield dia1
    dia2 = [board.get((i,2 - i), 0) for i in range(3)]
    yield dia2


def end_game(board):
    """
    Check if the game has ended. Return a pair (bool, int) where bool is
    True if game has ended and int is the winner's number, 0 if it is a draw.
    This function can be improved due to the Ultimate Tic-tac-toe particularities.
    For example if one of the diagonals is full of 0 (meaning a draw in each diagonals small boards)
    the game is over and it is a draw. Unfortunately I didn't have time to implement it.
    """
    # The value 3 here is because is Ultimate Tic-tac-toe, a player can play multiple times
    # in the same board without alternating with the other player
    if len(board) < 3:
        return (False, 0)
    else:
        for row in rows(board):
            if 0 in row:
                continue
            elif sum(row) == 3:
                return (True, 1)
            elif sum(row) == 6:
                return (True, 2)
        else:
            # Draw condition: the board is full and no one won
            if len(board) == 9:
                return (True, 0)
            else:
                return (False, 0)


def playgame():
    # Initialization of the game variables
    # Dictionary of dictionary index by pair representing each small_board
    big_board = {(i,j): {} for (i,j) in product(range(3), range(3))}
    # Dictionary no key if the game is still going on, 0 if game has ended in a stale,s and 1/2 if player 1/2 won the sub board (i,j)
    big_board_status = {}
    player = 1
    last_move = None
    # Welcome Screen
    print('Welcome in Ultimate Tic-tac-toe.')
    print('1. Each turn you make a move in one of the small boards.')
    print('2. When you get three in a row on a small board, you win that board.')
    print('3. To win the game, you need to win three small boards in a row.')
    print("4. Each player's next small board is determined by the coordinate of the previous player's move")
    print('For more information check: http://mathwithbaddrawings.com/2013/06/16/ultimate-tic-tac-toe/')
    # Game Loop
    while True:
        # Draw
        draw_big(big_board, big_board_status)
        # Ask for a small board if first turn or player sent to an already won board
        print('Player {0} is playing.'.format(player))
        if last_move in big_board_status or last_move == None:
            try:
                print 'Enter the coordinates of the small board where you will play next',
                last_move = ask(big_board_status)
            except ValueError as e:
                print('Enter a valid board. {0}'.format(e))
                continue
        # Update small_board and draw it
        small_board = big_board[last_move]
        print('You are playing in board ({0}, {1}): '.format(last_move[0] + 1, last_move[1] + 1))
        print('\n'.join(draw_small(small_board, True)))
        # Ask for a move
        try:
            print 'Enter the coordinates for your next move',
            move = ask(small_board)
        except ValueError as e:
            print('Enter a valid move. {0}'.format(e))
            continue
        # Update small_board
        small_board[move] = player
        # Check for won sub board
        (end, winner) = end_game(small_board)
        if end:
            print('Player {0} won board ({1}, {2}).'.format(winner, last_move[0] + 1, last_move[1] + 1))
            big_board_status[last_move] = winner
        # Check for end game
        (end, winner) = end_game(big_board_status)
        if end:
            draw_big(big_board, big_board_status)
            if winner == 0:
                print("Draw -_-'")
                break
            else:
                print('Player {0} wins!'.format(winner))
                break
        # Switch players, update last_move
        if player == 1:
            player = 2
        else:
            player = 1
        last_move = move

if __name__ == '__main__':
    playgame()
