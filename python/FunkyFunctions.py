# this file holds our functions for BeamBot that aren't critical

def CheckForFunkyCommands(DataLine): # here we look for some funky commands 
	FunkyCommands = ["user", "reg"]; # funky commands array
	PossiblyFunky = DataLine.split("!")[1].split(" ")[0];
	if(PossiblyFunky in FunkyCommands): # found a funky commands
		return "PRIVMSG " + Bot.Channel + " :" + "ayyyylmao";
	return "";