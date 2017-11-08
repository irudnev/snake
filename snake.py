#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from tkinter import *
from threading import Thread
import pickle
import hashlib
import random
#import ttk

import snake_main as m

root = Tk()
class MyGame():
	sn_id = 0
	score_koord = (m.SNAKE_SIZE/2, m.SNAKE_SIZE/2)
	heart_koord = (m.WIDTH - 3 * m.SNAKE_SIZE, m.SNAKE_SIZE/2)
	apple_id = 200
	score_id = 300
	heart_id = 500
	game_over_id = 400
	score = 0
	lives = 3
	item_is_move = BooleanVar()
	pc_game = BooleanVar()
	pc_game.set(False)
	pc_level = IntVar()
	pc_level.set(2)
	apple_pic = PhotoImage(file='apple.gif', width=m.APPLE_SIZE, height=m.APPLE_SIZE)
	kk_pic = PhotoImage(file='kk.gif', width=m.APPLE_SIZE, height=m.APPLE_SIZE)
	heart_pic = PhotoImage(file='heart.gif', width=m.APPLE_SIZE, height=m.APPLE_SIZE)
	tree_pic = PhotoImage(file='tree.gif', width=m.APPLE_SIZE, height=m.APPLE_SIZE)
	body_pic = PhotoImage(file='body.gif', width=m.APPLE_SIZE, height=m.APPLE_SIZE)
	head_pic = [PhotoImage(file='head1.gif', width=m.APPLE_SIZE, height=m.APPLE_SIZE),
				PhotoImage(file='head2.gif', width=m.APPLE_SIZE, height=m.APPLE_SIZE),
				PhotoImage(file='head3.gif', width=m.APPLE_SIZE, height=m.APPLE_SIZE),
				PhotoImage(file='head4.gif', width=m.APPLE_SIZE, height=m.APPLE_SIZE),
				PhotoImage(file='head5.gif', width=m.APPLE_SIZE, height=m.APPLE_SIZE),
				PhotoImage(file='head6.gif', width=m.APPLE_SIZE, height=m.APPLE_SIZE)]

	incorrect_login = None
	error_label = None
	log_label = None
	vs_pc = None
	ip_label = None
	ip_text = None
	port_label = None
	port_text = None
	login_label = None
	login_text = None
	pass_label = None
	pass_text = None
	login_btn = None
	game_type = None
	bot_label = None
	bot_count = None
	easy_level = None
	middle_level = None
	difficult_level = None

	scores_lable = None

	def create_apple(self):
		c.delete(self.apple_id)
		self.apple_id = c.create_image(g.apple_koord[0], g.apple_koord[1], image=self.apple_pic, anchor='nw')
		g.level_apple_count -= 1

	def create_score(self, score):
		c.delete(self.score_id)
		self.score_id = c.create_text(self.score_koord[0], self.score_koord[1], anchor='nw',
			text='Score: ' + str(score), font="Arial 12", fill="#000000")

	def create_scores(self):
		self.scores_lable.delete('all')
		sn_len = len(g.snakes)
		i = 0
		while i < sn_len:
			sn = g.snakes[i]
			self.scores_lable.create_rectangle(5 + i * 100, 0, 5 + i * 100 + m.SNAKE_SIZE, 1 + m.SNAKE_SIZE,
				fill=sn.color)
			self.scores_lable.create_text(26 + i * 100, 1, anchor='nw',
				text=str(sn.score), font="Arial 12", fill=sn.color)
			self.scores_lable.create_image(60 + i * 100, 1, image=self.heart_pic, anchor='nw')
			self.scores_lable.create_text(81 + i * 100, 1, anchor='nw',
				text=str(sn.lives), font="Arial 12", fill=sn.color)
			i += 1

	def create_heart(self, lives_count=3):
		c.delete('hearts')
		for i in range(lives_count):
			self.heart_id = c.create_image(self.heart_koord[0] + i * m.SNAKE_SIZE, self.heart_koord[1], image=self.heart_pic, tags='hearts', anchor='nw')

	def create_fence():
		c.delete('fence')
		for item in g.fence:
			c.create_image(item[0], item[1], image=MyGame.tree_pic, tags='fence', anchor='nw')
		#i = 40
		#while i < int(m.WIDTH / 2):
		#	g.fence.append((i, i))
		#	c.create_image(i, i, image=MyGame.tree_pic, tags='fence', anchor='nw')
		#	g.fence.append((m.WIDTH - m.SNAKE_SIZE - i, i))
		#	c.create_image(m.WIDTH - m.SNAKE_SIZE - i, i, image=MyGame.tree_pic, tags='fence', anchor='nw')
		#	i += m.SNAKE_SIZE

	def next_step():
		for sn in g.snakes:
			if not sn.sn_game_over:
				if sn.is_bot:
					sn.bot_vector(g)
				if sn.is_reverse:
					MySnake.change_tail(sn)
					sn.is_reverse = False
				new_koord = sn.snake_move(g)
				# съела яблоко
				if new_koord['event'] == 1:
					el = MySnake.create_element('snakes' + sn.name, new_koord['x'], new_koord['y'], sn.color, True, True, sn.id)
					sn.body[0].update({'id': el['id']})

					c.delete(sn.body[1]['id'])
					el = MySnake.create_element('snakes' + sn.name, new_koord['x'], new_koord['y'], sn.color, g.item_is_move, False)
					sn.body[1].update({'id': el['id']})
					
					if not sn.is_bot:
						mg.create_score(sn.score)
					mg.create_scores()
					mg.create_apple()
					if g.level_apple_count == 0:
						for i in range(10):
							g.fence.append(m.Game.calc_apple_koord())
						MyGame.create_fence()
						g.level_apple_count = 10
					m.Snake.dextra_ways(g)
				# врезалась
				elif new_koord['event'] == 2:
					print('crash', sn.name)
					c.delete('snakes' + sn.name)
					if sn.lives > 0:
						el = MySnake.create_element('snakes' + sn.name, sn.body[0]['x'], sn.body[0]['y'], sn.color, True, True, sn.id)
						sn.body.clear()
						sn.body.append(el)
						if not sn.is_bot:
							mg.create_heart(sn.lives)
					mg.create_scores()
				# двигается
				elif new_koord['event'] == 0:
					if g.item_is_move:
						i = len(sn.body) - 1
						while i > 0:
							#c.coords(sn.body[i]['id'], sn.body[i]['x'], sn.body[i]['y'])
							c.coords(sn.body[i]['id'], sn.body[i]['x'], sn.body[i]['y'],
								sn.body[i]['x'] + m.SNAKE_SIZE, sn.body[i]['y'] + m.SNAKE_SIZE)
							i -= 1
					c.coords(sn.body[0]['id'], sn.body[0]['x'], sn.body[0]['y'])
					#c.coords(sn.body[0]['id'], sn.body[0]['x'], sn.body[0]['y'],
					#	sn.body[0]['x'] + m.SNAKE_SIZE, sn.body[0]['y'] + m.SNAKE_SIZE)
		
		root.after(g.speed, MyGame.next_step)

	def move(snake, new_koord_x, new_koord_y):
		#print('move')
		new_koord = [new_koord_x, new_koord_y]
		if g.game_over == False:			
			# двигаем тело
			if g.item_is_move:
				#print('body move', snake.body)
				i = len(snake.body) - 1
				while i > 0:
					#print('item id', snake.body[i])
					snake.body[i]['x'] = snake.body[i - 1]['x']
					snake.body[i]['y'] = snake.body[i - 1]['y']
					c.coords(snake.body[i]['id'],
						snake.body[i]['x'],
						snake.body[i]['y'],
						snake.body[i]['x'] + m.SNAKE_SIZE,
						snake.body[i]['y'] + m.SNAKE_SIZE)
					i -= 1
			snake.body[0]['x'] = new_koord[0]
			snake.body[0]['y'] = new_koord[1]
			#print('move id', snake.body)
			c.coords(snake.body[0]['id'],
				snake.body[0]['x'],
				snake.body[0]['y'])#,
				#snake.body[0]['x'] + m.SNAKE_SIZE,
				#snake.body[0]['y'] + m.SNAKE_SIZE)
			#if MyGame.pc_game.get():
			#	root.after(g.speed, snake.get_move)

		else:
			snake.body = []
			g.game_over = True
			c.delete('all')
			MyGame.game_over_id = c.create_text(m.WIDTH/2, m.HEIGHT/2, anchor='center',
					text='GAME OVER\nScore: ' + str(MyGame.score), font="Arial 20", fill="#990000")
		#else:
		#	g.game_over_id = c.create_text(m.WIDTH/2, m.HEIGHT/2, anchor='center',
		#				text='Server error\nScore: ' + str(g.score), font="Arial 20", fill="#990000")

	def create_bots():
		i = 0
		while i < g.bot_count:
			m.Snake.add_snake(g, len(g.snakes), 'bot' + str(len(g.snakes)), 666, True, g.bot_level)
			MySnake.create_snake()
			i += 1

