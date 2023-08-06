/////////////////////////////////////////////////////////////////////////////
// This C file has been created automatically. Do not edit!!!
/////////////////////////////////////////////////////////////////////////////

/** @file mm31_op_misc.c

 File ``mm31_op_misc.c`` implements the operations on
 vectors in the representation \f$\rho_{31}\f$ of the
 monster.

 The representation \f$\rho_{31}\f$ is equal to the
 196884-dimensional representation  \f$\rho\f$ of the monster,
 with coefficients taken modulo 31, as defined in
 section **The representation of the monster group**
 in the **API reference**.

 An element of \f$\rho_{31}\f$ is implemented as an array
 of integers of type ``uint_mmv_t`` as described in
 section **Description of the mmgroup.mm extension**
 in this document.
*/

#include "mm_op31.h"

// %%EXPORT_KWD MM_OP%{P}_API


//  %%GEN h
//  %%GEN c

/** 
  @brief Copy vector ``mv1`` in \f$\rho_{31}\f$ to ``mv2``
*/
// %%EXPORT px
MM_OP31_API
uint32_t mm_op31_copy(uint_mmv_t *mv1, uint_mmv_t *mv2)
// Copy mv1 to mv2. Here mv1 and mv2 are vectors of the
// monster group representation modulo 31.
{
    uint_fast32_t len = 30936; 
    do {
       *mv2++ = *mv1++;
    } while(--len);
    return 0; 
}


/** 
  @brief Compare arrays ``mv1`` and ``mv2`` of integers

  The function compares parts of the two vectors ``mv1``
  and ``mv2``of the representation \f$\rho_{31}\f$.

  Here the function compares ``len`` integers of type
  ``uint_mmv_t`` starting at the pointers ``mv1`` and ``mv2``.
  These integers are interpreted as arrays of bit fields
  containing integers modulo 31.

  The function returns 0 in case of equality and 1 otherwise.
*/
// %%EXPORT px
MM_OP31_API
uint32_t mm_op31_compare_len(uint_mmv_t *mv1, uint_mmv_t *mv2, uint32_t len)
{
    uint_mmv_t a, b, t, c;
    while (len--) {
        a = *mv1++;
        b = *mv2++;
        // Next we compare integers a and b modulo p. 
        // Idea for p = 0x1fULL and unsigned 5-bit integers a, b:
        // t is in [0, p] iff (t ^ (t >> 1)) & 0xfULL == 0 
        // We have a = +- b (mod p)  iff  a ^ b in [0, p].
        t = a ^ b;
        c = (t ^ (t >> 1)) & 0xf0f0f0f0f0f0f0fULL; // c = 0 iff a = +- b (mod p)
        // In case c != 0 we already know that a != b holds.
        // So assume c == 0 and hence a = +-b, i.e.  t in [0, p].
        // Then a == b (mod p) iff t == 0 or (t & a) in [0, p].
        // Thus is suffices to check if (t & a) is in [0, p]. 
        t &= a;
        t = (t ^ (t >> 1)) & 0xf0f0f0f0f0f0f0fULL; // t = 0 iff old t in [0,p]
        if (c | t) return 1;
    }
    return 0; 
}

/** 
  @brief Compare vectors ``mv1`` and ``mv2`` of \f$\rho_{31}\f$

  The function compares two vectors ``mv1`` and ``mv2`` of 
  the representation \f$\rho_{31}\f$.

  It returns 0 in case of equality and 1 otherwise.
*/
// %%EXPORT px
MM_OP31_API
uint32_t mm_op31_compare(uint_mmv_t *mv1, uint_mmv_t *mv2)
//  Compare two vectors of the monster group representation modulo 31..
//  Comparison is done modulo 31.
//  The function returns 0 in case of equality and 1 otherwise.
{
    return mm_op31_compare_len(mv1, mv2, 30936); 
}
   
    

/** 
  @brief Add vectors ``mv1`` and ``mv2`` of \f$\rho_{31}\f$

  The function adds the two vectors ``mv1`` and ``mv2`` of 
  the representation \f$\rho_{31}\f$ and stores the
  result in the vector ``mv1``.
*/
// %%EXPORT px
MM_OP31_API
void mm_op31_vector_add(uint_mmv_t *mv1, uint_mmv_t *mv2)
//  Vector addition in the monster group representation modulo 31.
//  Put mv1 = mv1 + mv2.
{
    uint_fast32_t len = 30936;
    uint_mmv_t a1, b1;
    do {
        a1 = *mv1;
        b1 = *mv2++;
        a1 = (a1 & 0x1f1f1f1f1f1f1f1fULL) 
              + (b1 & 0x1f1f1f1f1f1f1f1fULL);                     
        a1 = (a1 & 0x1f1f1f1f1f1f1f1fULL) 
              + ((a1 >> 5) & 0x101010101010101ULL);
        *mv1++ = a1;
    } while (--len);
}


/** 
  @brief Multiply vector ``mv1`` of \f$\rho_{31}\f$ with scalar

  The function multiplies the vector ``mv1`` of the 
  representation \f$\rho_{31}\f$ and with the (signed)
  integer ``factor`` and stores the result in the vector ``mv1``.
*/
// %%EXPORT px
MM_OP31_API
void mm_op31_scalar_mul(int32_t factor, uint_mmv_t *mv1)
//  Scalar multiplication in the monster group representation modulo 31.
//  Put mv1 = factor * mv1.
{
    uint_fast32_t len = 30936;
    uint_mmv_t a1, a2;
    factor %= 31;
    if (factor < 0) factor += 31;
    do {
        a1 = *mv1;
        a2 = ((a1 >> 8) & 0x1f001f001f001fULL);
        a1 = (a1 & 0x1f001f001f001fULL);
        a1 *= factor;
        a1 = (a1 & 0x1f001f001f001fULL) 
              + ((a1 >> 5) & 0x1f001f001f001fULL);
        a1 = (a1 & 0x1f001f001f001fULL) 
              + ((a1 >> 5) & 0x1000100010001ULL);
        a2 *= factor;
        a2 = (a2 & 0x1f001f001f001fULL) 
              + ((a2 >> 5) & 0x1f001f001f001fULL);
        a2 = (a2 & 0x1f001f001f001fULL) 
              + ((a2 >> 5) & 0x1000100010001ULL);
        a1 = a1 + (a2 << 8);
        *mv1++ = a1;
    } while (--len);
}



/** 
  @brief Compare two vectors of \f$\rho_{31}\f$ modulo \f$q\f$

  The function compares two vectors ``mv1`` and ``mv2`` of 
  the representation \f$\rho_{31}\f$ modulo a number \f$q\f$.
  Here \f$q\f$ should divide \f$p\f$.

  It returns 0 in case of equality, 1 in case of inequality,
  and 2 if  \f$q\f$ does not divide \f$p\f$.
*/
// %%EXPORT px
MM_OP31_API
uint32_t mm_op31_compare_mod_q(uint_mmv_t *mv1, uint_mmv_t *mv2, uint32_t q)
//  Compare two vectors of the monster group representation modulo 31.
//  Comparison is done modulo q. q must divide 31. The function returns:
//  0  if mmv1 == mmv2 (mod q) 
//  1  if mmv1 != mmv2 (mod q) 
//  2  if q does not divide 31
{
    if (q == 31) return mm_op31_compare(mv1, mv2);
    return q == 1 ? 0 : 2;
}



//  %%GEN h
//  %%GEN c
