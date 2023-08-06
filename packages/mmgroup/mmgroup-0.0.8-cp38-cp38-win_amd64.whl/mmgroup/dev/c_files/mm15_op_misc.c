/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm15_op_misc.c

 File ``mm15_op_misc.c`` implements the operations on
 vectors in the representation \f$\rho_{15}\f$ of the
 monster.

 The representation \f$\rho_{15}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 15, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{15}\f$ is implemented as an array
 of integers of type ``uint_mmv_t`` as described in
 section **Description of the mmgroup.mm extension**
 in this document.
*/

#include "mm_op15.h"

// %%EXPORT_KWD MM_OP%{P}_API


//  %%GEN h
//  %%GEN c

/** 
  @brief Copy vector ``mv1`` in \f$\rho_{15}\f$ to ``mv2``
*/
// %%EXPORT px
MM_OP15_API
uint32_t mm_op15_copy(uint_mmv_t *mv1, uint_mmv_t *mv2)
// Copy mv1 to mv2. Here mv1 and mv2 are vectors of the
// monster group representation modulo 15.
{
    uint_fast32_t len = 15468; 
    do {
       *mv2++ = *mv1++;
    } while(--len);
    return 0; 
}


/** 
  @brief Compare arrays ``mv1`` and ``mv2`` of integers

  The function compares parts of the two vectors ``mv1``
  and ``mv2``of the representation \f$\rho_{15}\f$.

  Here the function compares ``len`` integers of type
  ``uint_mmv_t`` starting at the pointers ``mv1`` and ``mv2``.
  These integers are interpreted as arrays of bit fields
  containing integers modulo 15.

  The function returns 0 in case of equality and 1 otherwise.
*/
// %%EXPORT px
MM_OP15_API
uint32_t mm_op15_compare_len(uint_mmv_t *mv1, uint_mmv_t *mv2, uint32_t len)
{
    uint_mmv_t a, b, t, c;
    while (len--) {
        a = *mv1++;
        b = *mv2++;
        // Next we compare integers a and b modulo p. 
        // Idea for p = 0xfULL and unsigned 4-bit integers a, b:
        // t is in [0, p] iff (t ^ (t >> 1)) & 0x7ULL == 0 
        // We have a = +- b (mod p)  iff  a ^ b in [0, p].
        t = a ^ b;
        c = (t ^ (t >> 1)) & 0x7777777777777777ULL; // c = 0 iff a = +- b (mod p)
        // In case c != 0 we already know that a != b holds.
        // So assume c == 0 and hence a = +-b, i.e.  t in [0, p].
        // Then a == b (mod p) iff t == 0 or (t & a) in [0, p].
        // Thus is suffices to check if (t & a) is in [0, p]. 
        t &= a;
        t = (t ^ (t >> 1)) & 0x7777777777777777ULL; // t = 0 iff old t in [0,p]
        if (c | t) return 1;
    }
    return 0; 
}

/** 
  @brief Compare vectors ``mv1`` and ``mv2`` of \f$\rho_{15}\f$

  The function compares two vectors ``mv1`` and ``mv2`` of 
  the representation \f$\rho_{15}\f$.

  It returns 0 in case of equality and 1 otherwise.
*/
// %%EXPORT px
MM_OP15_API
uint32_t mm_op15_compare(uint_mmv_t *mv1, uint_mmv_t *mv2)
//  Compare two vectors of the monster group representation modulo 15..
//  Comparison is done modulo 15.
//  The function returns 0 in case of equality and 1 otherwise.
{
    return mm_op15_compare_len(mv1, mv2, 15468); 
}
   
    

/** 
  @brief Add vectors ``mv1`` and ``mv2`` of \f$\rho_{15}\f$

  The function adds the two vectors ``mv1`` and ``mv2`` of 
  the representation \f$\rho_{15}\f$ and stores the
  result in the vector ``mv1``.
*/
// %%EXPORT px
MM_OP15_API
void mm_op15_vector_add(uint_mmv_t *mv1, uint_mmv_t *mv2)
//  Vector addition in the monster group representation modulo 15.
//  Put mv1 = mv1 + mv2.
{
    uint_fast32_t len = 15468;
    uint_mmv_t a1, b1;
    uint_mmv_t a2;
    do {
        a1 = *mv1;
        b1 = *mv2++;
        a2 = ((a1 >> 4) & 0xf0f0f0f0f0f0f0fULL)
           + ((b1 >> 4) & 0xf0f0f0f0f0f0f0fULL);
        a1 = (a1 & 0xf0f0f0f0f0f0f0fULL)
           + (b1 & 0xf0f0f0f0f0f0f0fULL);
        a1 = (a1 & 0xf0f0f0f0f0f0f0fULL) 
              + ((a1 >> 4) & 0x101010101010101ULL);
        a2 = (a2 & 0xf0f0f0f0f0f0f0fULL) 
              + ((a2 >> 4) & 0x101010101010101ULL);
        a1 = a1 + (a2 << 4);
        *mv1++ = a1;
    } while (--len);
}


