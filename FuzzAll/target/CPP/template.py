FIRST = """
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

SECOND = """
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

THIRD = """
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

C_TEMPLATE = """
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
    "first": """
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
    "second": """
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
    "third": """
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
""",
}

CPP_TEMPLATE_multi_dimen_access = """
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
    "first": """
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
    "second": """
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
    "third": """""",
}


CPP_TEMPLATE_likely_unlikely = {
    "separator": 'Please create a fuzzing testcase for a C++ compiler to test feature "likely, unlikely attributes"',
    "first": """
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
    "second": """
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
    "third": """""",
}

CPP_TEMPLATE_immediate_function = {
    "separator": 'Please create a fuzzing testcase for a C++ compiler to test feature "immediate function"',
    "first": """
consteval int sqr(int n) {
  return n * n;
}

constexpr int r = sqr(100);
""",
    "second": """
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
""",
}

CPP_TEMPLATE_coroutines = {
    "separator": '// create a fuzzing testcase for a C++ compiler for feature "coroutines"',
    "first": """
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
    "second": """
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
    "third": """""",
}

cpp_expected = {
    "docstring": """
     C++ Utilities library std::expected
Defined in header <expected>
template< class T, class E >
class expected;
(since C++23)
The class template std::expected provides a way to store either of two values. An object of std::expected at any given time either holds an expected value of type T, or an unexpected value of type E. std::expected is never valueless.

The stored value is allocated directly within the storage occupied by the expected object. No dynamic memory allocation takes place.

A program is ill-formed if it instantiates an expected with a reference type, a function type, or a specialization of std::unexpected. In addition, T must not be std::in_place_t or std::unexpect_t.

Template parameters
T	-	the type of the expected value. The type must either be (possibly cv-qualified) void, or meet the Destructible requirements (in particular, array and reference types are not allowed).
E	-	the type of the unexpected value. The type must meet the Destructible requirements, and must be a valid template argument for std::unexpected (in particular, arrays, non-object types, and cv-qualified types are not allowed).
Member types
Member type	Definition
value_type (C++23)	T
error_type (C++23)	E
unexpected_type (C++23)	std::unexpected<E>
rebind (C++23)	template< class U >
using rebind = expected<U, error_type>;

Member functions
(constructor)

(C++23)

constructs the expected object
(public member function)
(destructor)

(C++23)

destroys the expected object, along with its contained value
(public member function)
operator=

(C++23)

assigns contents
(public member function)
Observers
operator->
operator*

(C++23)

accesses the expected value
(public member function)
operator bool
has_value

(C++23)

checks whether the object contains an expected value
(public member function)
value

(C++23)

returns the expected value
(public member function)
error

(C++23)

returns the unexpected value
(public member function)
value_or

(C++23)

returns the expected value if present, another value otherwise
(public member function)
Monadic operations
and_then

(C++23)

returns the result of the given function on the expected value if it exists; otherwise, returns the expected itself
(public member function)
transform

(C++23)

returns an expected containing the transformed expected value if it exists; otherwise, returns the expected itself
(public member function)
or_else

(C++23)

returns the expected itself if it contains an expected value; otherwise, returns the result of the given function on the unexpected value
(public member function)
transform_error

(C++23)

returns the expected itself if it contains an expected value; otherwise, returns an expected containing the transformed unexpected value
(public member function)
Modifiers
emplace

(C++23)

constructs the expected value in-place
(public member function)
swap

(C++23)

exchanges the contents
(public member function)
Non-member functions
operator==

(C++23)

compares expected objects
(function template)
swap(std::expected)

(C++23)

specializes the std::swap algorithm
(function)
Helper classes
unexpected

(C++23)

represented as an unexpected value
(class template)
bad_expected_access

(C++23)

exception indicating checked access to an expected that contains an unexpected value
(class template)
unexpect_t
unexpect

(C++23)

in-place construction tag for unexpected value in expected
    """,
    "hw_prompt": """
