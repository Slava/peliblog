Title: How JavaScript Hoisting can be dangerous
Slug: js-hoisting
Date: 2013-06-26

I learnt the way scoping and hoisting work in JS early enough so I didn't get
into these pitfalls. My thinking was, hoisting is so innocuous, it can't be
tricky once you know it exists. Today I randomly came up with this example:

    // Global object, window in browser or global in node
    G = this;
    function hoistingExample() {
      // this is global for sure
      G.answer = "global answer";
      // looks like we are modifying global var
      answer = 42;
      // create new local var
      var answer = 33;
      console.log(answer, G.answer);
    }

    hoistingExample();

Looks like it is really easy to forget about hoisting dealing with global and
local variable sharing same name as shadowing happens in the beginning of the
function as supposed to the place where you actually declare local variable.

I didn't fail on this yet, but pretty sure, it may happen soon, will keep you
posted.

