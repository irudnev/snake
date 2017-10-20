# coding: utf8

from socket import socket, timeout as exc_sock_timeout
import time as t
import pickle
import uuid
import hashlib
#from models import SnakeUser



#from tkinter import *
import random
#from sqlite3 import connect
import uuid
from threading import Thread
#import ttk

WIDTH = 400
HEIGHT = WIDTH
BACKGROUND = "#ccd5cc"
SNAKE_COLORS = ["#E74C3C", "#F1C40F", "#2980B9", "#72BAAC", "#E67E22", "#8B4D93"]
SNAKE_SIZE = 20
APPLE_SIZE = SNAKE_SIZE
#CON = connect('snake.db')
#CUR = CON.cursor()

#root = Tk()
class Game():
	clients = []
	game_over = False
	snakes = []
	apple_koord = (0, 0)
	speed = 1000
	item_is_move = True
	#apple_pic = PhotoImage(file='apple.gif', width=APPLE_SIZE, height=APPLE_SIZE)
	#kk_pic = PhotoImage(file='kk.gif', width=APPLE_SIZE, height=APPLE_SIZE)

	def get_apple_koord(self):
		self.apple_koord = (APPLE_SIZE * random.randint(0, (WIDTH - APPLE_SIZE)/APPLE_SIZE),
						APPLE_SIZE * random.randint(0, (WIDTH - APPLE_SIZE)/APPLE_SIZE))

	def check_game(self):
		g_over = True
		for sn in self.snakes:
			if sn.sn_game_over == False:
				g_over = False
		if g_over:
			print('check_game gameover')
			self.game_over = True


class Snake(object):
	name = "anonim"
	color = SNAKE_COLORS[len(Game.snakes)]
	id = 0
	vector = (1 , 0)
	body = []
	score = 0
	sn_game_over = False
	lives = 3
	is_reverse = False

	def __init__(self, id, name, koord, lives=3):
		self.name = name
		self.id = id
		self.body = []
		self.add_snake_len(koord[0], koord[1])
		self.lives = lives
		#self.move()

	def add_snake_len(self, x, y):
		# на вторую позицию, после головы
		self.body.insert(1, {'x': x, 'y': y})

	def is_crash(self):
		k_x = self.body[0]['x']
		k_y = self.body[0]['y']
		#print('koord', k_x, k_y)
		# за границами игрового поля
		if (k_x < 0 or k_x > WIDTH - SNAKE_SIZE
				or k_y < 0 or k_y > HEIGHT - SNAKE_SIZE):
			return True

		# укусила себя или другую змею
		for sn in g.snakes:
			i = 0
			# свою голову не проверяем
			if sn.id == self.id:
				i = 1
			while i < len(sn.body):
				if(k_x == sn.body[i]['x'] and k_y == sn.body[i]['y']):
					return True
				i += 1
		# врезалась в забор
		# забора пока нет

		return False

	def reverse(self, new_vect, vect_ind = 0):
		if(len(self.body) > 1 and self.vector[vect_ind] == -1 * new_vect[vect_ind]):
			self.body.reverse()
			self.choose_way()
			self.is_reverse = True
		else:
			self.vector = new_vect

	def choose_way(self):
		if(len(self.body) > 1):
			if(self.body[0]['x'] > self.body[1]['x']):
				#print('one')
				self.vector = (1, 0)
			elif(self.body[0]['x'] < self.body[1]['x']):
				#print('two')
				self.vector = (-1, 0)
			elif(self.body[0]['y'] < self.body[1]['y']):
				#print('three')
				self.vector = (0, -1)
			elif(self.body[0]['y'] > self.body[1]['y']):
				#print('four')
				self.vector = (0, 1)

	def check_lives(self):
		print('check lives')
		self.lives -= 1
		if self.lives > 0:
			self.body.clear()
			self.body.append({'x': 0, 'y': 0})
			self.vector = (1, 0)
			new_koord = (self.body[0]['x'] + SNAKE_SIZE * self.vector[0],
				self.body[0]['y'] + SNAKE_SIZE * self.vector[1])
		else:
			print('check lives sn gameover')
			self.sn_game_over = True
			g.check_game()

	def move(self):
		if g.game_over == False and self.sn_game_over == False:
			result = 0 # moved
			#threading.Thread(target=g.refresh_data, args=[self]).start()
			x_koord = self.body[0]['x']
			y_koord = self.body[0]['y']
			if(not self.is_crash()):
				new_koord = (self.body[0]['x'] + SNAKE_SIZE * self.vector[0],
					self.body[0]['y'] + SNAKE_SIZE * self.vector[1])

				# съела яблоко
				if(new_koord[0] == g.apple_koord[0] and new_koord[1] == g.apple_koord[1]):
					self.add_snake_len(x_koord, y_koord)
					g.get_apple_koord()
					self.score = self.score + 10
					result = 1 # apple
				# нет яблока, двигаем тело
				elif g.item_is_move:
					i = len(self.body) - 1
					while i > 0:
						self.body[i]['x'] = self.body[i - 1]['x']
						self.body[i]['y'] = self.body[i - 1]['y']
						i -= 1
				self.body[0]['x'] = new_koord[0]
				self.body[0]['y'] = new_koord[1]
				return result
				#root.after(g.speed, self.move)

			else:
				self.check_lives()
				return 3 # game over

