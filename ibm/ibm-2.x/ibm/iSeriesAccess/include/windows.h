/***********************************************************************/
/*                       LICENSE AND DISCLAIMER                        */
/*                                                                     */
/* This material contains IBM copyrighted sample programming source    */
/* code.  IBM grants you a nonexclusive license to use, execute,       */
/* display, reproduce, distribute and prepare derivative works of this */
/* sample code.  The sample code has not been thoroughly tested under  */
/* all conditions.  IBM, therefore, does not warrant or guarantee its  */
/* reliability, serviceablity, or function. All sample code contained  */
/* herein is provided to you "AS IS." ALL IMPLIED WARRANTIES,          */
/* INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF              */
/* MERCHANTABILLITY AND FITNESS FOR A PARTICULAR PURPOSE, ARE          */
/* EXPRESSLY DISCLAIMED.                                               */
/*                                                                     */
/*                              COPYRIGHT                              */
/*                              ---------                              */
/*               (C) Copyright IBM CORP. 1996,2006                     */
/*               All rights reserved.                                  */
/*               US Government Users Restricted Rights -               */
/*               Use, duplication or disclosure restricted             */
/*               by GSA ADP Schedule Contract with IBM Corp.           */
/*               Licensed Material - Property of IBM                   */
/***********************************************************************/

/***********************************************************************/
/*                                                                     */
/* Module:                                                             */
/*   windows.h                                                         */
/*                                                                     */
/* Purpose:                                                            */
/*   Some definitions needed to compile the sample programs            */
/*                                                                     */
/***********************************************************************/

/* Prevent multiple includes.*/
#if !defined( _WINDOWS_H_ )
  #define     _WINDOWS_H_

/* Standard includes */
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#define __STDC_LIMIT_MACROS
#include <stdint.h>
#include <errno.h>
#include <sys/types.h>
/* String stuff */
#include <string.h>
#include <ctype.h>
/* Byte Swap */
#include <byteswap.h>

/* Help out the c++ folks */
#if defined ( __cplusplus )
extern "C" {
#endif

/* Min Max */
#define  _I8_MIN    INT8_MIN
#define  _I8_MAX    INT8_MAX
#define _UI8_MIN    0
#define _UI8_MAX   UINT8_MAX

#define  _I16_MIN  INT16_MIN
#define  _I16_MAX  INT16_MAX
#define _UI16_MIN  0
#define _UI16_MAX UINT16_MAX

#define  _I32_MIN  INT32_MIN
#define  _I32_MAX  INT32_MAX
#define _UI32_MIN  0
#define _UI32_MAX UINT32_MAX

#define  _I64_MIN  INT64_MIN
#define  _I64_MAX  INT64_MAX
#define _UI64_MIN  0
#define _UI64_MAX UINT64_MAX

/* Types */
typedef unsigned char    BYTE;
typedef BYTE *           LPBYTE;

typedef long             LONG;
typedef LONG *           PLONG;
typedef LONG *           LPLONG;
typedef unsigned long    ULONG;
typedef ULONG *          PULONG;

typedef int              INT;
typedef INT *            LPINT;
typedef unsigned int     UINT;
typedef UINT *           PUINT;
typedef UINT             UINT32;

typedef short            SHORT;
typedef SHORT *          PSHORT;
typedef unsigned short   USHORT;
typedef USHORT *         PUSHORT;

typedef char             CHAR;
typedef CHAR *           PCHAR;
typedef unsigned char    UCHAR;
typedef UCHAR *          PUCHAR;
typedef char *           LPSTR;
typedef const char *     LPCSTR;
typedef wchar_t *        LPWSTR;
typedef const wchar_t *  LPCWSTR;
typedef wchar_t          WCHAR;

typedef void *           HWND;

typedef int              BOOL;
typedef BOOL *           LPBOOL;
typedef BYTE             BOOLEAN;
typedef unsigned char    boolean;
#ifndef FALSE
#define FALSE            (0)
#endif
#ifndef TRUE
#define TRUE             (1)
#endif

typedef unsigned short   WORD;
typedef   signed short  SWORD;

#if __WORDSIZE == 64
  #define __int64 long int
  typedef unsigned int     DWORD;
  typedef   signed int    SDWORD;
#else
  #define __int64 long long int
  typedef unsigned long    DWORD;
  typedef   signed long   SDWORD;
#endif /* 64-bit */
typedef WORD *           LPWORD;
typedef SWORD *          LPSWORD;
typedef DWORD *          LPDWORD;
typedef SDWORD *         LPSDWORD;
typedef void *           LPVOID;
typedef const void *     LPCVOID;

#define stricmp          strcasecmp
#define strnicmp         strncasecmp

#if defined ( __cplusplus )
}
#endif

#endif /* _WINDOWS_H_ */
