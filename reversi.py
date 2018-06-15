class game:

    def __init__(self, white=0x0000001008000000,
                 black=0x0000000810000000, current_player='black'):
        self.create_table()
        self.game_over = False
        self.white = white
        self.black = black
        self.flips = {}
        self.current_player = current_player
        self.can_put_pos()
        print(self.flips)
        for k, v in self.flips.items():
            print(hex(k), hex(v))

    def draw_board(self):
        result = ui.BOTTOM_LINE
        bit = 1
        for i in range(8):
            result = ui.VERTICAL_LINE + '\n' + result
            for j in range(8):
                if self.white & bit:
                    result = ui.WHITE_CHESS + result
                elif self.black & bit:
                    result = ui.BLACK_CHESS + result
                elif bit in self.flips:
                    result = ui.RED + result
                else:
                    result = ui.NONE_CHESS + result
                result = ui.VERTICAL_LINE + result
                bit = bit << 1
            result = str(8 - i) + ' ' + result

        result = ui.TOP_LINE + '\n' + result
        result = ui.HEAD + '\n' + result

        print(result)

    def can_put_pos(self):
        self.flips.clear()

        # get current player
        if self.current_player == 'black':
            cur_player, next_player = self.black, self.white
        else:
            cur_player, next_player = self.white, self.black

        # find player pos and get can move pos
        bit = 1
        for i in range(64):
            if bit & cur_player:
                self.get_flips(cur_player, next_player, bit)
            bit <<= 1

    def get_flips(self, cur_player, next_player, pos):
        directs = [0, 1, 0, -1, 1, 0, -1, 0, 1, 1, -1, -1, 1, -1, -1, 1]
        for i in range(0, len(directs), 2):
            flip, flip_pos = self.direct_find(cur_player, next_player, pos,
                                              directs[i], directs[i + 1])
            if flip:
                flip |= self.flips.setdefault(flip_pos, 0)
                self.flips[flip_pos] = flip

    def direct_find(self, cur_player, next_player, pos, dx, dy):
        x = self.pos2xy[pos][0]
        y = self.pos2xy[pos][1]
        x += dx
        y += dy
        flip = 0
        offset = -dx - 8 * dy
        pos = pos << offset if offset > 0 else pos >> abs(offset)
        while 0 <= x <= 7 and 0 <= y <= 7:
            if pos & next_player:
                flip |= pos
            elif pos & cur_player:
                return 0, 0
            elif flip == 0:
                return 0, 0
            else:
                return flip, pos

            pos = pos << offset if offset > 0 else pos >> abs(offset)
            x += dx
            y += dy
        return 0, 0

    def put_chess(self, pos):
        pos = self.str2pos(pos)

        if pos not in self.flips:
            print('invalid value')
        else:
            self.white ^= self.flips[pos]
            self.black ^= self.flips[pos]

            if self.current_player == 'black':
                self.black |= pos
                self.current_player = 'white'
            else:
                self.white |= pos
                self.current_player = 'black'

            self.can_put_pos()

            # opponent can't put chess
            if not self.flips:
                if self.current_player == 'black':
                    self.current_player = 'white'
                else:
                    self.current_player = 'black'
                self.can_put_pos()

                # game over
                if not self.flips:
                    self.game_over = True
                    self.get_who_win()

    def str2pos(self, pos):
        if len(pos) < 2:
            return 0
        x = ord(pos[0])
        y = ord(pos[1])
        if x > ord('h') or x < ord('a') or y > ord('8') or y < ord('1'):
            return 0
        x -= ord('a')
        y -= ord('1')
        return 0x8000000000000000 >> (x + 8 * y)

    def create_table(self):
        self.pos2xy = {}
        self.pos2str = {}
        pos = 1
        for i in range(64):
            self.pos2xy[pos] = [7 - i % 8, 7 - i // 8]
            self.pos2str[pos] = chr(7 - i % 8 + ord('a'))
            self.pos2str[pos] += chr(7 - i // 8 + ord('1'))
            pos <<= 1

        self.byte2count = []
        for i in range(0x100):
            bit = 1
            num = 0
            for j in range(8):
                if i & bit:
                    num += 1
                bit <<= 1
            self.byte2count.append(num)

    def get_who_win(self):
        white = self.count_chess(self.white)
        black = self.count_chess(self.black)

        print('white: {}, black {}'.format(white, black))
        if black > white:
            print('black win')
        elif black < white:
            print('white win')
        else:
            print('draw')

    def count_chess(self, chesses):
        num = 0
        for i in range(8):
            num += self.byte2count[chesses & 0xff]
            chesses >>= 8
        return num


class ui:
    WHITE_CHESS = '\033[42m\033[37m●\033[0m'
    BLACK_CHESS = '\033[42m\033[30m●\033[0m'
    NONE_CHESS = '\033[42m \033[0m'
    VERTICAL_LINE = '\033[42m│\033[0m'
    BOTTOM_LINE = '  \033[42m└' + '─┴' * 7 + '─' + '┘\033[0m'
    TOP_LINE = '  \033[42m┌' + '─┬' * 7 + '─' + '┐\033[0m'
    CENTER_LINE = '  \033[42m├' + '─┼' * 7 + '─' + '┤\033[0m'
    RED = '\033[42m\033[31m●\033[0m'
    HEAD = '   a b c d e f g h '
