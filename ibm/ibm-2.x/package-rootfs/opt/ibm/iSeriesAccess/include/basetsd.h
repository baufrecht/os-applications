/*                                                                   */
/* 5722-XE1                                                          */
/* (C) Copyright IBM Corp. 1995,2006                                 */
/* All rights reserved.                                              */
/* US Government Users Restricted Rights -                           */
/* Use, duplication or disclosure restricted                         */
/* by GSA ADP Schedule Contract with IBM Corp.                       */
/*                                                                   */
/* Licensed Materials-Property of IBM                                */
/*                                                                   */

/*********************************************************************/
/*                                                                   */
/* Module:                                                           */
/*   basetsd.h                                                       */
/*                                                                   */
/* Purpose:                                                          */
/*   Common declarations for Client Access/400 APIs                  */
/*                                                                   */
/* Usage Notes:                                                      */
/*                                                                   */
/*********************************************************************/

/*********************************************************************/
/* Prevent multiple includes                                         */
/*********************************************************************/
#if !defined( _BASETSD_H_ )
  #define     _BASETSD_H_

// 64-bit Windows or Linux
#if defined(_WIN64) || __WORDSIZE == 64
    typedef          long int  INT_PTR,   *PINT_PTR;
    typedef unsigned long int UINT_PTR,  *PUINT_PTR;

    typedef          long     LONG_PTR,  *PLONG_PTR;
    typedef unsigned long    ULONG_PTR, *PULONG_PTR;
#else
    typedef           int      INT_PTR,   *PINT_PTR;
    typedef unsigned  int     UINT_PTR,  *PUINT_PTR;

    typedef          long     LONG_PTR,  *PLONG_PTR;
    typedef unsigned long    ULONG_PTR, *PULONG_PTR;
#endif

#endif /* _BASETSD_H_  */
