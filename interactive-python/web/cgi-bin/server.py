#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb, socket

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
message = form.getvalue('message')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>Message: %s</h2>" % (message)
print "</body>"
print "</html>"


BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 6666))
s.send(message)
s.close()
