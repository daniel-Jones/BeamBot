package es.danieljon;

// this class will deal with parsing things

public class LineParsing { // line parsing

    public static String User; // this will hold the last user to send a message

    public static String CleanLine(String RawLine) { // clean line method
        String[] MessageArray = RawLine.split(":", 3); // split our string
        User = RawLine.split("!")[0].replace(":", "");
        return MessageArray[2].toString(); // return our message
    } // clean line method

} // line parsing
