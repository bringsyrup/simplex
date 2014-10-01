#! /bin/env python

'''
perform simplex algorithm with tableau format
'''

import numpy as np
import argparse as ap

def create_tableau(constraints, rows):
	'''create tableau from contraints'''

	sparse_tableau = np.zeros(len(constraints)).reshape(rows, len(constraints)/rows)
	tableau = np.asarray(np.split(np.asarray(constraints), rows))
	return tableau, sparse_tableau

def optimizer(constraints, rows, start, find_min=False):
	'''call create_tableau and loop through feasible points until optimal is found'''
	tableau, sparse_tableau = create_tableau(constraints, rows)
	counter = 0
	while True:
		print "\ncurrent tableau:" 
		print tableau
		if counter == 0:
			print "\ncurrent optimal point: " + str(start)
			current_opt = tableau[-1][-1]
			print "current optimal value: %d " % current_opt
		else:
			if find_min == True:
				print "\ncurrent optimal value: %d " % new_opt*-1
			else:
				print "\ncurrent optimal value: %d " % new_opt
			breaker = True
			for value in tableau[-1][:-1]:
				if find_min == True:
					if value < 0 or new_opt != prev_opt:
						breaker = False
				else:
					if value < 0:
						breaker = False
			if breaker == True:
				for row in range(len(tableau)-1):
					if 1 in tableau[row][:-(rows+1)]:
						print "\nx%d = %s" % ((np.where(tableau[row][:(rows+1)] == 1)[-1]+1)[0], str(tableau[row][-1]))
				print "\nall other variables have value zero"
				break
		print "\n====> new pivot <===="
		prev_opt = tableau[-1][-1]
		pivot_col_index = np.where(np.absolute(tableau[-1]) == np.amax(np.absolute(tableau[-1][:rows-1])))[0][0]
		print "\nentering variable: column %d" % pivot_col_index
		for i in range(len(tableau[:-1])):
			if tableau[i][-1]/tableau[i][pivot_col_index] >= 0:
				sparse_tableau[i][-1] = tableau[i][-1] / tableau[i][pivot_col_index]
			else:
				sparse_tableau[i][-1] = np.inf
		min_ratio = sparse_tableau[:-1].min(axis=0)[-1]
		pivot_row_index = np.where(sparse_tableau == min_ratio)[0][0]
		print "\nexiting variable: row %d, col %d" % (pivot_row_index, np.where(tableau[pivot_row_index][rows-1:-2] == 1)[0][0] + rows-1)
		pivot_row_denom = tableau[pivot_row_index][pivot_col_index]
		for index in range(len(tableau)):
			if index != pivot_row_index:
				denom = pivot_row_denom/tableau[index][pivot_col_index]
				for i in range(len(tableau[index])):
					tableau[index][i] = tableau[index][i] - tableau[pivot_row_index][i]/denom
		for i in range(len(tableau[pivot_row_index])):
			tableau[pivot_row_index][i] = tableau[pivot_row_index][i]/pivot_row_denom
		new_opt = tableau[-1][-1]
		counter += 1
		if counter % 10 == 0:
			boolean = raw_input("after ten iterations with no optimal found, would you like to continue? (y or n). ").lower
			if boolean == "n" or boolean == "no":
				break

	return

if __name__=="__main__":

	parser = ap.ArgumentParser(
			description = "perform the simplex method"
			)
	parser.add_argument("rows",
			type = int,
			help = "number of equations (rows) to use in tableau"
			)
	parser.add_argument("constraints",
			type = float,
			nargs = "+",
			help = "list of lists to create tableau format. last column should be the RHS. do not include a column for the ratio",
			)
	parser.add_argument("-o", "--origin",
			type = float,
			nargs = "+",
			action = "store",
			help = "if specified, this is the starting extreme point. else the origin is used"
			)
	parser.add_argument("-m", "--min",
			action = "store_true",
			help = "find min instead of max"
			)
	
	args = parser.parse_args()
	
	if not args.origin:
		start = np.zeros((len(args.constraints) / args.rows) - (args.rows + 1))
	else:
		start = np.asarray(args.origin)

	if len(args.constraints) % args.rows != 0:
		print "number of entries must be divisible by desired number of rows"
	else:
		if args.min:
			optimizer(args.constraints, args.rows, start, True)
		else:
			optimizer(args.constraints, args.rows, start)
	
