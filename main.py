from kandinsky import fill_rect
from ion import keydown, KEY_LEFT, KEY_UP, KEY_RIGHT, KEY_DOWN, KEY_OK
from time import sleep


# screen
screen_width, screen_height = 320, 222

chessboard_width = 216 # the biggest n <= min(screen_width, screen_height) such 8 | n
case_width = 27 # chessboard_with // 8

horizontal_border = 52 # (screen_width - chessboard_width) // 2
vertical_border = 3 # (screen_height - chessboard_width) // 2

# colors
colors = {
    'bcase':  (240, 217, 181), # black cases (brown here)
    'wcase':  (181, 136, 99), # white cases (beige here)
    'black':  (0, 0, 0), # needed sometimes
    'pblack': (60, 60, 60),     # black pieces
    'pwhite':  (255, 255, 255), # white pieces
    'prim':  (100, 109, 64), # general select/cursor ~ primary
    'seco':   (130,130,130), # promotion interface cursor ~ secondary
    'bg': (255,255,255) # general background color
}

# WARNING: this cannot exceed a certain amount of pixels as there will be an overlapping with the piece resource
cursor_width = 2

# resources
res = {
    "k":(
        '     bb     ',
        '    bccb    ',
        '    bccb    ',
        ' bbb bb bbb ',
        'bcccb  bcccb',
        'bc bcbbcb cb',
        'bc  bccb  cb',
        'bcb  cc  bcb',
        ' bcbbccbbcb ',
        ' bccccccccb ',
        '  bccccccb  ',
        '  bbbbbbbb  ',
        ' bccccccccb ',
        ' bbbbbbbbbb '
        ),
    "q":(
        '      bb      ',
        '     bccb     ',
        '     bccb     ',
        '      bb      ',
        'b            b',
        ' bb   bb   bb ',
        ' bcb bccb bcb ',
        ' bccbccccbccb ',
        '  bccccccccb  ',
        '  bccccccccb  ',
        '   bccccccb   ',
        '   bbbbbbbb   ',
        '  bccccccccb  ',
        '  bbbbbbbbbb  '
        ),
    "b":(
        '    bb    ',
        '   bccb   ',
        '   bccb   ',
        '    bb    ',
        '   bccb   ',
        '  bccccb  ',
        ' bccccbcb ',
        ' bcccbccb ',
        ' bccccccb ',
        ' bccccccb ',
        '  bccccb  ',
        ' bbbbbbbb ',
        'bccccccccb',
        'bbbbbbbbbb'
        ),
    "n":(
        '  bbbb     ',
        '  bcccbbb  ',
        '   bcccccb ',
        '  bcbcccccb',
        ' bccccccccb',
        'bcccccbcccb',
        'bccbcbccccb',
        ' bb  bccccb',
        '    bcccccb',
        '   bcccccb ',
        '  bccccccb ',
        '  bbbbbbbb ',
        ' bccccccccb',
        ' bbbbbbbbbb'
        ),
    "r":(
        ' bbb bbbbbb ',
        ' bcb bccccb ',
        ' bcbbbccccb ',
        ' bccccccccb ',
        ' bbbbbbbbbb ',
        '  bccccccb  ',
        '   bbbbbb   ',
        '   bccccb   ',
        '   bccccb   ',
        '   bccccb   ',
        '  bccccccb  ',
        ' bccccccccb ',
        'bccccccccccb',
        'bbbbbbbbbbbb'
        ),
    "p":(
        '  bbbb  ',
        ' bccccb ',
        ' bccccb ',
        ' bccccb ',
        '  bccb  ',
        ' bccccb ',
        ' bccccb ',
        '  bccb  ',
        ' bccccb ',
        'bccccccb',
        'bccccccb',
        'bbbbbbbb'
        )
}

# position
board = [
        "rnbqkbnr",
        "pppppppp",
        "        ",
        "        ",
        "        ",
        "        ",
        "PPPPPPPP",
        "RNBQKBNR"
        ]

board = [list(row) for row in board]

# as there's rotation, gotta know from which side you are
view = 'white'
kings = {
    'white': (4, 7),
    'black': (4, 0)
}

# no .isupper() so we use this to know if a piece is white or black
whites = ['K', 'N', 'B', 'P', 'Q', 'R']


# graphical funcs
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
    x_s = x * case_width + horizontal_border + 1 + (case_width - len(res[piece.lower()][0])) // 2
    y = y * case_width + vertical_border + 1 + (case_width - len(res[piece.lower()])) // 2

    c = colors['p'+get_piece_color(piece)]

    for row in res[piece.lower()]:
        x = x_s
        for pixel in row:
            if pixel == 'c':
                fill_rect(x,y,1,1, c)
            elif pixel == 'b':
                fill_rect(x,y,1,1, colors['black'])
            x += 1
        y += 1

def get_piece_color(piece): # piece must not be None
    return 'white' if piece in whites else 'black'

