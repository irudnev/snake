#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from tkinter import *
from threading import Thread
import pickle
import hashlib
#import ttk

WIDTH = 400
HEIGHT = WIDTH
BACKGROUND = "#ccd5cc"
SNAKE_COLORS = ["#E74C3C", "#F1C40F", "#2980B9", "#72BAAC", "#E67E22", "#8B4D93"]
SNAKE_SIZE = 20
APPLE_SIZE = SNAKE_SIZE

root = Tk()
class Game():
	game_over = False
	snakes = []
	sn_id = 0
	apple_koord = (0, 0)
	score_koord = (SNAKE_SIZE/2, SNAKE_SIZE/2)
	heart_koord = (WIDTH - 3 * SNAKE_SIZE, SNAKE_SIZE/2)
	apple_id = 200
	score_id = 300
	heart_id = 500
	game_over_id = 400
	score = 0
	lives = 3
	item_is_move = False
	apple_pic = PhotoImage(file='apple.gif', width=APPLE_SIZE, height=APPLE_SIZE)
	kk_pic = PhotoImage(file='kk.gif', width=APPLE_SIZE, height=APPLE_SIZE)
	heart_pic = PhotoImage(file='heart.gif', width=APPLE_SIZE, height=APPLE_SIZE)

	incorrect_login = None
	log_label = None
	login_label = None
	login_text = None
	pass_label = None
	pass_text = None
	login_btn = None

	def create_apple(self):
		c.delete(self.apple_id)
		self.apple_id = c.create_image(self.apple_koord[0], self.apple_koord[1], image=self.apple_pic, anchor='nw')

	def create_score(self, score):
		c.delete(self.score_id)
		self.score_id = c.create_text(self.score_koord[0], self.score_koord[1], anchor='nw',
			text='Score: ' + str(score), font="Arial 12", fill="#000000")

	def create_heart(self):
		c.delete('hearts')
		for i in range(self.lives):
			self.heart_id = c.create_image(self.heart_koord[0] + i * SNAKE_SIZE, self.heart_koord[1], image=self.heart_pic, tags='hearts', anchor='nw')

class Snake(object):
	name = "anonim"
	color = SNAKE_COLORS[len(Game.snakes)]
	id = 0
	body = []
	score = 0
	lives = 3

	def __init__(self, id, name, body):
		self.id = id
		self.name = name
		self.color = SNAKE_COLORS[id -1]
		self.body = []
		is_oval = True
		for item in body:
			self.add_snake_len(item['x'], item['y'], is_oval)
			is_oval = False

	def add_snake_len(self, x, y, is_oval=False):
		# на вторую позицию, после головы
		self.body.append(Snake.create_element(x, y, self.color, Game.item_is_move or len(self.body) == 0, is_oval))

	def create_element(x, y, color, is_snake=True, is_oval=False):
		if is_snake:
			if is_oval:
				t_id = c.create_oval(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE,
						fill=color)
			else:
				t_id = c.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE,
						fill=color)
		else:
			t_id = c.create_image(x, y, image=Game.kk_pic, anchor='nw')
		return {'id': t_id, 'x': x, 'y': y}

	def move(self, new_koord_x, new_koord_y):
		#print('move')
		new_koord = [new_koord_x, new_koord_y]
		if g.game_over == False:			
			# двигаем тело
			if g.item_is_move:
				#print('body move', self.body)
				i = len(self.body) - 1
				while i > 0:
					#print('item id', self.body[i])
					self.body[i]['x'] = self.body[i - 1]['x']
					self.body[i]['y'] = self.body[i - 1]['y']
					c.coords(self.body[i]['id'],
						self.body[i]['x'],
						self.body[i]['y'],
						self.body[i]['x'] + SNAKE_SIZE,
						self.body[i]['y'] + SNAKE_SIZE)
					i -= 1
			self.body[0]['x'] = new_koord[0]
			self.body[0]['y'] = new_koord[1]
			c.coords(self.body[0]['id'],
				self.body[0]['x'],
				self.body[0]['y'],
				self.body[0]['x'] + SNAKE_SIZE,
				self.body[0]['y'] + SNAKE_SIZE)

		else:
			self.body = []
			g.game_over = True
			c.delete('all')
			g.game_over_id = c.create_text(WIDTH/2, HEIGHT/2, anchor='center',
					text='GAME OVER\nScore: ' + str(g.score), font="Arial 20", fill="#990000")
		#else:
		#	g.game_over_id = c.create_text(WIDTH/2, HEIGHT/2, anchor='center',
		#				text='Server error\nScore: ' + str(g.score), font="Arial 20", fill="#990000")

