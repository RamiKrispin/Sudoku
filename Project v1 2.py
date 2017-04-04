import os
os.chdir("C:\\Users\\krispra\\Downloads\\Udacity\\AI\\Term 1\\Sudoku - AI")
from utils import *


rows = 'ABCDEFGHI'
cols = '123456789'


# return the units in the sqr box
# inputs r and c the number of row and column
def sqr_units(r,c):
    if r<1 or r>9 or c<1 or c>9: # return false if out of bounds
        return False
    r1 = (r-1)//3 + 1   # finding the square location
    c1 = (c-1)//3 + 1
    b_r = [chr(r1 * 3 -2 + 64) , chr(r1 * 3 -1 + 64) , chr(r1 * 3 + 64 )] # transform back the rows into letters
    b_c = [(c1 * 3 - 2), (c1 * 3 - 1), (c1 * 3)] # transform back the rows into numbers
    sqr_u = []
    for i in b_r:
        for l in b_c:
            sqr_u.append(i + str(l)) # combine together the possible rows and cols in the square
    return(sqr_u)

# return the row's indices
def new_row(r):
    if r<1 or r>9:
        return False
    new_row = []
    for i in range(1,10):
        new_row.append(chr(r +64)+str(i))
    return(new_row)
# return the column's indices
def new_col(c):
    if c<1 or c>9:
        return False
    new_col = []
    for i in range(1,10):
        new_col.append(chr(i +64)+str(c))
    return(new_col)

# Create a peer list
def peer_units(r,c):
    unit = chr(r + 64) + str(c)
    peer = new_row(r) + new_col(c) + sqr_units(r,c)
    peer.remove(unit)
    return(peer)

# define the diagonal's indices
diag_a = []
for i in cols:
    a = chr(int(i) + 64) + i
    diag_a.append(a)

diag_b = []
for i in range(1,len(rows[::-1])+1):
    diag_b.append(rows[::-1][i-1] + str(i))


def naked_twins(values):
    x = dict(values)
    for i in (row_units + column_units):
        reverse_dict = {}
        for l in i:
            reverse_dict[values[l]] = reverse_dict.get(values[l], [])
            reverse_dict[values[l]].append(l)
        for key,value in reverse_dict.items():
            if len(key)>1 and len(key) == len(value):
                digits_remove = key
                for n in i:
                    if len(x[n]) >  len(digits_remove) and digits_remove in x[n]:
                        x[n] = x[n].replace(digits_remove,"")
    return x
            

            




def elim(x):
    for k,v in x.items():
            if len(v) >= 2:
                if k in diag_a and k in diag_b: # check if the current box in both the first and second diag
                    r = ord(str.lower(k[0]))-96 
                    c = int(k[1])
                    peer = list(peer_units(r, c) ) + diag_a + diag_b
                    peer = list(set(peer))
                    peer.remove(k)
                elif k in diag_a and k not in diag_b: # check if the current box in the first diag
                    r = ord(str.lower(k[0]))-96 
                    c = int(k[1])
                    peer = list(peer_units(r, c) ) + diag_a 
                    peer = list(set(peer))
                    peer.remove(k)                   
                elif k in diag_b and k not in diag_a: # check if the current box in the second diag
                    r = ord(str.lower(k[0]))-96 
                    c = int(k[1])
                    peer = list(peer_units(r, c) ) + diag_b 
                    peer = list(set(peer))
                    peer.remove(k)
                elif k not in diag_a and k not in diag_b: # not in one of the diags
                    r = ord(str.lower(k[0]))-96 
                    c = int(k[1])
                    peer = list(peer_units(r, c))
                    peer = list(set(peer))
                    peer.remove(k)
                d = {key:value for key, value in x.items() if key in peer and len(v) == len(value) and key != k and v == value}
                
                if len(v) <=  len(d) + 1:
                    
                    peer2 = peer.copy()
                    for k1,v1 in d.items():
                        peer2.remove(k1)
                        
                        for i in v:
                            for l in peer2:
                                if i in x[l]:
                                    x[l] = x[l].replace(i, "")
    return(x)


                        
def diag_puzzle_reduce(x):
    stalled = False
    while not stalled:
        # calculate the len of all the values in the boxes, to compare with the length after the reduce
        before = 0
        for k3,v3 in x.items():
            before = before + len(v3)
        # defining the peers for the cases there more than one number in the box
        for k,v in x.items():
            if len(v) == 1:
                if k in diag_a and k in diag_b: # check if the current box in both the first and second diag
                    r = ord(str.lower(k[0]))-96 
                    c = int(k[1])
                    peer = list(peer_units(r, c) ) + diag_a + diag_b
                    peer = list(set(peer))
                    peer.remove(k)                    
                elif k in diag_a and k not in diag_b: # check if the current box in the first diag
                    r = ord(str.lower(k[0]))-96 
                    c = int(k[1])
                    peer = list(peer_units(r, c) ) + diag_a 
                    peer = list(set(peer))
                    peer.remove(k)  
                elif k in diag_b and k not in diag_a: # check if the current box in the second diag
                    r = ord(str.lower(k[0]))-96 
                    c = int(k[1])
                    peer = list(peer_units(r, c) ) + diag_b 
                    peer = list(set(peer))
                    peer.remove(k)
                elif k not in diag_a and k not in diag_b: # not in one of the diags
                    r = ord(str.lower(k[0]))-96 
                    c = int(k[1])
                    peer = list(peer_units(r, c))
                    peer = list(set(peer))
                    peer.remove(k)
                
                d = {key:value for key, 
                     value in x.items() if 
                     key in peer and
                     key != k and 
                     len(value) > 1 and 
                     v in value}
                if len(d) > 0:
                    print(d)
                    for k1,v1 in d.items():
                        x[k1] = x[k1].replace(v,"")
                    d.clear()
        after = 0
        for k2,v2 in x.items():
            after = after + len(v2)
        stalled = after == before 
        for k3,v3 in x.items():
            if v3 == '':
                return False
    return(x)                    
        
 
                        
                        
        


test = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3' 
x1 = grid_values(test)
display(x1)
x2 = x1.copy()
x2 = diag_puzzle_reduce(x2)
display(x2)
#x = x2.copy()
x3 = x2.copy()
x3 = elim(x3)
display(x3)
x4 = x3.copy()
x4 = diag_puzzle_reduce(x4)
display(x4)
x5 = x4.copy()
x5 = elim(x5)
display(x5)
x6 = x5.copy()
x6 = diag_puzzle_reduce(x6)
display(x6)


def search_diag(values):
    values = diag_puzzle_reduce(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    print(n,s)
    for i in range(2,10):
        print(i)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search_diag(new_sudoku)
        if attempt:
            return attempt

x7 = search_diag(x2)
display(x7)
