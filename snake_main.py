#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
from math import fabs

# временно
import time as t

WIDTH = 600
HEIGHT = 400
BACKGROUND = "#ccd5cc"
SNAKE_SIZE = 20
APPLE_SIZE = SNAKE_SIZE
SNAKE_COLORS = ["#E74C3C", "#F1C40F", "#2980B9", "#72BAAC", "#E67E22", "#8B4D93"]
START_POSITIONS = [(0, 100), (WIDTH - SNAKE_SIZE, 100), (0, 20), (WIDTH - SNAKE_SIZE, 20), (0, 180), (WIDTH - SNAKE_SIZE, 180)]
SNAKE_VECTORS = [(1, 0), (-1, 0), (1, 0), (-1, 0), (1, 0), (-1, 0)]
CLIENTS_COUNT = 3

class Game():
	clients = []
	game_over = False
	snakes = []
	fence = []
	#fence = [(120, 20), (360, 120)]
	apple_koord = (0, 0)
	speed = 100
	item_is_move = True
	bot_count = 1
	bot_level = 3
	distance_mas = []

	def calc_apple_koord():
		return (APPLE_SIZE * randint(0, int((WIDTH - APPLE_SIZE)/APPLE_SIZE)),
						APPLE_SIZE * randint(0, int((HEIGHT - APPLE_SIZE)/APPLE_SIZE)))

	def get_apple_koord(self):
		new_apple_koord = Game.calc_apple_koord()
		while new_apple_koord == self.apple_koord or not Game.check_apple_koord(new_apple_koord):
			new_apple_koord = Game.calc_apple_koord()
		self.apple_koord = new_apple_koord

	def check_apple_koord(new_koord):
		for sn in Game.snakes:
			i = 0
			while i < len(sn.body):
				if(new_koord[0] == sn.body[i]['x'] and new_koord[1] == sn.body[i]['y']):
					return False
				i += 1
		return True

	def check_game(self):
		g_over = True
		for sn in self.snakes:
			if sn.sn_game_over == False and not sn.is_bot:
				g_over = False
		if g_over:
			self.game_over = True

