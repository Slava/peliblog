Title: Top 5 syntactic weirdnesses to be aware of in MongoDB
Slug: wtf-mongo
Date: 2014-01-05

![mongodb logo](http://fc01.deviantart.net/fs70/f/2010/168/e/1/Icon_MongoDB_by_xkneo.png)

Rage posts about MongoDB are quite popular these days. Most of them are about
poor performance on specific data sets, reliability and sharding issues. Some of
those blog posts might be right, other are just saying that the most popular
NoSQL solution didn't fit their needs.

This article is not one of those. While most of the posts focus on operations
part, benchmarks and performance characteristics, I want to talk a little bit
about MongoDB query interfaces. That's right - programming interfaces,
specifically about node.js native driver but those are nearly identical across
different platform drivers and Mongo-shell.

Disclaimer: I try hard not to hate on MongoDB. In fact I work with MongoDB every
work day as part of my full-time job. I also take part in the development of
[Minimongo](https://github.com/meteor/meteor/tree/devel/packages/minimongo),
pure-JavaScript clone of MongoDB API to work with in-memory caches. There is no
reason for me to mock Mongo other than warning everyone about its sharp edges.
Most of these gotchas are found by [David Glasser](https://twitter.com/glasser).
This article assumes you are familiar with MongoDB's API.


***

# 1. Keys order in a hash object

Let's say you want to store a simple object literal:

    > db.books.insert({ title: "Woe from Wit", meta: { author: "A. Griboyedov", year: 1823 } });

Great! Now we have a book record. Let's say later we would want to find all
books published in 1823, written by this author ("A. Griboyedov"). It is
unlikely to return more than one result but at least it should return the "Woe
from Wit" book as we just inserted it, right?

    > db.books.find({ meta: { year: 1823, author: "A. Griboyedov" } });
    < No results returned

What happened? Didn't we just insert a book with such meta-data? Let's try
flipping the order of keys in the meta object:

    > db.books.find({ meta: { author: "A. Griboyedov", year: 1823 } });
    < { _id: ..., title: "Woe from Wit", meta: { ... } }

Here it is!

**The gotcha**: the order of keys matters in MongoDB, i.e. `{ a: 1, b: 2 }` does
not match `{ b: 2, a: 1 }`.

**Why does it happen**: MongoDB uses a binary data format called
[BSON](http://bsonspec.org/). In BSON, the order of keys always matters.
Notice, in JSON an object is an unordered set of key/value pairs.

What about JavaScript? ECMA-262 left it as 'undefined'. In some browsers
(usually old ones) the order of pairs is not preserved meaning they can be
anything. Thankfully most modern browsers' JavaScript engines preserve the order
(sometimes even in arrays), so we can actually control it from node.js code.

Read more about it at [John Resig's
blog](http://ejohn.org/blog/javascript-in-chrome/).

The answer to this is to either always specify pairs in the canonical form (keys
are sorted lexicographically) or just to be consistent across your code base.

Another workaround would be to use a different selector, specifying certain
key-paths rather than comparing to an object literal:

```javascript
> db.books.find({ 'meta.year': 1823, 'meta.author': 'A. Griboyedov' });
```

It would work in this particular case but note that the meaning of this selector
is different.

**The gotcha**: this behavior can be dangerous whenever you want to build a
multi-key index.

```javascript
> db.books.ensureIndex({ title: 1, 'meta.year': -1 });
```

In such command the priority of `title` would be higher than the priority of
`meta.year` field. This is important to the way MongoDB will lay out your data:
[Read more in docs](http://docs.mongodb.org/manual/core/index-multikey/).


***

# 2. undefined, null and undefined

Anyone remembers those times when the behavior of `undefined`, `null` and the
relation was confusing? In JavaScript world those are two different values and
they are not the same in a strict comparison `undefined !== null`. However, they
are equal in a non-strict comparison `undefined == null`. Some people are very
careful with them, others use them interchangeably. But the point is: you have
two different but similar values in JavaScript.

MongoDB brings it to the next level. The [BSON
spec](http://bsonspec.org/#/specification) defines `undefined` as "deprecated".

Node.js node-native-driver for MongoDB [doesn't implement
it](https://github.com/mongodb/js-bson/blob/master/lib/bson/bson.js#L77) at all.

In the current version (2.4.8) the behavior shows that `null` and `undefined`
are treated as the same value.

```javascript
> db.things.insert({ a: null, b: 1 });
> db.things.insert({ b: 2 }); // the 'a' is undefined implicitly
> db.things.find({ a: null });
< { a: null, b: 1 }
< { b: 2 }
```

I am not sure about the actual implementation, it looks like `undefined` is just
converted to `null` by node driver but is restricted in mongo-shell.

In the following code we will get the same result printed twice: all 3 objects.

```javascript
// from node.js code with mongo/node-native-driver
db.things.insert({ a: null, b: 1 });
db.things.insert({ b: 2 });
db.things.insert({ a: undefined, b: 3 });
console.log(db.things.find({ a: null }).fetch())
console.log(db.things.find({ a: undefined }).fetch())
```

However in mongo-shell you will be able to query only with `null` but we get all
three objects as well.

```javascript
// from mongo-shell
> db.things.find({a: undefined});
< error: { "$err" : "can't have undefined in a query expression", "code" : 13629 }
> db.things.find({a: null});
< { "a" : null, "b" : 1, "_id" : "wMWNPm7zrYXTNJpiA" }
< { "b" : 2, "_id" : "RjrYvmZF5EukhpuAY" }
< { "a" : null, "b" : 3, "_id" : "kethQ2khbyfFjJ7Sa" }
```

We can see that mongo/node-native-driver converted the explicit `undefined` to
`null` but left the implicit one as is (which is expected really).

The cool stuff happens when we insert an explicit `undefined` *from mongo-shell*:

```javascript
// from mongo-shell
> db.things.insert({ a: undefined, b: 4 });
> db.things.find({ a: null })
< { "a" : null, "b" : 1, "_id" : "wMWNPm7zrYXTNJpiA" }
< { "b" : 2, "_id" : "RjrYvmZF5EukhpuAY" }
< { "a" : null, "b" : 3, "_id" : "kethQ2khbyfFjJ7Sa" }
```

We get the same three values and no new object with `b=4`. Shouldn't `undefined`
match `null`? Let's look at the new object:

```javascript
> db.things.find({ b: 4 });
< { "_id" : ObjectId("52ca134f3e47d3d91146f2b5"), "a" : null, "b" : 4 }
```

It is still there, `a` field is holding something looking like `null` but
doesn't match the `null` from our selector.

**The gotcha**: there are more than 2 values looking like `null` in MongoDB:
`null`, `undefined` and `undefined` inserted from mongo-shell that looks like
`null` in the shell but in reality matches the deprecated `undefined` in BSON
(type number six). The last one doesn't match `null` from the selectors, first
two match both `undefined` and `null`. The absence of value also matches both.

Read the original [GitHub issue](https://github.com/meteor/meteor/issues/1646#issuecomment-29682964).


***

# 3. Soft limits, hard limits and no limits

Let's say you have a feed of items and you allow user to specify the number
items to return. You would return the result of a query looking like this:

    db.items.find({ ... }).limit(N);

Where `N` is supplied by user. Of course we want to be careful and restrict user
up to 50 items, otherwise anyone in the Internet would be able to load our
application server and the database simply by supplying a very large `N`:

    function getItems (N) {
      if (N > 50)
        N = 50;
      return db.items.find({}).sort({ year: 1 }).limit(N);
    }

Looks like a reasonable code running in your node.js app (server-side).

**The gotcha**: if user supplies `0` (zero) as a number of items he wants to get
the MongoDB would take it as "give me everything".

It is well documented but not obvious right away: zero means "no limit" to
MongoDB. My guess is some code just treats all falsy values the same way:
`undefined`, `null`, `0`, absence of value - everything means "no limit".

That's OK, we can treat `0` as a special case:

    function getItems (N) {
      if (N > 50 || !N) // check if N is falsy ("no limit")
        N = 50;
      return db.items.find({}).sort({ year: 1 }).limit(N);
    }

Looks good? But what happens if user supplies a negative number? Is it even
possible? What could it possibly mean?

In reality something like `db.items.find().limit(-1000000000000)` can return a
bazillion of items. It is hard to find the documentation about it but several
month ago I have seen the description of this behavior in node.js driver's docs,
it talked about "soft" and "hard" limits. I have no idea what does it mean.

So the final version of our server-side method would look like this:

    function getItems (N) {
      if (N < 0) N = -N;
      if (N > 50 || !N) // check if N is falsy ("no limit")
        N = 50;
      return db.items.find({}).sort({ year: 1 }).limit(N);
    }

**The gotcha**: limit can be negative. It would mean the same as positive in the
broader sense but the negative one is "soft".


***

# 4. Special treatment for arrays

A lot of people don't know this "feature" but arrays are treated specially.

```javascript
> db.c.insert({ a: [{x: 2}, {x: 3}], _id: "aaa"})

> db.c.find({'a.x': { $gt: 1 }})
< { "_id" : "aaa", "a" : [  {  "x" : 2 },  {  "x" : 3 } ] }

> db.c.find({'a.x': { $gt: 2 }})
< { "_id" : "aaa", "a" : [  {  "x" : 2 },  {  "x" : 3 } ] }

> db.c.find({'a.x': { $gt: 3 }})
< Nothing found
```

So whenever there is an array in object, the selector would "branch" to every
element and this acts like "if any of those match, then the whole document
matches".

Notably, it doesn't work for nested arrays:

```javascript
> db.x.insert({ _id: "bbb", b: [ [{x: 0}, {x: -1}], {x: 1} ] })

> db.x.find({ 'b.x': 1 })
< { "_id" : "bbb", "b" : [  [  {  "x" : 0 },  {  "x" : -1 } ],  {  "x" : 1 } ] }

> db.x.find({ 'b.x': 0 })
< Nothing found

> db.x.find({ 'b.x': -1 })
< Nothing found
```

Same feature applies to the fields projections:

```javascript
> db.z.insert({a:[[{b:1,c:2},{b:2,c:4}],{b:3,c:5},[{b:4, c:9}]]})
> db.z.find({}, {'a.b': 1})
< { "_id" : ObjectId("52ca24073e47d3d91146f2b7"), "a" : [  [  {  "b" : 1 },  {  "b" : 2 } ],  {  "b" : 3 },  [  {  "b" : 4 } ] ] }
```

If we play a bit more combining this feature with numeric keys in selectors the behavior becomes harder and harder to predict:

```javascript
> db.z.insert({a: [[{x: "00"}, {x: "01"}], [{x: "10"}, {x: "11"}]], _id: "zzz"})
> db.z.find({'a.x': '00'})
< Nothing found
> db.z.find({'a.x': '01'})
< Nothing found
> db.z.find({'a.x': '10'})
< Nothing found
> db.z.find({'a.x': '11'})
< Nothing found

> db.z.find({'a.0.0.x': '00'})
< { "_id" : "zzz", "a" : [     [   {   "x" : "00" },   {   "x" : "01" } ],     [   {   "x" : "10" },   {   "x" : "11" } ] ] }

> db.z.find({'a.0.0.x': '01'})
< Nothing found

> db.z.find({'a.0.x': '00'})
< { "_id" : "zzz", "a" : [     [   {   "x" : "00" },   {   "x" : "01" } ],     [   {   "x" : "10" },   {   "x" : "11" } ] ] }

> db.z.find({'a.0.x': '01'})
< { "_id" : "zzz", "a" : [     [   {   "x" : "00" },   {   "x" : "01" } ],     [   {   "x" : "10" },   {   "x" : "11" } ] ] }

> db.z.find({'a.0.x': '10'})
< Nothing found
> db.z.find({'a.0.x': '11'})
< Nothing found
> db.z.find({'a.1.x': '00'})
< Nothing found
> db.z.find({'a.1.x': '01'})
< Nothing found

> db.z.find({'a.1.x': '10'})
< { "_id" : "zzz", "a" : [     [   {   "x" : "00" },   {   "x" : "01" } ],     [   {   "x" : "10" },   {   "x" : "11" } ] ] }

> db.z.find({'a.1.x': '11'})
< { "_id" : "zzz", "a" : [ [ { "x" : "00" }, { "x" : "01" } ], [ { "x" : "10" }, { "x" : "11" } ] ] }
```

And later becomes just inconsistent. The difference between this and next
examples is just the inner value: in the last example it is an object, in the
following it is a number. It is enough for behavior to change:

```javascript
> db.p.insert({a: [0], _id: "xxx"})

> db.p.find({'a': 0})
< { "_id" : "xxx", "a" : [  0 ] }

> db.q.insert({a: [[0]], _id: "yyy"})

> db.q.find({a: 0})
< Nothing found

> db.q.find({'a.0': 0})
< Nothing found

> db.q.find({'a.0.0': 0})
< { "_id" : "yyy", "a" : [  [  0 ] ] }
```

**The gotcha**: avoid arrays and nested arrays or other one-to-many pairs in
your documents queried by selectors with a usual intend to query one-to-one
pairs. The combination with numeric keys (like `{ 'a.0.x': Y }` meaning the
field `x` of the first element of field `a` must be `Y`) may become very
confusing as it depends on your data.


***

# 5. $near geo-location operator

This one is simple. You have a collection of documents with a location field.
Location field represents a geo-location. The trick is in two different types of
locations MongoDB can index, each type has a slightly different API and a
slightly different behavior.

The first one looks like this:

```javascript
db.c.find({
  location: {
    $near: [12.3, 32.1],
    $maxDistance: 777
  }
});
```

The second one looks like this:

```javascript
db.c.find({
  location: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [ 12.3, 32.1 ]
      },
      $maxDistance: 777
    }
  }
});
```

**The gotcha**: the syntax of geo-query is slightly different depending on the
index type. `$maxDistance` is the sibling element of `$near` in case of plain
pairs and is a child in case of Geo-JSON.

But there is more! Sometimes you can get the same point twice in the result set!
To understand this we need to recall the previous gotcha about nested arrays.
Consider this code:

```javascript
> db.c.insert({ location: [[1, 2], [1, 0]] }); // inserting an array of two points
> db.c.ensureIndex({ location: "2d" });
> db.c.find({ location: { $near: [0, 0], $maxDistance: 500 } });
< { "_id" : ObjectId("52ca30ec3e47d3d91146f2b8"), "location" : [  [  1,  2 ],  [  1,  0 ] ] }
< { "_id" : ObjectId("52ca30ec3e47d3d91146f2b8"), "location" : [  [  1,  2 ],  [  1,  0 ] ] }
```

Same point is returned twice as both points from the array match the selector.


***

All these gotchas remind me the days when I first started coding in JavaScript.
There are several corner cases, some of them work inconsistently across browsers,
some of the features you never want to use, somewhere you want to be extra
careful. All of those are well known in JavaScript land, but not so well in
MongoDB land.

Almost every weird behavior listed here was found in the process of simulating
MongoDB in the project called
[Minimongo](https://github.com/meteor/meteor/tree/devel/packages/minimongo),
mostly by [David Glasser](https://twitter.com/glasser).

This article will be updated as new weirdnesses come to mind.

***

Update of 1 April 2014: I talked about some of these issues and some new gotchas
on SF Meteor Devshop, the recording of the talk is below. "Don't get bitten by
Mungos (or Mongos)":

<iframe width="640" height="360" src="//www.youtube.com/embed/amaR4Aqe0s0" frameborder="0" allowfullscreen></iframe>

[Discuss on Hacker News](https://news.ycombinator.com/item?id=7020300).

