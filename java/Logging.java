package es.danieljon;

// this class will handle all logging

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class Logging { // logging class

    // :daniel_j!daniel@god KICK #fun name :message test

    public static void LogLine(String Line) throws IOException { // this method will handle file logging
        try(PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter("BeamNG.txt", true)))) { // here we will write our log line
            if(LineParsing.User != "null") { // not an action
                out.println("<" + LineParsing.User + "> " + Line);
                System.out.println("<" + LineParsing.User + "> " + Line);
            } else { // an action is to be logged
                out.println(Line); // this was an action, log it raw
            } // log an action
        } // log to file
    } // file logging
} // logging class
