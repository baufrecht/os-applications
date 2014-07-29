/*
 * Program to get the encoded password from the environment
 * variable TCOS_TOKEN
 * 
 * copyright 2008 by levigo holding gmbh <info@levigo.de>
 *
 * Based on icadecrypt.c by Dug Song <dugsong@monkey.org>
 */

#include <sys/types.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define ENVVAR "TCOS_TOKEN"

int hex_decode(char *src, u_char *dst, int outsize)
{
	char *p, *pe;
	u_char *q, *qe, ch, cl;

	pe = src + strlen(src);
	qe = dst + outsize;

	for (p = src, q = dst; p < pe && q < qe && isxdigit((int)*p); p += 2) {
		ch = tolower(p[0]);
		cl = tolower(p[1]);
		if ((ch >= '0') && (ch <= '9')) ch -= '0';
		else if ((ch >= 'a') && (ch <= 'f')) ch -= 'a' - 10;
		else return (-1);

		if ((cl >= '0') && (cl <= '9')) cl -= '0';
		else if ((cl >= 'a') && (cl <= 'f')) cl -= 'a' - 10;
		else return (-1);

		*q++ = (ch << 4) | cl;
	}
	return (q - dst);
}

int ica_decrypt(u_char *pass, int len)
{
	u_short i;
	u_char *p, key;

	if(len < 4){
		return (0);
	}

	i = ntohs(*(u_short *)pass);

	if(i != len - 2){
		return (0);
	}
	key = pass[2];
	p = pass + 3;

	for(i -= 2; i > 0; i--){
		p[i] = p[i - 1] ^ p[i] ^ key;
	}
	p[0] ^= (key | 'C');

	i = len - 3;
	memmove(pass, pass + 3, i);
	pass[i] = '\0';

	return (1);
}

int main(void)
{
	char *token;
	if(token = getenv((const char *)ENVVAR)){
		u_char *pass;
		if(pass = malloc(strlen(token) + 1)){
			int len;
			len = hex_decode(token, pass, strlen(token) + 1);
			if (ica_decrypt(pass, len)){
				printf("%s", pass);
			} else {
				printf("\"\"");
			}
			free(pass);
			return(0);
			/* all went fine, done */
		}
	}
	/* in all other cases return empty string "" */
	printf("\"\"");
        return(0);
}

