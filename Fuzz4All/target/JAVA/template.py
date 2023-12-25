java_concurrent = {
    "docstring": """
Package java.util.concurrent
package java.util.concurrent
Utility classes commonly useful in concurrent programming. This package includes a few small standardized extensible frameworks, as well as some classes that provide useful functionality and are otherwise tedious or difficult to implement. Here are brief descriptions of the main components. See also the java.util.concurrent.locks and java.util.concurrent.atomic packages.
Executors
Interfaces. Executor is a simple standardized interface for defining custom thread-like subsystems, including thread pools, asynchronous I/O, and lightweight task frameworks. Depending on which concrete Executor class is being used, tasks may execute in a newly created thread, an existing task-execution thread, or the thread calling execute, and may execute sequentially or concurrently. ExecutorService provides a more complete asynchronous task execution framework. An ExecutorService manages queuing and scheduling of tasks, and allows controlled shutdown. The ScheduledExecutorService subinterface and associated interfaces add support for delayed and periodic task execution. ExecutorServices provide methods arranging asynchronous execution of any function expressed as Callable, the result-bearing analog of Runnable. A Future returns the results of a function, allows determination of whether execution has completed, and provides a means to cancel execution. A RunnableFuture is a Future that possesses a run method that upon execution, sets its results.
Implementations. Classes ThreadPoolExecutor and ScheduledThreadPoolExecutor provide tunable, flexible thread pools. The Executors class provides factory methods for the most common kinds and configurations of Executors, as well as a few utility methods for using them. Other utilities based on Executors include the concrete class FutureTask providing a common extensible implementation of Futures, and ExecutorCompletionService, that assists in coordinating the processing of groups of asynchronous tasks.

Class ForkJoinPool provides an Executor primarily designed for processing instances of ForkJoinTask and its subclasses. These classes employ a work-stealing scheduler that attains high throughput for tasks conforming to restrictions that often hold in computation-intensive parallel processing.

Queues
The ConcurrentLinkedQueue class supplies an efficient scalable thread-safe non-blocking FIFO queue. The ConcurrentLinkedDeque class is similar, but additionally supports the Deque interface.
Five implementations in java.util.concurrent support the extended BlockingQueue interface, that defines blocking versions of put and take: LinkedBlockingQueue, ArrayBlockingQueue, SynchronousQueue, PriorityBlockingQueue, and DelayQueue. The different classes cover the most common usage contexts for producer-consumer, messaging, parallel tasking, and related concurrent designs.

Extended interface TransferQueue, and implementation LinkedTransferQueue introduce a synchronous transfer method (along with related features) in which a producer may optionally block awaiting its consumer.

The BlockingDeque interface extends BlockingQueue to support both FIFO and LIFO (stack-based) operations. Class LinkedBlockingDeque provides an implementation.

Timing
The TimeUnit class provides multiple granularities (including nanoseconds) for specifying and controlling time-out based operations. Most classes in the package contain operations based on time-outs in addition to indefinite waits. In all cases that time-outs are used, the time-out specifies the minimum time that the method should wait before indicating that it timed-out. Implementations make a "best effort" to detect time-outs as soon as possible after they occur. However, an indefinite amount of time may elapse between a time-out being detected and a thread actually executing again after that time-out. All methods that accept timeout parameters treat values less than or equal to zero to mean not to wait at all. To wait "forever", you can use a value of Long.MAX_VALUE.
Synchronizers
Five classes aid common special-purpose synchronization idioms.
Semaphore is a classic concurrency tool.
CountDownLatch is a very simple yet very common utility for blocking until a given number of signals, events, or conditions hold.
A CyclicBarrier is a resettable multiway synchronization point useful in some styles of parallel programming.
A Phaser provides a more flexible form of barrier that may be used to control phased computation among multiple threads.
An Exchanger allows two threads to exchange objects at a rendezvous point, and is useful in several pipeline designs.
Concurrent Collections
Besides Queues, this package supplies Collection implementations designed for use in multithreaded contexts: ConcurrentHashMap, ConcurrentSkipListMap, ConcurrentSkipListSet, CopyOnWriteArrayList, and CopyOnWriteArraySet. When many threads are expected to access a given collection, a ConcurrentHashMap is normally preferable to a synchronized HashMap, and a ConcurrentSkipListMap is normally preferable to a synchronized TreeMap. A CopyOnWriteArrayList is preferable to a synchronized ArrayList when the expected number of reads and traversals greatly outnumber the number of updates to a list.
The "Concurrent" prefix used with some classes in this package is a shorthand indicating several differences from similar "synchronized" classes. For example java.util.Hashtable and Collections.synchronizedMap(new HashMap()) are synchronized. But ConcurrentHashMap is "concurrent". A concurrent collection is thread-safe, but not governed by a single exclusion lock. In the particular case of ConcurrentHashMap, it safely permits any number of concurrent reads as well as a large number of concurrent writes. "Synchronized" classes can be useful when you need to prevent all access to a collection via a single lock, at the expense of poorer scalability. In other cases in which multiple threads are expected to access a common collection, "concurrent" versions are normally preferable. And unsynchronized collections are preferable when either collections are unshared, or are accessible only when holding other locks.

Most concurrent Collection implementations (including most Queues) also differ from the usual java.util conventions in that their Iterators and Spliterators provide weakly consistent rather than fast-fail traversal:

they may proceed concurrently with other operations
they will never throw ConcurrentModificationException
they are guaranteed to traverse elements as they existed upon construction exactly once, and may (but are not guaranteed to) reflect any modifications subsequent to construction.
Memory Consistency Properties
Chapter 17 of The Java Language Specification defines the happens-before relation on memory operations such as reads and writes of shared variables. The results of a write by one thread are guaranteed to be visible to a read by another thread only if the write operation happens-before the read operation. The synchronized and volatile constructs, as well as the Thread.start() and Thread.join() methods, can form happens-before relationships. In particular:
Each action in a thread happens-before every action in that thread that comes later in the program's order.
An unlock (synchronized block or method exit) of a monitor happens-before every subsequent lock (synchronized block or method entry) of that same monitor. And because the happens-before relation is transitive, all actions of a thread prior to unlocking happen-before all actions subsequent to any thread locking that monitor.
A write to a volatile field happens-before every subsequent read of that same field. Writes and reads of volatile fields have similar memory consistency effects as entering and exiting monitors, but do not entail mutual exclusion locking.
A call to start on a thread happens-before any action in the started thread.
All actions in a thread happen-before any other thread successfully returns from a join on that thread.
The methods of all classes in java.util.concurrent and its subpackages extend these guarantees to higher-level synchronization. In particular:
Actions in a thread prior to placing an object into any concurrent collection happen-before actions subsequent to the access or removal of that element from the collection in another thread.
Actions in a thread prior to the submission of a Runnable to an Executor happen-before its execution begins. Similarly for Callables submitted to an ExecutorService.
Actions taken by the asynchronous computation represented by a Future happen-before actions subsequent to the retrieval of the result via Future.get() in another thread.
Actions prior to "releasing" synchronizer methods such as Lock.unlock, Semaphore.release, and CountDownLatch.countDown happen-before actions subsequent to a successful "acquiring" method such as Lock.lock, Semaphore.acquire, Condition.await, and CountDownLatch.await on the same synchronizer object in another thread.
For each pair of threads that successfully exchange objects via an Exchanger, actions prior to the exchange() in each thread happen-before those subsequent to the corresponding exchange() in another thread.
Actions prior to calling CyclicBarrier.await and Phaser.awaitAdvance (as well as its variants) happen-before actions performed by the barrier action, and actions performed by the barrier action happen-before actions subsequent to a successful return from the corresponding await in other threads.
""",
    "separator": "/* Please create a very short program which combines java.util.concurrent with new Java features in a complex way */",
    "begin": "import java.util.concurrent.*;",
    "target_api": "",
}

