Title: Fibers
Slug: fibers
Date: 2013-05-24

## What
`Fibers` is an npm module developed with C++. It is another flow control library like async, nue, batch, cascade, then, afuture and others. The biggest disadvantage of `Fibers` - they work only inside node.js. It is applicable only on server and will never work in your browser (at least because it is very JS engine specific library).
Checkout [the repo on Github](https://github.com/laverdet/node-fibers).

This library implements [coroutines](http://en.wikipedia.org/wiki/Coroutine). I imagine each fiber as a light-weight thread(for normal people these two words might mean the same thing) but fibers use co-operative multitasking. Fibers don't run simultaniously, each fiber takes its time to accomplish something small and then yields the execution flow to other fibers and waits for next time it is given control.

## Why
The main reason I see anyone using some flow control library by default: every I/O function in node.js (file system reads/writes, web requests, database access) is an asynchronous function that invokes a callback on success or error.

First of all, your code may end up looking really ugly. Writing a quick code you may consider [pyramids of callbacks](http://callbackhell.com/) 'good enough' but once your application gets bigger, fatter or more serious you will need to manage it with more named functions, use less lambda functions or use a flow control library.

People found some some approaches: futures, promises, signals. All are the same thing: some abstract object representing an action (or set of actions) running.

The second reason could be a reasonable substitution for threads. Fibers can give you some sort of multitasking in single-threaded Javascript.

## How

After you get `Fibers` npm module you can start:

```bash
$ npm install fibers
```

Require fibers library like anything else:

```javascript
var Fiber = require('fibers');
```

To create a fiber just pass any function:

```javascript
var fiber = Fiber(function () {
	console.log('I am inside fibers');
});
```

You can run it invoking the `run` method:

```javascript
fiber.run();
```

You can get the instance of fiber you are running in object `Fiber.current` and get the number of running fibers by accessing `Fiber.fibersCreated`.

There is the third member available: `yield`. That is where magic happens. It gives control to the caller of fiber. Everything you had in stack on fiber will be remain untouched and accessible when you will run the fiber next time. Once fiber function returns it will roll back to its original state - empty stack.

```javascript
var f = Fiber(function () {
	var n = 0;
	console.log(n);
	Fiber.yield();
	n++;
	console.log(n);
	Fiber.yield();
	n++;
	console.log(n);
});

for (var i = 0; i < 5; i++) {
	console.log('Will run the fiber: ' + i);
	f.run();
}
```

Running this code will give you following output:

```
Will run the fiber: 0
0
Will run the fiber: 1
1
Will run the fiber: 2
2
Will run the fiber: 3
0
Will run the fiber: 4
1
```

You can see how the fiber preserves the stack vars and starts over when it returns. We could show a bit more complicated example to prove that the whole stack is preserved.

```javascript
var f = Fiber(function () {
    var n = 0;
    var ff = function () {
        var m = 0;
        console.log(n, m);
        Fiber.yield();
        m--;
        console.log(n, m);
    };

    ff();
    Fiber.yield();
    n++;
    ff();
});

for (var i = 0; i < 5; i++) {
    console.log('Will run the fiber: ' + i);
    f.run();
}
```

```
Will run the fiber: 0
0 0
Will run the fiber: 1
0 -1
Will run the fiber: 2
1 0
Will run the fiber: 3
1 -1
Will run the fiber: 4
0 0
```

The next thing to learn is how to pass new values inside fiber: you can invoke the `run` method with an argument. This argument will be returned by `yield`.

```javascript
var f = Fiber(function (s) {
    console.log('passed %s, get something new', s);
    s = Fiber.yield();
    console.log('now it is %s!', s);
});

for (var i = 0; i < 5; i++) {
    f.run('string number ' + i);
}
```

```
passed string number 0, get something new
now it is string number 1!
passed string number 2, get something new
now it is string number 3!
passed string number 4, get something new
```

Similarly you can pass some argument to `yield` and it will be returned by `run` command. Now we can create a generator:

```javascript
// next - how many jumps further we want to make
var factorialGenerator = Fiber(function (next) {
    var factorial = 1, i = 1;
    while (true) {
        // default number of jumps to 1
        if (typeof next === 'underfined')
            next = 1;
        while (next--) {
            factorial *= i;
            i++;
        }

        next = Fiber.yield(factorial);
    }
});

var f3 = factorialGenerator.run(3);
var f7 = factorialGenerator.run(4);

console.log(f3, f7);
```

```
6 5040
```
That's how we use fibers, it is not easy to wrap your head around it from the first time and you don't need to. Most of the time you will be using an abstraction layer on top of fibers and `Fibers` comes with one built-in called `Future`. We will have a look at it in next blog-post. For now I want to finish with some words of wisdom:

> It took me time to realize: Fibers are just very structured goto

- David Glasser

