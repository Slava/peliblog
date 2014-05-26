Title: Callbacks, Promises, Generators and Fibers
Slug: solve-cb-hell
Date: 2014-04-27

![Promises](/images/promise.jpg)

The topic of the use of callbacks vs the use of promises has been rocking
through JavaScript community for several years now. Some people don't like
callbacks, other people think that promises are even worse and since generators
(a new feature of ES6) became available on Google Chrome and node.js (behind
experimental features flags) the battle became 3-sided: callbacks vs promises vs
promises via generators.

There is another approach to the "callbacks hell" problem available on all major
versions of node.js - the fibers npm package.

Each approach to the problem (if you accept the "callbacks hell" as a legitimate
problem) has multiple drawbacks. In this post I want to list several concerns I
have learnt about in the order of decreasing importance to me:

- JS novice friendliness (how quickly a person coming from Java or Python can
  learn it?)
- Platform availability and the distribution (Will your solution work on all
  browsers? Do you need to ship a library with your code or recompile your
  code?)
- Development scalability (in a project bigger than 5 files and 2 layers of
  abstractions/indirection will this approach bring more harm than good?)


Callbacks
---

Callbacks - provide an anonymous function for every async call or pass a
function that was defined somewhere else as the callback argument.

Here is a fictional example of a very common task: make two sequential http
requests, insert a computed result to the database and move on with some other
action.

In a simplest example we would not have a complex error handling logic and
sometimes we would prefer having anonymous functions to predefined functions.
We would surely balance between the two so our code doesn't become 10 layers
indented.

```javascript
var saveBookAuthorDescription = function (bookId, cb) {
  HTTP.get("https://api.site.com/book/" + bookId, function (err, response) {
    if (err) cb(err);
    var book = JSON.parse(response.content);
    HTTP.get("https://anothersite.com/api/v1/store/author/" + book.author,
      function (err, response) {
        if (err) cb(err);
        var author = JSON.parse(response.content);
        book.author = author;
        database.insert(book, function (err, res) {
          if (err) cb(err);
          cb(null, book);
        });
      });
  });
};
```

Even omiting complex error handling and avoiding a more complicated concurrent
examples - it still would look weird and alien to someone who is used to a
different imperative language.

Although code like this might look familiar to someone who worked with C# and
.NET framework where you can make an http request in a background thread from a
thread-pool or to someone who worked with Cocoa framework in Objective-C - there
is often a need to pass a block function (a slightly different anonymous
function) to the Grand Central Dispatcher (GCD).


It can definitely become one of the many JS/node confusions to a complete newbie
who just wants to build websites in the same fashion he was taught to add
numbers together.

From the availability prospective it is raw-perfect: you can write something
similar on node.js talking to other services or databases or reading files and
in your browser handling user actions, driving animations and making network
requests. No compilation, no problems in distribution.

From the middle to bigger projects prospective it can become hairy over time:

- indentation levels will become deeper, the number of named functions scattered
across the file will only grow, making reading and following the code harder
- error handling will be tricker as usual try-catch blocks will be worthless,
  stacktraces shorter, uninformative
- handling parallel async operations will require a non-trivial amount of
  additional variables, counters and confusion


Promises
---

Promise is an object that represents a "promised result" of an async
computation. Promises can be deferred, combined into series of consecutive or
parallel computations.

