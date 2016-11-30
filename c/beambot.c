/*
   Big thanks to http://www.patlathem.com/hello-irc-world/ for basically teaching me what to do. 
   BeamBot this time made in C!
   I think I am on the fourth complete BeamBot rewrite in as many years..
   But this time I know what I am doing (kind of, I did say this last time)
   ~ daniel_j
 */
#include <stdio.h> /* standard io */
#include <stdlib.h> /* standard library */
#include <string.h> /* string */
#include <sys/socket.h> /* sockets */
#include <netdb.h> /* network host */
#define MAXLINE 4096
/* function definitions */
int bot_connect(char *server, unsigned int port, int *sockfd); /* connect */
int bot_send(int sockfd, char *out, int debug); /* send */
int bot_read(int sockfd, char *recvline, int debug); /* read */
void handle_in(int sockfd, char *recvline, int debug); /* handle lines */

int main(int argc, char **argv)
{
	/* 
	   connect the bot to the server and enter a loop
	 */

	/* server definitions */
	char server[] = "172.82.180.204"; /* danieljon.es */
	//char server[] = "188.40.75.16"; /* 3phasegaming.net */
	int port = 6667; /* IRC port */
	/* sockets, buffers and debug definitions */
	int sockfd, in, debug; /* socket, data size and debug */
	char recvline[MAXLINE + 1], out[MAXLINE + 1]; /* receive and out buffers */
	char *pos;
	int joinedchannel = 0; /* ugly hack, fix one day */
	/*
	   set to 1 to toggle debugging
	   when set to 1 extra output information will be printed
	 */
	debug = 0;
	/* attempt connection */
	printf("attempting server connection\n"); 
	if (!bot_connect(server, port, &sockfd))
	{
		printf("Failed to connect to %s, check the IRC server exists.\n", server);
		exit(1);
	}
	/* connection at this point should be made, follow IRC standards */
	printf("connection was successful to %s %i\n", server, port);
	bot_send(sockfd, "USER BeamBot 8 * : Daniel Jones\r\n", debug);
	bot_send(sockfd, "NICK BeamBot\r\n", debug);
	/*
	   now that we are in our channel, enter a loop for commands/pings
	 */
	while(1)
	{
		recvline[0] = 0;
		in = bot_read(sockfd, recvline, debug);
		if (in > 0) {
			recvline[in] = 0;
			/* handle server pings, still runs if someone types PING, fix one day */
			if (strstr(recvline, "PING") != NULL) {
				out[0] = 0;
				pos = strstr(recvline, " ")+1;
				sprintf(out, "PONG %s\r\n", pos);
				bot_send(sockfd, out, debug);
				if (!joinedchannel)
				{
					joinedchannel = 1;
					bot_send(sockfd, "JOIN #tests\r\n", debug);
				}
			}
			/* message isn't a ping, send off to be handled */
			handle_in(sockfd, recvline, debug);
		}
	}
	exit(0);

}

int bot_connect(char *server, unsigned int port, int *sockfd)
{
	/*
	   this function will handle connecting the bot to our IRC server.
	 */
	struct sockaddr_in servaddr;
	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_port = htons(port);
	if ((*sockfd = socket(AF_INET, SOCK_STREAM, 0)) <= 0)
	{
		return 0;
	}
	if (inet_pton(AF_INET, server, &servaddr.sin_addr) <= 0)
	{
		return 0;
	}
	if (connect(*sockfd, (struct sockaddr*) &servaddr, sizeof(servaddr)) < 0)
	{
		return 0;
	}
	/* assume we are connected if we reach here */
	return 1;
}

int bot_send(int sockfd, char *out, int debug)
{
	/*
	   this function handles sending out through our socket 
	 */
	if (debug)
		printf("SENDING: %s", out);
	return send(sockfd, out, strlen(out), 0);
}

int bot_read(int sockfd, char *recvline, int debug)
{
	/*
	   this function handles receiving from our socket
	 */
	int in;
	in = read(sockfd, recvline, MAXLINE);
	if (in > 0 && debug)
		printf("RECEIVED: %s", recvline);
	return in;
}

void handle_in(int sockfd, char *recvline, int debug)
{
	/*
	   this function will handle incoming messages that aren't pings/pongs
	   here we will format our strings for logging, send them to be logged and get commands parsed and responded to
	 */
	if (strstr(recvline, "PRIVMSG") != NULL)
	{
		/* we received a message, lets handle it */
		if (debug)
			printf("%s\n", recvline);
		//bot_send(sockfd, "PRIVMSG #tests :message\r\n", debug);
	}
}