class MySnake(object):
	def create_element(tag, x, y, color, is_snake=True, is_oval=False, ind=0):
		if is_snake:
			if is_oval:
				#t_id = c.create_image(x, y, image=MyGame.head_pic, anchor='nw', tags=tag)
				t_id = c.create_image(x, y, image=MyGame.head_pic[ind], anchor='nw', tags=tag)
				#t_id = c.create_oval(x, y, x + m.SNAKE_SIZE, y + m.SNAKE_SIZE,
				#		fill=color, tags=tag)
			else:
				#t_id = c.create_image(x, y, image=MyGame.body_pic, anchor='nw', tags=tag)
				t_id = c.create_rectangle(x, y, x + m.SNAKE_SIZE, y + m.SNAKE_SIZE,
						fill=color, tags=tag)
		else:
			t_id = c.create_image(x, y, image=MyGame.kk_pic, anchor='nw', tags=tag)
		return {'id': t_id, 'x': x, 'y': y}

	def create_snake():
		new_snake = g.snakes[len(g.snakes) - 1]
		el = MySnake.create_element('snakes' + new_snake.name, new_snake.body[0]['x'], new_snake.body[0]['y'], new_snake.color, True, True, new_snake.id)
		new_snake.body[0].update({'id': el['id']})

	def change_tail(snake):
		last = len(snake.body) - 1
		if last > 0:
			t_id = snake.body[0]['id']
			snake.body[0]['id'] = snake.body[last]['id']
			snake.body[last]['id'] = t_id
			#el = MySnake.create_element('snakes' + sn.name, new_koord['x'], new_koord['y'], sn.color, False, True)
			#sn.body[1].update({'id': el['id'], 'x': new_koord['x'], 'y': new_koord['y']})


