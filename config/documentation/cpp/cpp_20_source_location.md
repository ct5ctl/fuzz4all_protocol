std::source_location
 C++ Utilities library std::source_location 
Defined in header <source_location>
struct source_location;
(since C++20)
The std::source_location class represents certain information about the source code, such as file names, line numbers, and function names. Previously, functions that desire to obtain this information about the call site (for logging, testing, or debugging purposes) must use macros so that predefined macros like __LINE__ and __FILE__ are expanded in the context of the caller. The std::source_location class provides a better alternative.

std::source_location meets the DefaultConstructible, CopyConstructible, CopyAssignable and Destructible requirements. Lvalue of std::source_location meets the Swappable requirement.

Additionally, the following conditions are true:

std::is_nothrow_move_constructible_v<std::source_location>,
std::is_nothrow_move_assignable_v<std::source_location>, and
std::is_nothrow_swappable_v<std::source_location>.
It is intended that std::source_location has a small size and can be copied efficiently.

It is unspecified whether the copy/move constructors and the copy/move assignment operators of std::source_location are trivial and/or constexpr.

Member functions
Creation
(constructor)
 
constructs a new source_location with implementation-defined values
(public member function)
current
  
[static]
 
constructs a new source_location corresponding to the location of the call site
(public static member function)
Field access
line
 
return the line number represented by this object
(public member function)
column
 
return the column number represented by this object
(public member function)
file_name
 
return the file name represented by this object
(public member function)
function_name
 
return the name of the function represented by this object, if any
(public member function)