```
template< class T, class E >
class expected;
```
The class template std::expected provides a way to store either of two values. An object of std::expected at any given time either holds an expected value of type T, or an unexpected value of type E. std::expected is never valueless.
The stored value is allocated directly within the storage occupied by the expected object. No dynamic memory allocation takes place.
A program is ill-formed if it instantiates an expected with a reference type, a function type, or a specialization of std::unexpected. In addition, T must not be std::in_place_t or std::unexpect_t.
""",
    "separator": "/* Please create a very short program which combines std::expected with new C++ features in a complex way */",
    "begin": "#include <expected>",
    "target_api": "expected",
    "example_code": """
Here is an example program using std::expected
```
#include <expected>
#include <iostream>
#include <string_view>

enum class parse_error {
    invalid_char,
    overflow
};
std::expected<double, parse_error>
parse_number(std::string_view& str) {
    const char* begin = str.data();
    char* end;
    double retval = std::strtod(begin, &end);
    if (begin == end) {
        return std::unexpected(parse_error::invalid_char);
    }
    str.remove_prefix(end - begin);
    return retval;
}
auto main(void) -> int {
    std::string_view src = "12";
    auto num = parse_number(src);
    if (num.has_value()) {}
    else if (num.error() == parse_error::invalid_char) {}
    else if (num.error() == parse_error::overflow) {}
    else {}
    return 0;
}
```
""",
}

cpp_variant = {
    "docstring": """
    std::variant
 C++ Utilities library std::variant
Defined in header <variant>
template< class... Types >
class variant;
(since C++17)
The class template std::variant represents a type-safe union. An instance of std::variant at any given time either holds a value of one of its alternative types, or in the case of error - no value (this state is hard to achieve, see valueless_by_exception).

As with unions, if a variant holds a value of some object type T, the object representation of T is allocated directly within the object representation of the variant itself. Variant is not allowed to allocate additional (dynamic) memory.

A variant is not permitted to hold references, arrays, or the type void. Empty variants are also ill-formed (std::variant<std::monostate> can be used instead).

A variant is permitted to hold the same type more than once, and to hold differently cv-qualified versions of the same type.

Consistent with the behavior of unions during aggregate initialization, a default-constructed variant holds a value of its first alternative, unless that alternative is not default-constructible (in which case the variant is not default-constructible either). The helper class std::monostate can be used to make such variants default-constructible.

Template parameters
Types	-	the types that may be stored in this variant. All types must meet the Destructible requirements (in particular, array types and non-object types are not allowed).
Member functions
(constructor)

constructs the variant object
(public member function)
(destructor)

destroys the variant, along with its contained value
(public member function)
operator=

assigns a variant
(public member function)
Observers
index

returns the zero-based index of the alternative held by the variant
(public member function)
valueless_by_exception

checks if the variant is in the invalid state
(public member function)
Modifiers
emplace

constructs a value in the variant, in place
(public member function)
swap

swaps with another variant
(public member function)
Non-member functions
visit

(C++17)

calls the provided functor with the arguments held by one or more variants
(function template)
holds_alternative

(C++17)

checks if a variant currently holds a given type
(function template)
std::get(std::variant)

(C++17)

reads the value of the variant given the index or the type (if the type is unique), throws on error
(function template)
get_if

(C++17)

obtains a pointer to the value of a pointed-to variant given the index or the type (if unique), returns null on error
(function template)
operator==
operator!=
operator<
operator<=
operator>
operator>=
operator<=>

(C++17)
(C++17)
(C++17)
(C++17)
(C++17)
(C++17)
(C++20)

compares variant objects as their contained values
(function template)
std::swap(std::variant)

(C++17)

specializes the std::swap algorithm
(function template)
Helper classes
monostate

(C++17)

placeholder type for use as the first alternative in a variant of non-default-constructible types
(class)
bad_variant_access

(C++17)

exception thrown on invalid accesses to the value of a variant
(class)
variant_size
variant_size_v

(C++17)

obtains the size of the variant's list of alternatives at compile time
(class template) (variable template)
variant_alternative
variant_alternative_t

(C++17)

obtains the type of the alternative specified by its index, at compile time
(class template) (alias template)
std::hash<std::variant>

