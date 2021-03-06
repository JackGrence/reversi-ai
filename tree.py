import queue
import random
import math
from reversi import *


class tree:
    def __init__(self, max_depth, cur_board, rates):
        self.__max = 0x7fffffff
        self.__min = -self.__max
        self.__max_depth = max_depth
        self.player = cur_board.current_player
        self.ai = reversi_ai(rates)
        self.root = self.node(self.__min, 0, None, cur_board, True, 1)
        self.build_tree(self.root, 0)
        self.alpha_beta_pruning(self.root, 0, self.__min, self.__max)
        # self.minimax(self.root, 0, True)
        # catch leaf_len < 1 or leaf is empty

    def print(self, print_node):
        last_node_depth = -1
        q = queue.Queue()
        q.put(print_node)
        while not q.empty():
            cur_node = q.get()
            if last_node_depth != cur_node.depth:
                print('')
            print(cur_node.board.pos2str[cur_node.pos], '-',
                  cur_node.value, end=' | ')
            for i in cur_node.child:
                q.put(i)
            last_node_depth = cur_node.depth
        print('')

    def change_root(self, steps, max_depth):
        self.__max_depth = max_depth
        for step in steps:
            step_in = False
            for child in self.root.child:
                if child.pos == step:
                    next_root = child
                    step_in = True
                else:
                    child.free(child)
            if not step_in:
                self.root.board = self.root.board.get_future_board(step)
                if self.root.board.current_player == self.player:
                    self.root.is_max = True
                else:
                    self.root.is_max = False
            else:
                self.root = next_root

        if not self.root.is_max:
            print('what? root is\'n max level(?' * 50)
        self.update_tree(self.root, 0)
        self.alpha_beta_pruning(self.root, 0, self.__min, self.__max)

    def update_tree(self, cur_node, depth):
        cur_node.depth = depth
        cur_node.value = self.__min if cur_node.is_max else self.__max
        if cur_node.board.game_over:
            cur_node.value = self.get_sbe(cur_node)
            return

        if not cur_node.child:
            for i in cur_node.board.flips:
                new_board = cur_node.board.get_future_board(i)
                if cur_node.board.current_player == new_board.current_player:
                    is_max = cur_node.is_max
                else:
                    is_max = not cur_node.is_max

                if is_max:
                    value = self.__min
                else:
                    value = self.__max
                new_node = self.node(value, depth + 1, cur_node,
                                     new_board, is_max, i)
                cur_node.child.append(new_node)

                if depth + 1 != self.__max_depth:
                    self.update_tree(new_node, depth + 1)
                else:
                    new_node.value = self.get_sbe(new_node)

        else:
            for i in cur_node.child:
                self.update_tree(i, depth + 1)

    def build_tree(self, cur_node, depth):
        if cur_node.board.game_over:
            cur_node.value = self.get_sbe(cur_node)
            return
        if not cur_node.board.flips:
            print('impossible')
            return
        for i in cur_node.board.flips:
            new_board = cur_node.board.get_future_board(i)
            if cur_node.board.current_player == new_board.current_player:
                is_max = cur_node.is_max
            else:
                is_max = not cur_node.is_max

            if is_max:
                value = self.__min
            else:
                value = self.__max
            new_node = self.node(value, depth + 1, cur_node,
                                 new_board, is_max, i)
            cur_node.child.append(new_node)

            if depth + 1 == self.__max_depth:
                new_node.value = self.get_sbe(new_node)
            else:
                self.build_tree(new_node, depth + 1)

    def get_sbe(self, cur_node):
        if cur_node.board.game_over:
            cur_node.board.get_winner()
            weight = abs(
                    cur_node.board.black_count - cur_node.board.white_count
                    )
            if cur_node.board.winner != self.player:
                weight = -weight
            weight *= self.ai.game_over_rate
        else:
            weight = self.ai.get_move_ability(cur_node)
            weight += self.ai.get_stability(cur_node)
            weight += self.ai.get_square_weight(cur_node)
            weight += self.ai.get_coin_parity(cur_node)
            weight += self.ai.get_corner_captured(cur_node)
        return weight

    def alpha_beta_pruning(self, cur_node, depth, alpha, beta):
        is_max = cur_node.is_max
        if not cur_node.child:
            return cur_node.value

        choices = [cur_node.child[0].pos]
        for child in cur_node.child:
            value = self.alpha_beta_pruning(child, depth + 1,
                                            alpha, beta)
            # add square weight at every move
            if is_max:
                # get maximizing of child
                if value > cur_node.value:
                    cur_node.value = value
                    choices.clear()
                    choices.append(child.pos)
                elif value == cur_node.value:
                    choices.append(child.pos)
                # update alpha
                if cur_node.value > alpha:
                    alpha = cur_node.value
            else:
                # get minimizing of child
                if value < cur_node.value:
                    cur_node.value = value
                    choices.clear()
                    choices.append(child.pos)
                elif value == cur_node.value:
                    choices.append(child.pos)
                # update beta
                if cur_node.value < beta:
                    beta = cur_node.value

            child.value = value

            # alpha-beta pruning
            if alpha >= beta:
                break

        cur_node.choice = random.choice(choices)

        return cur_node.value

    class node:
        def __init__(self, value, depth, parent, cur_board, is_max, pos):
            self.value = value
            self.depth = depth
            self.parent = parent
            self.child = []
            self.board = cur_board
            self.is_max = is_max
            self.choice = 0
            self.pos = pos

        def free(self, cur_node):
            for i in cur_node.child:
                self.free(i)

            del cur_node.board
            del cur_node


