Title: Javascript basics
Slug: javascript-basics
Date: 2013-01-15

In last couple days I realized that I feel very uncomfortable writing Javascript code. It might be a result of lack of knowledge how does language work, all the time I just used my C knowledge combined with Python experience. One evening I decided to learn very basics of Javascript and took notes.

### Data types:

* Number
* String
* Boolean
* Object
    * Function
    * Array
    * Date
    * RegExp
* Null
* Undefined
* Error

### Numbers

Numbers by specs are "double-precision 64-bit format IEEE 754 values", so there is no integers bt specs. But browsers' implementation of numbers can differ and can implement in simple 32-bit integer type.

Standard arithmetic operations are supported: +, -, *, /, %.

Most math operations are achived with built-in `Math` object.

To convert string to integer use `parseInt(str, base=2)`, to float use `parseFloat(str, base=10)`. Parsing bad string will give `NaN`. We can convert string prepending + sign, but it works in different way, so be carefull.

Anything combined with `NaN` is `NaN` and you can check for it using `isNaN(number)`.

Also JS has values `Infinity` and `-Infinity`. They are achiveable dividing by 0. Test for it using `isFinite(number)`.

### Strings
Strings are sequences of _unicode_ characters. To represent single char we use string of length 1.

And strings are objects as well. They have properties(`length`), methods(`replace(from, to)`, `charAt(pos)`).

### `null` vs `undefined`
`null` is an object of type `object` that indicates a deliberate non-value.
`undefined` is object of type `undefined` that indicates an uninitialized value.
### Boolean

* `false`, `0`, `""`, `NaN`, `null`, `undefined` give `false`
* everything else gives `true`

Convert to `Boolean` using `Boolean(var)`.

### Variables

Declare variable using `var` keyword. In JavaScript blocks do not have their scope. Only functions have their own scope.

#### `+` operator
Sums numbers and concatenates strings. Concatenates with string.

```javascript 
> "3" + 4 + 5
345
> 3 + 4 + "5"
75
```

#### Comparisons

```javascript 
> "dog" == "dog"
true
> 1 == true
true
```

To avoid type coercion, use the triple-equals operator:

```javascript 
> 1 === true
false
> true === true
true
```

There are also != and !== operators.

### Control Statements
`if`-`else`, `switch`-`case`, `for`-`while`-`do-while` work in the same way as in C.

### Objects
Objects are key-value pairs collections. Similar to `dict` in Python.

Create empty object:

```javascript 
var obj = new Object(); // or
var obj = {};
```

And there are two ways to access properties:

```javascript 
obj.name = 'Name';
obj['name'] = 'Name again';
```

Second way gives adventages for building property name in run-time or using reserved key-words as property name:

```javascript 
obj.for = "Simon"; // Syntax error, because 'for' is a reserved word
obj["for"] = "Simon"; // works fine
```

Object initialisation syntax:

```javascript 
var obj = {
    name: "Carrot",
    "for": "Max",
    details: {
        color: "orange",
        size: 12
    }
}
```

### Arrays
Arrays are a spectial type type of object.

```javascript 
// old way
var a = new Array();
a[0] = "dog";
a[1] = 23;
a[2] = "hen";
var len = a.length;

// convinient way
var a = ["dog", 23, "hen"];
a[100] = "FOX";
a.length == 101;
typeof a[90] == undefined;
```

Looks like a.length is inefficient and instead of:
    
```javascript 
for (var i = 0; i < a.length; i++) {
}
```

nicer is:

```javascript 
for (var i = 0, len = a.length; i < len; i++) {
}
```

Another way to iterate though all items is:
   
```javascript 
for (var i in a) {}
```

Some methods of arrays: `push(item[, itemN])`, `pop()`, `reverse()`, `shift()`, `join(sep)`, `toString()`, `concat(item[, itemN])`, `slice(start, end)`, `sort([compfn])`, `splice(start, delcount[, itemN])`, `unshift([item])`

### Functions
Function looks like this:

```javascript 
function add(x,y) {
    return x + y;
}
```

Call `add()` will be equivalent to `add(undefined, undefined)`

