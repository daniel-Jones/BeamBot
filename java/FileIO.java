package es.danieljon;

// this class will handle all file I/O

import java.io.*;
import java.nio.file.Files;


public class FileIO { // file IO

    public static String CommandToParse = null; // this will hold the command we parse for later use
    public static String CommandFromParse = null; // this string will hold the command used to display a '?' command
    public static String TextFromParse = null; // this string will hold the text that is displayed via a '?' command
    public static String CommandToAdd = null; // this will hold the final string we will append to our commands file
    public static String RemoveCommand = null; // this holds the command we will remove

    public static String GetCommandsFile(String Command) throws IOException { // this method will get the contents of our commands file
        BufferedReader File = new BufferedReader(new FileReader("commands.txt")); // open our file for reading
        String CurrentLine; // this holds our current line
        while ((CurrentLine = File.readLine()) != null) { // loops through entire file
            if(CurrentLine.split(":")[0].equals(Command.toUpperCase())) // our command is found
                return CurrentLine.split(":", 2)[1]; // return our command
        } // while loop
        File.close(); // close our file
        return "null"; // no output
    } // commands file

    public static void AddCommand(String Command) throws IOException { // this method will add a command to our commands file
        CommandToParse = Command.split(" ", 2)[1]; // this will remove the command portion of the line
        CommandFromParse = CommandToParse.split(":")[0].toUpperCase(); // set our command string
        if (!CommandFromParse.startsWith("?")) // first character isn't a ?
            CommandFromParse = "?" + CommandFromParse; // add a ? if one isn't found
        TextFromParse = CommandToParse.split(":", 2)[1]; // set our command response
        CommandToAdd = CommandFromParse + ":" + TextFromParse; // set our final string to append to file
        try(PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter("commands.txt", true)))) { // open our commands file for writing
            out.println(CommandToAdd); // print our string to the file writer
        } // try
    } // add command

    public static void RemoveCommand(String Command) throws IOException { // this method will remove a command from our commands file
        RemoveCommand = Command.split(" ")[1]; // set our string
        if (!RemoveCommand.startsWith("?")) // no ? found
            RemoveCommand = "?" + RemoveCommand; // add a ?
        BufferedReader File = new BufferedReader(new FileReader("commands.txt")); // open our file for reading
        String CurrentLine; // this holds our current line
        while ((CurrentLine = File.readLine()) != null) { // loops through entire file
            if(!CurrentLine.split(":")[0].equals(RemoveCommand.toUpperCase())) { // our command is found, add it to the new file
                try(PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter("temp.txt", true)))) { // open our commands file for writing
                    out.println(CurrentLine); // print our string to the file writer
                } // try
            } // add line to new file
        } // while loop
        File.close(); // close our file
        File file = new File("commands.txt"); // the old commands file
        file.delete(); // delete it
        File oldFile = new File("temp.txt"); // old name
        File newFile = new File("commands.txt"); // new name
        oldFile.renameTo(newFile); // rename our file
    } // remove command
} // file IO
