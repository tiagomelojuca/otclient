### ESSENTIAL RULES THAT MUST BE FOLLOWED
Before implementing anything, you must REALLY follow the next 8 code rules. They are coding techniques that changes the way you will implement anything. There is a logical reason behind each one.

* Avoid pointers at all costs, use only when really needed like for C strings (char*), avoid even for buffers of ints.
* If you need a buffer, use std::vector.
* Never use pointers for objects, if you think you need so I'm sure you can either use std::shared_ptr or pass the object by reference.
* Never use **delete** keyword, and when I say never, I mean NEVER. If you think you need to use delete you didn't read the previous two rules.
* Pass small objects like Position, Rect, std::string, by reference.
* Include only declarations from other objects in headers files, never definitions, you can see the declarations.h pattern in the source.
* If you think anything can go wrong on your code, you can use **assert** or throw an exception for checking.
* C++0x comes with a varieties of new utilities, you can and you are encouraged to use them.

### Indentation
* 4 spaces are used for indentation
* Spaces, not tabs!

### Declaring variables
* Variables/functions start with a small letter and each consecutive word starts with a capital letter.
* Avoid short names and abbreviations whenever possible. Use readable names.

```cpp
    int a; // Wrong
    int whorisize; // Wrong
    int hsize; // Wrong
    int windowHSize; // Wrong
    int windowHorizontalSize; // Correct
```

* Single character variable names are only suitable for counter variables, where the purpose of the variable is obvious.
* Classes always start with a uppercase character.
* Class members variables always begin with m_ followed by a name starting with a lower case character.

```cpp
    class DummyClass
    {
        int mVariable; // Wrong
        int m_Variable; // Wrong
        int m_variable; // Correct
    };
```

* Struct member variables must not begin with m_, avoid structs and use only when it feels right.
* Global variables begins with g_
* Use bultin int types:

```cpp
    uint32_t var; // Wrong
    uint32 var; // Correct

    unsigned long var; // Wrong
    ulong var; // Correct
```

### Singletons
* Use the following style to declare singletons:

```cpp
    // on game.cpp top
    Game g_game;
    // on game.h bottom
    class Game { ... };
    extern Game g_game;
```

### Loops and iterators
* Use **auto** keyword on every iterator:

```cpp
    std::map<int, std::string>::iterator it = myMap.begin(); // Wrong
    auto it = myMap.begin(); // Correct

    for(std::map<int, std::string>::iterator it = myMap.begin(); it != myMap.end(); it++) // Wrong
    for(auto it = myMap.begin(); it != myMap.end(); ++it) // Correct
    or
    for(auto pair : myMap) // Correct
```

* Use C++0x for each when you can:

```cpp
    for(auto it = files.begin(); it != files.end(); ++it) { } // Wrong
    for(const std::string& file : files) { } // Correct
```

### Sources files
* If you need any STL header use global.h, avoid flooding includes.
* All sources files must have the license and copyright notice on top.
* Only include needed headers.
* Whenever is possible, forward declare classes names instead of including it's headers.

```cpp
    // Wrong
    #include "foo.h"
    class Dummy {
        Foo *m_foo;
    };

    // Correct
    class Foo;
    class Dummy {
        Foo *m_foo;
    };
```

### Classes
* When using **new** keyword place brackets only when needed:

```cpp
    new DummyClass(); // Wrong
    new DummyClass; // Correct
```

* Avoid empty constructors in sources files.
* Declare destructors only when needed.
* Get methods must have **const** keyword.

### Documentation
* Comment anything that you feel relevant.
* Document functions on headers using /// to enable doxygen output.

### Algorithms
* Use high level classes like Rect, Point, std::string whenever is possible.
* Use high level APIs, e.g. for strings boost algorithm is there.
* Make algorithms readable and organized.
* Comment complex ones.

### Pointers and memory
* Avoid to use **delete** keyword or manage memory on you own, always prefer smart pointers.
* Prefer to forward complex objects variables by reference and using **const** keyword.