def t_key(name, snake):
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
		if(MyGame.speed == 10000000):
			MyGame.speed = 100
			m.Snake.get_move((snake.body[0]['x'], snake.body[0]['y']), snake.vector)
		else:
			MyGame.speed = 10000000
	elif(name == "Return"):
		start_game()

def key(event):
	is_pc = MyGame.pc_game.get()
	if not is_pc and sock != None:
		entry = {'way': event.keysym}
		#print('keysym', event.keysym)
		data = pickle.dumps(entry)
		sock.send(data)
		if entry['way'] == 'Escape':
			sock.close()
			root.destroy()
	elif event.keysym == 'Escape':
		root.destroy()
	elif is_pc:
		t_key(event.keysym, g.snakes[0])

def option_window(connect_error=False):
	mg.log_label = Label(root,text='Для входа в игру нужно зарегистрироваться на сайте:\nhttps://immense-reaches-92347.herokuapp.com/')
	mg.vs_pc = Checkbutton(root, text="PC", variable = MyGame.pc_game)
	mg.ip_label = Label(root,text='Сервер:')
	mg.ip_text = Entry(root,width=7,font='Arial 12')
	mg.ip_text.insert(END, 'localhost')
	mg.port_label = Label(root,text='Порт:')
	mg.port_text = Entry(root,width=7,font='Arial 12')
	mg.port_text.insert(END, '9090')
	mg.item_is_move.set(g.item_is_move)
	mg.game_type = Checkbutton(root, text="Обычный режим",variable = mg.item_is_move)
	mg.login_label = Label(root,text='Логин:')
	mg.login_text = Entry(root,width=7,font='Arial 12')
	mg.login_text.insert(END, 'Player1')
	mg.pass_label = Label(root,text='Пароль:')
	mg.pass_text = Entry(root,width=7,font='Arial 12',show='*')
	mg.pass_text.insert(END, 'Player1')
	mg.login_btn = Button(root, text="Войти", fg="red",
			command=login)
	mg.bot_label = Label(root,text='Кол-во ботов:')
	mg.bot_count = Entry(root,width=7,font='Arial 12')
	mg.bot_count.insert(END, str(g.bot_count))
	mg.pc_level.set(g.bot_level)
	mg.easy_level = Radiobutton(root, text="Легкий", variable=mg.pc_level, value=3)
	mg.middle_level = Radiobutton(root, text="Средний", variable=mg.pc_level, value=2)
	mg.difficult_level = Radiobutton(root, text="Сложный", variable=mg.pc_level, value=1)

	mg.log_label.grid(row=0,columnspan=4,pady=5)
	mg.vs_pc.grid(row=2,column=4,sticky="W")
	mg.ip_label.grid(row=1,column=0,padx=5,sticky="W")
	mg.ip_text.grid(row=1,column=1)
	mg.port_label.grid(row=1,column=2,sticky="W")
	mg.port_text.grid(row=1,column=3)
	mg.game_type.grid(row=1,column=4,sticky="W")
	mg.login_label.grid(row=2,column=0,padx=5,pady=5,sticky="W")
	mg.login_text.grid(row=2,column=1)
	mg.pass_label.grid(row=2,column=2,sticky="W")
	mg.pass_text.grid(row=2,column=3)
	mg.bot_label.grid(row=3,column=0,padx=5,sticky="W")
	mg.bot_count.grid(row=3,column=1)
	mg.easy_level.grid(row=3,column=2,sticky="E")
	mg.middle_level.grid(row=3,column=3)
	mg.difficult_level.grid(row=3,column=4,sticky="W")
	mg.login_btn.grid(row=0,column=4,padx=5)

	if connect_error:
		mg.error_label = Label(root,text='Cервер недоступен, проверьте адрес и порт!',fg="red")
		mg.error_label.grid(row=4,columnspan=5)