(C++17)

specializes the std::hash algorithm
(class template specialization)
Helper objects
variant_npos

(C++17)

index of the variant in the invalid state
(constant)
    """,
    "hw_prompt": """
The class template std::variant represents a type-safe union. An instance of std::variant at any given time either holds a value of one of its alternative types, or in the case of error - no value (this state is hard to achieve, see valueless_by_exception).
As with unions, if a variant holds a value of some object type T, the object representation of T is allocated directly within the object representation of the variant itself. Variant is not allowed to allocate additional (dynamic) memory.
A variant is not permitted to hold references, arrays, or the type void. Empty variants are also ill-formed (std::variant<std::monostate> can be used instead).
A variant is permitted to hold the same type more than once, and to hold differently cv-qualified versions of the same type.
Consistent with the behavior of unions during aggregate initialization, a default-constructed variant holds a value of its first alternative, unless that alternative is not default-constructible (in which case the variant is not default-constructible either). The helper class std::monostate can be used to make such variants default-constructible.

Member functions
index | returns the zero-based index of the alternative held by the variant
valueless_by_exception | checks if the variant is in the invalid state
emplace | constructs a value in the variant, in place
swap | swaps with another variant

Non-member functions
visit | calls the provided functor with the arguments held by one or more variants
holds_alternative | checks if a variant currently holds a given type
get_if | obtains a pointer to the value of a pointed-to variant given the index or the type (if unique), returns null on error

Helper classes
monostate | placeholder type for use as the first alternative in a variant of non-default-constructible types
bad_variant_access | exception thrown on invalid accesses to the value of a variant
""",
    # "separator": 'Please create a fuzzing testcase for a C++ compiler to test the std::variant class',
    # "separator": "Please create a very short program which combines std::variant with new C++ features in a complex way",
    "separator": "/* Please create a very short program which combines std::variant with new C++ features in a complex way */",
    "begin": "#include <variant>",
    "target_api": "variant",
    "example_code": """
Here is an example program using std::variant
```
#include <variant>
#include <string>
#include <cassert>
#include <iostream>

int main()
{
    std::variant<int, float> v, w;
    v = 42;
    int i = std::get<int>(v);
    assert(42 == i);
    w = std::get<int>(v);
    w = std::get<0>(v);
    w = v;
    try{std::get<float>(w);}
    catch (const std::bad_variant_access& ex){}
    using namespace std::literals;
    std::variant<std::string> x("abc");
    x = "def";
    std::variant<std::string, void const*> y("abc");
    assert(std::holds_alternative<void const*>(y));
    y = "xyz"s;
    assert(std::holds_alternative<std::string>(y));
}
```
""",
}

cpp_optional = {
    "docstring": """
std::optional
 C++ Utilities library std::optional
Defined in header <optional>
template< class T >
class optional;
(since C++17)
The class template std::optional manages an optional contained value, i.e. a value that may or may not be present.

A common use case for optional is the return value of a function that may fail. As opposed to other approaches, such as std::pair<T,bool>, optional handles expensive-to-construct objects well and is more readable, as the intent is expressed explicitly.

Any instance of optional<T> at any given point in time either contains a value or does not contain a value.

If an optional<T> contains a value, the value is guaranteed to be allocated as part of the optional object footprint, i.e. no dynamic memory allocation ever takes place. Thus, an optional object models an object, not a pointer, even though operator*() and operator->() are defined.

When an object of type optional<T> is contextually converted to bool, the conversion returns true if the object contains a value and false if it does not contain a value.

The optional object contains a value in the following conditions:

The object is initialized with/assigned from a value of type T or another optional that contains a value.
The object does not contain a value in the following conditions:

The object is default-initialized.
The object is initialized with/assigned from a value of type std::nullopt_t or an optional object that does not contain a value.
The member function reset() is called.
There are no optional references; a program is ill-formed if it instantiates an optional with a reference type. Alternatively, an optional of a std::reference_wrapper of type T may be used to hold a reference. In addition, a program is ill-formed if it instantiates an optional with the (possibly cv-qualified) tag types std::nullopt_t or std::in_place_t.