#Button(root, text = '1').place(x = 10, y = 10, width = 30)

#b = ttk.Button(root)
#b.pack()

def key(name, snake):
	if(name == "Left"):
		snake.reverse((-1, 0), 0)
	elif(name == "Right"):
		snake.reverse((1, 0), 0)
	elif(name == "Down"):
		snake.reverse((0, 1), 1)
	elif(name == "Up"):
		snake.reverse((0, -1), 1)
	#elif(name == "Escape"):
		#clean db
		#root.destroy()
	elif(name == "space"):
		if(Game.speed == 10000000):
			Game.speed = 100
			snake.move()
		else:
			Game.speed = 10000000
	elif(name == "Return"):
		start_game()

def client_key_listen(client, new_snake):
	try:
		while g.game_over == False:
			data = client.recv(1024)
			if not data:
				print('not data')
				#client.send(b'ff')
			else:
				entry = pickle.loads(data)
				way = entry.get('way', None)
				if way and way=='Escape':
					break;
				elif way:
					#print(way)
					key(way, new_snake)
	except:
		print('client_key_listen error')

def check_login(log, pas):
	return True

	#return hashlib.md5("2".encode()).hexdigest() == pas

	#if user:
	#	return user.check_password(pas)
	#else:
	#	return False

def client_listen(s):
	try:
		while len(g.clients) < 3:
			client, client_addr = s.accept()
			client.settimeout(30)
			print(client_addr)
			data = client.recv(1024)
			entry = pickle.loads(data)
			log = entry.get('log', None)
			print('log', log)
			pas = entry.get('pass', None)

			#user = User.objects.get(username=log)

			#while not check_login(user, pas):
			while not check_login(log, pas):
				client.send(b'n')
				data = client.recv(1024)
				entry = pickle.loads(data)
				log = entry.get('log', None)
				print('log', log)
				pas = entry.get('pass', None)
				way = entry.get('way', None)
				if way and way=='Escape':
					continue
			
			client.send(b'ok')
			client.settimeout(15)

			#cl_id = uuid.uuid4()
			cl_id = len(g.snakes) + 1
			#entry = {'id': cl_id}
			print('id', cl_id)

			g.clients.append({'id': cl_id, 'name': log, 'client': client, 'addr': client_addr})

			new_snake = Snake(cl_id, log, (0, 0))
			g.snakes.append(new_snake)
			
			Thread(target=client_key_listen, args=(client, new_snake)).start()
	except exc_sock_timeout:
		print('accept timeout')
		if(len(g.clients) == 0):
			g.game_over = True
			print('close sock from client_listen')
			s.close()
	except:
		print('client_listen error')
		g.game_over = True
		s.close()

def start_game():
	g.game_over = False
	#g.snake = []
	g.apple_koord = (0, 0)
	g.get_apple_koord()

	with s:
		s.bind(t_addr)
		s.settimeout(300)
		s.listen()
		#while True:
		#	client, client_addr = s.accept()
		#	client.settimeout(15)
		#	print(client_addr)
		#	data = client.recv(1024)
		#	entry = pickle.loads(data)
		#	cl_name = entry.get('name', None)
		#	print('NAME', cl_name)

		#	#cl_id = uuid.uuid4()
		#	cl_id = len(g.snakes) + 1
		#	#entry = {'id': cl_id}
		#	print('id', cl_id)

		#	new_snake = Snake(cl_id, cl_name, (0, 0))
		#	g.snakes.append(new_snake)

		#	Thread(target=client_key_listen, args=(client, new_snake)).start()

			#data = pickle.dumps(new_snake.body)
			#client.send(data)
			
			#while True:
		Thread(target=client_listen, args = (s,)).start()

		i = 0
		exception_count = 0
		while i<1000:
			i += 1
			for sn in g.snakes:
				sn.move()
			for sn in g.snakes:
				try:
					entry = {'apple_koord': g.apple_koord, 'id': sn.id, 'name': sn.name, 'snakes': g.snakes}
					data = pickle.dumps(entry)
					g.clients[sn.id - 1]['client'].send(data)
					exception_count = 0
					sn.is_reverse = False
				except:
					print('except', 'id', sn.id)
					exception_count += 1
			if g.game_over or exception_count > 5:
				g.game_over = True
				print('close sock from startgame', g.game_over, exception_count > 5)
				s.close()
				break;

			#t.sleep(g.speed/10000)
			t.sleep(0.1)
			#client.sendall(data.upper())
		#	t.sleep(5)
		#	break;

s = socket()
t_addr = ('0.0.0.0', 9090)
# 192.168.20.99
g = Game()
start_game()
#s = Snake('Player' + str(len(Game.snakes)), (0, len(Game.snakes) * SNAKE_SIZE + 0))
#s2 = Snake('Player2', (0, 30))
#c.bind("<Button-1>", callback)
