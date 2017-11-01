# coding: utf8

from socket import socket, timeout as exc_sock_timeout
import time as t
import pickle
import uuid
import hashlib
#from models import SnakeUser
import snake_main as m



#from tkinter import *
#from sqlite3 import connect
from threading import Thread
#import ttk

#CON = connect('snake.db')
#CUR = CON.cursor()

#root = Tk()

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
		if(m.Game.speed == 10000000):
			m.Game.speed = 100
			m.Snake.get_move((snake.body[0]['x'], snake.body[0]['y']), snake.vector)
		else:
			m.Game.speed = 10000000
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
					#s.close()
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
		while len(g.clients) <= m.CLIENTS_COUNT:
			client, client_addr = s.accept()
			client.settimeout(60)
			print(client_addr)
			data = client.recv(1024)
			entry = pickle.loads(data)
			log = entry.get('log', None)
			print('log', log)
			pas = entry.get('pass', None)
			# первый игрок задает тип игры
			it_move = entry.get('move', None)
			if(it_move != None and len(g.clients) == 0):
				g.item_is_move = it_move

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
			
			if g.item_is_move:
				client.send(b'mok')
			else:
				client.send(b'nok')
			client.settimeout(15)

			#cl_id = uuid.uuid4()
			cl_id = len(g.snakes) + 1
			#entry = {'id': cl_id}
			print('id', cl_id)

			g.clients.append({'id': cl_id, 'name': log, 'client': client, 'addr': client_addr})

			new_snake = m.Snake(cl_id, log, m.START_POSITIONS[len(g.snakes)])
			g.snakes.append(new_snake)
			
			Thread(target=client_key_listen, args=(client, new_snake)).start()
	except exc_sock_timeout:
		print('accept timeout')
		if(len(g.clients) == 0):
			g.game_over = True
			print('close sock from client_listen')
			s.close()
	except Exception as inst:
		print('client_listen error', inst)
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
		max_score = 0
		while max_score < 1000:
			i += 1
			for sn in g.snakes:
				new_koord = sn.snake_move(g)
				if sn.score > max_score:
					max_score = sn.score
			for sn in g.snakes:
				try:
					entry = {'apple_koord': g.apple_koord, 'id': sn.id, 'name': sn.name, 'snakes': g.snakes}
					#print('entry', sn.body)
					data = pickle.dumps(entry)
					g.clients[sn.id - 1]['client'].send(data)
					exception_count = 0
					sn.is_reverse = False
				except:
					print('except', 'id', sn.id)
					g.snakes.remove(sn)
					exception_count += 1
			#if g.game_over or exception_count > 5:
			#	g.game_over = True
			#	print('close sock from startgame', g.game_over, exception_count > 5)
			#	s.close()
			#	break;

			#t.sleep(g.speed/10000)
			t.sleep(0.1)
			#client.sendall(data.upper())
		#	t.sleep(5)
		#	break;

s = socket()
t_addr = ('0.0.0.0', 9090)
# 192.168.20.99
g = m.GAME
start_game()
#s = Snake('Player' + str(len(m.Game.snakes)), (0, len(m.Game.snakes) * m.SNAKE_SIZE + 0))
#s2 = Snake('Player2', (0, 30))
#c.bind("<Button-1>", callback)