def delete_option_window():
	mg.log_label.grid_remove()
	mg.vs_pc.grid_remove()
	mg.ip_label.grid_remove()
	mg.ip_text.grid_remove()
	mg.port_label.grid_remove()
	mg.port_text.grid_remove()
	mg.game_type.grid_remove()
	mg.login_label.grid_remove()
	mg.login_text.grid_remove()
	mg.pass_label.grid_remove()
	mg.pass_text.grid_remove()
	mg.login_btn.grid_remove()
	mg.bot_label.grid_remove()
	mg.bot_count.grid_remove()
	mg.easy_level.grid_remove()
	mg.middle_level.grid_remove()
	mg.difficult_level.grid_remove()
	if mg.error_label != None:
		mg.error_label.grid_remove()
	if mg.incorrect_login != None:
		mg.incorrect_login.grid_remove()

def login():
	if mg.pc_game.get():
		# игра против ПК
		delete_option_window()
		g.item_is_move = mg.item_is_move.get()
		try:
			g.bot_count = int(mg.bot_count.get())
			max_count = len(m.SNAKE_COLORS) - 1
			if g.bot_count > max_count:
				g.bot_count = max_count
		except:
			print('not integer bot count')
		g.bot_level = mg.pc_level.get()

		g.get_apple_koord()
		mg.create_apple()
		m.Snake.add_snake(g, len(g.snakes), mg.login_text.get(), 3)
		MySnake.create_snake()
		#m.Snake.get_move((new_snake.body[0]['x'], new_snake.body[0]['x']), new_snake.vector)
		# создание ботов
		MyGame.create_bots()

		mg.create_scores()

		c.focus_set()

		m.Snake.dextra_ways(g)
		
		MyGame.next_step()
	else:
		# игра против соперников
		try:
			sock.connect((mg.ip_text.get(), int(mg.port_text.get())))
			sock.settimeout(30)
		except:
			delete_option_window()
			option_window(True)

		entry = {'log': mg.login_text.get(), 'pass': hashlib.md5(mg.pass_text.get().encode()).hexdigest(), 'move':mg.item_is_move.get()}
		data = pickle.dumps(entry)
		sock.send(data)
		#print('sended')

		data = sock.recv(128)
		if data == b'mok' or data == b'nok':
			delete_option_window()

			if data == b'mok':
				g.item_is_move = True
			else:
				g.item_is_move = False
			mg.item_is_move.set(g.item_is_move)
			
			c.focus_set()
			sock.settimeout(10)
			
			Thread(target=listen_server, args=[sock]).start()
		elif mg.incorrect_login == None:
			if mg.error_label != None:
				mg.error_label.grid_remove()
			mg.incorrect_login = Label(root,text='Неправильный логин/пароль.',fg='#990000')
			mg.incorrect_login.grid(row=4,columnspan=5)

