from kandinsky import fill_rect as fr
from ion import keydown as kd, KEY_LEFT, KEY_UP, KEY_RIGHT, KEY_DOWN, KEY_OK
from time import sleep as sp
sw, sh = 320, 222
bw = 216 
cw = 27 
hb = 52 
vb = 3 
col = {
    'bca':  (240, 217, 181), 
    'wca':  (181, 136, 99), 
    'black':  (0, 0, 0), 
    'pblack': (60, 60, 60),     
    'pwhite':  (255, 255, 255), 
    'prim':  (100, 109, 64), 
    'seco':   (130,130,130), 
    'bg': (255,255,255) 
}
cuw = 2
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
b = [
  "rnbqkbnr",
  "pppppppp",
  "        ",
  "        ",
  "        ",
  "        ",
  "PPPPPPPP",
  "RNBQKBNR"
]
b = [list(row) for row in b]
v = 'white'
kgs = {
  'white': (4, 7),
  'black': (4, 0)
}
whites = ['K', 'N', 'B', 'P', 'Q', 'R']
def fc(x, y, color):
  if v == 'black':
    x = 7 - x
    y = 7 - y
  fr(hb + cw * x, vb + cw * y, cw, cw,
              col[color])
def dp(x, y, pc):
  if v == 'black':
    x = 7 - x
    y = 7 - y
  x_s = x * cw + hb + 1 + (cw - len(res[pc.lower()][0])) // 2
  y = y * cw + vb + 1 + (cw - len(res[pc.lower()])) // 2
  c = col['p'+gpc(pc)]
  for row in res[pc.lower()]:
    x = x_s
    for pixel in row:
      if pixel == 'c':
        fr(x,y,1,1, c)
      elif pixel == 'b':
        fr(x,y,1,1, col['black'])
      x += 1
    y += 1
def gpc(pc): 
  return 'white' if pc in whites else 'black'
def gcpc(ca):
  return gpc(b[ca[1]][ca[0]])
def gcc(ca):
  return 'wca' if (ca[0] + ca[1]) % 2 == 0 else 'bca'
def db(ca, c):
  x = ca[0]
  y = ca[1]
  if v == 'black':
    x = 7 - x
    y = 7 - y
  fr(hb + cw * x, vb + cw * y, cuw, cw,
            col[c])  
  fr(hb + cw * x, vb + cw * y, cw, cuw,
            col[c])  
  fr(hb + cw * (x + 1) - cuw, vb + cw * y, cuw,
            cw, col[c])  
  fr(hb + cw * x, vb + cw * (y + 1) - cuw, cw,
            cuw, col[c])  
def fb(ca, color):
  x = ca[0]
  y = ca[1]
  fc(x, y, color)
  if st( (x,y) ):
    dp(x, y, b[y][x])
def ap(ca, pa):
  return ca[0] + pa[0], ca[1] + pa[1]
def vc(co):
  return 0 <= co[0] <= 7 and 0 <= co[1] <= 7
def st(co):
  return b[co[1]][co[0]] != ' '
def gl(sc, dire, ec=None):
  ca = ap(sc, dire)
  l = []
  while vc(ca) and not st(ca):
    l.append(ca[:])
    if ec and ca == ec:
      break
    ca = ap(ca, dire)
  return l
def et(ca):
  return True if st(ca) and gcpc(ca) != v else False
def ft(ca):
  return True if st(ca) and gcpc(ca) == v else False
npas = ((-2, 1), (-1, 2), (2, 1), (1, 2), (-2, -1), (-1, -2), (2, -1), (1, -2))
kgps = ((1, 1), (0, 1), (-1, -1), (1, 0), (-1, 1), (-1, 0), (1, -1), (0, -1))
papa = {'white': ((-1, -1), (1, -1)), 'black': ((-1, 1), (1, 1))}
sdir = ((1, 0), (-1, 0), (0, -1), (0, 1))
ddir = ((-1, -1), (-1, 1), (1, -1), (1, 1))
def ia(ca):
  for dire in sdir:
    l = gl(ca, dire)
    x, y = ap(l[-1] if len(l) else ca, dire)
    if vc( (x,y) ) and et( (x,y) ) and b[y][x].lower() in ['r', 'q']:
      return True
  for dire in ddir:
    l = gl(ca, dire)
    x, y = ap(l[-1] if len(l) else ca, dire)
    if vc( (x,y) ) and et( (x,y) ) and b[y][x].lower() in ['b', 'q']:
      return True
  for pa in npas:
    x, y = ap(ca, pa)
    if vc( (x,y) ) and et( (x,y) ) and b[y][x].lower() == 'n':
      return True
  for pa in kgps:
    x,y = ap(ca, pa)
    if vc( (x,y) ) and et( (x,y) ) and b[y][x].lower() == 'k':
      return True
  for pa in papa[v]:
    x,y = ap(ca, pa)
    if vc( (x,y) ) and et( (x,y) ) and b[y][x].lower() == 'p':
      return True
  return False
