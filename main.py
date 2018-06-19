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
    new_round = game(0x38003911a1403c, 0x3c04ffc6ee5e3c00, 'white')
    #new_round = game()

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

    minimax = None
    steps = []
    minimax2 = None
    steps2 = []
    while not new_round.game_over:
        if new_round.current_player == ai:
            if minimax is None:
                pos, minimax = reversi_ai(new_round)
            else:
                print('steps:', steps)
                pos, minimax = reversi_ai(new_round, minimax, steps)
            steps.clear()
        else:
            #if minimax2 is None:
            #    pos, minimax2 = reversi_ai(new_round)
            #else:
            #    print('steps:', steps)
            #    pos, minimax2 = reversi_ai(new_round, minimax2, steps2)
            steps2.clear()

            pos = input('{} please put chess: '.format(new_round.current_player))
            #pos = reversi_ai(new_round)
        steps.append(pos)
        steps2.append(pos)
        if not new_round.put_chess(pos):
            steps.pop()
            steps2.pop()
        new_round.draw_board()
        print(hex(new_round.white) + ', ' + hex(new_round.black))
        new_round.get_who_win()


def reversi_ai(new_round, minimax=None, steps=None):
    max_depth = 4
    choice_num = len(new_round.flips)

    if choice_num >= 10:
        max_depth = 2
    if choice_num >= 6:
        max_depth = 3

    if minimax is None:
        minimax = tree(max_depth, new_round)
    else:
        steps = [new_round.str2pos(i) for i in steps]
        minimax.change_root(steps, max_depth)
    #pos = random.choice(list(new_round.flips))
    #minimax.print(minimax.root)
    pos = minimax.root.choice
    try:
        print('AI: ', new_round.pos2str[pos])
    except:
        print('something error')
        minimax.print(minimax.root)
    if debug_print:
        minimax.print(minimax.root)
    return new_round.pos2str[pos], minimax


if __name__ == "__main__":
    debug_print = True
    main()