java_std = {
    "docstring": """
Java® Platform, Standard Edition & Java Development Kit
Version 20 API Specification
This document is divided into two sections:

Java SE
The Java Platform, Standard Edition (Java SE) APIs define the core Java platform for general-purpose computing. These APIs are in modules whose names start with java.
JDK
The Java Development Kit (JDK) APIs are specific to the JDK and will not necessarily be available in all implementations of the Java SE Platform. These APIs are in modules whose names start with jdk.
All ModulesJava SEJDKOther Modules
Module
Description
java.base
Defines the foundational APIs of the Java SE Platform.
java.compiler
Defines the Language Model, Annotation Processing, and Java Compiler APIs.
java.datatransfer
Defines the API for transferring data between and within applications.
java.desktop
Defines the AWT and Swing user interface toolkits, plus APIs for accessibility, audio, imaging, printing, and JavaBeans.
java.instrument
Defines services that allow agents to instrument programs running on the JVM.
java.logging
Defines the Java Logging API.
java.management
Defines the Java Management Extensions (JMX) API.
java.management.rmi
Defines the RMI connector for the Java Management Extensions (JMX) Remote API.
java.naming
Defines the Java Naming and Directory Interface (JNDI) API.
java.net.http
Defines the HTTP Client and WebSocket APIs.
java.prefs
Defines the Preferences API.
java.rmi
Defines the Remote Method Invocation (RMI) API.
java.scripting
Defines the Scripting API.
java.se
Defines the API of the Java SE Platform.
java.security.jgss
Defines the Java binding of the IETF Generic Security Services API (GSS-API).
java.security.sasl
Defines Java support for the IETF Simple Authentication and Security Layer (SASL).
java.smartcardio
Defines the Java Smart Card I/O API.
java.sql
Defines the JDBC API.
java.sql.rowset
Defines the JDBC RowSet API.
java.transaction.xa
Defines an API for supporting distributed transactions in JDBC.
java.xml
Defines the Java API for XML Processing (JAXP), the Streaming API for XML (StAX), the Simple API for XML (SAX), and the W3C Document Object Model (DOM) API.
java.xml.crypto
Defines the API for XML cryptography.
jdk.accessibility
Defines JDK utility classes used by implementors of Assistive Technologies.
jdk.attach
Defines the attach API.
jdk.charsets
Provides charsets that are not in java.base (mostly double byte and IBM charsets).
jdk.compiler
Defines the implementation of the system Java compiler and its command line equivalent, javac.
jdk.crypto.cryptoki
Provides the implementation of the SunPKCS11 security provider.
jdk.crypto.ec
Provides the implementation of the SunEC security provider.
jdk.dynalink
Defines the API for dynamic linking of high-level operations on objects.
jdk.editpad
Provides the implementation of the edit pad service used by jdk.jshell.
jdk.hotspot.agent
Defines the implementation of the HotSpot Serviceability Agent.
jdk.httpserver
Defines the JDK-specific HTTP server API, and provides the jwebserver tool for running a minimal HTTP server.
jdk.incubator.concurrent
Defines non-final APIs for concurrent programming.
jdk.incubator.vector
Defines an API for expressing computations that can be reliably compiled at runtime into SIMD instructions, such as AVX instructions on x64, and NEON instructions on AArch64.
jdk.jartool
Defines tools for manipulating Java Archive (JAR) files, including the jar and jarsigner tools.
jdk.javadoc
Defines the implementation of the system documentation tool and its command-line equivalent, javadoc.
jdk.jcmd
Defines tools for diagnostics and troubleshooting a JVM such as the jcmd, jps, jstat tools.
jdk.jconsole
Defines the JMX graphical tool, jconsole, for monitoring and managing a running application.
jdk.jdeps
Defines tools for analysing dependencies in Java libraries and programs, including the jdeps, javap, and jdeprscan tools.
jdk.jdi
Defines the Java Debug Interface.
jdk.jdwp.agent
Provides the implementation of the Java Debug Wire Protocol (JDWP) agent.
jdk.jfr
Defines the API for JDK Flight Recorder.
jdk.jlink
Defines the jlink tool for creating run-time images, the jmod tool for creating and manipulating JMOD files, and the jimage tool for inspecting the JDK implementation-specific container file for classes and resources.
jdk.jpackage
Defines the Java Packaging tool, jpackage.
jdk.jshell
Provides the jshell tool for evaluating snippets of Java code, and defines a JDK-specific API for modeling and executing snippets.
jdk.jsobject
Defines the API for the JavaScript Object.
jdk.jstatd
Defines the jstatd tool for starting a daemon for the jstat tool to monitor JVM statistics remotely.
jdk.localedata
Provides the locale data for locales other than US locale.
jdk.management
Defines JDK-specific management interfaces for the JVM.
jdk.management.agent
Defines the JMX management agent.
jdk.management.jfr
Defines the Management Interface for JDK Flight Recorder.
jdk.naming.dns
Provides the implementation of the DNS Java Naming provider.
jdk.naming.rmi
Provides the implementation of the RMI Java Naming provider.
jdk.net
Defines the JDK-specific Networking API.
jdk.nio.mapmode
Defines JDK-specific file mapping modes.
jdk.sctp
Defines the JDK-specific API for SCTP.
jdk.security.auth
Provides implementations of the javax.security.auth.* interfaces and various authentication modules.
jdk.security.jgss
Defines JDK extensions to the GSS-API and an implementation of the SASL GSSAPI mechanism.
jdk.xml.dom
Defines the subset of the W3C Document Object Model (DOM) API that is not part of the Java SE API.
jdk.zipfs
Provides the implementation of the Zip file system provider.
""",
    "separator": "/* Please create a very short program which combines Java features in a complex way */",
    "begin": "import java.lang.Object;",
    "target_api": "",
}

