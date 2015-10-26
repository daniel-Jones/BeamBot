package es.danieljon;

import java.io.*;
import java.net.*;

// BeamBot made in Java by Daniel Jones for #BeamNG

public class Main { // main class
    // setting some needed variables
    public static String NickName = "BeamBot"; // the bots name
    public static final String Channel = "#beamng"; // the channel we will connect to
    private static final String ServerAddress = "irc.3phasegaming.net"; // the server we will connect to
    private static final int ServerPort = 6667; // the server port we will connect to
    public static String LineIn = null; // this will hold our raw input data
    public static String CleanLine = null; // this will hold our clean line
    public static boolean ConnectedToChannel = false; // this will hold our channel status

    public static void main(String[] args) throws IOException { // main method
        System.out.println("BeamBot in Java running.");
        // we shall initiate a connection here
        Socket Socket = new Socket(ServerAddress, ServerPort); // create our connection
        BufferedWriter Writer = new BufferedWriter(new OutputStreamWriter(Socket.getOutputStream())); // create an instance of our writer
        BufferedReader Reader = new BufferedReader(new InputStreamReader(Socket.getInputStream())); // create an instance of our reader
        // we are setup with our connection, now to follow IRC protocol and write some things to the socket
        Writer.write("NICK " + NickName + "\r\n"); // send our nickname
        Writer.write("USER " + NickName + " 8 * : Java BeamBot by daniel_j\r\n"); // send some user information
        Writer.flush(); // flush our socket
        // now we have sent our information
        while ((LineIn = Reader.readLine()) != null) { // this will not be null if we are connected and have received data
            if (LineIn.toUpperCase().startsWith("PING ")) { // ping found, we must reply
                Writer.write("PONG " + LineIn.substring(5) + "\r\n"); // write our pong reply
                System.out.println("Pong sent");
                if(!ConnectedToChannel) { // if we aren't connected to a channel, we must connect
                    Writer.write("JOIN " + Channel + "\r\n"); // join the channel
                    ConnectedToChannel = true; // set connected to true
                    System.out.println("Joined the channel");
                } // connect to channel
                Writer.flush(); // flush our socket
            } else { // raw line, we can deal with it here
                if (LineIn.contains("KICK " + Channel) || LineIn.contains("JOIN :" + Main.Channel) || LineIn.contains("PART " + Main.Channel) || LineIn.contains("ACTION")) { // action detected
                    ActionDetection.DetectAction(LineIn); // parse our action
                } else { // not an action, proceed
                    if (LineIn.contains("PRIVMSG " + Channel)) { // a channel message is detected
                        CleanLine = LineParsing.CleanLine(LineIn); // parse our line
                        Logging.LogLine(CleanLine); // send our clean line out for logging
                        if (CleanLine.startsWith("?") || CleanLine.startsWith("!")) { // if our clean line is a possible command, look for it
                            String InterpretReturn = CommandInterpretation.InterpretCommand(CleanLine); // interpret our possible command
                            if (InterpretReturn != "null") { // command found, print the return
                                Writer.write("PRIVMSG " + Channel + " :" + InterpretReturn + "\r\n");
                                Writer.flush(); // flush our socket
                            } // command found
                        } // possible command
                    } // channel message
                } // parsing our message
            } // raw line parsing
        } // we are connected
    } // main method
} // main class