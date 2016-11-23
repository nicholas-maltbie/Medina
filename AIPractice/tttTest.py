from ttt import *

def play_game(agent1, agent2, name1, name2):
    """Plays a game of tic tac toe with two agents and returns the winner."""
    board = make_board()
    names = [name1, name2]
    players = [agent1, agent2]
    pieces = [-1,1]
    current = random.randint(0,1)

    while check_winner(board) == None:
        print(get_board_as_numbers(board, pieces[current], pieces[(current + 1) % 2]))
        move = players[current](board, pieces[current])
        apply_move(board, move)
        current = (current + 1) % 2
    win = check_winner(board)
    if win == 'o':
        return name2
    elif win == 'x':
        return name1
    else:
        return 'tie'

if __name__ == "__main__":
    distrib = {'player1':0, 'player2':0, 'tie':0}
    plays = 1
    for i in range(plays):
        distrib[play_game(make_random_agent(), make_human_agent(), \
                'player1', 'player2')] += 1;
    print('player1 won ' + str(distrib['player1']) + ' times ' + \
            str(int(distrib['player1'] / plays * 100)) + "%")
    print('player2 won ' + str(distrib['player2']) + ' times ' + \
            str(int(distrib['player2'] / plays * 100)) + "%")
    print('tied        ' + str(distrib['tie']) + ' times ' + \
            str(int(distrib['tie'] / plays * 100)) + "%")
