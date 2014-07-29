/* pam_sso-tcos copyright 2008 levigo holding gmbh <info@levigo.de>
 *
 * Based on pam_storepw copyright 2002 Florian Lohoff <flo@rfc822.org> 
 * (which is in turn) Based on pam_pwdfile.c by Charl P. Botha */

#include <syslog.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/file.h>

#define ENVVAR "TCOS_TOKEN"

/*  */
static int hexencode(char *buf, char val)
{
	char *cur = buf, c;

	c = (val >> 4) & 0xf;
	if (c < 10) {
		c += '0';
	} else {
		c += 'a' - 10;
	}
	*cur++ = c;
	c = val & 0xf;
	if (c < 10) {
		c += '0';
	} else {
		c += 'a' - 10;
	}
	*cur++ = c;

	return(cur - buf);
}

/* */
static int encrypt(char **buf, char *pword)
{
	u_int len = strlen(pword) + 1;
	int i;
	char *cur,
	       c,
	       key = random() & 0xff;

	if(cur = malloc(strlen(ENVVAR) + 1 + len + 4)){
		*buf = cur;
		cur += sprintf(cur, "%s=", ENVVAR);
		cur += hexencode(cur, (u_char) ((len >> 8) & 0xff));
		cur += hexencode(cur, (u_char) (len & 0xff));
		cur += hexencode(cur, key);
		i = htons(len);

		c = pword[0] ^ (key | 'C');
		cur += hexencode(cur, c);

		for(i = 1; i < (len - 1); i++) {
			c = c ^ key ^ pword[i];
			cur += hexencode(cur, c);
		}
		*cur = '\0';
		return(1);
	} else {
		return(0);
	}
}

int main(int argc, const char **argv)
{
	char    *pword, *envvar;
	pword = argv[1];
	if(encrypt(&envvar, pword)){
		printf("%s\n", envvar);
	}
	return(0);
}
