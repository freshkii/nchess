from kandinsky import fill_rect
from ion import keydown, KEY_LEFT, KEY_UP, KEY_RIGHT, KEY_DOWN, KEY_OK
from time import sleep


# screen
screen_width, screen_height = 320, 222

chessboard_width = 216
case_width = chessboard_width // 8

horizontal_border = (screen_width - chessboard_width) // 2
vertical_border = (screen_height - chessboard_width) // 2

# colors
colors = {
    'brown':  (240, 217, 181),
    'beige':  (181, 136, 99),
    'black':  (0, 0, 0),
    'lblack': (60, 60, 60),
    'white':  (255, 255, 255),
    'lwhite': (243, 243, 243),
    'green':  (100, 109, 64),
    'grey':   (130,130,130),
    'pwhite': (255,255,255)
}

whites = ['K', 'N', 'B', 'P', 'Q', 'R']

# resources
resources = {
    'k': [['', '', '', '', '', 'b', 'b', '', '', '', '', ''], ['', '', '', '', 'b', 'c', 'c', 'b', '', '', '', ''],
          ['', '', '', '', 'b', 'c', 'c', 'b', '', '', '', ''],
          ['', 'b', 'b', 'b', '', 'b', 'b', '', 'b', 'b', 'b', ''],
          ['b', 'c', 'c', 'c', 'b', '', '', 'b', 'c', 'c', 'c', 'b'],
          ['b', 'c', '', 'b', 'c', 'b', 'b', 'c', 'b', '', 'c', 'b'],
          ['b', 'c', '', '', 'b', 'c', 'c', 'b', '', '', 'c', 'b'],
          ['b', 'c', 'b', '', '', 'c', 'c', '', '', 'b', 'c', 'b'],
          ['', 'b', 'c', 'b', 'b', 'c', 'c', 'b', 'b', 'c', 'b', ''],
          ['', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'b', ''],
          ['', '', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'b', '', ''],
          ['', '', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', '', ''],
          ['', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'b', ''],
          ['', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', '']],
    'q': [['', '', '', '', '', '', 'b', 'b', '', '', '', '', '', ''],
          ['', '', '', '', '', 'b', 'c', 'c', 'b', '', '', '', '', ''],
          ['', '', '', '', '', 'b', 'c', 'c', 'b', '', '', '', '', ''],
          ['', '', '', '', '', '', 'b', 'b', '', '', '', '', '', ''],
          ['b', '', '', '', '', '', '', '', '', '', '', '', '', 'b'],
          ['', 'b', 'b', '', '', '', 'b', 'b', '', '', '', 'b', 'b', ''],
          ['', 'b', 'c', 'b', '', 'b', 'c', 'c', 'b', '', 'b', 'c', 'b', ''],
          ['', 'b', 'c', 'c', 'b', 'c', 'c', 'c', 'c', 'b', 'c', 'c', 'b', ''],
          ['', '', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'b', '', ''],
          ['', '', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'b', '', ''],
          ['', '', '', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'b', '', '', ''],
          ['', '', '', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', '', '', ''],
          ['', '', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'b', '', ''],
          ['', '', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', '', '']],
    'b': [['', '', '', '', 'b', 'b', '', '', '', ''], ['', '', '', 'b', 'c', 'c', 'b', '', '', ''],
          ['', '', '', 'b', 'c', 'c', 'b', '', '', ''], ['', '', '', '', 'b', 'b', '', '', '', ''],
          ['', '', '', 'b', 'c', 'c', 'b', '', '', ''], ['', '', 'b', 'c', 'c', 'c', 'c', 'b', '', ''],
          ['', 'b', 'c', 'c', 'c', 'c', 'b', 'c', 'b', ''], ['', 'b', 'c', 'c', 'c', 'b', 'c', 'c', 'b', ''],
          ['', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'b', ''], ['', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'b', ''],
          ['', '', 'b', 'c', 'c', 'c', 'c', 'b', '', ''], ['', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', ''],
          ['b', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'b'], ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']],
    'n': [['', '', 'b', 'b', 'b', 'b', '', '', '', '', '', ''], ['', '', 'b', 'c', 'c', 'c', 'b', 'b', 'b', '', '', ''],
          ['', '', '', 'b', 'c', 'c', 'c', 'c', 'c', 'b', '', ''],
          ['', '', 'b', 'c', 'b', 'c', 'c', 'c', 'c', 'c', 'b', ''],
          ['', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'b', ''],
          ['b', 'c', 'c', 'c', 'c', 'c', 'b', 'c', 'c', 'c', 'b', ''],
          ['b', 'c', 'c', 'b', 'c', 'b', 'c', 'c', 'c', 'c', 'b', ''],
          ['', 'b', 'b', '', '', 'b', 'c', 'c', 'c', 'c', 'b', ''],
          ['', '', '', '', 'b', 'c', 'c', 'c', 'c', 'c', 'b', ''],
          ['', '', '', 'b', 'c', 'c', 'c', 'c', 'c', 'b', '', ''],
          ['', '', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'b', '', ''],
          ['', '', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', '', ''],
          ['', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'b', ''],
          ['', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', '']],
    'r': [['', 'b', 'b', 'b', '', 'b', 'b', 'b', 'b', 'b', 'b', ''],
          ['', 'b', 'c', 'b', '', 'b', 'c', 'c', 'c', 'c', 'b', ''],
          ['', 'b', 'c', 'b', 'b', 'b', 'c', 'c', 'c', 'c', 'b', ''],
          ['', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'b', ''],
          ['', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', ''],
          ['', '', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'b', '', ''],
          ['', '', '', 'b', 'b', 'b', 'b', 'b', 'b', '', '', ''],
          ['', '', '', 'b', 'c', 'c', 'c', 'c', 'b', '', '', ''],
          ['', '', '', 'b', 'c', 'c', 'c', 'c', 'b', '', '', ''],
          ['', '', '', 'b', 'c', 'c', 'c', 'c', 'b', '', '', ''],
          ['', '', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'b', '', ''],
          ['', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'b', ''],
          ['b', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'b'],
          ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']],
    'p': [['', '', 'b', 'b', 'b', 'b', '', ''], ['', 'b', 'c', 'c', 'c', 'c', 'b', ''],
          ['', 'b', 'c', 'c', 'c', 'c', 'b', ''], ['', 'b', 'c', 'c', 'c', 'c', 'b', ''],
          ['', '', 'b', 'c', 'c', 'b', '', ''], ['', 'b', 'c', 'c', 'c', 'c', 'b', ''],
          ['', 'b', 'c', 'c', 'c', 'c', 'b', ''], ['', '', 'b', 'c', 'c', 'b', '', ''],
          ['', 'b', 'c', 'c', 'c', 'c', 'b', ''], ['b', 'c', 'c', 'c', 'c', 'c', 'c', 'b'],
          ['b', 'c', 'c', 'c', 'c', 'c', 'c', 'b'], ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']]
}

# position
board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]
view = 'white'
kings = {
    'white': (4, 7),
    'black': (4, 0)
}


# graphics
def fill_case(x, y, color):
    if view == 'black':
        x = 7 - x
        y = 7 - y
    fill_rect(horizontal_border + case_width * x, vertical_border + case_width * y, case_width, case_width,
              colors[color])


def draw_piece(x, y, piece):
    if view == 'black':
        x = 7 - x
        y = 7 - y
    piece_resource = resources[piece.lower()]
    border_x = (case_width - len(piece_resource[0])) // 2
    border_y = (case_width - len(piece_resource)) // 2
    _y = 1
    color = colors['l' + get_piece_color(piece)]
    for row in piece_resource:
        _x = 1
        for element in row:
            if element:
                fill_rect(horizontal_border + case_width * x + border_x + _x,
                          vertical_border + case_width * y + border_y + _y, 1, 1,
                          color if element == 'c' else colors['black'])
            _x += 1
        _y += 1


def get_piece_color(piece):
    return 'white' if piece in whites else 'black'


def get_case_color(case):
    return 'beige' if (case[0] + case[1]) % 2 == 0 else 'brown'


border_width = 2


def draw_border(case, color):
    x = case[0]
    y = case[1]
    if view == 'black':
        x = 7 - x
        y = 7 - y
    fill_rect(horizontal_border + case_width * x, vertical_border + case_width * y, border_width, case_width,
              colors[color])  # left
    fill_rect(horizontal_border + case_width * x, vertical_border + case_width * y, case_width, border_width,
              colors[color])  # top
    fill_rect(horizontal_border + case_width * (x + 1) - border_width, vertical_border + case_width * y, border_width,
              case_width, colors[color])  # right
    fill_rect(horizontal_border + case_width * x, vertical_border + case_width * (y + 1) - border_width, case_width,
              border_width, colors[color])  # bottom


def fill_case_background(case, color):
    x = case[0]
    y = case[1]
    fill_case(x, y, color)
    if board[y][x]:
        draw_piece(x, y, board[y][x])


# moves
def get_line(start_case, direction, end_case=None):
    case = start_case[0] + direction[0], start_case[1] + direction[1]
    line = []
    while -1 < case[0] < 8 and -1 < case[1] < 8 and not board[case[1]][case[0]]:
        line.append(case[:])
        if end_case and case == end_case:
            break
        case = case[0] + direction[0], case[1] + direction[1]
    return line


def enemy_there(case):
    return True if board[case[1]][case[0]] and get_piece_color(board[case[1]][case[0]]) != view else False


def friend_there(case):
    return True if board[case[1]][case[0]] and get_piece_color(board[case[1]][case[0]]) == view else False


knight_patterns = [(-2, 1), (-1, 2), (2, 1), (1, 2), (-2, -1), (-1, -2), (2, -1), (1, -2)]
king_patterns = [(1, 1), (0, 1), (-1, -1), (1, 0), (-1, 1), (-1, 0), (1, -1), (0, -1)]
pawn_attacking_patterns = {'white': [(-1, -1), (1, -1)], 'black': [(-1, 1), (1, 1)]}

straight_directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def is_attacked(case):
    color = get_piece_color(board[case[1]][case[0]])
    for direction in straight_directions:
        line = get_line(case, direction)
        x = (line[-1][0] if len(line) else case[0]) + direction[0]
        y = (line[-1][1] if len(line) else case[1]) + direction[1]
        if -1 < x < 8 and -1 < y < 8 and board[y][x] and get_piece_color(board[y][x]) != color and board[y][x].lower() in ['r', 'q']:
            return True

    for direction in diagonal_directions:
        line = get_line(case, direction)
        x = (line[-1][0] if len(line) else case[0]) + direction[0]
        y = (line[-1][1] if len(line) else case[1]) + direction[1]
        if -1 < x < 8 and -1 < y < 8 and board[y][x] and get_piece_color(board[y][x]) != color and (board[y][x].lower() in ['b', 'q']):
            return True

    for pattern in knight_patterns:
        x = pattern[0] + case[0]
        y = pattern[1] + case[1]
        if -1 < x < 8 and -1 < y < 8 and board[y][x] and get_piece_color(board[y][x]) != color and board[y][x].lower() == 'n':
            return True

    for pattern in king_patterns:
        x = pattern[0] + case[0]
        y = pattern[1] + case[1]
        if -1 < x < 8 and -1 < y < 8 and board[y][x] and get_piece_color(board[y][x]) != color and board[y][x].lower() == 'k':
            return True

    for pattern in pawn_attacking_patterns[color]:
        x = pattern[0] + case[0]
        y = pattern[1] + case[1]
        if -1 < x < 8 and -1 < y < 8 and board[y][x] and get_piece_color(board[y][x]) != color and board[y][x].lower() == 'p':
            return True

    return False


en_passant = {'white': [], 'black': []}
castle = {'white': [1, 1], 'black': [1, 1]}

def checkmate():
    ...

def handle_move(start_case, end_case):
    global en_passant, castle, board, kings

    piece = board[start_case[1]][start_case[0]]
    opposite_color = 'black' if view == 'white' else 'white'
    castle_row = 0 if view == 'black' else 7

    saved_board = [[e for e in row] for row in board]
    saved_en_passant = {'white': en_passant['white'][:], 'black': en_passant['black'][:]}
    saved_castle = {'white': castle['white'][:], 'black': castle['black'][:]}
    saved_kings = {'white': kings['white'][:], 'black': kings['black'][:]}

    # pawn
    if piece.lower() == 'p':
        orientation = -1 if view == 'white' else 1
        move_range = (1 if start_case[1] != (6 if view == 'white' else 1) else 2)
        # common moves
        moves = get_line(start_case, (0, orientation), (start_case[0], start_case[1] + move_range * orientation))
        # common taking - checking first if case exists and is not something like -1 or 8
        if -1 < start_case[0]+1 < 8 and enemy_there((start_case[0] + 1, start_case[1] + orientation)):
            moves.append((start_case[0] + 1, start_case[1] + orientation))
        if -1 < start_case[0]-1 < 8 and enemy_there((start_case[0] - 1, start_case[1] + orientation)):
            moves.append((start_case[0] - 1, start_case[1] + orientation))
        # check if move in common moves
        if moves and tuple(end_case) in moves:
            board[end_case[1]][end_case[0]] = 'P' if view == 'white' else 'p'
            board[start_case[1]][start_case[0]] = ''
            if end_case[1] == (0 if view == 'white' else 7):
                board[end_case[1]][end_case[0]] = handle_promotion()
        else:
            # en passant
            en_passant_moves = []
            if start_case[1] == (3 if view == 'white' else 4):
                if start_case[0] + 1 in en_passant[opposite_color]:
                    en_passant_moves.append((start_case[0] + 1, start_case[1] + orientation))
                    en_passant[opposite_color].remove(start_case[0] + 1)
                if start_case[0] - 1 in en_passant[opposite_color]:
                    en_passant_moves.append((start_case[0] - 1, start_case[1] + orientation))
                    en_passant[opposite_color].remove(start_case[0] - 1)
            if en_passant_moves and tuple(end_case) in en_passant_moves:
                if start_case[1] == (3 if view == 'white' else 4):
                    board[end_case[1]][end_case[0]] = 'P' if view == 'white' else 'p'
                    board[start_case[1]][end_case[0]] = ''
                    board[start_case[1]][start_case[0]] = ''
            else:
                return False
        # update in consequence the general variables
        if end_case[1] == (4 if view == 'white' else 3):
            en_passant[view].append(end_case[0])
        elif end_case[1] == (0 if view == 'white' else 7):
            board[end_case[1]][end_case[0]] = handle_promotion()
        elif start_case[1] == (4 if view == 'white' else 3):
            en_passant[view].remove(start_case[0])

    # knight
    elif piece.lower() == 'n':
        direction = end_case[0] - start_case[0], end_case[1] - start_case[1]
        if direction not in knight_patterns: return False
        if board[end_case[1]][end_case[0]] and friend_there((end_case[0], end_case[1])): return False
        else:
            board[end_case[1]][end_case[0]] = 'N' if view == 'white' else 'n'
            board[start_case[1]][start_case[0]] = ''

    # bishop
    elif piece.lower() == 'b':
        moves = []
        for direction in diagonal_directions:
            line = get_line(start_case, direction)
            next_case = (line[-1][0] + direction[0], line[-1][1] + direction[1]) if len(line) else (start_case[0] + direction[0], start_case[1] + direction[1])
            if -1 < next_case[0] < 8 and -1 < next_case[1] < 8 and enemy_there(next_case):
                line.append(next_case)
            moves.extend(line)

        if tuple(end_case) not in moves:
            return False
        else:
            board[end_case[1]][end_case[0]] = 'B' if view == 'white' else 'b'
            board[start_case[1]][start_case[0]] = ''

    # rook
    elif piece.lower() == 'r':
        moves = []
        for direction in straight_directions:
            line = get_line(start_case, direction)
            next_case = (line[-1][0] + direction[0], line[-1][1] + direction[1]) if len(line) else (start_case[0] + direction[0], start_case[1] + direction[1])
            if -1 < next_case[0] < 8 and -1 < next_case[1] < 8 and enemy_there(next_case):
                line.append(next_case)
            moves.extend(line)

        if tuple(end_case) not in moves:
            return False

        board[end_case[1]][end_case[0]] = 'R' if view == 'white' else 'r'
        board[start_case[1]][start_case[0]] = ''

        # castle handling
        if castle[view][0] and start_case == [0, castle_row]:
            castle[view][0] = 0
        if castle[view][1] and start_case == [7, castle_row]:
            castle[view][1] = 0

    # queen
    elif piece.lower() == 'q':
        moves = []
        for direction in diagonal_directions:
            line = get_line(start_case, direction)
            next_case = (line[-1][0] + direction[0], line[-1][1] + direction[1]) if len(line) else (start_case[0] + direction[0], start_case[1] + direction[1])
            if -1 < next_case[0] < 8 and -1 < next_case[1] < 8 and enemy_there(next_case):
                line.append(next_case)
            moves.extend(line)
        for direction in straight_directions:
            line = get_line(start_case, direction)
            next_case = (line[-1][0] + direction[0], line[-1][1] + direction[1]) if len(line) else (start_case[0] + direction[0], start_case[1] + direction[1])
            if -1 < next_case[0] < 8 and -1 < next_case[1] < 8 and enemy_there(next_case):
                line.append(next_case)
            moves.extend(line)
        if tuple(end_case) not in moves:
            return False
        else:
            board[end_case[1]][end_case[0]] = 'Q' if view == 'white' else 'q'
            board[start_case[1]][start_case[0]] = ''

    # king
    elif piece.lower() == 'k':
        direction = end_case[0] - start_case[0], end_case[1] - start_case[1]
        if direction not in king_patterns:
            if castle[view] != [0, 0]:
                if castle[view][1]:
                    rook = board[castle_row][7]
                    # satisfying different conditions: end_case, rook present on his case(because we don't check if it's eaten), nothing between them
                    if end_case == [6, castle_row] and rook.lower() == 'r' and get_piece_color(rook) == view and not board[castle_row][5] and not board[castle_row][6]:
                        board[castle_row][5] = rook
                        board[castle_row][6] = board[start_case[1]][start_case[0]]
                        board[castle_row][4] = ''
                        board[castle_row][7] = ''

                        kings[view] = end_case

                        # checking if rook is attacked
                        if is_attacked((5, castle_row)) or is_attacked(end_case):
                            board = [[e for e in row] for row in saved_board]
                            kings = saved_kings.copy()
                            return False
                if castle[view][0]:
                    rook = board[castle_row][0]
                    # satisfying different conditions: ...
                    if end_case == [2, castle_row] and rook.lower() == 'r' and get_piece_color(rook) == view and not board[castle_row][1] and not board[castle_row][2] and not board[castle_row][3]:
                        board[castle_row][3] = rook
                        board[castle_row][2] = board[start_case[1]][start_case[0]]
                        if is_attacked((3,castle_row)):
                            board = [[e for e in row] for row in saved_board]
                            return False
            else: return False
        elif board[end_case[1]][end_case[0]] and friend_there((end_case[0], end_case[1])):
            return False
        else:
            board[end_case[1]][end_case[0]] = 'K' if view == 'white' else 'k'
            board[start_case[1]][start_case[0]] = ''
            kings[view] = end_case
        castle[view] = [0,0]

    # check if king in check
    if is_attacked(kings[view]):
        board = [[e for e in row] for row in saved_board]
        en_passant = saved_en_passant.copy()
        castle = saved_castle.copy()
        kings = saved_kings.copy()
        return False

    # other stuffs
    return True

def handle_promotion():
    pcursor = 0
    pieces = 'qrbn'.upper() if view == 'white' else 'qrbn'
    y = 8 if view == 'white' else -1
    for i in range(4):
        draw_piece(8,i,pieces[i])
    while True:
        if keydown(KEY_DOWN) and pcursor != 3:
            draw_border((y,pcursor), 'pwhite')
            pcursor += 1 if view == 'white' else -1
            draw_border((y,pcursor), 'grey')
        if keydown(KEY_UP) and pcursor != 0:
            draw_border((y,pcursor), 'pwhite')
            pcursor -= 1 if view == 'white' else -1
            draw_border((y,pcursor), 'grey')
        if keydown(KEY_OK):
            for i in range(4):
                fill_case(y,i,'pwhite')
            return pieces[pcursor]
        sleep(0.1)


    


def draw_board():
    for y in range(8):
        for x in range(8):
            fill_case(x, y, get_case_color([x, y]))
            if board[y][x]:
                draw_piece(x, y, board[y][x])


# settings general variables
cursor = {
    'white': [4, 6],
    'black': [4, 1]
}
select = [None, None]
selected = False

# game loop
while True:
    draw_board()
    draw_border(cursor[view], 'green')
    current_view = view
    while current_view == view:
        if keydown(KEY_LEFT) and cursor[view][0] != (0 if view == 'white' else 7):
            if cursor[view] != select:
                draw_border(cursor[view], get_case_color(cursor[view]))
            cursor[view][0] += -1 if view == 'white' else 1
            if cursor[view] != select:
                draw_border(cursor[view], 'green')
        if keydown(KEY_RIGHT) and cursor[view][0] != (7 if view == 'white' else 0):
            if cursor[view] != select:
                draw_border(cursor[view], get_case_color(cursor[view]))
            cursor[view][0] += 1 if view == 'white' else -1
            if cursor[view] != select:
                draw_border(cursor[view], 'green')
        if keydown(KEY_UP) and cursor[view][1] != (0 if view == 'white' else 7):
            if cursor[view] != select:
                draw_border(cursor[view], get_case_color(cursor[view]))
            cursor[view][1] += -1 if view == 'white' else 1
            if cursor[view] != select:
                draw_border(cursor[view], 'green')
        if keydown(KEY_DOWN) and cursor[view][1] != (7 if view == 'white' else 0):
            if cursor[view] != select:
                draw_border(cursor[view], get_case_color(cursor[view]))
            cursor[view][1] += 1 if view == 'white' else -1
            if cursor[view] != select:
                draw_border(cursor[view], 'green')
        if keydown(KEY_OK):
            if selected:
                if handle_move(select, cursor[view]):
                    view = 'black' if view == 'white' else 'white'
                else:
                    fill_case_background(select, get_case_color(select))
                    draw_border(cursor[view], 'green')
                selected = False
                select = (None, None)
            elif board[cursor[view][1]][cursor[view][0]] and get_piece_color(board[cursor[view][1]][cursor[view][0]]) == view:
                select = cursor[view][:]
                selected = True
                fill_case_background(select, 'green')


        sleep(0.1)

