import time
import random
from reversi import *
from tree import tree


def main():
    rates1 = [16.493296738018056, -2.883624559019017, -0.27522495676101005, 0.24883482375458854, -2.7879166342218102, -1.391894894844652, 0.21414223978775704, 0.24830969644457324, -0.2334222387914518, -0.31967043862508016, 0.36357947338445984, -0.0222878608526188, -0.4544234865629029, 0.4828408390965292, 0.11960137082476496, -0.10509588244347134, 0.9913504129076625, 15.894398655071832, 1]
    rates1 = [16.33123068189905, -3.2920875509957725, -0.38444733220037886, -0.6300235883304337, -3.343574148918484, -1.4671741087078969, -0.46881555015335474, -0.475367875420275, 0.01954970778676013, 0.03708781001044134, -0.2626206937637492, 0.1158889767977537, 0.5151706240343635, 0.22689806371290938, -0.19201568890432022, 0.7489962131422395, 2.0275209495931046, 16.027022677375243, 0.8088093387019347]
    rates1 = [16, -3, 0.2, 0, -3, -1, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0, 1, 16, 320, 1, 1.2814302601478789]
    rates2 = [16, -3, 0.2, 0, -3, -1, 0, 0, 0.2, 0, 0, 0, 0, 0, 0, 0, 1, 16, 1, 1, 1.2814302601478789]
    start(rates1, rates2)


def start(rates1, rates2):
    steps = 'f5d6c5f6e6b4c6b6d7f4d3c8a6b5d8e8e7f8c7c3f7e3g6a5a4h6h5h4g5g8a3c4g3f3g4h3c2b3d2f2f1e1d1e2b7c1b1a8b8'
    steps = 'e6f6c4e3f5f4f3d3c3d2d1c1b1c2e1e2f1f2g1c6g4g5d6h3h5g3g6c7b6a5c8d8e8d7e7f8g8f7b8b5c5b3a7b4a3a4a6b2h4h6g2h1h2a1g7h8h7a8a2b7'
    steps = ''
    new_round = game(0x38003911a1403c, 0x3c04ffc6ee5e3c00, 'white')
    new_round = game(0x7c3470e8d45e0500, 0x98f172ba1783f, 'black')
    new_round = game(0x1c287ca0202000, 0x3c2091021c000000, 'black')
    new_round = game(0x1030397031900, 0x3c3cfcfc68fc263c, 'white')
    new_round = game(0x40ccde0e4ec3c24, 0x830301f18100000, 'white')
    new_round = game(0x4c2830200400, 0x1010081c1800, 'white')
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
                pos, minimax = reversi_ai(new_round, rates=rates1)
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
            #pos = random_ai(new_round)
        steps.append(pos)
        steps2.append(pos)
        if not new_round.put_chess(pos):
            steps.pop()
            steps2.pop()
        new_round.draw_board()
        print(hex(new_round.white) + ', ' + hex(new_round.black))
        new_round.get_who_win()


def reversi_ai(new_round, minimax=None, steps=None, rates=None):
    max_depth = 3
    choice_num = len(new_round.flips)

    #if choice_num >= 10:
    #    max_depth = 2
    #if choice_num >= 6:
    #    max_depth = 3

    if minimax is None:
        minimax = tree(max_depth, new_round, rates)
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


def random_ai(new_round):
    pos = random.choice(list(new_round.flips))
    return new_round.pos2str[pos]


if __name__ == "__main__":
    debug_print = True
    main()
