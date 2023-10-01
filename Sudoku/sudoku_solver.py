import sys; args = sys.argv[1:]
puzzles = open(args[0], 'r').read().splitlines()

import time

def checkSum(pzl):
    return sum(ord(ch) for ch in [*pzl]) - len(pzl)*ord('1')

def findBlanks(choices):
    bestChoices = [(0, 0) for i in range(9)] #each one of form (char, idx)
    for blank in choices:
        if (l := len(choices[blank])) == 1: return [(choices[blank].pop(), blank)] #only one possibility
        if l == 0: return [] #no possibilities
        if l < len(bestChoices): bestChoices = [(ch, blank) for ch in choices[blank]] #if there's a better one, sets new bestchoices
    for i in range(81): #looks thru all constraint sets
        for ch in symbols: #looks thru each char
            ct = 0 #unique positions the char could appear in
            for nbr in gNbrs1[i]:
                if nbr in choices and ch in choices[nbr]: ct += 1 #char could appear here
                if ct>2: continue #breaks out of loop if ct too big
            if ct == 1:
                for nbr in gNbrs1[i]:
                    if nbr in choices and ch in choices[nbr]: return [(ch, nbr)]
            if ct != 0 and len(bestChoices)>ct:
                bestChoices = [(ch, nbr) for nbr in gNbrs1[i] if nbr in choices and ch in choices[nbr]]
    return bestChoices

def fillRCS(): #fills the row, column, subblock table
    for idx in range(81):
        gRCS[0][idx] = {(idx//9)*9+col for col in range(9)}
        gRCS[1][idx] = {idx%9+row*9 for row in range(9)}
        i = idx//(27)*3 + idx%9//3
        block = [[(3*(i//3)+j)*9+i%3*3+d for d in range(3)] for j in range(3)]
        gRCS[2][idx] = set()
        for elem in block:
            for ch in [*elem]:
                gRCS[2][idx].add(ch)

def bruteForce1(pzl): #initial call is different from subsequent calls
    if (blanksleft:=pzl.count('.'))==0: return pzl #puzzle is filled out
    choices = {} #the ones that it can be
    for blank in range(len(pzl)): #sets up the choices dictionary
        if pzl[blank] == '.':
            choices[blank] = {pzl[idx] for idx in gNbrs[blank]} - {'.'}
            choices[blank] = choices[blank] ^ symbols
    for possibles in findBlanks(choices): #finds the best choices
        ch, blank = possibles
        subPzl = ''.join([pzl[:blank], ch, pzl[blank+1:]]) #makes the subpzl
        newChoices = {b:choices[b] for b in choices if b!=blank}
        for nbr in gNbrs[blank]: #removes the char from all its neighbors' choices
            if pzl[nbr] == '.': newChoices[nbr] = newChoices[nbr] - {ch}
        bF = bruteForce(subPzl, blanksleft-1, newChoices) #recursive call
        if bF: return bF
    return "" #no solution

def bruteForce(pzl, blanksleft, choices):
    if blanksleft==0: return pzl #puzzle is filled out
    for possibles in findBlanks(choices): #finds best chocies
        ch, blank = possibles
        subPzl = ''.join([pzl[:blank], ch, pzl[blank+1:]]) #makes subpzl
        newChoices = {b:choices[b] for b in choices if b!=blank}
        for nbr in gNbrs[blank]: #removes the char from all its neighbors' choices
            if pzl[nbr] == '.': newChoices[nbr] = newChoices[nbr] - {ch}
        bF = bruteForce(subPzl, blanksleft-1, newChoices) #recursive call
        if bF: return bF
    return ""

symbols = {*("123456789")}
gRCS = [{}, {}, {}] #lookup table of the form index -> row, column, subblock
fillRCS()
gNbrs = [gRCS[0][idx].union(gRCS[1][idx], gRCS[2][idx])-{idx} for idx in range(81)] #removes element itself
gNbrs1 = [gRCS[0][idx].union(gRCS[1][idx], gRCS[2][idx]) for idx in range(81)] #does not remove element itself

start = time.process_time()
for idx in range(len(puzzles)):
    pzl = puzzles[idx]
    print(f'{idx+1}: {pzl}')
    if idx<9: print(f'   {(solved := bruteForce1(pzl))} {checkSum(solved)} {round(time.process_time()-start, 3)}s')
    elif idx<99: print(f'    {(solved := bruteForce1(pzl))} {checkSum(solved)} {round(time.process_time()-start, 3)}s')
    else: print(f'     {(solved := bruteForce1(pzl))} {checkSum(solved)} {round(time.process_time()-start, 3)}s')

#Luke Wang, pd. 6, 2023