Template parameters
T	-	the type of the value to manage initialization state for. The type must meet the requirements of Destructible (in particular, array and reference types are not allowed).
Member types
Member type	Definition
value_type	T
Member functions
(constructor)

constructs the optional object
(public member function)
(destructor)

destroys the contained value, if there is one
(public member function)
operator=

assigns contents
(public member function)
Observers
operator->
operator*

accesses the contained value
(public member function)
operator bool
has_value

checks whether the object contains a value
(public member function)
value

returns the contained value
(public member function)
value_or

returns the contained value if available, another value otherwise
(public member function)
Monadic operations
and_then

(C++23)

returns the result of the given function on the contained value if it exists, or an empty optional otherwise
(public member function)
transform

(C++23)

returns an optional containing the transformed contained value if it exists, or an empty optional otherwise
(public member function)
or_else

(C++23)

returns the optional itself if it contains a value, or the result of the given function otherwise
(public member function)
Modifiers
swap

exchanges the contents
(public member function)
reset

destroys any contained value
(public member function)
emplace

constructs the contained value in-place
(public member function)
Non-member functions
operator==
operator!=
operator<
operator<=
operator>
operator>=
operator<=>

(C++17)
(C++17)
(C++17)
(C++17)
(C++17)
(C++17)
(C++20)

compares optional objects
(function template)
make_optional

(C++17)

creates an optional object
(function template)
std::swap(std::optional)

(C++17)

specializes the std::swap algorithm
(function template)
Helper classes
std::hash<std::optional>

(C++17)

specializes the std::hash algorithm
(class template specialization)
nullopt_t

(C++17)

indicator of optional type with uninitialized state
(class)
bad_optional_access

(C++17)

exception indicating checked access to an optional that doesn't contain a value
(class)
Helpers
nullopt

(C++17)

an object of type nullopt_t
(constant)
in_place
in_place_type
in_place_index
in_place_t
in_place_type_t
in_place_index_t

(C++17)

in-place construction tag
(class template)
Deduction guides
Notes
Feature-test macro	Value	Std	Comment
__cpp_lib_optional	201606L	(C++17)	std::optional
__cpp_lib_optional	202106L	(C++20)
(DR)	Fully constexpr
__cpp_lib_optional	202110L	(C++23)	Monadic operations
""",
    "separator": "/* Please create a very short program which combines std::optional with new C++ features in a complex way */",
    "begin": "#include <optional>",
    "target_api": "optional",
    "example_code": """
