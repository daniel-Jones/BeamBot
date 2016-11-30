# -*- coding: utf-8 -*-
########################################
# BeamBot written as a web application #
########################################

import socket, SocketServer, urllib2, os, time;
from threading import Thread;

###########################
# bot and logging classes #
###########################

class bot:
        server = "irc.danieljon.es";
        port = 6667;
        name = "BeamBot";
        channel = "#fun";
	debug = False;
        connected = False;
        ops = ["daniel_j", "badSol"];
        socket = socket.socket();
	commandfile = "commands.txt";

class log:
        file = "log.txt";

bot = bot;
log = log;

################################
# command input server handler #
################################

class MyTCPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		self.data = self.request.recv(1024).strip();
		if (bot.debug):
			print("{} wrote:".format(self.client_address[0]));
			print(self.data);
		self.request.sendall("ACKNOWLEDGED");
		socket_send_msg(self.data);

###########################
# bot connection function #
###########################

def connection_thread():
	print("Connecting to " + bot.server + " as " + bot.name);
	try:
		bot.socket.connect((bot.server, bot.port));
		data = bot.socket.makefile('r', 4096);
	except socket.error, msg:
		print("Failed to connect to the server: %s" % msg);
		raise SystemExit(0);
	bot.socket.send("NICK " + bot.name + "\r\n");
	bot.socket.send("USER " + bot.name + " bot bot bot \r\n");
	while True:
		line = data.readline().strip();
	        if (line.find("PING")) != -1:
		        bot.socket.send("PONG :" + line.split(":")[1]);
			bot.connected = False;
		if (not bot.connected):
			bot.socket.send("MODE " + bot.name + " +x\r\n");
			bot.socket.send("JOIN " + bot.channel + "\r\n");
			bot.connected = True;
			if (bot.debug):
				print("bot.connected = False");
		if (bot.debug):
			print line;
		if (len(line) > 1 and bot.connected and line.find("!") != -1):
			try:
				user = line.split("!", 1)[0][1:];
				message = line.split("@", 1)[1].split(":", 1)[1];
				if (message[:1] == "?"):
					command_check(message);
				log_line(user, message);
			except IndexError:
				print("Index error in connection_thread() setting user/message");


########################
# command input server #
########################

def server_thread():
	if (bot.debug):
		print("Server thread started");
	HOST, PORT = "localhost", 6666;
	server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler);
	server.serve_forever();

####################
# socket functions #
####################
	
def socket_send_msg(message):
	bot.socket.send("PRIVMSG " + bot.channel + " :" + message + "\r\n");

def socket_send_action(message):
	bot.socket.send("PRIVMSG " + bot.channel + " \x01ACTION " + message + "\r\n");

##########################
# console input function #
##########################

def parse_input(com):
	err = True;
	try:
		if (com.split(" ", 1)[0] == "say"):
			socket_send_msg(com.split(" ", 1)[1]);
			err = False;
		if (com.split(" ", 1)[0] == "action"):
			socket_send_action(com.split(" ", 1)[1]);
			err = False;
		if (com == "debug"):
			if (bot.debug):
				bot.debug = False;
				print("Debugging off");
				err = False;
			else:
				bot.debug = True;
				print("Debugging on");
				err = False;
	except IndexError:
		print("Index error in parse_input");
	if (err):
		print("Unknown command");

#####################
# logging functions #
#####################

# TODO implement join/part messages

def log_line(user, message):
	try:
		flog = open(log.file, 'a+');
		flog.write(user + ": " + message + "\n");
	except IOError:
		if (bot.debug):
			print("Error parsing/writing log file in log_line(), line: + " + line);

#####################
# check for command #
#####################

def command_check(message):
	try:
		file = open(bot.commandfile, "a+");
		for line in file.readlines():
			if (line.split(":", 1)[0].upper() == message.split(" ", 1)[0].upper()):
				socket_send_msg(line.split(":", 1)[1]);	

		
	except IOError:
		print("Cannot parse command/read commands file.");

#################
# main function #
#################

def main():
	print("main function run, beginning threads");
        con_thread = Thread(target=connection_thread, args=());
	serv_thread = Thread(target=server_thread, args=());
	# run the threads
	con_thread.daemon = True;
	serv_thread.daemon = True;
	con_thread.start();
	serv_thread.start();
	time.sleep(3);
	print("***********************");
	print("* Console for BeamBot *");
	print("***********************");
	while True:
		com = raw_input("> ");
		parse_input(com);

if __name__ == "__main__":
	main();
