import colorama # pip3 install colorama
from colorama import Fore, Back, Style
from collections import deque
import random
import sys
import select

def drawBoard(empty_set, food, snake, height, width):
	s = ""
	for x in range(width):
		for y in range(height):
			if (x, y) == food:
				char = 'F'
				color = Fore.GREEN
			elif (x, y) in empty_set:
				char = 'X'
				color = Fore.BLACK
			elif (x, y) == snake[0]:
				char = 'H'
				color = Fore.MAGENTA
			else:
				char = 'S'
				color = Fore.MAGENTA
			s += color + char + Style.RESET_ALL + ' '
		s += "\n"
	print(s)

def input_with_timeout(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [],[], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n') # expect stdin to be line-buffered
    print()

def getInput(last_input, timeout):
	if last_input == (-1, -1):
		user = input(">> ")
	else:
		user = input_with_timeout(">> ", timeout)

	if user in ["w"]:
		return (-1, 0)
	elif user in ['s']:
		return (1, 0)
	elif user in ['a']:
		return (0, -1)
	elif user in ['d']:
		return (0, 1)
	else:
		return last_input

def placeFood(empty_set):
	return random.choice(list(empty_set))

def getNum(message, type):
    '''Given a message to display to the user, ensure they give an int as
    input'''
    while(True):
        num = input(message)
        try:
            num = type(num)
            return num
        except:
            print(Fore.RED + "That was not a valid number. Please try again.\n" + Style.RESET_ALL)

def main():
	print("\n\nWelcome to Snake!\nPlease select your difficulty level, or choose custom to set your own preferences!.\n")
	print("[1] Easy\n[2] Medium\n[3] Hard\n[4] Custom")
	choice = getNum("\n>> ", int)
	if choice in [1, 2, 3]:
		timeout = 1 - (0.25*choice)
		height = 5 + (5*choice)
		width = height
	else:
		print("Please input the following: ")
		timeout = getNum("  Tick Rate: ", float)
		height = getNum("  Board Height: ", int)
		width = getNum("  Board Width: ", int)

	dx, dy = -1, -1
	if height < 1 or width < 1:
		return
	snake = deque()
	empty_set = set([(x, y) for x in range(width) for y in range(height)])
	snake.appendleft((0,0))
	empty_set.remove((0,0))
	food = placeFood(empty_set)
	game_over = False
	while not game_over:
		drawBoard(empty_set, food, snake, height, width)
		dx, dy = getInput((dx, dy), timeout)
		new_head = (snake[0][0] + dx, snake[0][1] + dy)
		if width <= new_head[0] < 0 or height <= new_head[1] < 0:
			game_over = True
			continue
		if new_head not in empty_set and new_head != snake[-1]:
			game_over = True
			continue
		snake.appendleft(new_head)
		if new_head == food:
			if len(snake) == height*width:
				game_over = True
				continue
			food = placeFood(empty_set)
		else:
			old_tail = snake.pop()
			empty_set.add(old_tail)
		empty_set.remove(new_head)

main()
