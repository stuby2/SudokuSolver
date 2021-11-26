## Sudoku Solver ## by stu
import copy 
# Global Variable #
nums_added = 0

def print_puzzle(cells):
	# function to *neatly* print puzzle to console
	for lv1 in range(9):
		if lv1 == 3 or lv1 == 6:
			print("-"*21)
		for lv2 in range(9):
			if lv2 == 3 or lv2 == 6:
				print("|", end=" ")
			if cells[lv2 + lv1*9][3] == 0:
				print(" ", end=" ")
			else:
				print(cells[lv2 + lv1*9][3], end=" ")
		print(' ')
	return

def puzzle_in(lines):

	x = [[0]*9]*9

	print("Which puzzle do you want me to solve?")
	entry = input("Enter 2-digit number from 01 to 50 (00 to manually input puzzle): ")
	while len(entry) != 2 or int(entry) > 50:
		entry = input("Try again: ")
	
	if entry == '00': 
		puzzle_title = 'User Given Puzzle'
		print("Manual Entry. Enter 9 digit lines with zeros as placeholders.\n")
		for i in range(9):
			man_in = input()
			x[i] = list(man_in[0:9])
			for j in range(9):
				x[i][j] = int(x[i][j])

	else: # Find puzzle user asked for and copy it to x
		puzzle_title = 'Grid ' + entry + '\n'
		puzzle_loc = lines.index(puzzle_title) + 1

		for i in range(9):
			x[i] = list(lines[puzzle_loc+i][0:9])
			for j in range(9):
				x[i][j] = int(x[i][j])

	return x, puzzle_title 

def which_box(row,col):
	if row <= 2:
		if col <= 2:
			return [0,0]
		elif col > 2 and col <= 5:
			return [0,1]
		else:
			return [0,2]
	elif row > 2 and row <= 5:
		if col <= 2:
			return [1,0]
		elif col > 2 and col <= 5:
			return [1,1]
		else:
			return [1,2]
	else:
		if col <= 2:
			return [2,0]
		elif col > 2 and col <= 5:
			return [2,1]
		else:
			return [2,2]

def populate_cans(cells):
	possibleNums = {1,2,3,4,5,6,7,8,9}

	for cell in cells:
		cants = set()
		if cell[3]: continue
		for lv1 in range(81):
			if not cells[lv1][3]:
				continue
			elif cells[lv1][0] == cell[0]:
				cants.add(cells[lv1][3])
			elif cells[lv1][1] == cell[1]:
				cants.add(cells[lv1][3])
			elif cells[lv1][2] == cell[2]:
				cants.add(cells[lv1][3])
		cans = possibleNums - cants
		cell[4] = cans 

	return cells

def predictor(cells, z, steps=False):
	# input("Press Enter to Launch Predictor")
	print("## LAUNCHING PREDICTOR ##")
	# print(f"Cans set length is {z}.")
	global nums_added
	# Solves by trial and error

	for cell in cells:
		nums_added = 0
		nums_removed = 0
		if len(cell[4]) == z:
			put_back = set()
			for i in range(z):
				attempt = cell[4].pop()
				if steps:
					print(f"Will try {attempt} at ({cell[0]},{cell[1]}).")
					input()
				
				try: # Running into an error means this value is incorrect.
					copy1, notSolved = add_update(cells, cell[0], cell[1], cell[2], attempt, pre=True)			
					if not notSolved:
						print("Solved by Predictor.")
						return copy1, True

					else: # We don't know if the value is right or wrong.
						put_back.add(attempt) 
						if steps:
							print("Inconclusive.")
						continue 
				except: # Value is wrong, leave it out.
					nums_added = 0
					nums_removed += 1
			cell[4] = put_back
		
		if nums_removed:
			# No longer predictions, we can update cell data.
			if len(cell[4]) == 1:
				new_val = cell[4].pop()
				copy1, notSolved = add_update(cells, cell[0], cell[1], cell[2], new_val)
				print(f"Predictor didn't solve but added {nums_added} numbers.")
				return solver(copy1, steps) # Not solved because it would've in line 115 
			
			else: # We've removed values from cells that weren't correct.
				print("Got some info.")
				solver(cells, steps)
				continue # This is unneccessary, for now.
	
	return cells, False 