class reversi_ai:

    def __init__(self, rates):
        xy2weight = [rates[i:i + 4] for i in range(0, 16, 4)]
        self.xy2weight = [i + i[::-1] for i in xy2weight]
        self.xy2weight = self.xy2weight + self.xy2weight[::-1]
        self.move_rate = rates[16]
        self.get_corner_rate = rates[17]
        self.game_over_rate = rates[18]
        self.square_rate = rates[19]
        self.stability_rate = rates[20]

    def get_move_ability(self, cur_node):
        flips_len = self.get_flips_move_ability(cur_node.board.flips)
        if cur_node.is_max:
            ai_move = flips_len
        else:
            opponent_move = flips_len

        board = cur_node.board
        tmp_player = board.current_player
        if board.current_player == game.black_str:
            board.current_player = game.white_str
        else:
            board.current_player = game.black_str

        # copy and get new flips
        tmp_flips = dict(board.flips)
        board.can_put_pos()

        # recover flips
        board.current_player = tmp_player
        tmp_flips, board.flips = board.flips, tmp_flips

        flips_len = self.get_flips_move_ability(tmp_flips)
        if cur_node.is_max:
            opponent_move = flips_len
        else:
            ai_move = flips_len

        if ai_move + opponent_move == 0:
            return 0

        val = (ai_move - opponent_move) / (ai_move + opponent_move)
        return self.move_rate * val

    def get_flips_move_ability(self, flips):
        mask = 0xc3c300000000c3c3
        count = 0
        for flip in flips:
            if flip & mask:
                continue
            count += 1
        return count

    def get_square_weight(self, cur_node):
        cur_board = cur_node.board

        # max level XOR current player is black == True, then ai is white
        if cur_node.is_max ^ (cur_board.current_player == cur_board.black_str):
            ai_chess = cur_board.white
            opponent_chess = cur_board.black
        else:
            ai_chess = cur_board.black
            opponent_chess = cur_board.white

        ai_weight = 0
        opponent_weight = 0
        pos = 1
        for i in range(64):
            value = 0
            if cur_board.corner_null(pos):
                xy = cur_node.board.pos2xy[pos]
                value += self.xy2weight[xy[1]][xy[0]]

            if pos & ai_chess:
                ai_weight += value
            elif pos & opponent_chess:
                opponent_weight += value

            pos <<= 1

        return (ai_weight - opponent_weight)

    def get_stability(self, cur_node):
        cur_board = cur_node.board

        # max level XOR current player is black == True, then ai is white
        if cur_node.is_max ^ (cur_board.current_player == cur_board.black_str):
            ai_chess = cur_board.white
            opponent_chess = cur_board.black
        else:
            ai_chess = cur_board.black
            opponent_chess = cur_board.white

        chess_lines = [chess_line() for i in range(46)]
        # line order:
        # -, |, /, \
        # 0, 8, 16, 31
        line_index = [0, 8, 16, 31]

        pos = 0x8000000000000000
        for row in range(8):
            for col in range(8):
                if pos & ai_chess:
                    chess = 0
                elif pos & opponent_chess:
                    chess = 1
                else:
                    chess = 2
                # update line
                chess_lines[line_index[0] + row].update(chess)
                chess_lines[line_index[1] + col].update(chess)
                chess_lines[line_index[2] + row + col].update(chess)
                chess_lines[line_index[3] + (7 - row) + col].update(chess)
                pos >>= 1

        ai_stability = 0
        opponent_stability = 0
        for line in chess_lines:
            ai_stability += line.ai_stability + line.ai_conti_num
            opponent_stability += line.opponent_stability
            opponent_stability += line.opponent_conti_num

        if ai_stability + opponent_stability == 0:
            return 0

        val = ai_stability - opponent_stability
        val /= ai_stability + opponent_stability
        return self.stability_rate * val

    def get_coin_parity(self, cur_node):
        cur_board = cur_node.board

        # max level XOR current player is black == True, then ai is white
        if cur_node.is_max ^ (cur_board.current_player == cur_board.black_str):
            ai_chess = cur_board.white
            opponent_chess = cur_board.black
        else:
            ai_chess = cur_board.black
            opponent_chess = cur_board.white

        ai_chess = cur_board.count_chess(ai_chess)
        opponent_chess = cur_board.count_chess(opponent_chess)

        ai = ai_chess / (ai_chess + opponent_chess)
        opponent = opponent_chess / (ai_chess + opponent_chess)
        entropy = - ai * math.log2(ai) - opponent * math.log2(opponent)

        return entropy

    def get_corner_captured(self, cur_node):
        cur_board = cur_node.board

        # max level XOR current player is black == True, then ai is white
        if cur_node.is_max ^ (cur_board.current_player == cur_board.black_str):
            ai_chess = cur_board.white
            opponent_chess = cur_board.black
        else:
            ai_chess = cur_board.black
            opponent_chess = cur_board.white

        ai_corner = self.get_corner_stability(ai_chess)
        opponent_corner = self.get_corner_stability(opponent_chess)

        if ai_corner + opponent_corner == 0:
            return 0

        return (ai_corner - opponent_corner) / (ai_corner + opponent_corner)

    def get_corner_stability(self, player):
        corners = [0x8000000000000000, 0x0100000000000000, 0x80, 0x01]
        offsets = [[1, 8], [-1, 8], [1, -8], [-1, -8]]
        stability = 0
        for corner, offset in zip(corners, offsets):
            if player & corner:
                pos1 = corner
                pos2 = corner
                pos1_conti = True
                pos2_conti = True
                for i in range(7):
                    if pos1 & player and pos1_conti:
                        stability += 1
                    else:
                        pos1_conti = False

                    if pos2 & player and pos2_conti:
                        stability += 1
                    else:
                        pos2_conti = False

                    if offset[0] > 0:
                        pos1 >>= offset[0]
                    else:
                        pos1 <<= -offset[0]

                    if offset[1] > 0:
                        pos2 >>= offset[1]
                    else:
                        pos2 <<= -offset[1]

        return stability


class chess_line:

    def __init__(self):
        self.ai_stability = 0
        self.opponent_stability = 0
        self.ai_conti_num = 0
        self.ai_stack = 1
        self.opponent_conti_num = 0
        self.opponent_stack = 1

    def update(self, chess):
        # 0 is ai, 1 is opponent, 2 is null
        if chess == 0:
            if self.ai_stack:
                if self.opponent_conti_num != 0:
                    self.opponent_stability += self.opponent_conti_num
            else:
                self.ai_stack = 1

            self.ai_conti_num += 1
            self.opponent_conti_num = 0

        elif chess == 1:
            if self.opponent_stack:
                if self.ai_conti_num != 0:
                    self.ai_stability += self.ai_conti_num
            else:
                self.opponent_stack = 1

            self.opponent_conti_num += 1
            self.ai_conti_num = 0

        elif chess == 2:
            self.ai_conti_num = 0
            self.ai_stack = 0
            self.opponent_conti_num = 0
            self.opponent_stack = 0
