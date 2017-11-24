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
			m.Snake.get_move((snake.body[0]['x'], snake.body[0]['y']), snake.vector, g)
		else:
			m.Game.speed = 10000000
	elif(name == "Return"):
		start_game()

def client_key_listen(client, new_snake):
	try:
		while g.game_over == False:
			#print('key listen before')
			data = client.recv(1024)
			if not data:
				pass
				#print('not data')
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
			#print('key listen after')
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
		while s and len(g.clients) <= m.CLIENTS_COUNT:
			print('listen before')
			client, client_addr = s.accept()
			print('listen after')
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
				print('change move')
			bots = entry.get('bot', None)
			if(bots != None and len(g.clients) == 0):
				try:
					g.bot_count = int(bots)
					print('change b count')
				except:
					g.bot_count = 0
			b_lvl = entry.get('b_lvl', None)
			if(b_lvl != None and len(g.clients) == 0):
				try:
					g.bot_level = int(b_lvl)
					print('change b level')
				except:
					g.bot_level = 0

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
			
			entry = {'move':g.item_is_move, 'bot': g.bot_count, 'b_lvl': g.bot_level}
			data = pickle.dumps(entry)
			client.send(data)
			#client.settimeout(30)

			#cl_id = uuid.uuid4()
			cl_id = len(g.snakes)
			#entry = {'id': cl_id}

			for cl in g.clients:
				if cl['name'] == log:
					log = log + "1"
					break

			print('id', cl_id, log, len(g.snakes), len(g.clients))

			g.clients.append({'id': cl_id, 'name': log, 'client': client, 'addr': client_addr})

			new_snake = m.Snake(cl_id, log, m.START_POSITIONS[len(g.snakes)], 3, cl_id)
			g.snakes.append(new_snake)

			if len(g.snakes) == 1:
				print('new game')
				g.game_over = False
				i = 0
				while i < g.bot_count:
					m.Snake.add_snake(g, len(g.snakes), 'bot' + str(len(g.snakes)), 3, True, g.bot_level)
					i += 1
			m.Snake.dextra_ways(g)
			
			Thread(target=client_key_listen, args=(client, new_snake)).start()
	except exc_sock_timeout:
		print('accept timeout')
		if(len(g.clients) == 0):
			g.game_over = True
			print('close sock from client_listen')
			s.close()
	except Exception as inst:
		print('client_listen error', inst)
		print('sock', s)
		#g.game_over = True
		s = None

def start_game():
	while True:
		g.game_over = False
		#g.snake = []
		g.apple_koord = (0, 0)
		g.get_apple_koord()
		g.fortune.clear()
		g.fortune.append(m.Game.calc_apple_koord())
		s = socket()

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
			while max_score < 250:
				i += 1
				for sn in g.snakes:
					if not sn.sn_game_over and len(sn.body) > 0:
						if sn.is_bot:
							sn.bot_vector(g)
						#print('before', sn.name, sn.body, g.game_over)
						new_koord = sn.snake_move(g)
						if new_koord['event'] == 4:
							g.fortune.clear()
							g.fortune.append(m.Game.calc_apple_koord())
						#print('after', sn.name, sn.body, new_koord)
						if sn.score > max_score:
							max_score = sn.score
				for sn in g.snakes:
					try:
						if not sn.is_bot:
							entry = {'apple_koord': g.apple_koord, 'id': sn.id, 'name': sn.name, 'snakes': g.snakes, 'fortune': g.fortune}
							if g.game_over or sn.sn_game_over:
								entry['end'] = 1
							#print('entry', sn.body)
							data = pickle.dumps(entry)
							#print('send to', sn.name, len(g.clients))
							for cl in g.clients:
								if cl['name'] == sn.name:
									cl['client'].send(data)
									break
							#g.clients[sn.id]['client'].send(data)
						#exception_count = 0
						sn.is_reverse = False
					except:
						#print('except', 'name', sn.name)
						m.SNAKE_COLORS.append(sn.color)
						g.snakes.remove(sn)
						cl_len = len(g.clients)
						j = 0
						while j < cl_len:
							#print('check name', g.clients[j]['name'])
							if g.clients[j]['name'] == sn.name:
								el = g.clients.pop(j)
								#print('popped', el['name'])
								cl_len -= 1
							else:
								j += 1
						#print('check')
						g.check_game()
						if g.game_over:
							for t_sn in g.snakes:
								m.SNAKE_COLORS.append(t_sn.color)
							g.snakes.clear()
						#print('check2', g.game_over)
						#exception_count += 1
				#if g.game_over or exception_count > 5:
				#	g.game_over = True
				#	print('close sock from startgame', g.game_over, exception_count > 5)
				#	s.close()
				#	break;

				#t.sleep(g.speed/1000)
				t.sleep(g.speed/100)
				#client.sendall(data.upper())
			#	t.sleep(5)
			#	break;
			else:
				#print('del else')
				s = None
				entry = {'end': 1}
				data = pickle.dumps(entry)
				for sn in g.snakes:
					m.SNAKE_COLORS.append(sn.color)
				for cl in g.clients:
					cl['client'].send(data)
				#print('del snakes')
				g.snakes.clear()
				g.clients.clear()
				g.game_over = True

s = socket()
t_addr = ('0.0.0.0', 9090)
# 192.168.20.99
g = m.GAME
start_game()
#s = Snake('Player' + str(len(m.Game.snakes)), (0, len(m.Game.snakes) * m.SNAKE_SIZE + 0))
#s2 = Snake('Player2', (0, 30))
#c.bind("<Button-1>", callback)
