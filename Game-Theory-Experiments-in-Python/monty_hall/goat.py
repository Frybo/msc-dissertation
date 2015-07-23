import random
import sys

#Simulation of the Monty Hall Problem

def remove_doors(removables, win):
	
#	Adding a for loop to this function
#	allows changes to the number of doors.

	if win in removables:
		rem = win
	else:
		rem = random.choice(removables)
	
	removables.remove(rem)

def doors_eval(wfs):

#	Assign a state number to the outcome.
#	0 = no prize, switch
#	1 = yes prize, switch
#	10 = no prize, no switch
#	11 = yes prize, no switch

	state = 0
	w, f, s = wfs

	if w == s:
		state = 1
	if f == s:
		state += 10

	return state

def doors_game():
	
#	This is where a single Monty Hall game happens.
#	A list of three items (doors) is created. Then
#	the winning "door" and the player choice "door"
#	get randomly chosen.

	doors = list(range(3))
	winning_door = random.choice(doors)
	first_choice = random.choice(doors)

#	This part is analogous to opening one of the 
#	doors. One of the options is removed from 
#	the list. The code ensures, that neither the
#	chosen, nor the winning doors are removed.

	removable_doors = list(doors)
	removable_doors.remove(first_choice)
	remove_doors(removable_doors, winning_door)
	doors.remove(removable_doors[0])

#	The second door is chosen and a tuple is retuned.

	second_choice = random.choice(doors)
	return winning_door, first_choice, second_choice

def count(state_list):

#	Count up the states.
	
	d = { "1" : 0, "0" : 0, "11" : 0, "10" : 0 }

	for case in state_list:
		if case == 1:
			d["1"] += 1
		elif case == 0:
			d["0"] += 1
		elif case == 10:
			d["10"] += 1
		elif case == 11:
			d["11"] += 1
	return d

def main():
	
	state_list = []
	iterations = int(sys.argv[1])

	for i in range(iterations):
		state_list.append(doors_eval(doors_game()))

#	Assess the results in human interpretable form.

	c_dict = count(state_list)
	lost_total = c_dict["0"] + c_dict["10"]
	win_total = c_dict["1"] + c_dict["11"]
	win_percent = (win_total / iterations) * 100
	win_switch = (c_dict["1"] / win_total) * 100
	win_noswitch = (c_dict["11"] / win_total) * 100
	print("Total number of games:", win_total + lost_total)
	print("Number of victories:", win_total,"	Number of lost games:", lost_total)
	print("Percentage of victories:", round(win_percent, 2), "%")
	print("Percentage of victories when switched:", round(win_switch, 2), "%") 
	print("Percentage of victories when stayed:", round(win_noswitch, 2), "%")

if __name__ == '__main__':
	main()
