import sys; args = sys.argv[1:]
# Luke Wang
from time import process_time
r1 = [70,0,20,15,15,20,0,70, 0,-8,-2,0,0,-2,-8,0, 20,-2,2,1.5,1.5,2,-2,20, 15,0,1.5,-1,-1,1.5,0,15]
gameEval = r1 + r1[::-1]
openings = {'...........................ox......xo...........................': 37,
   '...........................ox......xxx..........................': 43, #perfect
   '...........................ox......oxx.....o....................': 26,
   '..........................xxx......oxx.....o....................': 19,
   '...................o......xox......oxx.....o....................': 18,
   '..................xo......xxx......oxx.....o....................': 29,
   '..................xo......xxxo.....oox.....o....................': 34,
   '..................xo......xxxo....xxxx.....o....................': 17,
   '.................ooo......xxxo....xxxx.....o....................': 10,
   '..........x......oxx......xxxo....xxxx.....o....................': 25,
   '..........x......oxx.....ooooo....oxxx.....o....................': 20,
   '..........x......oxxx....oooxo....oxxx.....o....................': 44,
   '..........x......oxxx....oooxo....ooxx.....oo...................': 42,
   '..........x......oxxx....oxoxo....xxxx....xoo...................': 45,
   '..........x......oxxx....oxoxo....xxoo....xooo..................': 32,
   '..........x......oxxx....xxoxo..x.xxoo....xooo..................': 24,
   '....................o.....xxo......xx........x..................': 44, #perp -> diag
   '....................o.....xxo......xo.......ox..................': 37,
   '....................o.....xxo......xxx......ox..................': 34,
   '....................o.....xoo.....oxxx......ox..................': 29,
   '....................o.....xxxx....oxxx......ox..................': 46,
   '....................o.....xxxx....oxxx......ooo.................': 53,
   '....................o.....xxxx....oxxx......xxo......x..........': 43,
   '....................o.....xxxx....oxxx.....oooo......x..........': 52,
   '....................o.....xxxo....ooooo.....xxo......x..........': 43,
   '...................oo.....xxox....oxxo......xxo......x..........': 21,
   '....................o.....xxo......xxo......ooo.................': 21, #aubrey-tanaka
   '....................o....oooo......xx........x..................': 21, #bent ganglion
   '....................o....oooo......xxx..........................': 21, #ganglion/no-cat
   '....................ox...ooox......xxx..........................': 29,
   '..........................xxx.....ooo...........................': 43, #parallel
   '..................o.......xox......xo...........................': 19,
   '..................ox......xxx......xo...........................': 34,
   '..................ox......oxx.....ooo...........................': 25, #heath
   '..................ox.....xxxx.....ooo...........................': 11,
   '...........o......oo.....xxox.....ooo...........................': 43,
   '...........o......oo.....xxox.....xoo......x....................': 17, #bat
   '..................ooo....xxoo.....ooo...........................': 12, #chimney
   '...........ox.....ox.....xxox.....ooo...........................': 17, #iwasaki
   '..................ox......oxx.....ooo...........................': 43, #cow
   '..................ooo.....ooo.....oxo......x....................': 21, #chimney
   '..................ox......oxx.....oxo......x....................': 29, #cow+
   '..................ox.....xoooo....xxo......x....................': 41, #bat
   '..................ox......oooo....oxo......x....................': 37, #rose v toth
   '..................ox......ooxo....oxxx.....x....................': 11,
   '...........o......oo......ooxo....oxxx.....x....................': 21, #tanida
   '...........o......oo......ooxo...xxxxx.....x....................': 42} #aircraft/feldborg