def get_case_piece_color(case):
    return get_piece_color(board[case[1]][case[0]])

def get_case_color(case):
    return 'wcase' if (case[0] + case[1]) % 2 == 0 else 'bcase'

def draw_border(case, c):
    x = case[0]
    y = case[1]
    if view == 'black':
        x = 7 - x
        y = 7 - y
    fill_rect(horizontal_border + case_width * x, vertical_border + case_width * y, cursor_width, case_width,
              colors[c])  # left
    fill_rect(horizontal_border + case_width * x, vertical_border + case_width * y, case_width, cursor_width,
              colors[c])  # top
    fill_rect(horizontal_border + case_width * (x + 1) - cursor_width, vertical_border + case_width * y, cursor_width,
              case_width, colors[c])  # right
    fill_rect(horizontal_border + case_width * x, vertical_border + case_width * (y + 1) - cursor_width, case_width,
              cursor_width, colors[c])  # bottom

def fill_case_background(case, color):
    x = case[0]
    y = case[1]
    fill_case(x, y, color)
    if someone_there( (x,y) ):
        draw_piece(x, y, board[y][x])

# MOVES

# very useful
def apply_pattern(case, pattern):
    return case[0] + pattern[0], case[1] + pattern[1]

def valid_cords(cords):
    return 0 <= cords[0] <= 7 and 0 <= cords[1] <= 7

# case must have valid cords
def someone_there(cords):
    return board[cords[1]][cords[0]] != ' '

def get_line(start_case, direction, end_case=None):
    case = apply_pattern(start_case, direction)
    line = []
    while valid_cords(case) and not someone_there(case):
        line.append(case[:])
        if end_case and case == end_case:
            break
        case = apply_pattern(case, direction)
    return line

# case must have valid cords
def enemy_there(case):
    return True if someone_there(case) and get_case_piece_color(case) != view else False

def friend_there(case):
    return True if someone_there(case) and get_case_piece_color(case) == view else False

knight_patterns = [(-2, 1), (-1, 2), (2, 1), (1, 2), (-2, -1), (-1, -2), (2, -1), (1, -2)]
king_patterns = [(1, 1), (0, 1), (-1, -1), (1, 0), (-1, 1), (-1, 0), (1, -1), (0, -1)]
pawn_attacking_patterns = {'white': [(-1, -1), (1, -1)], 'black': [(-1, 1), (1, 1)]}

straight_directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

def is_attacked(case):
    for direction in straight_directions:
        line = get_line(case, direction)
        x, y = apply_pattern(line[-1] if len(line) else case, direction)
        if valid_cords( (x,y) ) and enemy_there( (x,y) ) and board[y][x].lower() in ['r', 'q']:
            return True

    for direction in diagonal_directions:
        line = get_line(case, direction)
        x, y = apply_pattern(line[-1] if len(line) else case, direction)
        if valid_cords( (x,y) ) and enemy_there( (x,y) ) and board[y][x].lower() in ['b', 'q']:
            return True

    for pattern in knight_patterns:
        x, y = apply_pattern(case, pattern)
        if valid_cords( (x,y) ) and enemy_there( (x,y) ) and board[y][x].lower() == 'n':
            return True

    # make sure one's king cannot touch the oppponent's one
    for pattern in king_patterns:
        x,y = apply_pattern(case, pattern)
        if valid_cords( (x,y) ) and enemy_there( (x,y) ) and board[y][x].lower() == 'k':
            return True

    for pattern in pawn_attacking_patterns[get_case_piece_color(case)]:
        x,y = apply_pattern(case, pattern)
        if valid_cords( (x,y) ) and enemy_there( (x,y) ) and board[y][x].lower() == 'p':
            return True

    return False