def solver(cells, steps=False):
	print("## LAUNCHING SOLVER ##")
	global nums_added
	# Go through rows, columns, and boxes to see
	# if any number is only in one set of cans
	notSolved = True

	# ROWS #
	for row in range(9):
		missing_nums = set()
		for col in range(9):
			idx = col + row*9
			if cells[idx][3]:continue
			missing_nums.update(cells[idx][4])
		for num in missing_nums:
			count = 0
			for col in range(9):
				idx = col + row*9
				if cells[idx][3]: continue
				if num in cells[idx][4]:
					new_row = cells[idx][0]
					new_col = cells[idx][1]
					new_box = cells[idx][2]
					count += 1
			if steps:
				print(f"Row {row}: The number {num} can go in {count} spot(s).")
				input()
			if count == 1:
				cells, notSolved = add_update(cells, new_row, new_col, new_box, num)
				if not notSolved:
					print("Solved.")
					return cells, True

	# COLUMNS #
	for col in range(9):
		missing_nums = set()
		for row in range(9):
			idx = col + row*9
			if cells[idx][3]: continue
			missing_nums.update(cells[idx][4])
		for num in missing_nums:
			count = 0
			for row in range(9):
				idx = col + row*9
				if cells[idx][3]: continue
				if num in cells[idx][4]:
					new_row = cells[idx][0]
					new_col = cells[idx][1]
					new_box = cells[idx][2]
					count += 1
			if steps:
				print(f"Column {col}: The number {num} can go in {count} spot(s).")
				input()
			if count == 1:
				cells, notSolved = add_update(cells, new_row, new_col, new_box, num)
				if not notSolved:
					print("Solved.")
					return cells, True

	# BOXES # 
	for lv1 in range(3):
		for lv2 in range(3):
			missing_nums = set()
			cells_in_box = []
			for cell in cells:
				if cell[3]: continue
				if cell[2] == [lv1, lv2]:
					missing_nums.update(cell[4])
					cells_in_box.append(cell)
			for num in missing_nums:
				count = 0
				for cell in cells_in_box:
					if num in cell[4]:
						new_row = cell[0]
						new_col = cell[1]
						new_box = cell[2]
						count += 1
				if steps:
					print(f"Box ({lv1},{lv2}): The number {num} can go in {count} spot(s).")
					input()
				if count == 1:
					cells, notSolved = add_update(cells, new_row, new_col, new_box, num)
				if not notSolved:
					print("Solved.")
					return cells, True

	return cells, not notSolved

def add_update(cells, row, col, box, value, pre=False):
	global nums_added
	copy_0 = copy.deepcopy(cells)
	# ADD NEW VALUE #
	copy_0[col + row*9][3] = value
	copy_0[col + row*9][4] = set()
	nums_added += 1
	# print(f"Added a {value} at ({row},{col}).")
	# input()

	# UPDATE AFFECTED CANS SETS #
	for cell in copy_0:
		if cell[3]:continue	
		
		# Discard value from cans set
		if cell[0] == row or cell[1] == col or cell[2] == box:
			cell[4].discard(value)
	
	# Check if any cans set has length 1 and recurse if so.
	notSolved = 0
	for cell in copy_0:
		if cell[3]: continue		
		notSolved += 1
		if len(cell[4]) == 1:
			new_row = cell[0]
			new_col = cell[1]
			new_box = cell[2]
			new_val = cell[4].pop()
			# print(f"Cans set at ({new_row},{new_col}) reduced to one value.")
			# input()
			return add_update(copy_0, new_row, new_col, new_box, new_val, pre)

		# For predictor #
		if (len(cell[4]) == 0) and pre:
			# print("This number can't go here.")
			return ValueError

	return copy_0, notSolved

def main():
	global nums_added
	# Gather puzzles from file and ask for user input

	## NOTE: Studoku can solve all but one puzzle (#49) from file. ##
	infile = open('p096_sudoku.txt','r')
	lines = infile.readlines()
	infile.close()	

	x, puzzle_title = puzzle_in(lines)

	# Populate the cells data list (cell[] = [row,col,box,value,cans])
	cells = [[] for i in range(81)]
	for row in range(9):
		for col in range(9):
			cells[col + row*9].append(row) 
			cells[col + row*9].append(col)
			cells[col + row*9].append(which_box(row,col))
			cells[col + row*9].append(x[row][col])
			cells[col + row*9].append({})

	cells = populate_cans(cells)

	print(puzzle_title)
	print_puzzle(cells)
	input("Press Enter to Solve")
	
	passes = 0
	Solved = False
	steps = False
	
	while not Solved:
		cans_set_length = 2
		passes += 1
		nums_added = 0
		cells, Solved = solver(cells, steps)
		while not nums_added:
			if cans_set_length == 7:
				print_puzzle(cells)
				print(cells)
				input()
				cans_set_length = 2
			passes += 1
			print("No numbers added.")
			# Use predictor to solve
			cells, Solved = predictor(cells, cans_set_length, steps)
			if Solved:
				print("Solved.")
			else:
				cells, Solved = solver(cells, steps) # Assuming we got some info.
				cans_set_length += 1

		print(f"After pass {passes}, {nums_added} numbers were added.")
		print_puzzle(cells)
		input()

main()