epa = {'white': [], 'black': []}
cstl = {'white': [1, 1], 'black': [1, 1]}
def hmv(sc, ec):
  global epa, cstl, b, kgs
  pc = b[sc[1]][sc[0]]
  oc = 'black' if v == 'white' else 'white'
  csr = 0 if v == 'black' else 7
  svb = [[e for e in row] for row in b]
  svepa = {'white': epa['white'][:], 'black': epa['black'][:]}
  svcstl = {'white': cstl['white'][:], 'black': cstl['black'][:]}
  svkgs = {'white': kgs['white'][:], 'black': kgs['black'][:]}
  if pc.lower() == 'p':
    ort = -1 if v == 'white' else 1
    move_range = (1 if sc[1] != (6 if v == 'white' else 1) else 2)
    mvs = gl(sc, (0, ort), (sc[0], sc[1] + move_range * ort))
    if -1 < sc[0]+1 < 8 and et((sc[0] + 1, sc[1] + ort)):
      mvs.append((sc[0] + 1, sc[1] + ort))
    if -1 < sc[0]-1 < 8 and et((sc[0] - 1, sc[1] + ort)):
      mvs.append((sc[0] - 1, sc[1] + ort))
    if mvs and tuple(ec) in mvs:
      b[ec[1]][ec[0]] = 'P' if v == 'white' else 'p'
      b[sc[1]][sc[0]] = ' '
      if ec[1] == (0 if v == 'white' else 7):
        b[ec[1]][ec[0]] = hpt()
    else:
      epam = []
      if sc[1] == (3 if v == 'white' else 4):
        if sc[0] + 1 in epa[oc]:
          epam.append((sc[0] + 1, sc[1] + ort))
          epa[oc].remove(sc[0] + 1)
        if sc[0] - 1 in epa[oc]:
          epam.append((sc[0] - 1, sc[1] + ort))
          epa[oc].remove(sc[0] - 1)
      if epam and tuple(ec) in epam:
        if sc[1] == (3 if v == 'white' else 4):
          b[ec[1]][ec[0]] = 'P' if v == 'white' else 'p'
          b[sc[1]][ec[0]] = ' '
          b[sc[1]][sc[0]] = ' '
      else:
        return False
    if ec[1] == (4 if v == 'white' else 3):
      epa[v].append(ec[0])
    elif ec[1] == (0 if v == 'white' else 7):
      b[ec[1]][ec[0]] = hpt()
    elif sc[1] == (4 if v == 'white' else 3):
      epa[v].remove(sc[0])
  elif pc.lower() == 'n':
    rap = (ec[0] - sc[0]) * (ec[1] - sc[1])
    if rap!= 2 and rap!=-2: return False
    if b[ec[1]][ec[0]] and ft((ec[0], ec[1])): return False
    else:
      b[ec[1]][ec[0]] = 'N' if v == 'white' else 'n'
      b[sc[1]][sc[0]] = ' '
  elif pc.lower() == 'b':
    mvs = []
    for dire in ddir:
      l = gl(sc, dire)
      next_ca = ap(l[-1] if len(l) else sc, dire)
      if vc(next_ca) and et(next_ca):
        l.append(next_ca)
      mvs.extend(l)
    if tuple(ec) not in mvs:
      return False
    else:
      b[ec[1]][ec[0]] = 'B' if v == 'white' else 'b'
      b[sc[1]][sc[0]] = ' '
  elif pc.lower() == 'r':
    mvs = []
    for dire in sdir:
      l = gl(sc, dire)
      next_ca = ap(l[-1] if len(l) else sc, dire)
      if vc(next_ca) and et(next_ca):
        l.append(next_ca)
      mvs.extend(l)
    if tuple(ec) not in mvs:
      return False
    b[ec[1]][ec[0]] = 'R' if v == 'white' else 'r'
    b[sc[1]][sc[0]] = ' '
    if cstl[v][0] and sc == [0, csr]:
      cstl[v][0] = 0
    if cstl[v][1] and sc == [7, csr]:
      cstl[v][1] = 0
  elif pc.lower() == 'q':
    mvs = []
    for dire in ddir:
      l = gl(sc, dire)
      next_ca = ap(l[-1] if len(l) else sc, dire)
      if vc(next_ca) and et(next_ca):
        l.append(next_ca)
      mvs.extend(l)
    for dire in sdir:
      l = gl(sc, dire)
      next_ca = (l[-1][0] + dire[0], l[-1][1] + dire[1]) if len(l) else (sc[0] + dire[0], sc[1] + dire[1])
      if -1 < next_ca[0] < 8 and -1 < next_ca[1] < 8 and et(next_ca):
        l.append(next_ca)
      mvs.extend(l)
    if tuple(ec) not in mvs:
      return False
    else:
      b[ec[1]][ec[0]] = 'Q' if v == 'white' else 'q'
      b[sc[1]][sc[0]] = ' '
  elif pc.lower() == 'k':
    dire = ec[0] - sc[0], ec[1] - sc[1]
    if dire not in kgps:
      if cstl[v] != [0,0]:
        if cstl[v][1]:
          rook = b[csr][7]
          if ec == [6, csr] and rook.lower() == 'r' and gpc(rook) == v and not st((5,csr)) and not st((6,csr)):
            b[csr][5] = rook
            b[csr][6] = b[sc[1]][sc[0]]
            b[csr][4] = ' '
            b[csr][7] = ' '
            kgs[v] = ec
            if ia((5, csr)) or ia(ec):
              b = svb[:]
              kgs = svkgs[:]
              return False
        if cstl[v][0]:
          rook = b[csr][0]
          if ec[0] == 2 and ec[1] == csr and rook.lower() == 'r' and gpc(rook) == v and not st((1,csr)) and not st((2,csr)) and not st((3,csr)):
            b[csr][4] = ' '
            b[csr][3] = rook
            b[csr][2] = 'K' if v == 'white' else 'k'
            b[csr][0] = ' '
            if ia((3,csr)):
              b = svb[:]
              return False
      else:
        return False
    elif b[ec[1]][ec[0]] and ft((ec[0], ec[1])):
      return False
    else:
      b[ec[1]][ec[0]] = 'K' if v == 'white' else 'k'
      b[sc[1]][sc[0]] = 'K'
      kgs[v] = ec
    cstl[v] = [0,0]
  if ia(kgs[v]):
    b = [[e for e in row] for row in svb]
    epa = svepa.copy()
    cstl = svcstl.copy()
    kgs = svkgs.copy()
    return False
  return True
