# -*- coding: utf-8 -*-
import socket, urllib2, os;
from time import gmtime, strftime;
'''
BeamBot remade.
The old BeamBot was a compilation of horrible scripts written when I really had no idea what I was doing.
By Dan Jones for #BeamNG
'''

class BeamBot:
    HostName = "irc.danieljon.es"; # the hostname/IP of the IRC server
    Port = 6667; # the port used
    NickName = "BeamBot"; # the bots nickname
    Channel = "#fun" # our default channel to join
    Connected = False; # we use this later when connecting
    ImportantPeople = ["daniel_j", "badSol", "akino_germany", "DarthCain"]; # people who can use special commands

class Logging:
    LogName = "BeamNG.txt" # the file we will log messages to
    CleanLine = "null"; # this will hold the lines we use for logging
    CurrentUser = "null"; # last user who sent a message
    FileLine = "null"; # this is our file line
Bot = BeamBot; # initialize our bot information class
Log = Logging; # initialize our logging class

def WelcomeMessage(): # this function will send new users a welcome message
    WelcomeFile = "welcome.txt"; # set our welcome file name
    try: # try to load our file
        WelcomeMessage = open(WelcomeFile).read(); # read our welcome file
        ToReturn = "PRIVMSG #fun :" + Log.CurrentUser + " " + WelcomeMessage; # send our welcome message
        #return "PRIVMSG " + Bot.Channel + " :" + WelcomeMessage;

        #print "sent: " + WelcomeMessage + " to : " + Log.CurrentUser

    except: # file not found
        print("Can't load the welcome file");



def CheckForCommands(DataLine): # check for commands
    CommandsFile = open("commands.txt", "a+"); # open our file that contains the commands
    for Log.FileLine in CommandsFile.readlines():
        if(Log.FileLine.split(":")[0].upper() == Log.CleanLine.split(" ", 1)[0].upper()): # if the command is found we will send the response to the channel
            CommandsFile.close();
            return "PRIVMSG " + Bot.Channel + " :" + Log.FileLine.split(":", 1)[1]; # return the message we will send to the channel
        Log.FileLine = CommandsFile.readline(); # read a new line into the buffer
    CommandsFile.close();
    return "";


def CheckForFunkyCommands(DataLine): # here we look for some funky commands 
    try: # make sure we have the required info
        PossiblyFunky = DataLine.split("!")[1].split(" ")[0];
        FunkyParameter = DataLine.split("!")[1].split(" ", 1)[1];
    except: # funky paramter missing
        return "PRIVMSG " + Bot.Channel + " :Command parameter missing. All '!' commands require atleast one parameter!";

    if(PossiblyFunky.upper() == "USER"): # user wants to find someones BeamNG account...
        ToReturn = "PRIVMSG " + Bot.Channel + " :" + "http://www.beamng.com/member.php?username=" + FunkyParameter.replace(" ", "%20"); # set our return variable
        Log.FileLine = ToReturn;
        return ToReturn;

    if(PossiblyFunky.upper() == "ADDCOMMAND"): # add a command
        if(Log.CurrentUser in BeamBot.ImportantPeople): # is the user important?
            if(FunkyParameter[0] != "?"): # a ? is needed
                FunkyParameter = "?" + FunkyParameter; # append a ?
            if(FunkyParameter.find(":") == -1): # no text, the user is an idiot
                ToReturn = "PRIVMSG " + Bot.Channel + " :" + "You aren't very good at this. Example: !addcommand ?command:text to add"; # return message
            else:
                File = open('commands.txt','a') # open the file
                File.write('\n' + FunkyParameter) # write the new command
                File.close() # close file
                ToReturn = "PRIVMSG " + Bot.Channel + " :" + "Command " + str(FunkyParameter.split(":", 1)) + " added to the list"; # return message

        else:
            ToReturn = "PRIVMSG " + Bot.Channel + " :" + "You can't do this, I have no idea who you are."; # return message
        Log.FileLine = ToReturn;
        return ToReturn;

    if(PossiblyFunky.upper() == "REMOVECOMMAND"): # uremove a command
        Check = 0; # check if a command was deleted
        if(Log.CurrentUser in BeamBot.ImportantPeople): # is the user important?
            log = open("new.txt", "w"); # new file
            for line in open("commands.txt"): # all commands
                print line.split(":", 1)[0];
                print FunkyParameter;
                if not FunkyParameter.upper() in line.split(":", 1): # find the one selected
                    log.write(line) # write to our new file
                    log.close; # close file 
                else:
                    Check+= 1;
            if(Check < 1): # no command deleted
                ToReturn = "PRIVMSG " + Bot.Channel + " :" + "Command not found in the list"; # return message
            else:
                os.remove("commands.txt"); # remove our old commands file
                os.rename("new.txt", "commands.txt"); # rename our new file
                ToReturn = "PRIVMSG " + Bot.Channel + " :" + "Command (" + FunkyParameter + ") removed."; # return message
        else:
            ToReturn = "PRIVMSG " + Bot.Channel + " :" + "You can't do this, I have no idea who you are."; # return message
        Log.FileLine = ToReturn;
        return ToReturn;

