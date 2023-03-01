FIRST = \
"""
typedef signed char int8_t;
typedef int int32_t;
typedef unsigned short int uint16_t;
typedef unsigned int uint32_t;
static inline unsigned long int
div_rhs (long int rhs)
{
  if (rhs)
    return 1;
  return rhs;
}

uint32_t g_65;
int32_t g_122;
int32_t func_64 (uint32_t p_66, uint16_t p_67);
int32_t func_86 (uint16_t p_87);
int32_t func_88 (uint16_t p_89);
int32_t
func_2 (int8_t p_4)
{
  int32_t l_450;
  for (l_450 = 0; (l_450 < 8); ++l_450)
    func_43 (func_60 (func_64 (func_86 (1), 1), 1), 1, 1);
}

int32_t
func_64 (uint32_t p_66, uint16_t p_67)
{
  for (g_65 = 0; 0; ++g_65)
    {
    }
}
int32_t
func_86 (uint16_t p_87)
{
  func_88 (g_122);
}

int32_t
func_88 (uint16_t p_89)
{
  if (0 / div_rhs (func_91 (1, 1)))
    {
    }
  else if (p_89)
    for (g_65 = 1; 1; g_65 -= 1)
      return 1;
}
"""

SECOND = \
"""
struct S2
{
  int f6;
};

int g_65;

struct S2 g_180;

void func_121 (struct S2 p_122);

int func_56 (int p_58, int p_59)
{
  int i;
  for (i = 0; i < 1; i = 1)
    for (p_59 = 0; p_59 < 1; p_59 = 1);
  return p_59;
}

void foo (void)
{
  func_106 (0);
}

int func_106 (const int p_107, int p_108)
{
  if (func_56 (func_56 (0, p_107), 0))
    return 0;
  else
    func_121 (g_180);
  return 0;
}

void func_121 (struct S2 p_122)
{
  for (0; 1; 0)
    for (; p_122.f6;)
      g_65 = 0 ? : func_56 (0,0);
}
"""

THIRD = \
"""
unsigned char g_17;

const unsigned char func_39 (unsigned char p_40, unsigned char * p_41)
{
  return 0;
}

void int327 (const unsigned char p_48, unsigned char p_49)
{
  unsigned l_52;
  unsigned char l_58[2];
  int i, j;
  if (func_39 (l_52, &p_49), p_48) {
    unsigned char *l_60;
    unsigned char *l = &l_58[1];
    for (j; j; j++) {
    lbl_59:
      break;
    }
    for (l = 0; 1; l += 1) {
      for (p_49 = 1; p_49; p_49 += 0) {
	unsigned char **l_61[1][6];
	for (j = 0; j < 1; j++)
	  l_61[i][j] = &l_60;
	goto lbl_59;
      }
    }
  }
}
"""


C_TEMPLATE = \
"""
// create a fuzzing testcase for a C compiler

typedef signed char int8_t;
typedef int int32_t;
typedef unsigned short int uint16_t;
typedef unsigned int uint32_t;
static inline unsigned long int
div_rhs (long int rhs)
{
  if (rhs)
    return 1;
  return rhs;
}

uint32_t g_65;
int32_t g_122;
int32_t func_64 (uint32_t p_66, uint16_t p_67);
int32_t func_86 (uint16_t p_87);
int32_t func_88 (uint16_t p_89);
int32_t
func_2 (int8_t p_4)
{
  int32_t l_450;
  for (l_450 = 0; (l_450 < 8); ++l_450)
    func_43 (func_60 (func_64 (func_86 (1), 1), 1), 1, 1);
}

int32_t
func_64 (uint32_t p_66, uint16_t p_67)
{
  for (g_65 = 0; 0; ++g_65)
    {
    }
}
int32_t
func_86 (uint16_t p_87)
{
  func_88 (g_122);
}

int32_t
func_88 (uint16_t p_89)
{
  if (0 / div_rhs (func_91 (1, 1)))
    {
    }
  else if (p_89)
    for (g_65 = 1; 1; g_65 -= 1)
      return 1;
}

// create a fuzzing testcase for a C compiler
struct S2
{
  int f6;
};

int g_65;

struct S2 g_180;

void func_121 (struct S2 p_122);

int func_56 (int p_58, int p_59)
{
  int i;
  for (i = 0; i < 1; i = 1)
    for (p_59 = 0; p_59 < 1; p_59 = 1);
  return p_59;
}

void foo (void)
{
  func_106 (0);
}

int func_106 (const int p_107, int p_108)
{
  if (func_56 (func_56 (0, p_107), 0))
    return 0;
  else
    func_121 (g_180);
  return 0;
}

void func_121 (struct S2 p_122)
{
  for (0; 1; 0)
    for (; p_122.f6;)
      g_65 = 0 ? : func_56 (0,0);
}

// create a fuzzing testcase for a C compiler
unsigned char g_17;

const unsigned char func_39 (unsigned char p_40, unsigned char * p_41)
{
  return 0;
}

void int327 (const unsigned char p_48, unsigned char p_49)
{
  unsigned l_52;
  unsigned char l_58[2];
  int i, j;
  if (func_39 (l_52, &p_49), p_48) {
    unsigned char *l_60;
    unsigned char *l = &l_58[1];
    for (j; j; j++) {
    lbl_59:
      break;
    }
    for (l = 0; 1; l += 1) {
      for (p_49 = 1; p_49; p_49 += 0) {
	unsigned char **l_61[1][6];
	for (j = 0; j < 1; j++)
	  l_61[i][j] = &l_60;
	goto lbl_59;
      }
    }
  }
}

// create a fuzzing testcase for a C compiler
"""