java_text = {
    "docstring": """
package java.text
Provides classes and interfaces for handling text, dates, numbers, and messages in a manner independent of natural languages. This means your main application or applet can be written to be language-independent, and it can rely upon separate, dynamically-linked localized resources. This allows the flexibility of adding localizations for new localizations at any time.
These classes are capable of formatting dates, numbers, and messages, parsing; searching and sorting strings; and iterating over characters, words, sentences, and line breaks. This package contains three main groups of classes and interfaces:

Classes for iteration over text
Classes for formatting and parsing
Classes for string collation
Since:
1.1
Related Packages
Package
Description
java.text.spi
Service provider classes for the classes in the java.text package.
All Classes and InterfacesInterfacesClassesEnum ClassesException Classes
Class
Description
Annotation
An Annotation object is used as a wrapper for a text attribute value if the attribute has annotation characteristics.
AttributedCharacterIterator
An AttributedCharacterIterator allows iteration through both text and related attribute information.
AttributedCharacterIterator.Attribute
Defines attribute keys that are used to identify text attributes.
AttributedString
An AttributedString holds text and related attribute information.
Bidi
This class implements the Unicode Bidirectional Algorithm.
BreakIterator
The BreakIterator class implements methods for finding the location of boundaries in text.
CharacterIterator
This interface defines a protocol for bidirectional iteration over text.
ChoiceFormat
A ChoiceFormat allows you to attach a format to a range of numbers.
CollationElementIterator
The CollationElementIterator class is used as an iterator to walk through each character of an international string.
CollationKey
A CollationKey represents a String under the rules of a specific Collator object.
Collator
The Collator class performs locale-sensitive String comparison.
CompactNumberFormat
CompactNumberFormat is a concrete subclass of NumberFormat that formats a decimal number in its compact form.
DateFormat
DateFormat is an abstract class for date/time formatting subclasses which formats and parses dates or time in a language-independent manner.
DateFormat.Field
Defines constants that are used as attribute keys in the AttributedCharacterIterator returned from DateFormat.formatToCharacterIterator and as field identifiers in FieldPosition.
DateFormatSymbols
DateFormatSymbols is a public class for encapsulating localizable date-time formatting data, such as the names of the months, the names of the days of the week, and the time zone data.
DecimalFormat
DecimalFormat is a concrete subclass of NumberFormat that formats decimal numbers.
DecimalFormatSymbols
This class represents the set of symbols (such as the decimal separator, the grouping separator, and so on) needed by DecimalFormat to format numbers.
FieldPosition
FieldPosition is a simple class used by Format and its subclasses to identify fields in formatted output.
Format
Format is an abstract base class for formatting locale-sensitive information such as dates, messages, and numbers.
Format.Field
Defines constants that are used as attribute keys in the AttributedCharacterIterator returned from Format.formatToCharacterIterator and as field identifiers in FieldPosition.
MessageFormat
MessageFormat provides a means to produce concatenated messages in a language-neutral way.
MessageFormat.Field
Defines constants that are used as attribute keys in the AttributedCharacterIterator returned from MessageFormat.formatToCharacterIterator.
Normalizer
This class provides the method normalize which transforms Unicode text into an equivalent composed or decomposed form, allowing for easier sorting and searching of text.
Normalizer.Form
This enum provides constants of the four Unicode normalization forms that are described in Unicode Standard Annex #15 — Unicode Normalization Forms and two methods to access them.
NumberFormat
NumberFormat is the abstract base class for all number formats.
NumberFormat.Field
Defines constants that are used as attribute keys in the AttributedCharacterIterator returned from NumberFormat.formatToCharacterIterator and as field identifiers in FieldPosition.
NumberFormat.Style
A number format style.
ParseException
Signals that an error has been reached unexpectedly while parsing.
ParsePosition
ParsePosition is a simple class used by Format and its subclasses to keep track of the current position during parsing.
RuleBasedCollator
The RuleBasedCollator class is a concrete subclass of Collator that provides a simple, data-driven, table collator.
SimpleDateFormat
SimpleDateFormat is a concrete class for formatting and parsing dates in a locale-sensitive manner.
StringCharacterIterator
StringCharacterIterator implements the CharacterIterator protocol for a String.
    """,
    "separator": "/* Please create a very short program which combines java.text with new Java features in a complex way */",
    "begin": "import java.text.*;",
    "target_api": "",
}