def ParseRawDataAndLog(DataLine): # this function will return a clean string to log with etc
    try:
        Log.CurrentUser = DataLine.split("!")[0][1:]; # last user to send a message
        Log.CleanLine = DataLine.split("@")[1].split(":", 1)[1]; # the message sent
        if(DataLine.split("@")[1].split(":")[0][-6:].find("JOIN") != -1): # user joined the channel
            print(Log.CurrentUser + " Joined the channel\n");
            LoggingFile = open(Log.LogName, 'a+'); # open our log for writing, ONLY ONCE!
            LoggingFile.write("(" + Log.CurrentUser + " joined the channel)\n"); # write to our logging file
            LoggingFile.close(); # close our file after writing the line
            WelcomeMessage(); # send the user the welcome message


        if(DataLine.split("@")[1].split(":", 1)[0].find("KICK") != -1): # user was kicked
            print(DataLine.split("#")[1].split(" ")[1].split(" ")[0] + " was kicked from the channel. Reason: " + Log.CleanLine + "\n");
            LoggingFile = open(Log.LogName, 'a+'); # open our log for writing, ONLY ONCE!
            LoggingFile.write("(" + DataLine.split("#")[1].split(" ")[1].split(" ")[0] + " was kicked from the channel. Reason: " + Log.CleanLine + ")\n"); # write to our logging file
            LoggingFile.close(); # close our file after writing the line

        if((DataLine.split("@")[1].split(":", 1)[0].find("QUIT") != -1) or (DataLine.split("@")[1].split(":", 1)[0].find("PART") != -1) or (DataLine.split("@")[1].split(":", 1)[0].find("TIMEOUT") != -1)): # user quit
            print(Log.CurrentUser + " Left the channel.\n");
            LoggingFile = open(Log.LogName, 'a+'); # open our log for writing, ONLY ONCE!
            LoggingFile.write("(" + Log.CurrentUser + " Left the channel.)\n"); # write to our logging file
            LoggingFile.close(); # close our file after writing the line

        # Don't juge this line, he's a very special retard
        if(Log.CurrentUser != Bot.NickName and DataLine.split("@")[1].split(":", 1)[0][-6:].find("JOIN") == -1 and DataLine.split("@")[1].split(":")[0].find("KICK") == -1): # we really want to ignore the bot...
            print("<" + Log.CurrentUser + "> " + " " + Log.CleanLine);
            LoggingFile = open(Log.LogName, 'a+'); # open our log for writing, ONLY ONCE!
            LoggingFile.write(strftime("%H:%M:%S", gmtime()) + " <" + Log.CurrentUser + "> " + " " + Log.CleanLine + "\n"); # write to our logging file
            LoggingFile.close(); # close our file after writing the line


    except: # line confused as a channel message, simply ignore
        print("Line confused as channel message, ignoring...\n");

print("Connecting as: " + Bot.NickName + " to: " + Bot.HostName + " : " + str(Bot.Port));

'''
at this point we are ready to create and connect to our socket
we will then run a loop that will recieve information, handle PING/PONG, log messages, parse commands from file etc
'''
try:
    Socket = socket.socket(); # setup our socket for connections
    Socket.connect((Bot.HostName, Bot.Port)); # connect to our IRC server
    Data = Socket.makefile('r', 4096); # our data stream
    MessageToSend = "";
except:
    print("Connection error.\nAre you sure " + Bot.HostName + " has an IRC daemon running on port " + str(Bot.Port) + "?");
    raise SystemExit(0); # stop the bot at this point
# We are connected to the server, we must now send IMPORTANT user information to be accepted
Socket.send("NICK " + Bot.NickName + "\r\n"); # auth with our nickname
Socket.send("USER " + Bot.NickName + " " + Bot.NickName + " " + Bot.NickName + " :" + Bot.NickName + "\r\n"); # auth our real name etc
while True: # this loop will run forever
    DataLine = Data.readline().strip(); # this will hold our raw line of data
    if(DataLine.find("PING")) != -1: # detected ping
        Socket.send("PONG :" + DataLine.split(":")[1]); # send pong
        if(not Bot.Connected): # if we are not connected, we need to auth
            print("Authenticating and joining " + Bot.Channel + "..");
            Socket.send("PRIVMSG R : Login <>\r\n");
            Socket.send("MODE " + Bot.NickName + " +x\r\n"); # set mode +x
            Socket.send("JOIN " + Bot.Channel + "\r\n"); # join our channel
            Bot.Connected = True; #set the bot as connected
    if(len(DataLine) > 1 and Bot.Connected and DataLine.find("!") != -1):
        ParseRawDataAndLog(DataLine); # this will return a clean string that we can use for commans and logging
        if(Log.CleanLine[:1].find("?") != -1): # if the line is a POSSIBLE command, look for it
            MessageToSend = CheckForCommands(DataLine); # this will call our function that will check a list of commands for one matching what a user has typed
           
        if(Log.CleanLine[:1].find("!") != -1 and len(Log.CleanLine) > 4): # this line could POSSIBLY be a funky command, lets get FUNKAH
            MessageToSend = CheckForFunkyCommands(Log.CleanLine); # lets look for some funky commands
            
        if(MessageToSend != ""): # make sure we have a message to send
            try:
                Socket.sendall("\n" + MessageToSend + "\n"); # send the message to the channel
                LoggingFile = open(Log.LogName, 'a+'); # open our log for writing, ONLY ONCE!
                LoggingFile.write(strftime("%H:%M:%S", gmtime()) + "<" + Bot.NickName + "> " + " " + Log.FileLine.split(":", 1)[1]); # write to our logging file
                LoggingFile.close(); # close our file after writing the line
            except:
                print("Unknown error, ignoring everything.");
            MessageToSend = "";

