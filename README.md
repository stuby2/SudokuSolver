Sudoku Solver (studoku.py)

Works with a solver and - if needed - a predictor to fill puzzles from either p096_sudoku.txt (from Project Euler) 
or from user input. The program populates lists of 'cans' (values that can go in an empty cell) and then the solver,
predictor and add_update methods work to whittle those lists down to one value: the correct value for that cell.

The solver is called repeatedly until it can't find any new numbers, then the predictor starts by checking cans lists
of length 2 (incremented until a solution is found) and testing each value in that list to learn information. 

Updates to come: Include a back up solver with advanced techniques. Switch the cells list of 81 lists to a pandas data frame.


