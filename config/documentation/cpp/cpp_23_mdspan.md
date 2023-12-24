std::mdspan
 C++ Containers library std::mdspan 
Defined in header <mdspan>
template<
    class T,
    class Extents,
    class LayoutPolicy = std::layout_right,
    class AccessorPolicy = std::default_accessor<T>
> class mdspan;
(since C++23)
std::mdspan is a non-owning view into a contiguous sequence of objects that reinterprets it as a multidimensional array.

Each specialization MDS of mdspan models copyable and satisfies:

std::is_nothrow_move_constructible_v<MDS> is true,
std::is_nothrow_move_assignable_v<MDS> is true, and
std::is_nothrow_swappable_v<MDS> is true
A specialization of mdspan is a TriviallyCopyable type if its accessor_type, mapping_type and data_handle_type are TriviallyCopyable types.

Template parameters
T	-	element type; a complete object type that is neither an abstract class type nor an array type,
Extents	-	specifies number of dimensions, their sizes, and which are known at compile time. Must be a specialization of std::extents,
LayoutPolicy	-	specifies how to convert multidimensional index to underlying 1D index (column-major 3D array, symmetric triangular 2D matrix, etc).
AccessorPolicy	-	specifies how to convert underlying 1D index to a reference to T. Must satisfy the constraint that std::is_same_v<T, typename AccessorPolicy​::​element_type> is true.
This section is incomplete
Reason: add the requirement of layout policy and accessor policy.
Member types
Member type	Definition
extents_type	Extents
layout_type	LayoutPolicy
accessor_type	AccessorPolicy
mapping_type	LayoutPolicy::mapping<Extents>
element_type	T
value_type	std::remove_cv_t<T>
index_type	Extents::index_type
size_type	Extents::size_type
rank_type	Extents::rank_type
data_handle_type	AccessorPolicy::data_handle_type
reference	AccessorPolicy::reference
Data members
Typical implementations of mdspan hold only three non-static data member:

An accessor of type accessor_type (shown here as acc_ for exposition only).
A layout mapping of type mapping_type (shown here as map_ for exposition only).
A underlying data handle of type data_handle_type (shown here as ptr_ for exposition only).
Member functions
(constructor)
 
constructs an mdspan
(public member function)
operator=
 
assigns an mdspan
(public member function)
Element access
operator[]
 
accesses an element at the specified multidimensional index
(public member function)
Observers
size
 
returns the size of the multidimensional index space
(public member function)
empty
 
checks if the size of the index space is zero
(public member function)
stride
 
obtains the stride along the specified dimension
(public member function)
extents
 
obtains the extents object
(public member function)
data_handle
 
obtains the pointer to the underlying 1D sequence
(public member function)
mapping
 
obtains the mapping object
(public member function)
accessor
 
obtains the accessor policy object
(public member function)
is_unique
 
determines if this mdspan's mapping is unique (every combination of indexes maps to a different underlying element)
(public member function)
is_exhaustive
 
determines if this mdspan's mapping is exhaustive (every underlying element can be accessed with some combination of indexes)
(public member function)
is_strided
 
determines if this mdspan's mapping is strided (in each dimension, incrementing an index jumps over the same number of underlying elements every time)
(public member function)
is_always_unique
  
[static]
 
determines if this mdspan's layout mapping is always unique
(public static member function)
is_always_exhaustive
  
[static]
 
determines if this mdspan's layout mapping is always exhaustive
(public static member function)
is_always_strided
  
[static]
 
determines if this mdspan's layout mapping is always strided
(public static member function)
Non-member functions
std::swap(std::mdspan)
  
(C++23)
 
specializes the std::swap algorithm for mdspan
(function template)
Helper types and templates
extents
  
(C++23)
 
a descriptor of a multidimensional index space of some rank
(class template)
dextents
  
(C++23)
 
convenience alias for an all-dynamic std::extents
(class template)
layout_right
  
(C++23)
 
row-major multidimensional array layout mapping; rightmost extent has stride 1
(class)
layout_left
  
(C++23)
 
column-major multidimensional array layout mapping; leftmost extent has stride 1
(class)
layout_stride
  
(C++23)
 
a layout mapping with user-defined strides
(class)
default_accessor
  
(C++23)
 
a type for indexed access to elements of mdspan
(class template)