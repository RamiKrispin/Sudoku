import os
os.chdir("C:\\Users\\krispra\\Downloads\\Udacity\\AI\\Term 1\\AI - Sudoku")
from utils import *


rows = 'ABCDEFGHI'
cols = '123456789'

unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])




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

diag_a = []
for i in cols:
    a = chr(int(i) + 64) + i
    diag_a.append(a)

diag_b = []
for i in range(1,len(rows[::-1])+1):
    diag_b.append(rows[::-1][i-1] + str(i))


def eliminate(values):
    def mini_elim(values, unit_list):
        for i in unit_list:
            if len(values[i]) == 1:
                peer_unit = unit_list[:]
                peer_unit.remove(i)
                for n in peer_unit:
                    if values[i] in values[n] and len(values[n]) > 1:
                        values[n] = values[n].replace(values[i], "")
        return(values)
    
    values = mini_elim(values, diag_a)
    values = mini_elim(values, diag_b)
    for i in row_units:
        values = mini_elim(values,i)
    for i in column_units:
        values = mini_elim(values,i)
    for i in square_units:
        values = mini_elim(values,i)
    return(values)


def naked_twins(values):
    for i in row_units + column_units:
        for l in i:
            unit = i[:]
            unit.remove(l)
            unit1 = unit[:]
            v = values[l]
            counter = 1
            if len(v) > 1:
                for u in unit:
                    if v == values[u]:
                        unit1.remove(u)
                        counter += 1
            if len(v) == counter:
                for r in unit1:
                    for n in v:
                        if n in values[r] and len(values[r]) > 1:
                            values[r] = values[r].replace(n, "")
    return(values)        


# This function apply the naked twins method on the diag
def diag_naked_twins(diag, x):
    for i in diag:
        if len(x[i]) > 1:
            unit = diag[:]
            unit.remove(i)
            unit1 = unit[:]
            counter = 1
            for u in unit:
                if x[i] == x[u]:
                    unit1.remove(u)
                    counter +=1
            if len(x[i]) == counter:
                for r in unit1:
                    for n in x[i]:
                        if n in x[r] and len(x[r]) > 1:
                            x[r] = x[r].replace(n,"")
    return(x)



def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
    

# Testing the functions
values = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'                        
values = grid_values(values) 
display(values)
values = eliminate(values)
display(values)
values = diag_naked_twins(diag_a, values)
values = diag_naked_twins(diag_b, values)
values = only_choice(values)
values = naked_twins(values)
display(values)

def reduce(values):
    end = False
    while not end:
        before = 0
        for k,v in values.items():
            before = before + len(v)  
        values = eliminate(values)
        values = diag_naked_twins(diag_a, values)
        values = diag_naked_twins(diag_b, values)
        values = naked_twins(values)
        values = only_choice(values)
        display(values)
        after = 0
        for k1,v1 in values.items():
            after = after + len(v1)
        if after == before:
            end = True
    return(values)
# Testing the  reduce function
values = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'                        
values = grid_values(values) 
display(values)
values = reduce(values)
display(values)


                    
    
# this function validate the units numbers       
def validation(values):
    all_units = row_units + column_units + diag_a + diag_b 
    for u in all_units:
        d = "123456789"
        for i in u:
            if values[i] in d:
                d = d.replace(values[i],"")
        if len(d) != 0:
            return(False)
 
def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        valid = validation(values)
        if attempt and valid:
            return attempt
		

values = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'                        
values = grid_values(values) 
display(values)
values = search(values)
display(values)