/** 
  @brief Multiply vector ``mv1`` of \f$\rho_{15}\f$ with scalar

  The function multiplies the vector ``mv1`` of the 
  representation \f$\rho_{15}\f$ and with the (signed)
  integer ``factor`` and stores the result in the vector ``mv1``.
*/
// %%EXPORT px
MM_OP15_API
void mm_op15_scalar_mul(int32_t factor, uint_mmv_t *mv1)
//  Scalar multiplication in the monster group representation modulo 15.
//  Put mv1 = factor * mv1.
{
    uint_fast32_t len = 15468;
    uint_mmv_t a1, a2;
    factor %= 15;
    if (factor < 0) factor += 15;
    do {
        a1 = *mv1;
        a2 = ((a1 >> 4) & 0xf0f0f0f0f0f0f0fULL);
        a1 = (a1 & 0xf0f0f0f0f0f0f0fULL);
        a1 *= factor;
        a1 = (a1 & 0xf0f0f0f0f0f0f0fULL) 
              + ((a1 >> 4) & 0xf0f0f0f0f0f0f0fULL);
        a1 = (a1 & 0xf0f0f0f0f0f0f0fULL) 
              + ((a1 >> 4) & 0x101010101010101ULL);
        a2 *= factor;
        a2 = (a2 & 0xf0f0f0f0f0f0f0fULL) 
              + ((a2 >> 4) & 0xf0f0f0f0f0f0f0fULL);
        a2 = (a2 & 0xf0f0f0f0f0f0f0fULL) 
              + ((a2 >> 4) & 0x101010101010101ULL);
        a1 = a1 + (a2 << 4);
        *mv1++ = a1;
    } while (--len);
}



/** 
  @brief Compare two vectors of \f$\rho_{15}\f$ modulo \f$q\f$

  The function compares two vectors ``mv1`` and ``mv2`` of 
  the representation \f$\rho_{15}\f$ modulo a number \f$q\f$.
  Here \f$q\f$ should divide \f$p\f$.

  It returns 0 in case of equality, 1 in case of inequality,
  and 2 if  \f$q\f$ does not divide \f$p\f$.
*/
// %%EXPORT px
MM_OP15_API
uint32_t mm_op15_compare_mod_q(uint_mmv_t *mv1, uint_mmv_t *mv2, uint32_t q)
//  Compare two vectors of the monster group representation modulo 15.
//  Comparison is done modulo q. q must divide 15. The function returns:
//  0  if mmv1 == mmv2 (mod q) 
//  1  if mmv1 != mmv2 (mod q) 
//  2  if q does not divide 15
{
    uint_fast32_t d1, d2, len = 15468;
    if (q == 15) return mm_op15_compare(mv1, mv2);
    if (q <= 1) return 2 - 2 * q;
    d1 = 15 / q;
    if (d1 * q != 15) return 2;
    d2 = 15 - d1;
    do {
        uint_mmv_t a, b;
        a = (*mv1 & 0xf0f0f0f0f0f0f0fULL) * d1 
          + (*mv2 & 0xf0f0f0f0f0f0f0fULL) * d2;
        a = (a & 0xf0f0f0f0f0f0f0fULL) + ((a >> 4) & 0xf0f0f0f0f0f0f0fULL);
        a = (a & 0xf0f0f0f0f0f0f0fULL) + ((a >> 4) & 0xf0f0f0f0f0f0f0fULL);

        b = ((*mv1++ >> 4) & 0xf0f0f0f0f0f0f0fULL) * d1
          + ((*mv2++ >> 4) & 0xf0f0f0f0f0f0f0fULL) * d2;
        b = (b & 0xf0f0f0f0f0f0f0fULL) + ((b >> 4) & 0xf0f0f0f0f0f0f0fULL);
        b = (b & 0xf0f0f0f0f0f0f0fULL) + ((b >> 4) & 0xf0f0f0f0f0f0f0fULL);

        a += b << 4;
        a ^= a >> 1;
        if (a & 0x7777777777777777ULL) return 1;
    } while (--len);
    return 0;
}



//  %%GEN h
//  %%GEN c
