import queue
from reversi import *


class tree:
    def __init__(self, max_depth, cur_board):
        self.__max = 0x7fffffff
        self.__min = -self.__max
        self.__max_depth = max_depth
        self.root = self.node(self.__min, 0, None, cur_board, True, 0)
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
            print(cur_node.value, end=' | ')
            for i in cur_node.child:
                q.put(i)
            last_node_depth = cur_node.depth
        print('')

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
            new_node = self.node(value, depth + 1, cur_node, new_board, is_max, i)
            cur_node.child.append(new_node)

            if depth + 1 == self.__max_depth:
                new_node.value = self.get_sbe(new_node)
            else:
                self.build_tree(new_node, depth + 1)

    def get_sbe(self, cur_node):
        return 5

    def alpha_beta_pruning(self, cur_node, depth, alpha, beta):
        is_max = cur_node.is_max
        if not cur_node.child:
            return cur_node.value
        for i in cur_node.child:
            value = self.alpha_beta_pruning(i, depth + 1,
                                            alpha, beta)
            if is_max:
                # get maximizing of child
                if value > cur_node.value:
                    cur_node.value = value
                    cur_node.choice = i.pos
                # update alpha
                if cur_node.value > alpha:
                    alpha = cur_node.value
            else:
                # get minimizing of child
                if value < cur_node.value:
                    cur_node.value = value
                    cur_node.choice = i.pos
                # update beta
                if cur_node.value < beta:
                    beta = cur_node.value

            # alpha-beta pruning
            if alpha >= beta:
                break
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