Here is an example program using std::optional
```
#include <string>
#include <functional>
#include <iostream>
#include <optional>
std::optional<std::string> create(bool b) {
    if (b)
        return "Godzilla";
    return {};
}
auto create2(bool b) {
    return b ? std::optional<std::string>{"Godzilla"} : std::nullopt;
}
auto create_ref(bool b) {
    static std::string value = "Godzilla";
    return b ? std::optional<std::reference_wrapper<std::string>>{value}
             : std::nullopt;
}
int main() {
    std::cout << "create(false) returned "
              << create(false).value_or("empty");
    if (auto str = create2(true)) {
    }
    if (auto str = create_ref(true)) {
        str->get() = "Mothra";
    }
}
```
""",
}

cpp_span = {
    #     "docstring": """
    # We want to target the std::span class, here are the documentation of the std::span class:
    # `std::span`
    # Description:
    # ```
    # template<
    #     class T,
    #     std::size_t Extent = std::dynamic_extent
    # > class span;
    # ```
    # The class template span describes an object that can refer to a contiguous sequence of objects with the first element of the sequence at position zero. A span can either have a static extent, in which case the number of elements in the sequence is known at compile-time and encoded in the type, or a dynamic extent.
    # If a span has dynamic extent, a typical implementation holds two members: a pointer to T and a size. A span with static extent may have only one member: a pointer to T.
    #
    # Member functions:
    # begin | returns an iterator to the beginning
    # end | returns an iterator to the end
    # first | obtains a subspan consisting of the first N elements of the sequence
    # last | obtains a subspan consisting of the last N elements of the sequence
    # subspan | obtains a subspan
    # """,
    "docstring": """
/* `std::span` is a C++ containers library that allows you to reference a contiguous sequence of objects. It can have a static or dynamic extent, with the number of elements known at compile-time or runtime, respectively. `std::span` provides functions for construction, assignment, element access (e.g., `front()`, `back()`, `operator[]`), iterators (e.g., `begin()`, `end()`, `rbegin()`, `rend()`), size information (e.g., `size()`, `size_bytes()`), and creating subspans. You can also convert a span into a view of its underlying bytes using non-member functions (`as_bytes()`, `as_writable_bytes()`). This library is ideal for handling and manipulating contiguous sequences of objects efficiently in C++ programs. */
""",
    # "separator": 'Please create a fuzzing testcase for a C++ compiler to test the std::span class',
    # "separator": "/* Please create a very short program which combines std::span with new C++ features in a complex way */",
    "separator": "/* A fuzzing program which combines std::span with new C++ features in a complex way */",
    "begin": "#include <span>",
    "target_api": "span",
    "example_code": """
Here is an example program using std::span
```
#include <algorithm>
#include <cstddef>
#include <iostream>
#include <span>
template<class T, std::size_t N>
[[nodiscard]]
constexpr auto slide(std::span<T,N> s, std::size_t offset, std::size_t width) {
    return s.subspan(offset, offset + width <= s.size() ? width : 0U);
}

template<class T, std::size_t N, std::size_t M>
constexpr bool starts_with(std::span<T,N> data, std::span<T,M> prefix) {
    return data.size() >= prefix.size()
        && std::equal(prefix.begin(), prefix.end(), data.begin());
}

template<class T, std::size_t N, std::size_t M>
constexpr bool ends_with(std::span<T,N> data, std::span<T,M> suffix) {
    return data.size() >= suffix.size()
        && std::equal(data.end() - suffix.size(), data.end(),
                      suffix.end() - suffix.size());
}
template<class T, std::size_t N, std::size_t M>
constexpr bool contains(std::span<T,N> span, std::span<T,M> sub) {
    return std::search(span.begin(), span.end(), sub.begin(), sub.end()) != span.end();
}
int main()
{
    constexpr int a[] { 0, 1, 2, 3, 4, 5, 6, 7, 8 };
    constexpr int b[] { 8, 7, 6 };
    for (std::size_t offset{}; ; ++offset) {
        static constexpr std::size_t width{6};
        auto s = slide(std::span{a}, offset, width);
        if (s.empty())
            break;
    }
    static_assert(
        starts_with( std::span{a}, std::span{a, 4} ) and
        starts_with( std::span{a + 1, 4}, std::span{a + 1, 3} ) and
      ! starts_with( std::span{a}, std::span{b} ) and
      ! starts_with( std::span{a, 8}, std::span{a + 1, 3} ) and
        ends_with( std::span{a}, std::span{a + 6, 3} ) and
      ! ends_with( std::span{a}, std::span{a + 6, 2} ) and
        contains( std::span{a}, std::span{a + 1, 4} ) and
      ! contains( std::span{a, 8}, std::span{a, 9} )
    );
}
```
""",
}

