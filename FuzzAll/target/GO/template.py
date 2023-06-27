go_atomic = {
    "docstring": """
    Overview ¶
Package atomic provides low-level atomic memory primitives useful for implementing synchronization algorithms.

These functions require great care to be used correctly. Except for special, low-level applications, synchronization is better done with channels or the facilities of the sync package. Share memory by communicating; don't communicate by sharing memory.

The swap operation, implemented by the SwapT functions, is the atomic equivalent of:

old = *addr
*addr = new
return old
The compare-and-swap operation, implemented by the CompareAndSwapT functions, is the atomic equivalent of:

if *addr == old {
	*addr = new
	return true
}
return false
The add operation, implemented by the AddT functions, is the atomic equivalent of:

*addr += delta
return *addr
The load and store operations, implemented by the LoadT and StoreT functions, are the atomic equivalents of "return *addr" and "*addr = val".

In the terminology of the Go memory model, if the effect of an atomic operation A is observed by atomic operation B, then A “synchronizes before” B. Additionally, all the atomic operations executed in a program behave as though executed in some sequentially consistent order. This definition provides the same semantics as C++'s sequentially consistent atomics and Java's volatile variables.

func AddInt32(addr *int32, delta int32) (new int32)
func AddInt64(addr *int64, delta int64) (new int64)
func AddUint32(addr *uint32, delta uint32) (new uint32)
func AddUint64(addr *uint64, delta uint64) (new uint64)
func AddUintptr(addr *uintptr, delta uintptr) (new uintptr)
func CompareAndSwapInt32(addr *int32, old, new int32) (swapped bool)
func CompareAndSwapInt64(addr *int64, old, new int64) (swapped bool)
func CompareAndSwapPointer(addr *unsafe.Pointer, old, new unsafe.Pointer) (swapped bool)
func CompareAndSwapUint32(addr *uint32, old, new uint32) (swapped bool)
func CompareAndSwapUint64(addr *uint64, old, new uint64) (swapped bool)
func CompareAndSwapUintptr(addr *uintptr, old, new uintptr) (swapped bool)
func LoadInt32(addr *int32) (val int32)
func LoadInt64(addr *int64) (val int64)
func LoadPointer(addr *unsafe.Pointer) (val unsafe.Pointer)
func LoadUint32(addr *uint32) (val uint32)
func LoadUint64(addr *uint64) (val uint64)
func LoadUintptr(addr *uintptr) (val uintptr)
func StoreInt32(addr *int32, val int32)
func StoreInt64(addr *int64, val int64)
func StorePointer(addr *unsafe.Pointer, val unsafe.Pointer)
func StoreUint32(addr *uint32, val uint32)
func StoreUint64(addr *uint64, val uint64)
func StoreUintptr(addr *uintptr, val uintptr)
func SwapInt32(addr *int32, new int32) (old int32)
func SwapInt64(addr *int64, new int64) (old int64)
func SwapPointer(addr *unsafe.Pointer, new unsafe.Pointer) (old unsafe.Pointer)
func SwapUint32(addr *uint32, new uint32) (old uint32)
func SwapUint64(addr *uint64, new uint64) (old uint64)
func SwapUintptr(addr *uintptr, new uintptr) (old uintptr)
type Bool
func (x *Bool) CompareAndSwap(old, new bool) (swapped bool)
func (x *Bool) Load() bool
func (x *Bool) Store(val bool)
func (x *Bool) Swap(new bool) (old bool)
type Int32
func (x *Int32) Add(delta int32) (new int32)
func (x *Int32) CompareAndSwap(old, new int32) (swapped bool)
func (x *Int32) Load() int32
func (x *Int32) Store(val int32)
func (x *Int32) Swap(new int32) (old int32)
type Int64
func (x *Int64) Add(delta int64) (new int64)
func (x *Int64) CompareAndSwap(old, new int64) (swapped bool)
func (x *Int64) Load() int64
func (x *Int64) Store(val int64)
func (x *Int64) Swap(new int64) (old int64)
type Pointer
func (x *Pointer[T]) CompareAndSwap(old, new *T) (swapped bool)
func (x *Pointer[T]) Load() *T
func (x *Pointer[T]) Store(val *T)
func (x *Pointer[T]) Swap(new *T) (old *T)
type Uint32
func (x *Uint32) Add(delta uint32) (new uint32)
func (x *Uint32) CompareAndSwap(old, new uint32) (swapped bool)
func (x *Uint32) Load() uint32
func (x *Uint32) Store(val uint32)
func (x *Uint32) Swap(new uint32) (old uint32)
type Uint64
func (x *Uint64) Add(delta uint64) (new uint64)
func (x *Uint64) CompareAndSwap(old, new uint64) (swapped bool)
func (x *Uint64) Load() uint64
func (x *Uint64) Store(val uint64)
func (x *Uint64) Swap(new uint64) (old uint64)
type Uintptr
func (x *Uintptr) Add(delta uintptr) (new uintptr)
func (x *Uintptr) CompareAndSwap(old, new uintptr) (swapped bool)
func (x *Uintptr) Load() uintptr
func (x *Uintptr) Store(val uintptr)
func (x *Uintptr) Swap(new uintptr) (old uintptr)
type Value
func (v *Value) CompareAndSwap(old, new any) (swapped bool)
func (v *Value) Load() (val any)
func (v *Value) Store(val any)
func (v *Value) Swap(new any) (old any)
    """,
    "separator": "// Please create a very short program which combines atomic with other go features in a complex way",
    "begin": 'package main\nimport (\n\t"sync/atomic"\n)\n',
    "target_api": "atomic",
}
go_reflect = {
    "docstring": """
    Overview ¶
Package reflect implements run-time reflection, allowing a program to manipulate objects with arbitrary types. The typical use is to take a value with static type interface{} and extract its dynamic type information by calling TypeOf, which returns a Type.

A call to ValueOf returns a Value representing the run-time data. Zero takes a Type and returns a Value representing a zero value for that type.

See "The Laws of Reflection" for an introduction to reflection in Go: https://golang.org/doc/articles/laws_of_reflection.html

Index ¶
Constants
func Copy(dst, src Value) int
func DeepEqual(x, y any) bool
func Swapper(slice any) func(i, j int)
type ChanDir
func (d ChanDir) String() string
type Kind
func (k Kind) String() string
type MapIter
func (iter *MapIter) Key() Value
func (iter *MapIter) Next() bool
func (iter *MapIter) Reset(v Value)
func (iter *MapIter) Value() Value
type Method
func (m Method) IsExported() bool
type SelectCase
type SelectDir
type SliceHeader
type StringHeader
type StructField
func VisibleFields(t Type) []StructField
func (f StructField) IsExported() bool
type StructTag
func (tag StructTag) Get(key string) string
func (tag StructTag) Lookup(key string) (value string, ok bool)
type Type
func ArrayOf(length int, elem Type) Type
func ChanOf(dir ChanDir, t Type) Type
func FuncOf(in, out []Type, variadic bool) Type
func MapOf(key, elem Type) Type
func PointerTo(t Type) Type
func PtrTo(t Type) Type
func SliceOf(t Type) Type
func StructOf(fields []StructField) Type
func TypeOf(i any) Type
type Value
func Append(s Value, x ...Value) Value
func AppendSlice(s, t Value) Value
func Indirect(v Value) Value
func MakeChan(typ Type, buffer int) Value
func MakeFunc(typ Type, fn func(args []Value) (results []Value)) Value
func MakeMap(typ Type) Value
func MakeMapWithSize(typ Type, n int) Value
func MakeSlice(typ Type, len, cap int) Value
func New(typ Type) Value
func NewAt(typ Type, p unsafe.Pointer) Value
func Select(cases []SelectCase) (chosen int, recv Value, recvOK bool)
func ValueOf(i any) Value
func Zero(typ Type) Value
func (v Value) Addr() Value
func (v Value) Bool() bool
func (v Value) Bytes() []byte
func (v Value) Call(in []Value) []Value
func (v Value) CallSlice(in []Value) []Value
func (v Value) CanAddr() bool
func (v Value) CanComplex() bool
func (v Value) CanConvert(t Type) bool
func (v Value) CanFloat() bool
func (v Value) CanInt() bool
func (v Value) CanInterface() bool
func (v Value) CanSet() bool
func (v Value) CanUint() bool
func (v Value) Cap() int
func (v Value) Close()
func (v Value) Comparable() bool
func (v Value) Complex() complex128
func (v Value) Convert(t Type) Value
func (v Value) Elem() Value
func (v Value) Equal(u Value) bool
func (v Value) Field(i int) Value
func (v Value) FieldByIndex(index []int) Value
func (v Value) FieldByIndexErr(index []int) (Value, error)
func (v Value) FieldByName(name string) Value
func (v Value) FieldByNameFunc(match func(string) bool) Value
func (v Value) Float() float64
func (v Value) Grow(n int)
func (v Value) Index(i int) Value
func (v Value) Int() int64
func (v Value) Interface() (i any)
func (v Value) InterfaceData() [2]uintptrDEPRECATED
func (v Value) IsNil() bool
func (v Value) IsValid() bool
func (v Value) IsZero() bool
func (v Value) Kind() Kind
func (v Value) Len() int
func (v Value) MapIndex(key Value) Value
func (v Value) MapKeys() []Value
func (v Value) MapRange() *MapIter
func (v Value) Method(i int) Value
func (v Value) MethodByName(name string) Value
func (v Value) NumField() int
func (v Value) NumMethod() int
func (v Value) OverflowComplex(x complex128) bool
func (v Value) OverflowFloat(x float64) bool
func (v Value) OverflowInt(x int64) bool
func (v Value) OverflowUint(x uint64) bool
func (v Value) Pointer() uintptr
func (v Value) Recv() (x Value, ok bool)
func (v Value) Send(x Value)
func (v Value) Set(x Value)
func (v Value) SetBool(x bool)
func (v Value) SetBytes(x []byte)
func (v Value) SetCap(n int)
func (v Value) SetComplex(x complex128)
func (v Value) SetFloat(x float64)
func (v Value) SetInt(x int64)
func (v Value) SetIterKey(iter *MapIter)
func (v Value) SetIterValue(iter *MapIter)
func (v Value) SetLen(n int)
func (v Value) SetMapIndex(key, elem Value)
func (v Value) SetPointer(x unsafe.Pointer)
func (v Value) SetString(x string)
func (v Value) SetUint(x uint64)
func (v Value) SetZero()
func (v Value) Slice(i, j int) Value
func (v Value) Slice3(i, j, k int) Value
func (v Value) String() string
func (v Value) TryRecv() (x Value, ok bool)
func (v Value) TrySend(x Value) bool
func (v Value) Type() Type
func (v Value) Uint() uint64
func (v Value) UnsafeAddr() uintptr
func (v Value) UnsafePointer() unsafe.Pointer
type ValueError
func (e *ValueError) Error() string
""",
    "separator": "// Please create a very short program which combines reflect with other go features in a complex way",
    "begin": 'package main\nimport (\n\t"reflect"\n)\n',
    "target_api": "reflect",
}
go_big_math = {
    "docstring": """
Overview ¶
Package big implements arbitrary-precision arithmetic (big numbers). The following numeric types are supported:

Int    signed integers
Rat    rational numbers
Float  floating-point numbers
The zero value for an Int, Rat, or Float correspond to 0. Thus, new values can be declared in the usual ways and denote 0 without further initialization:

var x Int        // &x is an *Int of value 0
var r = &Rat{}   // r is a *Rat of value 0
y := new(Float)  // y is a *Float of value 0
Alternatively, new values can be allocated and initialized with factory functions of the form:

func NewT(v V) *T
For instance, NewInt(x) returns an *Int set to the value of the int64 argument x, NewRat(a, b) returns a *Rat set to the fraction a/b where a and b are int64 values, and NewFloat(f) returns a *Float initialized to the float64 argument f. More flexibility is provided with explicit setters, for instance:

var z1 Int
z1.SetUint64(123)                 // z1 := 123
z2 := new(Rat).SetFloat64(1.25)   // z2 := 5/4
z3 := new(Float).SetInt(z1)       // z3 := 123.0
Setters, numeric operations and predicates are represented as methods of the form:

func (z *T) SetV(v V) *T          // z = v
func (z *T) Unary(x *T) *T        // z = unary x
func (z *T) Binary(x, y *T) *T    // z = x binary y
func (x *T) Pred() P              // p = pred(x)
with T one of Int, Rat, or Float. For unary and binary operations, the result is the receiver (usually named z in that case; see below); if it is one of the operands x or y it may be safely overwritten (and its memory reused).

Arithmetic expressions are typically written as a sequence of individual method calls, with each call corresponding to an operation. The receiver denotes the result and the method arguments are the operation's operands. For instance, given three *Int values a, b and c, the invocation

c.Add(a, b)
computes the sum a + b and stores the result in c, overwriting whatever value was held in c before. Unless specified otherwise, operations permit aliasing of parameters, so it is perfectly ok to write

sum.Add(sum, x)
to accumulate values x in a sum.

(By always passing in a result value via the receiver, memory use can be much better controlled. Instead of having to allocate new memory for each result, an operation can reuse the space allocated for the result value, and overwrite that value with the new result in the process.)

Notational convention: Incoming method parameters (including the receiver) are named consistently in the API to clarify their use. Incoming operands are usually named x, y, a, b, and so on, but never z. A parameter specifying the result is named z (typically the receiver).

For instance, the arguments for (*Int).Add are named x and y, and because the receiver specifies the result destination, it is called z:

func (z *Int) Add(x, y *Int) *Int
Methods of this form typically return the incoming receiver as well, to enable simple call chaining.

Methods which don't require a result value to be passed in (for instance, Int.Sign), simply return the result. In this case, the receiver is typically the first operand, named x:

func (x *Int) Sign() int
Various methods support conversions between strings and corresponding numeric values, and vice versa: *Int, *Rat, and *Float values implement the Stringer interface for a (default) string representation of the value, but also provide SetString methods to initialize a value from a string in a variety of supported formats (see the respective SetString documentation).

Finally, *Int, *Rat, and *Float satisfy the fmt package's Scanner interface for scanning and (except for *Rat) the Formatter interface for formatted printing.

Example (EConvergents) ¶
Example (Fibonacci) ¶
Example (Sqrt2) ¶
Index ¶
Constants
func Jacobi(x, y *Int) int
type Accuracy
func (i Accuracy) String() string
type ErrNaN
func (err ErrNaN) Error() string
type Float
func NewFloat(x float64) *Float
func ParseFloat(s string, base int, prec uint, mode RoundingMode) (f *Float, b int, err error)
func (z *Float) Abs(x *Float) *Float
func (x *Float) Acc() Accuracy
func (z *Float) Add(x, y *Float) *Float
func (x *Float) Append(buf []byte, fmt byte, prec int) []byte
func (x *Float) Cmp(y *Float) int
func (z *Float) Copy(x *Float) *Float
func (x *Float) Float32() (float32, Accuracy)
func (x *Float) Float64() (float64, Accuracy)
func (x *Float) Format(s fmt.State, format rune)
func (z *Float) GobDecode(buf []byte) error
func (x *Float) GobEncode() ([]byte, error)
func (x *Float) Int(z *Int) (*Int, Accuracy)
func (x *Float) Int64() (int64, Accuracy)
func (x *Float) IsInf() bool
func (x *Float) IsInt() bool
func (x *Float) MantExp(mant *Float) (exp int)
func (x *Float) MarshalText() (text []byte, err error)
func (x *Float) MinPrec() uint
func (x *Float) Mode() RoundingMode
func (z *Float) Mul(x, y *Float) *Float
func (z *Float) Neg(x *Float) *Float
func (z *Float) Parse(s string, base int) (f *Float, b int, err error)
func (x *Float) Prec() uint
func (z *Float) Quo(x, y *Float) *Float
func (x *Float) Rat(z *Rat) (*Rat, Accuracy)
func (z *Float) Scan(s fmt.ScanState, ch rune) error
func (z *Float) Set(x *Float) *Float
func (z *Float) SetFloat64(x float64) *Float
func (z *Float) SetInf(signbit bool) *Float
func (z *Float) SetInt(x *Int) *Float
func (z *Float) SetInt64(x int64) *Float
func (z *Float) SetMantExp(mant *Float, exp int) *Float
func (z *Float) SetMode(mode RoundingMode) *Float
func (z *Float) SetPrec(prec uint) *Float
func (z *Float) SetRat(x *Rat) *Float
func (z *Float) SetString(s string) (*Float, bool)
func (z *Float) SetUint64(x uint64) *Float
func (x *Float) Sign() int
func (x *Float) Signbit() bool
func (z *Float) Sqrt(x *Float) *Float
func (x *Float) String() string
func (z *Float) Sub(x, y *Float) *Float
func (x *Float) Text(format byte, prec int) string
func (x *Float) Uint64() (uint64, Accuracy)
func (z *Float) UnmarshalText(text []byte) error
type Int
func NewInt(x int64) *Int
func (z *Int) Abs(x *Int) *Int
func (z *Int) Add(x, y *Int) *Int
func (z *Int) And(x, y *Int) *Int
func (z *Int) AndNot(x, y *Int) *Int
func (x *Int) Append(buf []byte, base int) []byte
func (z *Int) Binomial(n, k int64) *Int
func (x *Int) Bit(i int) uint
func (x *Int) BitLen() int
func (x *Int) Bits() []Word
func (x *Int) Bytes() []byte
func (x *Int) Cmp(y *Int) (r int)
func (x *Int) CmpAbs(y *Int) int
func (z *Int) Div(x, y *Int) *Int
func (z *Int) DivMod(x, y, m *Int) (*Int, *Int)
func (z *Int) Exp(x, y, m *Int) *Int
func (x *Int) FillBytes(buf []byte) []byte
func (x *Int) Format(s fmt.State, ch rune)
func (z *Int) GCD(x, y, a, b *Int) *Int
func (z *Int) GobDecode(buf []byte) error
func (x *Int) GobEncode() ([]byte, error)
func (x *Int) Int64() int64
func (x *Int) IsInt64() bool
func (x *Int) IsUint64() bool
func (z *Int) Lsh(x *Int, n uint) *Int
func (x *Int) MarshalJSON() ([]byte, error)
func (x *Int) MarshalText() (text []byte, err error)
func (z *Int) Mod(x, y *Int) *Int
func (z *Int) ModInverse(g, n *Int) *Int
func (z *Int) ModSqrt(x, p *Int) *Int
func (z *Int) Mul(x, y *Int) *Int
func (z *Int) MulRange(a, b int64) *Int
func (z *Int) Neg(x *Int) *Int
func (z *Int) Not(x *Int) *Int
func (z *Int) Or(x, y *Int) *Int
func (x *Int) ProbablyPrime(n int) bool
func (z *Int) Quo(x, y *Int) *Int
func (z *Int) QuoRem(x, y, r *Int) (*Int, *Int)
func (z *Int) Rand(rnd *rand.Rand, n *Int) *Int
func (z *Int) Rem(x, y *Int) *Int
func (z *Int) Rsh(x *Int, n uint) *Int
func (z *Int) Scan(s fmt.ScanState, ch rune) error
func (z *Int) Set(x *Int) *Int
func (z *Int) SetBit(x *Int, i int, b uint) *Int
func (z *Int) SetBits(abs []Word) *Int
func (z *Int) SetBytes(buf []byte) *Int
func (z *Int) SetInt64(x int64) *Int
func (z *Int) SetString(s string, base int) (*Int, bool)
func (z *Int) SetUint64(x uint64) *Int
func (x *Int) Sign() int
func (z *Int) Sqrt(x *Int) *Int
func (x *Int) String() string
func (z *Int) Sub(x, y *Int) *Int
func (x *Int) Text(base int) string
func (x *Int) TrailingZeroBits() uint
func (x *Int) Uint64() uint64
func (z *Int) UnmarshalJSON(text []byte) error
func (z *Int) UnmarshalText(text []byte) error
func (z *Int) Xor(x, y *Int) *Int
type Rat
func NewRat(a, b int64) *Rat
func (z *Rat) Abs(x *Rat) *Rat
func (z *Rat) Add(x, y *Rat) *Rat
func (x *Rat) Cmp(y *Rat) int
func (x *Rat) Denom() *Int
func (x *Rat) Float32() (f float32, exact bool)
func (x *Rat) Float64() (f float64, exact bool)
func (x *Rat) FloatString(prec int) string
func (z *Rat) GobDecode(buf []byte) error
func (x *Rat) GobEncode() ([]byte, error)
func (z *Rat) Inv(x *Rat) *Rat
func (x *Rat) IsInt() bool
func (x *Rat) MarshalText() (text []byte, err error)
func (z *Rat) Mul(x, y *Rat) *Rat
func (z *Rat) Neg(x *Rat) *Rat
func (x *Rat) Num() *Int
func (z *Rat) Quo(x, y *Rat) *Rat
func (x *Rat) RatString() string
func (z *Rat) Scan(s fmt.ScanState, ch rune) error
func (z *Rat) Set(x *Rat) *Rat
func (z *Rat) SetFloat64(f float64) *Rat
func (z *Rat) SetFrac(a, b *Int) *Rat
func (z *Rat) SetFrac64(a, b int64) *Rat
func (z *Rat) SetInt(x *Int) *Rat
func (z *Rat) SetInt64(x int64) *Rat
func (z *Rat) SetString(s string) (*Rat, bool)
func (z *Rat) SetUint64(x uint64) *Rat
func (x *Rat) Sign() int
func (x *Rat) String() string
func (z *Rat) Sub(x, y *Rat) *Rat
func (z *Rat) UnmarshalText(text []byte) error
type RoundingMode
func (i RoundingMode) String() string
type Word
""",
    "separator": "// Please create a very short program which combines big math with other go features in a complex way",
    "begin": 'package main\nimport (\n\t"math/big"\n)\n',
    "target_api": "big",
}

