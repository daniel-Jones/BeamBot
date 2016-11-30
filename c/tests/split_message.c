#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *get_username(char *message);

int main (int argc, char *argv[])
{
	/* we need to:
	* - get username
	* - get message
	*/
	char *message = ":daniel_j!admin@danieljon.es PRIVMSG #fun :message here";
	printf("%s\n", get_username(message));
	return 0;
}



char *get_username(char *message)
{
	/* to get username - remove message[0] copy until : char */
        char *user = message + 1;
	char *ret = "";
	char temp[128];
	int token_end = 0;
	for (int x = 0; x < strlen(user); x++)
	{
		if (user[x] == '!')
			token_end = 1;
		if (token_end != 1)
		{
			temp[x] = user[x];
		}
	}
	temp[sizeof(temp)] = '\0';
	printf("%s\n", temp);
	ret = temp;
	return ret;
}