def findMvs(brd, tkn):
   mvsPsbl = [False for i in range(64)]
   for i in range(64):
      if brd[i] != '.': continue
      if i>=8 and brd[i-8] not in {tkn, '.'}:
         psbl = False
         for k in range(i-8, -1, -8):
            if brd[k] == tkn: psbl = True
            if brd[k] == '.' or psbl: break
         mvsPsbl[i] = psbl
      if mvsPsbl[i]: continue
      if i<56 and brd[i+8] not in {tkn, '.'}:
         psbl = False
         for k in range(i+8, 64, 8):
            if brd[k] == tkn: psbl = True
            if brd[k] == '.' or psbl: break
         mvsPsbl[i] = psbl
      if mvsPsbl[i]: continue
      if i%8!=0 and brd[i-1] not in {tkn, '.'}:
         psbl = False
         for k in range(i-1, 8*(i//8)-1, -1):
            if brd[k] == tkn: psbl = True
            if brd[k] == '.' or psbl: break
         mvsPsbl[i] = psbl
      if mvsPsbl[i]: continue
      if i%8!=7 and brd[i+1] not in {tkn, '.'}:
         psbl = False
         for k in range(i+1, 8*(i//8)+8, 1):
            if brd[k] == tkn: psbl = True
            if brd[k] == '.' or psbl: break
         mvsPsbl[i] = psbl
      if mvsPsbl[i]: continue
      if i%8!=0 and i>=8 and brd[i-9] not in {tkn, '.'}:
         psbl = False
         k = i-9
         while k%8!=7 and k>=0:
            if brd[k] == tkn: psbl = True
            if brd[k] == '.' or psbl: break
            k -= 9
         mvsPsbl[i] = psbl
      if mvsPsbl[i]: continue
      if i%8!=7 and i<56 and brd[i+9] not in {tkn, '.'}:
         psbl = False
         k = i+9
         while k%8!=0 and k<64:
            if brd[k] == tkn: psbl = True
            if brd[k] == '.' or psbl: break
            k += 9
         mvsPsbl[i] = psbl
      if mvsPsbl[i]: continue
      if i%8!=0 and i<56 and brd[i+7] not in {tkn, '.'}:
         psbl = False
         k = i+7
         while k%8!=7 and k<64:
            if brd[k] == tkn: psbl = True
            if brd[k] == '.' or psbl: break
            k += 7
         mvsPsbl[i] = psbl
      if mvsPsbl[i]: continue
      if i%8!=7 and i>=8 and brd[i-7] not in {tkn, '.'}:
         psbl = False
         k = i-7
         while k%8!=0 and k>=0:
            if brd[k] == tkn: psbl = True
            if brd[k] == '.' or psbl: break
            k -= 7
         mvsPsbl[i] = psbl
      if mvsPsbl[i]: continue
   return {i for i in range(64) if mvsPsbl[i]}
def makeMove(brd, tkn, mv):
   brd = [*brd]
   enemy = 'xo'[tkn=='x']
   brd[mv] = tkn
   if mv>=16:
      for i in range(mv-8, -1, -8):
         if brd[i]==tkn:
            for j in range(i, mv, 8): brd[j] = tkn
         if brd[i]!=enemy: break
   if mv<48:
      for i in range(mv+8, 64, 8):
         if brd[i]==tkn:
            for j in range(i, mv, -8): brd[j] = tkn
         if brd[i]!=enemy: break
   if mv%8>=2:
      for i in range(mv-1, mv//8*8-1, -1):
         if brd[i]==tkn:
            for j in range(i, mv, 1): brd[j] = tkn
         if brd[i]!=enemy: break
   if mv%8<6:
      for i in range(mv+1, mv//8*8+8, 1):
         if brd[i]==tkn:
            for j in range(i, mv, -1): brd[j] = tkn
         if brd[i]!=enemy: break
   if mv%8>=2 and mv>=16:
      i = mv-9
      while i%8!=7 and i>=0:
         if brd[i]==tkn:
            for j in range(i, mv, 9): brd[j] = tkn
         if brd[i]!=enemy: break
         i -= 9
   if mv%8<6 and mv<48:
      i = mv+9
      while i%8!=0 and i<64:
         if brd[i]==tkn:
            for j in range(i, mv, -9): brd[j] = tkn
         if brd[i]!=enemy: break
         i += 9
   if mv%8>=2 and mv<48:
      i = mv+7
      while i%8!=7 and i<64:
         if brd[i]==tkn:
            for j in range(i, mv, -7): brd[j] = tkn
         if brd[i]!=enemy: break
         i += 7
   if mv%8<6 and mv>=16:
      i = mv-7
      while i%8!=0 and i>=0:
         if brd[i]==tkn:
            for j in range(i, mv, 7): brd[j] = tkn
         if brd[i]!=enemy: break
         i -= 7
   return ''.join(brd)
def quickMove(brd, tkn):
   psbls = findMvs(brd, tkn)
   if not psbls: return -1
   if psbls.intersection({0,7,56,63}): return psbls.intersection({0,7,56,63}).pop()
   greatMvs = findSafeMove(brd, tkn, psbls)
   if greatMvs: return greatMvs.pop()
   optkn = 'xo'[tkn=='x']
   mvs = []
   goodMvs = {2,3,4,5, 16,24,32,40, 23,31,39,47, 58,59,60,61}
   riskyMvs = {10,11,12,13, 17,25,33,41, 22,30,38,46, 50,51,52,53}
   for mv in psbls-{1,8,9, 6,14,15, 48,49,57, 54,55,62}:
      newBrd = makeMove(brd, tkn, mv)
      opPsbl = findMvs(newBrd, optkn)
      opScore = len(opPsbl)
      if mv in goodMvs: opScore -= 1.2
      if mv in riskyMvs: opScore -= 0.1
      for opMv in opPsbl:
         if opMv in {0,7,56,63} | findSafeMove(newBrd, optkn, opPsbl): opScore += 8
      mvs.append((opScore, mv))
   if mvs: return min(mvs)[1]
   for mv in psbls:
      newBrd = makeMove(brd, tkn, mv)
      opPsbl = findMvs(newBrd, optkn)
      opScore = len(opPsbl)
      for opMv in opPsbl:
         if opMv in {0,7,56,63} | findSafeMove(newBrd, optkn, opPsbl): opScore += 8
      if mv in {9,14,49,54}: opScore += 1.1
      mvs.append((opScore, mv))
   return min(mvs)[1]
def findSafeMove(brd, tkn, psbls):
   sfs = set()
   optkn = 'xo'[tkn=='x']
   if brd[0]==tkn:
      flpn = False
      for i in range(8):
         if flpn and brd[i]!=optkn:
            if brd[i]=='.': sfs.add(i)
            break
         if brd[i]==optkn: flpn = True
         if brd[i]=='.':
            if i in psbls: sfs.add(i)
            break
      flpn = False
      for i in range(0,64,8):
         if flpn and brd[i]!=optkn:
            if brd[i]=='.': sfs.add(i)
            break
         if brd[i]==optkn: flpn = True
         if brd[i]=='.':
            if i in psbls: sfs.add(i)
            break
      if 9 in psbls: sfs.add(9)
   if brd[7]==tkn:
      flpn = False
      for i in range(7,-1,-1):
         if flpn and brd[i]!=optkn:
            if brd[i]=='.': sfs.add(i)
            break
         if brd[i]==optkn: flpn = True
         if brd[i]=='.':
            if i in psbls: sfs.add(i)
            break
      flpn = False
      for i in range(7,64,8):
         if flpn and brd[i]!=optkn:
            if brd[i]=='.': sfs.add(i)
            break
         if brd[i]==optkn: flpn = True
         if brd[i]=='.':
            if i in psbls: sfs.add(i)
            break
      if 14 in psbls: sfs.add(14)
   if brd[56]==tkn:
      flpn = False
      for i in range(56,64):
         if flpn and brd[i]!=optkn:
            if brd[i]=='.': sfs.add(i)
            break
         if brd[i]==optkn: flpn = True
         if brd[i]=='.':
            if i in psbls: sfs.add(i)
            break
      flpn = False
      for i in range(56,-1,-8):
         if flpn and brd[i]!=optkn:
            if brd[i]=='.': sfs.add(i)
            break
         if brd[i]==optkn: flpn = True
         if brd[i]=='.':
            if i in psbls: sfs.add(i)
            break
      if 49 in psbls: sfs.add(49)
   if brd[63]==tkn:
      flpn = False
      for i in range(63,55,-1):
         if flpn and brd[i]!=optkn:
            if brd[i]=='.': sfs.add(i)
            break
         if brd[i]==optkn: flpn = True
         if brd[i]=='.':
            if i in psbls: sfs.add(i)
            break
      flpn = False
      for i in range(63,-1,-8):
         if flpn and brd[i]!=optkn:
            if brd[i]=='.': sfs.add(i)
            break
         if brd[i]==optkn: flpn = True
         if brd[i]=='.':
            if i in psbls: sfs.add(i)
            break
      if 54 in psbls: sfs.add(54)
   return sfs
def orderMoves(brd, tkn, psbls):
   ordered = []
   for mv in psbls.intersection({0,7,56,63}):
      ordered.append(mv)
      psbls.remove(mv)
   for mv in findSafeMove(brd, tkn, psbls):
      if mv in {0,7,56,63}: continue
      ordered.append(mv)
      psbls.remove(mv)
   for mv in psbls-{1,8,9, 6,14,15, 48,49,57, 54,55,62}:
      ordered.append(mv)
      psbls.remove(mv)
   for mv in psbls: ordered.append(mv)
   return ordered

def alphabeta(brd, tkn, alpha, beta, level):
   psbls = findMvs(brd, tkn)
   optkn = 'xo'[tkn=='x']
   if not psbls:
      if not findMvs(brd, optkn):
         return {-1: - brd.count(tkn) + brd.count(optkn)}
      return {-1:-1*max(alphabeta(brd, optkn, -beta, -alpha, level-1).values())}
   best = -1
   if level>5: #can change around; low levels don't need to order
      psbls = orderMoves(brd, tkn, psbls)
   for move in psbls:
      score = -list(alphabeta(makeMove(brd,tkn,move), optkn, -beta, -alpha, level-1).values())[0]
      if score > alpha:
         alpha = score
         best = move
      if alpha >= beta: break
   return {best:alpha}
def getABMove(alphabetaRaw):
   mvs = alphabetaRaw
   bestscore = max([mvs[mv] for mv in mvs])
   for mv in mvs:
      if mvs[mv]==bestscore: return mv
def midgameAB(brd, tkn, alpha, beta, level):
   psbls = findMvs(brd, tkn)
   optkn = 'xo'[tkn=='x']
   if not psbls:
      if not findMvs(brd, optkn):
         return {-1: 999*(brd.count(tkn)-brd.count(optkn))}
      return {-1:-1*max(midgameAB(brd, optkn, -beta, -alpha, level-1).values())}
   if level <= 1:
      score = soloMidgameScore(brd, tkn)-soloMidgameScore(brd, optkn)
      mM,oM = len(psbls), len(findMvs(brd, optkn))
      score += 70*(mM-oM)/(mM+oM)
      return {-1: -score}
   if level>=3: psbls = orderMoves(brd, tkn, psbls)
   best = -1
   for mv in psbls:
      score = -list(midgameAB(makeMove(brd,tkn,mv), optkn, -beta, -alpha, level-1).values())[0]
      if score > alpha:
         alpha = score
         best = mv
      if alpha >= beta: break
   return {best:alpha}
def soloMidgameScore(brd, tkn):
   score = 0
   for i in range(64):
      if brd[i]==tkn:
         score += 0.075*gameEval[i]+(-5+2*(brd.count('.')<=36)+5*(brd.count('.')<=20))*0.17
   #if not 'xo'[tkn=='x'] in {brd[0], brd[7], brd[56], brd[63]}: #idea: make this dependent on which corners have been taken (ex. 0 and 7 empty? weigh those more heavily)
   edges = {1,2,3,4,5,6, 8,16,24,32,40,48, 15,23,31,39,47,55, 57,58,59,60,61,62}
   score += 1.2*len([i for i in edges if brd[i] == tkn])
   #if 'xo'[tkn=='x'] in {brd[0], brd[7], brd[56], brd[63]}: score -= 0.7*len([i for i in edges if brd[i] == tkn])
   if brd[0] == tkn:
      score += 29
      if brd[9]==tkn: score += 5.5
      if brd[1]==tkn or brd[8]==tkn: score += 2
   elif brd[0] == '.':
      if brd[9]==tkn: score -= 6
      if brd[1]==tkn or brd[8]==tkn: score -= 2.5
   if brd[7] == tkn:
      score += 29
      if brd[14]==tkn: score += 5.5
      if brd[15]==tkn or brd[6]==tkn: score += 2
   elif brd[7] == '.':
      if brd[14]==tkn: score -= 6
      if brd[15]==tkn or brd[6]==tkn: score -= 2.5
   if brd[56] == tkn:
      score += 29
      if brd[49]==tkn: score += 5.5
      if brd[57]==tkn or brd[48]==tkn: score += 2
   elif brd[56] == '.':
      if brd[49]==tkn: score -= 6
      if brd[57]==tkn or brd[48]==tkn: score -= 2.5
   if brd[63] == tkn:
      score += 29
      if brd[54]==tkn: score += 5.5
      if brd[62]==tkn or brd[55]==tkn: score += 2
   elif brd[63] == '.':
      if brd[54]==tkn: score -= 6
      if brd[62]==tkn or brd[55]==tkn: score -= 2.5
   return score

def flip(brd): #board, width; flips across horizontal middle
    #height = len(brd)//w
   w = 8
   brdLst = [brd[i:i+w] for i in range(0,len(brd), w)]
   brdLst = brdLst[::-1]
   brd = ''.join(brdLst)
   return brd
def rotate90(brd):
   w = 8
   sections, final = [], ''
   h = 8
   for x in range(h):
      sections.append(brd[w*x:w*x+w])
   sections = sections[::-1]
   for char in range(len(sections[0])):
      for section in sections:
         final += section[char]
   return final
def rotate180(brd):
   return brd[::-1]
def checkBook(brd):
   for i in range(8):
      rotated = brd
      if i%2==1: rotated = rotate90(rotated)
      if i in {2,3,6,7}: rotated = rotate180(rotated)
      if i>=4: rotated = flip(rotated)
      if rotated in openings: #apply the same transformations
         move = openings[rotated]
         rotated = ''.join([rotated[:move], 'A', rotated[move+1:]])
         if i%2==1: rotated = rotate90(rotated)
         if i in {2,3,6,7}: rotated = rotate180(rotated)
         if i>=4: rotated = flip(rotated)
         return rotated.find('A')
   return False
class Strategy:
   logging = True
   def best_strategy(self, board, player, best_move, still_running, time_limit):
      t = process_time()
      score = soloMidgameScore(board, player)-soloMidgameScore(board, 'xo'[player=='x'])
      mM,oM = len(findMvs(board, player)), len(findMvs(board, 'xo'[player=='x']))
      print(f'Current evaluation: {round(score + 50*(mM-oM)/(mM+oM), 2)}')
      best_move.value = quickMove(board, player)
      #if board.count('.')>=45:
         #if (mv := checkBook(board)):
         #   print(f'Found move via opening book in {round(1000*(process_time()-t))}ms')
         #   best_move.value = mv
         #   return
      if board.count('.')<17 and 4**(board.count('.')-14)*8 <= time_limit:
         if (l := board.count('.'))>7:
            mgAB = midgameAB(board, player, -2000, 2000, 7)
            best_move.value = getABMove(mgAB)
            print(f'Midgame level 7: {round(process_time()-t, 2)}s')
            print(f'Evaluation: {round(mgAB[getABMove(mgAB)], 2)}')
         
         if l>7: print(f'Trying endgame on level {l}')
         best_move.value = getABMove(alphabeta(board, player, -65, 65, board.count('.')))
         if l>7: print(f'Level {l}: {round(process_time()-t, 2)}s')
         return
      midgameABval = 3 #iterative deepening
      while still_running.value:
         mgAB = midgameAB(board, player, -2000, 2000, midgameABval)
         best_move.value = getABMove(mgAB)
         print(f'Midgame level {midgameABval}: {round(process_time()-t, 2)}s')
         print(f'Evaluation: {round(mgAB[getABMove(mgAB)], 2)}')
         midgameABval += 1
      return
        
#Luke Wang, pd. 6, 2023