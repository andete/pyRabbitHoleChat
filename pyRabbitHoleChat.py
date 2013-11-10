#! /usr/bin/env python2

'''
	Program Created by Paul Schimmelpfenning and is licensed under the 
	GNU Affero General Public License version 3 or later License.
	See the COPYRIGHT file.
	My website is at http://www.pjschim.com
'''

import ConfigParser
import gtk
import pygtk
import random
import socket
import sys
import threading
import time
import warnings

pygtk.require('2.0')

class pyRabbitHoleChat:

	def __init__(self):
		parser = ConfigParser.SafeConfigParser()
		parser.read('config')
		self.username = parser.get('login_settings', 'username')
		self.address = parser.get('login_settings', 'address')
		self.port = int(parser.get('login_settings', 'port'))
		self.users = {}
		self.s = socket.socket()
		self.recv_data = ''
		self.bufferSize = 1024
		self.startup = 1
		self.buffer = ''
		self.userID = ''
		self.uNameGather = 0
		if self.username == '':
			self.username = 'RabbitHole' + str(random.randint(0, 5000))
		self.builder = gtk.Builder()
		self.builder.add_from_file('GUI.xml')
		self.window = self.builder.get_object('window')
		self.window.set_title ("pyRabbitHoleChat")
		self.status = self.builder.get_object('status')
		self.scrolledwindow = self.builder.get_object('scrolledwindow')
		self.messages = self.builder.get_object('messages')
		self.unamelabel = self.builder.get_object('unamelabel')
		self.input = self.builder.get_object('input')
		self.input.connect('activate', self.sendPacket)
		self.chatConnect()
		self.window.connect('destroy', gtk.main_quit)
		self.window.set_default_size(640,480)
		self.window.show()
		warnings.filterwarnings("ignore")

	def main(self):
		gtk.threads_enter()
		gtk.main()
		gtk.threads_leave()
	
	def chatConnect(self):
		try:
			self.s.connect((self.address, self.port))
		except Exception, e:
			self.printOutput("Could Not Connect")
		data = self.s.recv(self.bufferSize)
		hash = data[3:]
		authString = chr(len(self.username)) + self.username + hash
		authLen = self.strLen(authString)
		authType = chr(0)
		self.s.send(authLen + authType + authString)

		progStartThread = threading.Thread(target=self.progStart)
		progStartThread.daemon = True
		progStartThread.start()
		recvDataThread = threading.Thread(target=self.recvData)
		recvDataThread.daemon = True
		recvDataThread.start()

	def progStart(self):
		while self.uNameGather == 0:
			pass
		time.sleep(.5)
		self.startup = 0
		self.namelistOutput()

	def strLen(self, string):
		lenX = len(string) / 256
		lenY = len(string) % 256
		return chr(lenX) + chr(lenY)
	
	def namelistOutput(self):
		namelist = ''
		for name in sorted(self.users.values()):
			namelist += '[ ' + name + ' ] '
		self.printOutput(namelist[:-1])

	def printOutput(self, output):
		self.tBox = self.messages.get_buffer()
		visible = self.messages.get_visible_rect()
		max_y_pos = visible.y + visible.height
		last_line_pos = sum(self.messages.get_line_yrange(self.tBox.get_end_iter()), -2)
		self.tBox.insert(self.tBox.get_end_iter(), str(output) + '\n')
		if last_line_pos < max_y_pos:
			self.messages.scroll_to_mark(self.tBox.get_insert(), 0);

	def recvData(self):
		while 1:
			self.buffer += self.s.recv(self.bufferSize)
			self.uNameGather = 1
			while len(self.buffer) > 0:
				packetLen = ord(self.buffer[0]) * 256 + ord(self.buffer[1]) + 3
				if len(self.buffer) >= packetLen:
					tmp = self.buffer[:packetLen]
					self.tmpEval(tmp)
					self.buffer = self.buffer[len(tmp):]

	def tmpEval(self, tmp):
		curTime = time.strftime("%H:%M", time.localtime())
		if ord(tmp[2]) == 0:
			self.userID = tmp[3:]
		if ord(tmp[2]) == 1:
			if ord(tmp[3]) == 0:
				chatRoomName = tmp[4:]
				self.status.set_label('Connected to Chat Room: ' + chatRoomName)
			if ord(tmp[3]) == 1:
				xMax = tmp[4:]
			if ord(tmp[3]) == 2:
				yMax = tmp[4:]
			if ord(tmp[3]) == 3:
				zMax = tmp[4:]
			if ord(tmp[3]) == 4:
				xPos = tmp[4:]
			if ord(tmp[3]) == 5:
				yPos = tmp[4:]
			if ord(tmp[3]) == 6:
				zPos = tmp[4:]
		if ord(tmp[2]) == 3:
			uID = tmp[5:5 + ord(tmp[4])]
			uName = tmp[5 + ord(tmp[4]):]
			uNameOld = ''
			if ord(tmp[3]) == 0:
				if uID == self.userID:
					self.username = uName
					self.unamelabel.set_label(self.username)
				if len(tmp[5:]) > ord(tmp[4]):
					if uID in self.users:
						uNameOld = self.users[uID]
					self.users[uID] = uName
					if self.startup == 0:
						if uNameOld == '':
							self.printOutput(curTime + ' -!- ' + uName +
								' has logged in')
						else:
							if uID == self.userID:
								self.printOutput(curTime + ' -!- ' + 
									uNameOld + ' is now known'
									' as ' + uName)
							else:
								self.printOutput(curTime + ' -!- ' +
									uNameOld + ' is now known as ' + uName)
				else:
					if uID in self.users:
						if self.startup == 0:
							self.printOutput(curTime + ' -!- ' +
								self.users[uID] + ' has quit')
						del self.users[uID]
		if ord(tmp[2]) == 4:
			uID = tmp[5:5 + ord(tmp[4])]
			broadcast = tmp[5 + ord(tmp[4]):]
			if ord(tmp[3]) == 0:	
				self.printOutput(curTime + ' <' + self.users[uID] + '> ' +
					broadcast)
	
	def sendPacket(self, widget, data = None):
		commands = {'/h': 'Displays usable commands',
			'/help': 'Displays usable commands',
			'/n': 'Displays online users',
			'/nick' : '/nick n changes your username to n',
			'/quit': 'Quit pyRabbitHoleChat'
			}
		finalMessage = self.input.get_text()
		self.input.set_text('')
		curTime = time.strftime("%H:%M", time.localtime())
		if finalMessage == '/quit':
			self.s.shutdown(socket.SHUT_RDWR)
			self.s.close()
			gtk.main_quit()
		elif finalMessage == '/nick' or finalMessage[:6] == '/nick ':
			if len(finalMessage) > 6:
				alias = '\x00' + finalMessage[6:]
				self.s.send(self.strLen(alias) + '\x03' + alias)
			elif len(finalMessage) == 5:
				self.printOutput(curTime + ' -!- Your current username is ' +
					self.username)
			elif len(finalMessage) == 6:
				self.printOutput('You need to specify a desired username')
		elif finalMessage == '/n':
			self.namelistOutput()
		elif finalMessage == '/h' or finalMessage == '/help':
			for command in sorted(commands):
				self.printOutput(command + ' - ' + commands[command])
		elif len(finalMessage) > 0:
			if finalMessage[0] != '/':
				message = '\x00' + finalMessage
				self.printOutput(curTime + ' <' + self.users[self.userID] +
					'> ' + finalMessage)
				self.s.send(self.strLen(message) + '\x04' + message)
			else:
				if finalMessage.split(' ')[0] in commands:
					self.printOutput("Invalid Command")
				else:
					self.printOutput("Command " + finalMessage.split(' ')[0] + 
						' is not recognized')

if __name__ == '__main__':
	gtk.gdk.threads_init()
	application = pyRabbitHoleChat()
	application.main()