cpp_is_scoped_enum = {
    "docstring": """
std::is_scoped_enum
 C++ Metaprogramming library
Defined in header <type_traits>
template< class T >
struct is_scoped_enum;
(since C++23)
Checks whether T is a scoped enumeration type. Provides the member constant value which is equal to true, if T is a scoped enumeration type. Otherwise, value is equal to false.

The behavior of a program that adds specializations for is_scoped_enum or is_scoped_enum_v is undefined.

Template parameters
T	-	a type to check
Helper variable template
template< class T >
inline constexpr bool is_scoped_enum_v = is_scoped_enum<T>::value;
(since C++23)
Inherited from std::integral_constant
Member constants
value

[static]

true if T is a scoped enumeration type, false otherwise
(public static member constant)
Member functions
operator bool

converts the object to bool, returns value
(public member function)
operator()

(C++14)

returns value
(public member function)
Member types
Type	Definition
value_type	bool
type	std::integral_constant<bool, value>
Notes
Feature-test macro	Value	Std	Comment
__cpp_lib_is_scoped_enum	202011L	(C++23)	std::is_scoped_enum

""",
    #     "docstring": """
    # /* The std::is_scoped_enum library in C++ is a metaprogramming tool provided by the <type_traits> header. It allows you to check whether a given type T is a scoped enumeration type. The library provides a member constant value, which is true if T is a scoped enumeration type, and false otherwise.
    #    To utilize std::is_scoped_enum, you can use the value member constant directly or the helper variable template is_scoped_enum_v, which provides the same functionality.
    #    It's important to note that adding specializations for std::is_scoped_enum or is_scoped_enum_v is undefined behavior.
    #    In summary, std::is_scoped_enum is a C++ library that allows you to check whether a type is a scoped enumeration. You can use the provided member constant or helper variable template to determine if a type is a scoped enumeration in your code. */
    # """,
    # "separator": 'Please create a fuzzing testcase for a C++ compiler to test the std::optional class',
    # "separator": 'Please create a short but complex program which combines many new features of C++ with std::optional',
    "separator": "/* Please create a very short program which combines std::is_scoped_enum with new C++ features in a complex way */",
    "begin": "#include <type_traits>",
    "target_api": "is_scoped_enum",
    # "separator": 'Please create a short program which has complex usages of std::optional',
    # "separator": 'Please create a fuzzing testcase for a C++ compiler to test the std::optional class',
    "example_code": """
Here is an example program using std::is_scoped_enum
```
#include <iostream>
#include <type_traits>

class A {};
enum E {};
enum struct Es { oz };
enum class Ec : int {};

int main()
{
    std::boolalpha;
    std::is_scoped_enum_v<A>;
    std::is_scoped_enum_v<E>;
    std::is_scoped_enum_v<Es>;
    std::is_scoped_enum_v<Ec>;
    std::is_scoped_enum_v<int>;
}
```
""",
}

cpp_apply = {
    "docstring": """
std::apply
 C++ Utilities library
Defined in header <tuple>
template< class F, class Tuple >
constexpr decltype(auto) apply( F&& f, Tuple&& t );
(since C++17)
(until C++23)
template< class F, tuple-like Tuple >
constexpr decltype(auto) apply( F&& f, Tuple&& t ) noexcept(/* see below */);
(since C++23)
Invoke the Callable object f with the elements of t as arguments.

Given the exposition-only function apply-impl defined as follows: template<class F, tuple-like Tuple, std::size_t... I> // no constraint on Tuple before C++23
constexpr decltype(auto)
    apply-impl(F&& f, Tuple&& t, std::index_sequence<I...>) // exposition only
{
    return INVOKE(std::forward<F>(f), std::get<I>(std::forward<Tuple>(t))...);
}


The effect is equivalent to return apply-impl(std::forward<F>(f), std::forward<Tuple>(t),
                  std::make_index_sequence<
                      std::tuple_size_v<std::decay_t<Tuple>>>{});.

Parameters
f	-	Callable object to be invoked
t	-	tuple whose elements to be used as arguments to f
Return value
The value returned by f.

Exceptions
(none)

(until C++23)
noexcept specification:
noexcept(
    noexcept(std::invoke(std::forward<F>(f),
                         std::get<Is>(std::forward<Tuple>(t))...))
)
where Is... denotes the parameter pack:

0, 1, ..., std::tuple_size_v<std::remove_reference_t<Tuple>> - 1.
(since C++23)
Notes
Tuple need not be std::tuple, and instead may be anything that supports std::get and std::tuple_size; in particular, std::array and std::pair may be used.

(until C++23)
Tuple is constrained to be tuple-like, i.e. each type therein is required to be a specialization of std::tuple or another type (such as std::array and std::pair) that models tuple-like.

(since C++23)
""",
    "hw_prompt": """
`std::apply`
Description:
```
template< class F, class Tuple >
constexpr decltype(auto) apply( F&& f, Tuple&& t ) noexcept(/* see below */);
```
Checks whether T is a scoped enumeration type. Provides the member constant value which is equal to true, if T is a scoped enumeration type. Otherwise, value is equal to false.
The behavior of a program that adds specializations for is_scoped_enum or is_scoped_enum_v is undefined.
""",
    # "separator": 'Please create a fuzzing testcase for a C++ compiler to test the std::optional class',
    # "separator": 'Please create a short but complex program which combines many new features of C++ with std::optional',
    "separator": "/* Please create a very short program which combines std::apply with new C++ features in a complex way */",
    "begin": "#include <tuple>",
    "target_api": "apply",
    # "separator": 'Please create a short program which has complex usages of std::optional',
    # "separator": 'Please create a fuzzing testcase for a C++ compiler to test the std::optional class',
    "example_code": """
Here is an example program using std::apply
```
#include <iostream>
#include <tuple>
#include <utility>

int add(int first, int second) { return first + second; }

template<typename T>
T add_generic(T first, T second) { return first + second; }

auto add_lambda = [](auto first, auto second) { return first + second; };

template<typename... Ts>
std::ostream& operator<<(std::ostream& os, std::tuple<Ts...> const& theTuple) {
    std::apply
    (
        [&os](Ts const&... tupleArgs)
        {
            os << '[';
            std::size_t n{0};
            ((os << tupleArgs << (++n != sizeof...(Ts) ? ", " : "")), ...);
            os << ']';
        }, theTuple
    );
    return os;
}

int main() {
    std::apply(add, std::pair(1, 2));
    // Error: can't deduce the function type
    // std::apply(add_generic, std::make_pair(2.0f, 3.0f));
    std::apply(add_lambda, std::pair(2.0f, 3.0f));
}
```
""",
}