def hpt():
  pcr = 0
  pcs = 'qrbn'.upper() if v == 'white' else 'qrbn'
  y = 8 if v == 'white' else -1
  for i in range(4):
    dp(8,i,pcs[i])
  while True:
    if kd(KEY_DOWN) and pcr != 3:
      db((y,pcr), 'bg')
      pcr += 1 if v == 'white' else -1
      db((y,pcr), 'seco')
    if kd(KEY_UP) and pcr != 0:
      db((y,pcr), 'bg')
      pcr -= 1 if v == 'white' else -1
      db((y,pcr), 'seco')
    if kd(KEY_OK):
      for i in range(4):
        fc(y,i,'bg')
      return pcs[pcr]
    sp(0.1)
def draw_b():
  for y in range(8):
    for x in range(8):
      fc(x, y, gcc([x, y]))
      if st( (x,y) ):
        dp(x, y, b[y][x])
crs = {
    'white': [4, 6],
    'black': [4, 1]
}
slt = [None, None]
sltd = False
while True:
  draw_b()
  db(crs[v], 'prim')
  current_v = v
  while current_v == v:
    if kd(KEY_LEFT) and crs[v][0] != (0 if v == 'white' else 7):
      if crs[v] != slt:
        db(crs[v], gcc(crs[v]))
      crs[v][0] += -1 if v == 'white' else 1
      if crs[v] != slt:
        db(crs[v], 'prim')
    if kd(KEY_RIGHT) and crs[v][0] != (7 if v == 'white' else 0):
      if crs[v] != slt:
        db(crs[v], gcc(crs[v]))
      crs[v][0] += 1 if v == 'white' else -1
      if crs[v] != slt:
        db(crs[v], 'prim')
    if kd(KEY_UP) and crs[v][1] != (0 if v == 'white' else 7):
      if crs[v] != slt:
        db(crs[v], gcc(crs[v]))
      crs[v][1] += -1 if v == 'white' else 1
      if crs[v] != slt:
        db(crs[v], 'prim')
    if kd(KEY_DOWN) and crs[v][1] != (7 if v == 'white' else 0):
      if crs[v] != slt:
        db(crs[v], gcc(crs[v]))
      crs[v][1] += 1 if v == 'white' else -1
      if crs[v] != slt:
        db(crs[v], 'prim')
    if kd(KEY_OK):
      if sltd:
        if hmv(slt, crs[v]):
          v = 'black' if v == 'white' else 'white'
        else:
          fb(slt, gcc(slt))
          db(crs[v], 'prim')
        sltd = False
        slt = (None, None)
      elif b[crs[v][1]][crs[v][0]] and gpc(b[crs[v][1]][crs[v][0]]) == v:
        slt = crs[v][:]
        sltd = True
        fb(slt, 'prim')
    sp(0.1)