def key(event):
	if sock != None:
		entry = {'way': event.keysym}
		#print('keysym', event.keysym)
		data = pickle.dumps(entry)
		sock.send(data)
		if entry['way'] == 'Escape':
			sock.close()
			root.destroy()
	elif event.keysym == 'Escape':
		root.destroy()

def option_window():
	g.log_label = Label(root,text='Для входа в игру нужно зарегистрироваться на сайте: snake.com')
	g.login_label = Label(root,text='Логин:')
	g.login_text = Entry(root,width=7,font='Arial 14')
	g.pass_label = Label(root,text='Пароль:')
	g.pass_text = Entry(root,width=7,font='Arial 14',show='*')
	g.login_btn = Button(root, text="Войти", fg="red",
			command=login)

	g.log_label.grid(row=0,columnspan=5)
	g.login_label.grid(row=1,column=0)
	g.login_text.grid(row=1,column=1,padx=10)
	g.pass_label.grid(row=1,column=2)
	g.pass_text.grid(row=1,column=3,padx=10)
	g.login_btn.grid(row=1,column=4,padx=10)

def login():
	entry = {'log': g.login_text.get(), 'pass': hashlib.md5(g.pass_text.get().encode()).hexdigest()}
	data = pickle.dumps(entry)
	sock.send(data)
	#print('sended')

	data = sock.recv(128)
	if data == b'ok':
		g.log_label.grid_remove()
		g.login_label.grid_remove()
		g.login_text.grid_remove()
		g.pass_label.grid_remove()
		g.pass_text.grid_remove()
		g.login_btn.grid_remove()
		if g.incorrect_login != None:
			g.incorrect_login.grid_remove()
		
		c.focus_set()
		sock.settimeout(10)
		
		Thread(target=listen_server, args=[sock]).start()
	elif g.incorrect_login == None:
		g.incorrect_login = Label(root,text='Неправильный логин/пароль.',fg='#990000')
		g.incorrect_login.grid(row=2,columnspan=5)

def start_game():
	c.delete(g.game_over_id)
	g.game_over = False
	g.apple_koord = (0, 0)
	g.apple_id = 200
	g.score_id = 300
	g.score = 0

	g.create_score(0)
	g.create_heart()

def listen_server(sock):
	i = 0
	try:
		while i<1000:
			i += 1
			data = sock.recv(1024)
			#print('recv')
			entry = pickle.loads(data)
			
			apple_koord = entry.get('apple_koord', None)
			if apple_koord:
				if g.apple_koord != apple_koord:
					c.delete(g.apple_id)
					g.apple_koord = apple_koord
					g.create_apple()

					#body = entry.get('body', None)
					#if body:
					#	for it in body:
					#		sn = Snake.create_element(it['x'], it['y'], SNAKE_COLORS[0], True)
			if not g.sn_id:
				id = entry.get('id', None)
				if id:
					g.sn_id = id

			snakes = entry.get('snakes', None)
			if snakes:
				i = 0
				#print('snake')
				for sn in snakes:
					if len(g.snakes) < i + 1:
						#print('new snake')
						new_snake = Snake(i + 1, 'name1', sn.body)
						g.snakes.append(new_snake)
					else:
						#print('else', len(sn.body) == len(g.snakes[i].body))
						if len(sn.body) == len(g.snakes[i].body):
							#print('equal len', sn.body[0]['x'], sn.body[0]['y'])
							#print('g.snakes', g.snakes[i].body)
							if sn.is_reverse:
								g.snakes[i].body.reverse()
							g.snakes[i].move(sn.body[0]['x'], sn.body[0]['y'])
						else:
							#print('else')
							for it in g.snakes[i].body:
								c.delete(it['id'])
							if len(sn.body) > 0:
								new_snake = Snake(i + 1, 'name1', sn.body)
								if g.sn_id == sn.id:
									g.score = sn.score
									g.create_score(sn.score)
									g.lives = sn.lives
									g.create_heart()
								g.snakes[i].body = []
								#print('del g.body', g.snakes[i].body)
								g.snakes[i].body = new_snake.body
								#print('new g.body', g.snakes[i].body)

					i += 1
	except:
		print('except in listen_server')
		g.game_over = True	

c = Canvas(root, width=WIDTH, height=HEIGHT, bg=BACKGROUND)
c.grid(row=3,columnspan=5,padx=10,pady=10)
c.focus_set()
c.bind("<KeyPress>", key)
g = Game()

start_game()

sock = socket.socket()
#sock.connect(('172.16.161.178', 9090)) 
sock.connect(('192.168.20.99', 9090))
#sock.connect(('https://immense-reaches-92347.herokuapp.com', 9090))
sock.settimeout(30)

option_window()
#Thread(target=listen_server, args=[sock]).start()

root.resizable(width=False, height=False)
root.mainloop()