cpp_to_underlying = {
    "docstring": """
We want to target the std::to_underlying class, here are the documentation of the std::to_underlying class:
`std::to_underlying`
Description:
```
template< class Enum >
constexpr std::underlying_type_t<Enum> to_underlying( Enum e ) noexcept;
```
Converts an enumeration to its underlying type. Equivalent to return static_cast<std::underlying_type_t<Enum>>(e);.
Parameters
e | enumeration value to convert
Return value
The integer value of the underlying type of Enum, converted from e.
Notes
std::to_underlying can be used to avoid converting an enumeration to an integer type other than its underlying type.
""",
    # "separator": 'Please create a fuzzing testcase for a C++ compiler to test the std::optional class',
    # "separator": 'Please create a short but complex program which combines many new features of C++ with std::optional',
    "separator": "Please create a very short program which combines std::to_underlying with new C++ features in a complex way",
    # "separator": 'Please create a short program which has complex usages of std::optional',
    # "separator": 'Please create a fuzzing testcase for a C++ compiler to test the std::optional class',
    "example_code": """
Here is an example program using std::to_underlying
```
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <type_traits>
#include <utility>

int main()
{
    enum class E1 : char { e };
    static_assert(std::is_same_v<char, decltype(std::to_underlying(E1::e))>);
    enum struct E2 : long { e };
    static_assert(std::is_same_v<long, decltype(std::to_underlying(E2::e))>);
    enum E3 : unsigned { e };
    static_assert(std::is_same_v<unsigned, decltype(std::to_underlying(e))>);

    enum class ColorMask : std::uint32_t {
        red = 0xFF, green = (red << 8), blue = (green << 8), alpha = (blue << 8)
    };
    std::cout << std::hex << std::uppercase << std::setfill('0')
        << std::setw(8) << std::to_underlying(ColorMask::red)
        << std::setw(8) << std::to_underlying(ColorMask::green)
        << std::setw(8) << std::to_underlying(ColorMask::blue)
        << std::setw(8) << std::to_underlying(ColorMask::alpha);
    [[maybe_unused]]
    std::underlying_type_t<ColorMask> y = std::to_underlying(ColorMask::alpha); // OK
}
```
""",
}
