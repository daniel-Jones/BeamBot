package es.danieljon;

// this class with interpret our commands
import java.io.IOException;
import java.util.Arrays;

public class CommandInterpretation { // interpret commands

    public static String Command = null; // this will hold the command
    public static String Parameters = null; // this will hold our parameters if any
    private static String TempLine = null; // this will hold our temporary string
    public static String[] SpecialUsers = {"daniel_j", "badSol", "akino_germany", "DarthCain"}; // this list contains the users that can perform special commands

    public static String InterpretCommand(String Line) throws IOException { // this method will interpret our command
        Command = Line.split(" ")[0];
        if(Line.startsWith("?")) { // no parameter command
            TempLine = FileIO.GetCommandsFile(Command); // set our return string
            if(TempLine != "null")
                Logging.LogLine("(Bot response from " + Main.NickName + ") " + TempLine);
            return TempLine; // find our command and output the results
        } // no parameter command

        if(Line.startsWith("!")) { // parameter command
            try { // try to complete the command
                Parameters = Line.split(" ", 2)[1]; // set our parameters
                if (Command.equals("!user")) { // user page command
                    return "http://www.beamng.com/member.php?username=" + Parameters.replace(" ", "%20"); // make sure to replace spaces
                } // user page command
                if (Command.equals("!addcommand") && Arrays.asList(SpecialUsers).contains(LineParsing.User)) { // add command
                    FileIO.AddCommand(Line); // send our line to the command handler
                } // add command
                if (Command.equals("!removecommand") && Arrays.asList(SpecialUsers).contains(LineParsing.User)) { // remove command
                    FileIO.RemoveCommand(Line); // send our line to the remove command handler
                } // remove command
            } catch(ArrayIndexOutOfBoundsException e) { // try the command
                return "null";
            }
        } // parameter command
        return "null";
    } // interpret command
} // interpret commands