There exist a wild variety of the Promises libraries. Some libraries even
based all their async APIs on Promises (ex.: jQuery, Ember.js). Unfortunately,
not all Promises implementations are fully compatible with each other, but most
of them implement the community defined spec
[Promises/A+](http://promises-aplus.github.io/promises-spec/).

Our simple example will now look something like this:

```javascript
// Presumably you have converted your HTTP.get and database.insert functions to
// promises as well
var saveBookAuthorDescription = function (bookId, cb) {
  HTTP.get("https://api.site.com/book/" + bookId).then(function (response) {
    var book = JSON.parse(response.content);
    // cannot chain this call as it depends on the result of previous operation
    HTTP.get("https://anothersite.com/api/v1/store/author/" + book.author).then(function (response) {
      var author = JSON.parse(response.content);
      book.author = author;
      return database.insert(book);
    }).then(function (res) {
      cb(null, book); // success
    }, cb); // failure
  }, cb); // failure
};
```

We have converted our example to a function with the same interface but all
computations are based on Promises. It looks a bit cleaner, the level of
indentation clearly can be reduced.

But it still does look different to someone who has never used a promises
library before:

- code still has a lot of anonymous functions
- since closures don't share the scope, some of the calls are still required to
  be nested (or other library APIs need to be learnt and used)
- now you need to learn a new syntax of Promises, learn how to transform
existing methods to promises-based methods
- need to learn another way of error handling: usual try/catch/finally wouldn't
work

From the availability and distribution point of view:

- there are a lot of libraries to pick from
- some libraries use Promises with slightly different behavior (like jQuery) you
would need to interoperate with
- if your application depends on other libraries those use different promises
  libraries, you would need to load all of them even though they implement the
  same functionality. Probably not a big problem considering their code sizes.

Lastly, complex parallel or racy operations are probably easier as a lot of
common functionality is already baked into the libraries. With time and practice
these tasks would be trivial to write. However:

- you would need to convert all callbacks-based APIs to Promises when external
libraries are used (or find an equivalent already converted to Promises)
- the code still can be difficult to read as every other line is wrapped into a
callback for promises


Generators
---

You might have heard of them already. Generators is a concept successfully
implemented and used in many programming languages (Generators in Python 3, lazy
sequences in Clojure, etc). ES6 standard defines Generators as a part of the
standard but it is yet to be implemented and fully supported in major JS
engines.

From the name, you can guess, that Generators are somehow related to the process
of generating some values. You can read more about their syntax and primary use
[here on MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function*).

Generators are interesting in the context of the callbacks because using them in
an interesting way we can recreate the concept of
[coroutines](http://en.wikipedia.org/wiki/Coroutine) or rather
[semicoroutines](http://en.wikipedia.org/wiki/Coroutine#Comparison_with_generators).

Coroutines aren't new either. They were used sucessfully in a lot of popular
programming languages and frameworks. I first met them in Python
[Tornado](http://tornado.readthedocs.org/en/latest/gen.html) and Python
[Greenlets](http://greenlet.readthedocs.org/en/latest/).

There has been enough excitement in the node community about generators and how
they can solve the callbacks hell, reading
[this](http://jlongster.com/A-Study-on-Solving-Callbacks-with-JavaScript-Generators)
and [this](https://medium.com/code-adventures/174f1fe66127) pieces might be
enough for you to recover your faith into ECMA-262 committee.

If you decide to use the generators approach, then you wouldn't use raw
generator functions and yielding. Rather then that, you would either write a
set of helper functions or one of the written ones. After converting all async
methods to support awaiting on, you would use the `yield` keyword to mark the
awaiting.

```javascript
// Presumably you have converted your HTTP.get and database.insert functions to
// generators. Use a helper library Q.
var saveBookAuthorDescription = function(bookId, cb) {
  Q.spawn(function *() {
    try {
      // get the book in the http request
      var bookResponse =
        yield HTTP.get("https://api.site.com/book/" + bookId);
      var book = JSON.parse(bookResponse.content);

      // get the author in http request
      var authorResponse =
        yield HTTP.get("https://anothersite.com/api/v1/store/author/" + book.author);
      var author = JSON.parse(authorResponse.content);

      book.author = author;

      // insert into the database and wait for the result of the write
      yield database.insert(book);

      cb(null);
    } catch(err) {
      // failure handling
      cb(err);
    }
  });
};
```

We have a clear improvement: the indentation doesn't change as we use async
methods. We now can put everything into a native try-catch block. The
readability of code improved as we can keep the same scope w/o passing all
necessary variables down the async operation, i.e. the stack is preserved.

There are some disadvantages for someone who is not super-familiar with
coroutines or generators:

- the `function*` and `yield` syntax might be confusing
- since `yield` doesn't suspend the whole stack, programmer needs to manually
  `yield` on every level or use a callbacks and generators mixed approach as
  shown above
- there is a big chance that almost every function will be a generator in your
  code-base as everything uses the async methods in your app's business logic
  (on the bright side: it is very easy to tell which method yields)

From the distribution standpoint there are these issues you would need to face:

- isn't implemented by browsers, only available in node behind a flag
- you can transpile the generators code to a regular es5 code but then there is
  a need to support compilation, source-maps and long stack-traces correctly
- even if you use native generators, there is a possibility they are not
  optimized by the V8 engine or are not as optimized as a regular
  generators-free code
- tooling such as autocompletion plugins (ex.: tern.js) or IDEs didn't catch up
  on new ES6 features yet

Finally, from the code-base scalability point of view:

- you would need to convert all 3rd party code to generators or use the mixed
  approach which may require some discipline

Fibers
---

TODO