def start_game():
	c.delete(MyGame.game_over_id)
	g.game_over = False
	g.apple_koord = (0, 0)
	MyGame.apple_id = 200
	MyGame.score_id = 300
	MyGame.score = 0

	mg.create_score(0)
	mg.create_heart(mg.lives)
	MyGame.create_fence()

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
					c.delete(MyGame.apple_id)
					g.apple_koord = apple_koord
					mg.create_apple()

					#body = entry.get('body', None)
					#if body:
					#	for it in body:
					#		sn = m.Snake.create_element(it['x'], it['y'], m.SNAKE_COLORS[0], True)
			if not MyGame.sn_id:
				id = entry.get('id', None)
				if id:
					MyGame.sn_id = id

			snakes = entry.get('snakes', None)
			if snakes:
				i = 0
				#print('snake')
				for sn in snakes:
					if len(g.snakes) < i + 1:
						# добавился игрок
						print('new snake')
						new_snake = m.Snake(i + 1, sn.name, (sn.body[0]['x'], sn.body[0]['y']))
						el = MySnake.create_element('snakes' + new_snake.name, 0, 0, new_snake.color, True, True)
						new_snake.body[0].update({'id': el['id']})
						g.snakes.append(new_snake)
					else:
						# новых игроков нет
						#print('else', len(sn.body) == len(g.snakes[i].body))
						if len(sn.body) == len(g.snakes[i].body):
							# размер текущего игрока не изменился
							#print('equal len', sn.body[0]['x'], sn.body[0]['y'])
							#print('g.snakes', g.snakes[i].body)
							if sn.is_reverse:
								g.snakes[i].body.reverse()
								MySnake.change_tail(g.snakes[i])
								g.snakes[i].is_reverse = False
							MyGame.move(g.snakes[i], sn.body[0]['x'], sn.body[0]['y'])
						else:
							# размер текущего игрока изменился
							#print('else', sn.name)
							c.delete('snakes' + sn.name)
							g.snakes[i].body.clear()
							if len(sn.body) > 0:
								j = len(sn.body) - 1
								while j >= 0:
									#print('while', j)
									g.snakes[i].add_snake_len(sn.body[j]['x'], sn.body[j]['y'])
									el = MySnake.create_element('snakes' + g.snakes[i].name, sn.body[j]['x'], sn.body[j]['y'], g.snakes[i].color, j == 0 or g.item_is_move, j == 0)
									g.snakes[i].body[0].update({'id': el['id']})
									j -= 1

								if MyGame.sn_id == sn.id:
									MyGame.score = sn.score
									mg.create_score(sn.score)
									MyGame.lives = sn.lives
									mg.create_heart(sn.lives)
								#print('new g.body', g.snakes[i].body)

					i += 1
	except Exception as inst:
		print('except in listen_server', inst)
		g.game_over = True	

c = Canvas(root, width=m.WIDTH, height=m.HEIGHT, bg=m.BACKGROUND)
c.grid(row=4,columnspan=5,padx=5,pady=5)
c.focus_set()
c.bind("<KeyPress>", key)
g = m.GAME
mg = MyGame()
mg.scores_lable = Canvas(root, width=m.WIDTH, height=m.SNAKE_SIZE + 2, bg='#888')
mg.scores_lable.grid(row=5,columnspan=5,padx=5)

start_game()

sock = socket.socket()
#sock.connect(('172.16.161.178', 9090)) 
#sock.connect(('192.168.20.99', 9090))
#sock.connect(('https://immense-reaches-92347.herokuapp.com', 9090))
#sock.settimeout(30)

option_window()
#Thread(target=listen_server, args=[sock]).start()

root.resizable(width=False, height=False)
root.mainloop()