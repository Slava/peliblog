Title: Less known Y combinator
Slug: less-known-y-combinator
Date: 2013-03-30

We all know the YCombinator company. But where did the name come from?

Since I didn't get my degree in Computer Science yet, I was surprised by its origin. Found it accidetally and loved it.

<iframe src="http://player.vimeo.com/video/45140590" width="500" height="400" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe> <a href="http://vimeo.com/45140590">Link.</a>

Those who are lazy can look it up in Wikipedia.

Spoiler from video: javascript version of Y Combinator looks like this:

```javascript
y = function(f) {
    return function(g) { return function(n) { return f(g(g))(n) } } (
       function(g) { return function(n) { return f(g(g))(n) } }
    )
}
```

So as far as I got it: Y combinator is higher order function that gets function improver and produces infinitively better function applying improver. Now we understand the meaning of Paul Graham's startup funding company, it takes company and makes it infinitively better and bigger, at least it trys to.

