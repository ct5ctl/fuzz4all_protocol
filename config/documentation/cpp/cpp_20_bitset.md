std::bitset
 C++ Utilities library std::bitset 
Defined in header <bitset>
template<
    std::size_t N
> class bitset;
The class template bitset represents a fixed-size sequence of N bits. Bitsets can be manipulated by standard logic operators and converted to and from strings and integers. For the purpose of the string representation and of naming directions for shift operations, the sequence is thought of as having its lowest indexed elements at the right, as in the binary representation of integers.

bitset meets the requirements of CopyConstructible and CopyAssignable.

All member functions of std::bitset are constexpr: it is possible to create and use std::bitset objects in the evaluation of a constant expression.

(since C++23)
Template parameters
N	-	the number of bits to allocate storage for
Member types
reference
 
proxy class representing a reference to a bit
(class)
Member functions
(constructor)
 
constructs the bitset
(public member function)
operator==
operator!=
  
(removed in C++20)
 
compares the contents
(public member function)
Element access
operator[]
 
accesses specific bit
(public member function)
test
 
accesses specific bit
(public member function)
all
any
none
 
checks if all, any or none of the bits are set to true
(public member function)
count
 
returns the number of bits set to true
(public member function)
Capacity
size
 
returns the number of bits that the bitset holds
(public member function)
Modifiers
operator&=
operator|=
operator^=
operator~
 
performs binary AND, OR, XOR and NOT
(public member function)
operator<<=
operator>>=
operator<<
operator>>
 
performs binary shift left and shift right
(public member function)
set
 
sets bits to true or given value
(public member function)
reset
 
sets bits to false
(public member function)
flip
 
toggles the values of bits
(public member function)
Conversions
to_string
 
returns a string representation of the data
(public member function)
to_ulong
 
returns an unsigned long integer representation of the data
(public member function)
to_ullong
  
(C++11)
 
returns an unsigned long long integer representation of the data
(public member function)
Non-member functions
operator&
operator|
operator^
 
performs binary logic operations on bitsets
(function template)
operator<<
operator>>
 
performs stream input and output of bitsets
(function template)
Helper classes
std::hash<std::bitset>
  
(C++11)
 
hash support for std::bitset
(class template specialization)
