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

CPP_TEMPLATE_consteval = {
    "separator": 'Please create a fuzzing testcase for a C++ compiler to test feature "if consteval"',
    "first":
        """
#include <type_traits>

int slow (int);
consteval int fast (int n) { return n << 1; }

constexpr int fn (int n)
{
  if consteval {
    return fast (n); // OK
  } else {
    return slow (n);
  }
}

constexpr int i = fn (10);
""",
    "second":
        """
consteval int bar(int i) {
    return 2*i;
}

int foo(int i) {
    if consteval {
        return bar(i);
    }
    return 2*i;
}

int main() {
  [[maybe_unused]] auto a = foo(5);
}
""",
    "third":
        """
consteval int f( int i ) { return 1; }

int fallback() { return 0; }

constexpr int g( int i )
{
  if consteval {    //1
    return f( i );
  }
  else { 
    return fallback();
  }
}
"""
}

CPP_TEMPLATE_multi_dimen_access = \
    """
// create a fuzzing testcase for a C++ compiler for feature "multidimensional subscript operator"
template <typename... T>
struct W {
  constexpr auto operator[](T&&...);
};

W<> w1;
W<int> w2;
W<int, int> w3;

// create a fuzzing testcase for a C++ compiler for feature "multidimensional subscript operator"
#include <cstddef>
#include <array>

template <typename T, size_t R, size_t C>
struct matrix
{
   T& operator[](size_t const r, size_t const c) noexcept
{
   return data_[r * C + c];
}
T const & operator[](size_t const r, size_t const c) const noexcept
{
   return data_[r * C + c];
}
   static constexpr size_t Rows = R;
   static constexpr size_t Columns = C;
private:
   std::array<T, R* C> data_;
};

int main()
{
   matrix<int, 3, 2> m;
   for (size_t i = 0; i < m.Rows; ++i)
   {
      for (size_t j = 0; j < m.Columns; ++j)
      {
         m[i, j] = i * m.Columns + (j + 1);
      }
   }
}

// create a fuzzing testcase for a C++ compiler for feature "multidimensional subscript operator"
"""

CPP_TEMPLATE_auto_functional = {
    "separator": '// create a fuzzing testcase for a C++ compiler for feature "auto in functional-style cast"',
    "first" :
        """
struct A {};
void f(A&);  // #1
void f(A&&); // #2
A& g();

void
h()
{
  f(g()); // calls #1
  f(auto(g())); // calls #2 with a temporary object
}
""",
    "second" :
        """
class A {
    int x;

public:
    A();
    int f(A x) {
        return 0;
    }
    auto run() {
        f(A(*this));           // ok
        f(auto(*this));        // ok as proposed
    }

protected:
    A(const A&);
};
""",
    "third": """"""
}


CPP_TEMPLATE_likely_unlikely = {
    "separator": 'Please create a fuzzing testcase for a C++ compiler to test feature "likely, unlikely attributes"',
    "first" :
        """
int f(int i)
{
    switch(i)
    {
        case 1: [[fallthrough]];
        [[likely]] case 2: return 1;
    }
    return 2;
}
""",
    "second" :
        """
int g(int x) {
  return x;
}

int f(int n) {
    if (n > 5) [[unlikely]] {
        g(0);
        return n * 2 + 1;
    }

    return 3;
}
""",
    "third": """"""
}

CPP_TEMPLATE_immediate_function = {
    "separator": 'Please create a fuzzing testcase for a C++ compiler to test feature "immediate function"',
    "first" :
        """
consteval int sqr(int n) {
  return n * n;
}

constexpr int r = sqr(100);
""",
    "second" :
        """
#include <iostream>
using namespace std;
  
// Constexpr function if replaced with
// consteval, program works fine
constexpr int fib(int n)
{
    // Base Case
    if (n <= 1)
        return n;
  
    // Find the Fibonacci Number
    return fib(n - 1) + fib(n - 2);
}
  
// Driver Code
int main()
{
    // Constant expression evaluated
    // at compile time
    const int val = fib(22);
  
    cout << "The fibonacci number "
         << "is: " << val << "\n";
  
    return 0;
}
""",
    "third": """
class point3d
{
  double x_;
  double y_;
  double z_;
public:
  consteval point3d(double const x = 0,
                    double const y = 0,
                    double const z = 0)
    :x_{x}, y_{y}, z_{z}
  {}
  consteval double get_x() const {return x_;}
  consteval double get_y() const {return y_;}
  consteval double get_z() const {return z_;}
};
"""
}

CPP_TEMPLATE_coroutines = {
    "separator": '// create a fuzzing testcase for a C++ compiler for feature "coroutines"',
    "first" :
        """
#include <concepts>
#include <coroutine>
#include <exception>
#include <iostream>

struct ReturnObject {
  struct promise_type {
    ReturnObject get_return_object() { return {}; }
    std::suspend_never initial_suspend() { return {}; }
    std::suspend_never final_suspend() noexcept { return {}; }
    void unhandled_exception() {}
  };
};

struct Awaiter {
  std::coroutine_handle<> *hp_;
  constexpr bool await_ready() const noexcept { return false; }
  void await_suspend(std::coroutine_handle<> h) { *hp_ = h; }
  constexpr void await_resume() const noexcept {}
};

ReturnObject
counter(std::coroutine_handle<> *continuation_out)
{
  Awaiter a{continuation_out};
  for (unsigned i = 0;; ++i) {
    co_await a;
    std::cout << "counter: " << i << std::endl;
  }
}

void
main1()
{
  std::coroutine_handle<> h;
  counter(&h);
  for (int i = 0; i < 3; ++i) {
    std::cout << "In main1 function\n";
    h();
  }
  h.destroy();
}
""",
    "second" :
        """
#include <coroutine>
#include <iostream>
 
struct promise;
 
struct coroutine : std::coroutine_handle<promise>
{
    using promise_type = struct promise;
};
 
struct promise
{
    coroutine get_return_object() { return {coroutine::from_promise(*this)}; }
    std::suspend_always initial_suspend() noexcept { return {}; }
    std::suspend_always final_suspend() noexcept { return {}; }
    void return_void() {}
    void unhandled_exception() {}
};
 
struct S
{
    int i;
    coroutine f()
    {
        std::cout << i;
        co_return;
    }
};
 
void bad1()
{
    coroutine h = S{0}.f();
    // S{0} destroyed
    h.resume(); // resumed coroutine executes std::cout << i, uses S::i after free
    h.destroy();
}
 
coroutine bad2()
{
    S s{0};
    return s.f(); // returned coroutine can't be resumed without committing use after free
}
 
void bad3()
{
    coroutine h = [i = 0]() -> coroutine // a lambda that's also a coroutine
    {
        std::cout << i;
        co_return;
    }(); // immediately invoked
    // lambda destroyed
    h.resume(); // uses (anonymous lambda type)::i after free
    h.destroy();
}
 
void good()
{
    coroutine h = [](int i) -> coroutine // make i a coroutine parameter
    {
        std::cout << i;
        co_return;
    }(0);
    // lambda destroyed
    h.resume(); // no problem, i has been copied to the coroutine
                // frame as a by-value parameter
    h.destroy();
}
""",
    "third": """"""
}
