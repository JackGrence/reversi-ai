import time
import random
from reversi import *
from tree import tree


def main():
    rates1 = [16, -3, 0.2, 0, -3, -1, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0,
              1, 16, 320, 1, 1]
    start(rates1)


def start(rates1):
    new_round = game()

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
    ai_step = []
    while not new_round.game_over:
        if new_round.current_player == ai:
            if minimax is None:
                pos, minimax = reversi_ai(new_round, rates=rates1)
            else:
                print('steps:', steps)
                pos, minimax = reversi_ai(new_round, minimax, steps)
            steps.clear()
            ai_step.append(pos)
        else:
            print('ai steps: ', ai_step)
            ai_step.clear()
            cur_player = new_round.current_player
            pos = input('{} please put chess: '.format(cur_player))

        steps.append(pos)
        if not new_round.put_chess(pos):
            steps.pop()
        new_round.draw_board()
        print(hex(new_round.white) + ', ' + hex(new_round.black))
        new_round.get_who_win()


def reversi_ai(new_round, minimax=None, steps=None, rates=None):
    max_depth = 3
    choice_num = len(new_round.flips)

    if minimax is None:
        minimax = tree(max_depth, new_round, rates)
    else:
        steps = [new_round.str2pos(i) for i in steps]
        minimax.change_root(steps, max_depth)

    pos = minimax.root.choice
    try:
        print('AI: ', new_round.pos2str[pos])
    except:
        print('something error')
        minimax.print(minimax.root)
    if debug_print:
        minimax.print(minimax.root)
    return new_round.pos2str[pos], minimax


def random_ai(new_round):
    pos = random.choice(list(new_round.flips))
    return new_round.pos2str[pos]


if __name__ == "__main__":
    debug_print = False
    main()