go_heap = {
    "docstring": """
Overview ¶
Package heap provides heap operations for any type that implements heap.Interface. A heap is a tree with the property that each node is the minimum-valued node in its subtree.

The minimum element in the tree is the root, at index 0.

A heap is a common way to implement a priority queue. To build a priority queue, implement the Heap interface with the (negative) priority as the ordering for the Less method, so Push adds items while Pop removes the highest-priority item from the queue. The Examples include such an implementation; the file example_pq_test.go has the complete source.

Index ¶
func Fix(h Interface, i int)
func Init(h Interface)
func Pop(h Interface) any
func Push(h Interface, x any)
func Remove(h Interface, i int) any
type Interface
Examples ¶
Package (IntHeap)
Package (PriorityQueue)
Constants ¶
This section is empty.

Variables ¶
This section is empty.

Functions ¶
func Fix ¶
added in go1.2
func Fix(h Interface, i int)
Fix re-establishes the heap ordering after the element at index i has changed its value. Changing the value of the element at index i and then calling Fix is equivalent to, but less expensive than, calling Remove(h, i) followed by a Push of the new value. The complexity is O(log n) where n = h.Len().

func Init ¶
func Init(h Interface)
Init establishes the heap invariants required by the other routines in this package. Init is idempotent with respect to the heap invariants and may be called whenever the heap invariants may have been invalidated. The complexity is O(n) where n = h.Len().

func Pop ¶
func Pop(h Interface) any
Pop removes and returns the minimum element (according to Less) from the heap. The complexity is O(log n) where n = h.Len(). Pop is equivalent to Remove(h, 0).

func Push ¶
func Push(h Interface, x any)
Push pushes the element x onto the heap. The complexity is O(log n) where n = h.Len().

func Remove ¶
func Remove(h Interface, i int) any
Remove removes and returns the element at index i from the heap. The complexity is O(log n) where n = h.Len().

Types ¶
type Interface ¶
type Interface interface {
	sort.Interface
	Push(x any) // add x as element Len()
	Pop() any   // remove and return element Len() - 1.
}
The Interface type describes the requirements for a type using the routines in this package. Any type that implements it may be used as a min-heap with the following invariants (established after Init has been called or if the data is empty or sorted):

!h.Less(j, i) for 0 <= i < h.Len() and 2*i+1 <= j <= 2*i+2 and j < h.Len()
Note that Push and Pop in this interface are for package heap's implementation to call. To add and remove things from the heap, use heap.Push and heap.Pop.
""",
    "separator": "// Please create a very short program which combines heap with other go features in a complex way",
    "begin": 'package main\nimport (\n\t"container/heap"\n)\n',
    "target_api": "heap",
}
