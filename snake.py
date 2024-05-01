def drawBoard(empty_set, food, snake, height, width):
	s = ""
	for x in range(width):
		for y in range(height):
			if (x, y) == food:
				s += 'F '
			elif (x, y) in empty_set:
				s += 'X '
			elif (x, y) == snake[0]:
				s += 'H '
			else:
				s += 'S '
		s += "\n"
	print(s)

from collections import deque
import random
import sys
import select

def input_with_timeout(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [],[], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n') # expect stdin to be line-buffered
    print()

def getInput(last_input):
	if last_input == (-1, -1):
		user = input(">> ")
	else:
		user = input_with_timeout(">> ", 0.25)

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

def main(height, width):
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
		dx, dy = getInput((dx, dy))
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

main(10, 10)
