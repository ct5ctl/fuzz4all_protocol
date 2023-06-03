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