en_passant = {'white': [], 'black': []}
castle = {'white': [1, 1], 'black': [1, 1]}

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
            board[start_case[1]][start_case[0]] = ' '
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
                    board[start_case[1]][end_case[0]] = ' '
                    board[start_case[1]][start_case[0]] = ' '
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
            board[start_case[1]][start_case[0]] = ' '

    # bishop
    elif piece.lower() == 'b':
        moves = []
        for direction in diagonal_directions:
            line = get_line(start_case, direction)
            next_case = apply_pattern(line[-1] if len(line) else start_case, direction)
            if valid_cords(next_case) and enemy_there(next_case):
                line.append(next_case)
            moves.extend(line)

        if tuple(end_case) not in moves:
            return False
        else:
            board[end_case[1]][end_case[0]] = 'B' if view == 'white' else 'b'
            board[start_case[1]][start_case[0]] = ' '

    # rook
    elif piece.lower() == 'r':
        moves = []
        for direction in straight_directions:
            line = get_line(start_case, direction)
            next_case = apply_pattern(line[-1] if len(line) else start_case, direction)
            if valid_cords(next_case) and enemy_there(next_case):
                line.append(next_case)
            moves.extend(line)

        if tuple(end_case) not in moves:
            return False

        board[end_case[1]][end_case[0]] = 'R' if view == 'white' else 'r'
        board[start_case[1]][start_case[0]] = ' '

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
            next_case = apply_pattern(line[-1] if len(line) else start_case, direction)
            if valid_cords(next_case) and enemy_there(next_case):
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
            board[start_case[1]][start_case[0]] = ' '

    # king
    elif piece.lower() == 'k':
        direction = end_case[0] - start_case[0], end_case[1] - start_case[1]
        if direction not in king_patterns:
            if castle[view] != [0,0]:
                if castle[view][1]:
                    rook = board[castle_row][7]
                    # satisfying different conditions: end_case, rook present on his case(because we don't check if it's eaten), nothing between them
                    if end_case == [6, castle_row] and rook.lower() == 'r' and get_piece_color(rook) == view and not someone_there((5,castle_row)) and not someone_there((6,castle_row)):
                        board[castle_row][5] = rook
                        board[castle_row][6] = board[start_case[1]][start_case[0]]
                        board[castle_row][4] = ' '
                        board[castle_row][7] = ' '

                        kings[view] = end_case

                        # checking if rook is attacked
                        if is_attacked((5, castle_row)) or is_attacked(end_case):
                            board = saved_board[:]
                            kings = saved_kings[:]
                            return False
                if castle[view][0]:
                    rook = board[castle_row][0]
                    # satisfying different conditions: ...
                    if end_case[0] == 2 and end_case[1] == castle_row and rook.lower() == 'r' and get_piece_color(rook) == view and not someone_there((1,castle_row)) and not someone_there((2,castle_row)) and not someone_there((3,castle_row)):
                        board[castle_row][4] = ' '
                        board[castle_row][3] = rook
                        board[castle_row][2] = 'K' if view == 'white' else 'k'
                        board[castle_row][0] = ' '
                        if is_attacked((3,castle_row)):
                            board = saved_board[:]
                            return False
            else:
                return False
        elif board[end_case[1]][end_case[0]] and friend_there((end_case[0], end_case[1])):
            return False
        else:
            board[end_case[1]][end_case[0]] = 'K' if view == 'white' else 'k'
            board[start_case[1]][start_case[0]] = 'K'
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
            draw_border((y,pcursor), 'bg')
            pcursor += 1 if view == 'white' else -1
            draw_border((y,pcursor), 'grey')
        if keydown(KEY_UP) and pcursor != 0:
            draw_border((y,pcursor), 'bg')
            pcursor -= 1 if view == 'white' else -1
            draw_border((y,pcursor), 'grey')
        if keydown(KEY_OK):
            for i in range(4):
                fill_case(y,i,'bg')
            return pieces[pcursor]
        sleep(0.1)

def draw_board():
    for y in range(8):
        for x in range(8):
            fill_case(x, y, get_case_color([x, y]))
            if someone_there( (x,y) ):
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
    draw_border(cursor[view], 'prim')
    current_view = view
    while current_view == view:
        if keydown(KEY_LEFT) and cursor[view][0] != (0 if view == 'white' else 7):
            if cursor[view] != select:
                draw_border(cursor[view], get_case_color(cursor[view]))
            cursor[view][0] += -1 if view == 'white' else 1
            if cursor[view] != select:
                draw_border(cursor[view], 'prim')
        if keydown(KEY_RIGHT) and cursor[view][0] != (7 if view == 'white' else 0):
            if cursor[view] != select:
                draw_border(cursor[view], get_case_color(cursor[view]))
            cursor[view][0] += 1 if view == 'white' else -1
            if cursor[view] != select:
                draw_border(cursor[view], 'prim')
        if keydown(KEY_UP) and cursor[view][1] != (0 if view == 'white' else 7):
            if cursor[view] != select:
                draw_border(cursor[view], get_case_color(cursor[view]))
            cursor[view][1] += -1 if view == 'white' else 1
            if cursor[view] != select:
                draw_border(cursor[view], 'prim')
        if keydown(KEY_DOWN) and cursor[view][1] != (7 if view == 'white' else 0):
            if cursor[view] != select:
                draw_border(cursor[view], get_case_color(cursor[view]))
            cursor[view][1] += 1 if view == 'white' else -1
            if cursor[view] != select:
                draw_border(cursor[view], 'prim')
        if keydown(KEY_OK):
            if selected:
                if handle_move(select, cursor[view]):
                    view = 'black' if view == 'white' else 'white'
                else:
                    fill_case_background(select, get_case_color(select))
                    draw_border(cursor[view], 'prim')
                selected = False
                select = (None, None)
            elif board[cursor[view][1]][cursor[view][0]] and get_piece_color(board[cursor[view][1]][cursor[view][0]]) == view:
                select = cursor[view][:]
                selected = True
                fill_case_background(select, 'prim')
        sleep(0.1)