class Snake(object):
	name = "anonim"
	color = SNAKE_COLORS[len(Game.snakes)]
	id = 0
	vector = (1 , 0)
	body = []
	score = 0
	x_score = 2
	sn_game_over = False
	lives = 3
	is_reverse = False
	is_bot = False
	bot_level = 0

	def __init__(self, id, name, koord, lives=3, index=0):
		self.id = id
		self.name = name
		self.body = []
		self.color = SNAKE_COLORS[index]
		self.vector = SNAKE_VECTORS[index]
		self.add_snake_len(koord[0], koord[1])
		self.lives = lives

	def add_snake_len(self, x, y):
		# на первую позицию (голова)
		self.body.insert(0, {'x': x, 'y': y})

	def is_crash(koords):
		# за границами игрового поля
		if (koords[0] < 0 or koords[0] > WIDTH - SNAKE_SIZE
				or koords[1] < 0 or koords[1] > HEIGHT - SNAKE_SIZE):
			return True

		# укусила себя или другую змею
		for sn in GAME.snakes:
			i = 0
			while i < len(sn.body):
				if(koords[0] == sn.body[i]['x'] and koords[1] == sn.body[i]['y']):
					return True
				i += 1
		
		# врезалась в забор
		for fn in GAME.fence:
			if(koords[0] == fn[0] and koords[1] == fn[1]):
				return True

		return False

	def reverse(self, new_vect, vect_ind = 0):
		if(GAME.item_is_move and len(self.body) > 1 and self.vector[vect_ind] == -1 * new_vect[vect_ind]):
			self.body.reverse()
			self.choose_way()
			self.is_reverse = True
		else:
			self.vector = new_vect

	def choose_way(self):
		if(len(self.body) > 1):
			if(self.body[0]['x'] > self.body[1]['x']):
				self.vector = (1, 0)
			elif(self.body[0]['x'] < self.body[1]['x']):
				self.vector = (-1, 0)
			elif(self.body[0]['y'] < self.body[1]['y']):
				self.vector = (0, -1)
			elif(self.body[0]['y'] > self.body[1]['y']):
				self.vector = (0, 1)

	def check_lives(self):
		self.lives -= 1
		self.body.clear()
		if self.lives > 0:
			self.body.append({'x': 0, 'y': 0})
			self.vector = (1, 0)
		else:
			self.sn_game_over = True
			GAME.check_game()

	def get_move(koords, vector):
		if GAME.game_over == False: # and self.sn_game_over == False:
			new_koord = (koords[0] + SNAKE_SIZE * vector[0],
					koords[1] + SNAKE_SIZE * vector[1])

			# съела яблоко
			if(new_koord[0] == GAME.apple_koord[0] and new_koord[1] == GAME.apple_koord[1]):
				return {'x': new_koord[0], 'y': new_koord[1], 'event': 1}
			# врезалась
			elif Snake.is_crash(new_koord):
				return {'x': 0, 'y': 0, 'event': 2}
			# двигается
			else:
				return {'x': new_koord[0], 'y': new_koord[1], 'event': 0}
		# game over
		return {'x': 0, 'y': 0, 'event': 3}

	def snake_move(self, t_game):
		new_koord = Snake.get_move((self.body[0]['x'], self.body[0]['y']), self.vector)
		# съела яблоко
		if new_koord['event'] == 1:
			self.add_snake_len(new_koord['x'], new_koord['y'])
			t_game.get_apple_koord()
			self.score = self.score + 10 * self.x_score
			if not t_game.item_is_move:
				self.body[1]['x'] = new_koord['x']
				self.body[1]['y'] = new_koord['y']
		# врезалась
		elif new_koord['event'] == 2:
			self.check_lives()
		# двигается
		elif new_koord['event'] == 0:
			if t_game.item_is_move:
				i = len(self.body) - 1
				while i > 0:
					self.body[i]['x'] = self.body[i - 1]['x']
					self.body[i]['y'] = self.body[i - 1]['y']
					i -= 1
			self.body[0]['x'] = new_koord['x']
			self.body[0]['y'] = new_koord['y']

		return new_koord

	def add_snake(g, index, name, lives, is_bot=False, level=2):
		n_snake = Snake(index, name, START_POSITIONS[index], lives, index)
		if is_bot:
			n_snake.is_bot = True
			n_snake.bot_level = level
		g.snakes.append(n_snake)

	def bot_vector(self, g):
		if g.game_over == False:
			option = randint(0, self.bot_level * self.bot_level * 100)
			old_v = self.vector
			if option < 90 or (option < 550 and option > 190):
				res = 10000
				vect = self.vector
				x = int(self.body[0]['x'] / SNAKE_SIZE)
				y = int(self.body[0]['y'] / SNAKE_SIZE)
				n = int(WIDTH / SNAKE_SIZE)
				m = int(HEIGHT / SNAKE_SIZE)

				if x > 0 and g.distance_mas[x - 1][y] < res:
					res = g.distance_mas[x - 1][y]
					vect = (-1, 0)
				if x < n - 1 and g.distance_mas[x + 1][y] < res:
					res = g.distance_mas[x + 1][y]
					vect = (1, 0)
				if y > 0 and g.distance_mas[x][y - 1] < res:
					res = g.distance_mas[x][y - 1]
					vect = (0, -1)
				if y < m - 1 and g.distance_mas[x][y + 1] < res:
					res = g.distance_mas[x][y + 1]
					vect = (0, 1)
				self.vector = vect
			else:
				vectors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
				v_len = len(vectors)
				if v_len > 0:
					self.vector = vectors[randint(0, v_len - 1)]

			if g.item_is_move and len(self.body) > 1 and old_v[0] * -1 == self.vector[0] and old_v[1] * -1 == self.vector[1]:
				new_v = self.vector
				self.vector = old_v
				ind = 0
				if old_v[1] != 0:
					ind = 1
				self.reverse(new_v, ind)

	def bot_vector_old(self, g):
		if g.game_over == False:
			option = randint(0, self.bot_level * self.bot_level * 100)
			#vectors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
			vectors = []
			old_v = self.vector
			#if option == 4 or option == 9:
			#	self.vector = vectors[randint(0,3)]
			#	#print('vector_rnd', self.vector, self.body[0])
			#	return True
			result = (self.vector[0], self.vector[1], 10000)
			for koord in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
				last = len(self.body) - 1
				if g.item_is_move and last != 0 and self.vector[0] * -1 == koord[0] and self.vector[1] * -1 == koord[1]:
					if option < 101:
						res = Snake.get_move((self.body[last]['x'], self.body[last]['y']), koord)
						if res['event'] == 1:
							ind = 0
							if old_v[1] != 0:
								ind = 1
							self.reverse(koord, ind)
							return True
					else:
						continue
				else:
					res = Snake.get_move((self.body[0]['x'], self.body[0]['y']), koord)
				if res['event'] == 1:
					self.vector = koord
					#print('vector apple', self.vector, self.body[0])
					return True
				elif res['event'] == 0:
					distance = fabs(res['x'] - g.apple_koord[0]) + fabs(res['y'] - g.apple_koord[1])
					#print(self.body[0], 'distance',distance, result[2], res, g.apple_koord, option)
					if distance < result[2]:
						result = (koord[0], koord[1], distance)
					vectors.append(koord)
					if self.vector == koord:
						vectors.append(self.vector)
						vectors.append(self.vector)

			if option < 90 or (option < 550 and option > 190):
				self.vector = (result[0], result[1])
			else:
				#print('vector rnd last')
				v_len = len(vectors)
				if v_len > 0:
					self.vector = vectors[randint(0, v_len - 1)]
			if g.item_is_move and len(self.body) > 1 and old_v[0] * -1 == self.vector[0] and old_v[1] * -1 == self.vector[1]:
				new_v = self.vector
				self.vector = old_v
				ind = 0
				if old_v[1] != 0:
					ind = 1
				self.reverse(new_v, ind)
			#print('vector last', self.vector, self.body[0], option)

	def dextra_ways(g):
		n = int(WIDTH / SNAKE_SIZE)
		m = int(HEIGHT / SNAKE_SIZE)
		g.distance_mas = [[0] * m for i in range(n)]
		control_mas = [[0] * m for i in range(n)]
		Snake.get_let_mas(g, control_mas)
		vertex = (int(g.apple_koord[0] / SNAKE_SIZE), int(g.apple_koord[1] / SNAKE_SIZE))
		control_mas[vertex[0]][vertex[1]] = 0
		
		Snake.change_ways(vertex, g.distance_mas, n, m, control_mas)

	def get_let_mas(g, let_mas):
		for sn in GAME.snakes:
			i = 0
			while i < len(sn.body):
				let_mas[int(sn.body[i]['x'] / SNAKE_SIZE)][int(sn.body[i]['y'] / SNAKE_SIZE)] = 2
				i += 1
		
		# забор
		for fn in g.fence:
			#print('fence', fn)
			let_mas[int(fn[0] / SNAKE_SIZE)][int(fn[1] / SNAKE_SIZE)] = 2

	def change_ways(vertex, distance_mas, n, m, control_mas):
		if control_mas[vertex[0]][vertex[1]] != 0:
			#print('return', vertex[1], vertex[0])
			return
		else:
			control_mas[vertex[0]][vertex[1]] = 1
		items = []
		distance = distance_mas[vertex[0]][vertex[1]]
		# up
		if(vertex[0] > 0):
			items.append((vertex[0] - 1, vertex[1]))
			Snake.count_cell(vertex[0] - 1, vertex[1], distance + 1, distance_mas, items, control_mas)
		# down
		if(vertex[0] < n - 1):
			items.append((vertex[0] + 1, vertex[1]))
			Snake.count_cell(vertex[0] + 1, vertex[1], distance + 1, distance_mas, items, control_mas)
		# left
		if(vertex[1] > 0):
			items.append((vertex[0], vertex[1] - 1))
			Snake.count_cell(vertex[0], vertex[1] - 1, distance + 1, distance_mas, items, control_mas)
		# right
		if(vertex[1] < m - 1):
			items.append((vertex[0], vertex[1] + 1))
			Snake.count_cell(vertex[0], vertex[1] + 1, distance + 1, distance_mas, items, control_mas)
		for item in items:
			Snake.change_ways(item, distance_mas, n, m, control_mas)

	def count_cell(x, y, distance, distance_mas, items, control_mas):
		if control_mas[x][y] != 2:
			if distance_mas[x][y] == 0 or distance < distance_mas[x][y]:
				distance_mas[x][y] = distance
				# для пересчета соседних заново
				control_mas[x][y] = 0

GAME = Game()
