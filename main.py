import time
import random
from reversi import *
from tree import tree


def main():
    start()


def start():
    steps = 'f5d6c5f6e6b4c6b6d7f4d3c8a6b5d8e8e7f8c7c3f7e3g6a5a4h6h5h4g5g8a3c4g3f3g4h3c2b3d2f2f1e1d1e2b7c1b1a8b8'
    steps = 'e6f6c4e3f5f4f3d3c3d2d1c1b1c2e1e2f1f2g1c6g4g5d6h3h5g3g6c7b6a5c8d8e8d7e7f8g8f7b8b5c5b3a7b4a3a4a6b2h4h6g2h1h2a1g7h8h7a8a2b7'
    steps = ''
    #new_round = game(0x1002000007, 0x81c0e0700, 'white')
    new_round = game()

    for i in range(0, len(steps), 2):
        new_round.draw_board()
        new_round.put_chess(steps[i:i+2])
        time.sleep(0.2)

    choose = input("AI is (1)offensive (2)defensive")
    invalid_input = True
    while invalid_input:
        if len(choose) >= 1:
            ai = 'black' if choose[0] == '1' else 'white'
            invalid_input = False
            break
        choose = input("AI is (1)offensive (2)defensive")

    new_round.draw_board()

    while not new_round.game_over:
        if new_round.current_player == ai:
            pos = reversi_ai(new_round)
        else:
            pos = input('{} please put chess: '.format(new_round.current_player))
            #pos = reversi_ai(new_round)
        new_round.put_chess(pos)
        new_round.draw_board()
        print(hex(new_round.white), hex(new_round.black))
        new_round.get_who_win()


def reversi_ai(new_round):
    max_depth = 4
    minimax = tree(max_depth, new_round)
    #pos = random.choice(list(new_round.flips))
    pos = minimax.root.choice
    print('AI: ', new_round.pos2str[pos])
    del minimax
    return new_round.pos2str[pos]


if __name__ == "__main__":
    main()
