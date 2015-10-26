package es.danieljon;

// this class will detect actions and log them accordingly
// :test!webchat@daniels.irc.network-C05D99D.lns20.adl2.internode.on.net PART #fun :

import java.io.IOException;

public class ActionDetection { // main class

    public static String UserActionName = null; // this stores who performed the action
    public static String Message = null; // this will store any message that may have been stated

    public static void DetectAction(String Line) throws IOException { // this method will detect any actions
        if(Line.contains("KICK " + Main.Channel)) { // a user was kicked
            LineParsing.User = "null"; // set our user to null
            UserActionName = Line.split("KICK " + Main.Channel + " ")[1].split(" ")[0]; // set our users name
            Message = Line.split("KICK " + Main.Channel + " ")[1]; // set our message
            System.out.println(UserActionName + " was kicked from " + Main.Channel + " reason: " + Message);
            Logging.LogLine(UserActionName + " was kicked from " + Main.Channel + " reason: " + Message); // log our line
        } // user kicked

        if(Line.contains("PART " + Main.Channel)) { // user parted
            LineParsing.User = "null"; // set our user to null
            UserActionName = Line.split("!")[0].split(":")[1]; // set our user name
            try { // try set a part message
                Message = Line.split(Main.Channel + " :")[1]; // set our message if one exists
            } catch (Exception e) {Message = "no reason set";} // no message set
            System.out.println(UserActionName + " parted from " + Main.Channel + " reason: " + Message);
            Logging.LogLine(UserActionName + " parted from " + Main.Channel + " reason: " + Message); // log our line
        } // user parted

        if(Line.contains("JOIN :" + Main.Channel)) { // user joined the channel
            LineParsing.User = "null"; // set our user to null
            UserActionName = Line.split("!")[0].split(":")[1]; // set our user name
            System.out.println(UserActionName + " joined " + Main.Channel);
            Logging.LogLine(UserActionName + " joined " + Main.Channel); // log our action
        } // user joined the channel

        if(Line.contains("\u0001ACTION")) { // action detected
            LineParsing.User = "null"; // set our user to null
            String ActionUser = Line.split("!")[0].replace(":", ""); // set our action user
            String ActionMessage = Line.split("\u0001ACTION")[1].replace("\u0001", ""); // set our action message
            System.out.println("* " + ActionUser + " " + ActionMessage);
            Logging.LogLine("* " + ActionUser + " " + ActionMessage); // log our action
        } // action detected
    } // detect action
} // main class
