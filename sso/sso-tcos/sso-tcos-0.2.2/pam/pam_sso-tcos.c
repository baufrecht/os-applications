/*
 * pam_sso-tcos copyright 2008 levigo holding gmbh <info@levigo.de>
 *
 * Based on pam_storepw copyright 2002 Florian Lohoff <flo@rfc822.org> 
 * (which is in turn) Based on pam_pwdfile.c by Charl P. Botha
 *
 */

#ifndef LINUX 
#include <security/pam_appl.h>
#endif  /* LINUX */

#define PAM_SM_AUTH
#include <security/pam_modules.h>
/* #include <security/_pam_types.h> */

#include <syslog.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>

#define _XOPEN_SOURCE
#include <unistd.h>

#define ENVVAR "TCOS_TOKEN"

/* logging function ripped from pam_listfile.c */
static void _pam_log(int err, const char *format, ...)
{
	va_list args;

	va_start(args, format);
	openlog("pam_sso-tcos", LOG_CONS|LOG_PID, LOG_AUTH);
	vsyslog(err, format, args);
	va_end(args);
	closelog();
}

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

/*  */
static int do_encrypt(char *buf, char *pword)
{
	u_int	len = strlen(pword) + 1;
	int	i;
	char	*cur,
		c,
		key = rand() & 0xff;

	cur = buf;
	cur += sprintf(cur, "%s=", ENVVAR);
	cur += hexencode(cur, (u_char) ((len >> 8) & 0xff));
	cur += hexencode(cur, (u_char) (len & 0xff));
	cur += hexencode(cur, key);
	i = htons(len);

	c = pword[0] ^ (key | 'C');
	cur += hexencode(cur, c);

	for(i=1; i < (len - 1); i++) {
		c = c ^ key ^ pword[i];
		cur += hexencode(cur, c);
	}
	*cur = '\0';
	return(1);
}

/* expected hook for auth service */
PAM_EXTERN int pam_sm_authenticate(pam_handle_t *pamh, int flags,
				   int argc, const char **argv)
{
	char	*pword, *envvar;

	pam_get_item(pamh, PAM_AUTHTOK, (void *) &pword);
	if (!pword) {
      		_pam_log(LOG_ERR,"no password to write - got stacked wrong ?");
		return PAM_AUTHINFO_UNAVAIL;
	}

	if(envvar = malloc(strlen(ENVVAR) + 1 + 3*2 + strlen(pword)*2 + 1)){
		if(do_encrypt(envvar, pword)){
			pam_putenv(pamh, envvar);
		}
	}
	return PAM_SUCCESS;;
}

/* another expected hook */
PAM_EXTERN int pam_sm_setcred(pam_handle_t *pamh, int flags, 
			      int argc, const char **argv)
{
	return PAM_SUCCESS;
}

#ifdef PAM_STATIC
struct pam_module _pam_listfile_modstruct = {
     "pam_sso-tcos",
     pam_sm_authenticate,
     pam_sm_setcred,
     NULL,
     NULL,
     NULL,
     NULL,
};
#endif
