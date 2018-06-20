import queue
import random
from reversi import *


class tree:
    def __init__(self, max_depth, cur_board, root=None):
        self.__max = 0x7fffffff
        self.__min = -self.__max
        self.__max_depth = max_depth
        self.player = cur_board.current_player
        self.ai = reversi_ai()
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
            if cur_node.board.winner == self.player:
                weight = self.__max
            elif cur_node.board.winner == 'draw':
                weight = 0
            else:
                weight = self.__min
        else:
            weight = self.ai.get_move_ability(cur_node)
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
                value += self.ai.get_square_weight(child)
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
                value -= self.ai.get_square_weight(child)
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

    def __init__(self):
        self.xy2weight = [[16, -3, 0.2, 0, 0, 0.2, -3, 16],
                         [-3, -1, 0, 0, 0, 0, -1, -3],
                         [0.2, 0, 0, 0, 0, 0, 0, 0.2],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0.2, 0, 0, 0, 0, 0, 0, 0.2],
                         [-3, -1, 0, 0, 0, 0, -1, -3],
                         [16, -3, 0.2, 0, 0, 0.2, -3, 16]]

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

        return (ai_move - opponent_move) / (ai_move + opponent_move)

    def get_flips_move_ability(self, flips):
        mask = 0xc3c300000000c3c3
        count = 0
        for flip in flips:
            if flip & mask:
                continue
            count += 1
        return count

    def get_square_weight(self, cur_node):
        value = 0
        if cur_node.parent.board.corner_null(cur_node.pos):
            xy = cur_node.board.pos2xy[cur_node.pos]
            value += self.xy2weight[xy[1]][xy[0]]

        if cur_node.board.can_put_corner(cur_node.pos):
            # avoid opponent get corner
            value -= 16
        return value