Call `add(1,2,3)` to `add(1,2)`, so 3 is ignored.

But function can access all arguments in `arguments` array passed to it.

```javascript 
function add() {
    var sum = 0;
    for (var i = 0, j = arguments.length; i < j; i++) {
        sum += arguments[i];
    }
    return sum;
}
 
> add(2, 3, 4, 5)
14
```

So function is an object, we can assign it to anything and use anonymous functions.

```javascript 
var fun = function(x, y) { return x + y; }
```

Make call of anonymous function:
    
```javascript 
(function(a, b) { return a + b; })();
```

### Custom objects
There is no `class` keyword, so people use bunch of different methods to create OO-classes. But simple classes are functions.

Used inside a function, `this` refers to the current object. What that actually means is specified by the way in which you called that function. If you called it using dot notation or bracket notation on an object, that object becomes `this`. If dot notation wasn't used for the call, `this` refers to the global object. This is a frequent cause of mistakes.

```javascript 
function Person(first, last) {
    this.first = first;
    this.last = last;
    this.fullName = function() {
        return this.first + ' ' + this.last;
    }
    this.fullNameReversed = function() {
        return this.last + ', ' + this.first;
    }
}
var s = new Person("Simon", "Willison");
```

`new` is strongly related to `this`. What it does is it creates a brand new empty object, and then calls the function specified, with `this` set to that new object. Functions that are designed to be called by `new` are called constructor functions. Common practise is to capitalise these functions as a reminder to call them with `new`.

Using function prototype:

```javascript 
function Person(first, last) {
    this.first = first;
    this.last = last;
}
Person.prototype.fullName = function() {
    return this.first + ' ' + this.last;
}
Person.prototype.fullNameReversed = function() {
    return this.last + ', ' + this.first;
}
```

It means using `prototype` we can change classes on runtime.

```javascript 
> String.prototype.reversed = function() {
    var r = "";
    for (var i = this.length - 1; i >= 0; i--) {
        r += this[i];
    }
    return r;
}
> "Simon".reversed()
nomiS
```

The prototype forms part of a chain. The root of that chain is Object.prototype, whose methods include toString() — it is this method that is called when you try to represent an object as a string. This is useful for debugging our Person objects:

```javascript 
> var s = new Person("Simon", "Willison");
> s
[object Object]
> Person.prototype.toString = function() {
    return '<Person: ' + this.fullName() + '>';
}
> s
<Person: Simon Willison>
```

### Inner functions
We can declare function inside function:

```javascript 
function first(x) {
    function second(y) {
        return x + y;
    }
    return second(17);
}
```

Inner functions share namespace of parent function.
### Closures

```javascript 
function makeAdder(a) {
    return function(b) {
        return a + b;
    }
}
x = makeAdder(5);
y = makeAdder(20);
x(6)
11
y(7)
27
```

Here's what's actually happening. Whenever JavaScript executes a function, a 'scope' object is created to hold the local variables created within that function. It is initialised with any variables passed in as function parameters. This is similar to the global object that all global variables and functions live in, but with a couple of important differences: firstly, a brand new scope object is created every time a function starts executing, and secondly, unlike the global object (which in browsers is accessible as window) these scope objects cannot be directly accessed from your JavaScript code. There is no mechanism for iterating over the properties of the current scope object for example.

So when makeAdder is called, a scope object is created with one property: a, which is the argument passed to the makeAdder function. makeAdder then returns a newly created function. Normally JavaScript's garbage collector would clean up the scope object created for makeAdder at this point, but the returned function maintains a reference back to that scope object. As a result, the scope object will not be garbage collected until there are no more references to the function object that makeAdder returned.

Scope objects form a chain called the scope chain, similar to the prototype chain used by JavaScript's object system.

A closure is the combination of a function and the scope object in which it was created.

Closures let you save state — as such, they can often be used in place of objects.
[Source][0] is the article on developers.mozilla.org

[0]: https://developer.mozilla.org/en-US/docs/JavaScript/A_re-introduction_to_JavaScript?redirectlocale=en-US&redirectslug=A_re-introduction_to_JavaScript

