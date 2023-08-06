/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm3_op_misc.c

 File ``mm3_op_misc.c`` implements the operations on
 vectors in the representation \f$\rho_{3}\f$ of the
 monster.

 The representation \f$\rho_{3}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 3, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{3}\f$ is implemented as an array
 of integers of type ``uint_mmv_t`` as described in
 section **Description of the mmgroup.mm extension**
 in this document.
*/

#include "mm_op3.h"

// %%EXPORT_KWD MM_OP%{P}_API


//  %%GEN h
//  %%GEN c

/** 
  @brief Copy vector ``mv1`` in \f$\rho_{3}\f$ to ``mv2``
*/
// %%EXPORT px
MM_OP3_API
uint32_t mm_op3_copy(uint_mmv_t *mv1, uint_mmv_t *mv2)
// Copy mv1 to mv2. Here mv1 and mv2 are vectors of the
// monster group representation modulo 3.
{
    uint_fast32_t len = 7734; 
    do {
       *mv2++ = *mv1++;
    } while(--len);
    return 0; 
}


/** 
  @brief Compare arrays ``mv1`` and ``mv2`` of integers

  The function compares parts of the two vectors ``mv1``
  and ``mv2``of the representation \f$\rho_{3}\f$.

  Here the function compares ``len`` integers of type
  ``uint_mmv_t`` starting at the pointers ``mv1`` and ``mv2``.
  These integers are interpreted as arrays of bit fields
  containing integers modulo 3.

  The function returns 0 in case of equality and 1 otherwise.
*/
// %%EXPORT px
MM_OP3_API
uint32_t mm_op3_compare_len(uint_mmv_t *mv1, uint_mmv_t *mv2, uint32_t len)
{
    uint_mmv_t a, b, t, c;
    while (len--) {
        a = *mv1++;
        b = *mv2++;
        // Next we compare integers a and b modulo p. 
        // Idea for p = 0x3ULL and unsigned 2-bit integers a, b:
        // t is in [0, p] iff (t ^ (t >> 1)) & 0x1ULL == 0 
        // We have a = +- b (mod p)  iff  a ^ b in [0, p].
        t = a ^ b;
        c = (t ^ (t >> 1)) & 0x5555555555555555ULL; // c = 0 iff a = +- b (mod p)
        // In case c != 0 we already know that a != b holds.
        // So assume c == 0 and hence a = +-b, i.e.  t in [0, p].
        // Then a == b (mod p) iff t == 0 or (t & a) in [0, p].
        // Thus is suffices to check if (t & a) is in [0, p]. 
        t &= a;
        t = (t ^ (t >> 1)) & 0x5555555555555555ULL; // t = 0 iff old t in [0,p]
        if (c | t) return 1;
    }
    return 0; 
}

/** 
  @brief Compare vectors ``mv1`` and ``mv2`` of \f$\rho_{3}\f$

  The function compares two vectors ``mv1`` and ``mv2`` of 
  the representation \f$\rho_{3}\f$.

  It returns 0 in case of equality and 1 otherwise.
*/
// %%EXPORT px
MM_OP3_API
uint32_t mm_op3_compare(uint_mmv_t *mv1, uint_mmv_t *mv2)
//  Compare two vectors of the monster group representation modulo 3..
//  Comparison is done modulo 3.
//  The function returns 0 in case of equality and 1 otherwise.
{
    return mm_op3_compare_len(mv1, mv2, 7734); 
}
   
    

/** 
  @brief Add vectors ``mv1`` and ``mv2`` of \f$\rho_{3}\f$

  The function adds the two vectors ``mv1`` and ``mv2`` of 
  the representation \f$\rho_{3}\f$ and stores the
  result in the vector ``mv1``.
*/
// %%EXPORT px
MM_OP3_API
void mm_op3_vector_add(uint_mmv_t *mv1, uint_mmv_t *mv2)
//  Vector addition in the monster group representation modulo 3.
//  Put mv1 = mv1 + mv2.
{
    uint_fast32_t len = 7734;
    uint_mmv_t a1, b1;
    uint_mmv_t a2;
    do {
        a1 = *mv1;
        b1 = *mv2++;
        a2 = ((a1 >> 2) & 0x3333333333333333ULL)
           + ((b1 >> 2) & 0x3333333333333333ULL);
        a1 = (a1 & 0x3333333333333333ULL)
           + (b1 & 0x3333333333333333ULL);
        a1 = (a1 & 0x3333333333333333ULL) 
              + ((a1 >> 2) & 0x1111111111111111ULL);
        a2 = (a2 & 0x3333333333333333ULL) 
              + ((a2 >> 2) & 0x1111111111111111ULL);
        a1 = a1 + (a2 << 2);
        *mv1++ = a1;
    } while (--len);
}


/** 
  @brief Multiply vector ``mv1`` of \f$\rho_{3}\f$ with scalar

  The function multiplies the vector ``mv1`` of the 
  representation \f$\rho_{3}\f$ and with the (signed)
  integer ``factor`` and stores the result in the vector ``mv1``.
*/
// %%EXPORT px
MM_OP3_API
void mm_op3_scalar_mul(int32_t factor, uint_mmv_t *mv1)
//  Scalar multiplication in the monster group representation modulo 3.
//  Put mv1 = factor * mv1.
{
    uint_fast32_t len = 7734;
    uint_mmv_t a1, a2;
    factor %= 3;
    if (factor < 0) factor += 3;
    do {
        a1 = *mv1;
        a2 = ((a1 >> 2) & 0x3333333333333333ULL);
        a1 = (a1 & 0x3333333333333333ULL);
        a1 *= factor;
        a1 = (a1 & 0x3333333333333333ULL) 
              + ((a1 >> 2) & 0x3333333333333333ULL);
        a1 = (a1 & 0x3333333333333333ULL) 
              + ((a1 >> 2) & 0x1111111111111111ULL);
        a2 *= factor;
        a2 = (a2 & 0x3333333333333333ULL) 
              + ((a2 >> 2) & 0x3333333333333333ULL);
        a2 = (a2 & 0x3333333333333333ULL) 
              + ((a2 >> 2) & 0x1111111111111111ULL);
        a1 = a1 + (a2 << 2);
        *mv1++ = a1;
    } while (--len);
}



/** 
  @brief Compare two vectors of \f$\rho_{3}\f$ modulo \f$q\f$

  The function compares two vectors ``mv1`` and ``mv2`` of 
  the representation \f$\rho_{3}\f$ modulo a number \f$q\f$.
  Here \f$q\f$ should divide \f$p\f$.

  It returns 0 in case of equality, 1 in case of inequality,
  and 2 if  \f$q\f$ does not divide \f$p\f$.
*/
// %%EXPORT px
MM_OP3_API
uint32_t mm_op3_compare_mod_q(uint_mmv_t *mv1, uint_mmv_t *mv2, uint32_t q)
//  Compare two vectors of the monster group representation modulo 3.
//  Comparison is done modulo q. q must divide 3. The function returns:
//  0  if mmv1 == mmv2 (mod q) 
//  1  if mmv1 != mmv2 (mod q) 
//  2  if q does not divide 3
{
    if (q == 3) return mm_op3_compare(mv1, mv2);
    return q == 1 ? 0 : 2;
}



//  %%GEN h
//  %%GEN c
