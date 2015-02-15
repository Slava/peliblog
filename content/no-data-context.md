Title: Handlebars without data context
Slug: no-data-context
Date: 2015-02-14

![Handlebars](/images/handlebars.png)

In this post I am proposing a better way to write your Meteor templates. The
goal is to have more explicit variables and a scope similar to what you can see
in a regular JavaScript code.

## A short history lesson

Handlebars - a popular templating language. At the time a web developer would
pick Handlebars to render their html pages. That was before the world of web
development moved to cilent-heavy templating and most application servers became
a dumb API layer for the database.

For a person like me, who came to web dev a couple of years ago, little is known
about the dark time of 2010, when the project was born. Various evidence shows
that people were debating about "logicless templates" and good
"presentation/logic" separation. At the time, Handlebars have borrowed the
syntax from Mustache templates and introduced more syntax: constructs like `#if`
and `#each`, template helpers, compiled templates.

The success of curly braces (`{{`, `}}`) propagated to the client-side
templating. Multiple projects has adapted the syntax and structure while
bringing some "life" to the braced expressions.

[Ember.js][ember], [Ractive][ractive] and [Meteor's Blaze][blaze] (and its
predecessor [Spark][spark]) all use the Handlebars syntax to create "Live HTML
templates" - templates changing the HTML page on the fly as the underlying data
model changes. That's it - if your JavaScript value changes, you can expect the
presentation constructed by your templates will change accordingly.


## Handlebars at Meteor

A lot of efforts has been spent by the Meteor Core team to maintain a lot of the
syntax features and behaviors of Handlebars while making it more reactive and
"live".

Around the time of arrival of [Blaze][blaze], Meteor's latest iteration of
reactive templates, the syntax started to diverge. The Meteor fork of the syntax
is called ["Spacebars"][spacebars], similar to other front-end frameworks,
Spacebars enforce structured templates for fine-grained updates, some of the
features of Handlebars are dropped but most of the semantics remained the same.

## Data context - the root of all confusion

One feature remained the same and that's the "data context". In Handlebars this
is the only way to pass data from template to template. "Data context" can be
accessed with [troublesome `this` keyword][this]. It is inherited by default on
templates inclusions, so it sneaks into everything; It is silent and the only
argument, it is also implicit.

```handlebars
<template name="people">
  {{!-- the data context here is { people: [...] } --}}
  {{#each people}}
    {{!-- the data context here is changed by #each and it is { name: ... } --}}
    {{> person}}
  {{/each}}
</template>

<template name="person">
  {{!-- the data context here is expected to be an object --}}
  {{!-- with fields 'name' and 'age' --}}
  <span>{{name}}: {{age}}</span>
</template>
```

As always, the confusion happens when the data context changes. Constructs like
`#each` and `#with` change the data context and often do it in such a way, that
you can't access the parent data unless you reside to a weird dotted syntax.

```handlebars
{{#each people}}
  {{#each favoriteFruits}}
    {{!-- accessing the parent data with a weird ../ syntax --}}
    {{!-- also using {{this}} to refer to the current data --}}
    <span>The favorite fruit of {{../name}} is {{this}}</span>
  {{/each}}
{{/each}}
```

The reason for such syntax is the concept of "paths" in Handlebars. So every
time you see a construct like `{{person.bio.homeTown}}`, it is not a property
access - it is a path. This is why `{{../name}}` construct makes sense if you
think of it as a path. In fact, an expression `{{.}}` would be equivalent to
`{{this}}` in Handlebars. Path is another confusing syntax feature that just
adds to the data context.


## Data context is a dynamic variable

If you have a template `"person"` and it displays a name and an age from the
current data context. What is the current data context? How do we know if there
are other fields on it that we can use in this template? It completely depends
on the template that includes the `"person"` template.

In other words, data context is just a dynamic variable, something that depends
on the chain of calls that led you to here, rather than the environment that
existed when your template was defined (lexical variable).

Dynamic variables and dynamic scope are the programming language features from
60s and no other modern sane programming languages uses them as the main way to
refer to variables. In fact, if you search for materials online explaining
dynamic variables, most likely you will find something about Emacs Lisp or Bash
or Perl (the last two keep it for backwards compatibility).

JavaScript has only one sort-of dynamic variable called `this`. And guess what?
People are confused as hell by it. Thankfully, in JavaScript `this` is not the
main way of passing arguments to a function. Unfortunately, in Handlebars it is
the only way.

Similar to Handlebars' `{{#with}}` JavaScript the [`with`][with] keyword. Guess
what?  Every JS developer will tell you to never ever use it. It makes the code
confusing, it cripples the scope, it is a source of bugs, it is deprecated in
the strict mode.


## Handlebars without data context

How would we get rid of the data context? Recently, I have been working on a
Pull Request to Meteor's Blaze to introduce a concept of lexical scope into the
templating language: [PR #3560 at
meteor/meteor](https://github.com/meteor/meteor/pull/3560).

### #let

First, let's introduce the notion of scope and tools to manipulate it. I thought
that the `let` keyword would be appropriate here. It would be familiar to people
who have seen the `let` form in Scheme and the `let .. in ..` construct in ML.

```handlebars
{{#let city=person.bio.homeTown name=person.name}}
  <div>
    {{!-- access newly introduced variables city and name in this let block --}}
    {{name}} is from {{city}}!

    {{!-- still can access person from the scope above --}}
    Get to know {{person.name}}.
  </div>
{{/let}}
```

Since templates are not a full-fledged programming language and their use is
usually simpler and limited, it makes sense to make these variables immutable.
That's it. They can be overshadowed by a different `{{#let}}` but cannot be
changed. Their application is limited to their block and they don't leak to
other templates included within their block.

### New #each

Now let's fix the most commonly used construct that relies on the dynamic data
context: `{{#each}}`. The new `{{#each}}` plays the game of lexical scoping and
introduces a new variable within its body representing the iteration variable:

```handlebars
{{#each person in people}}
  <div>{{person.name}} is from {{person.bio.homeTown}}.</div>
{{/each}}
```

`person` as a variable makes a lot more sense to the reader than an unnamed
`this`. This is very similar to what you would do in JavaScript:

```javascript
people.forEach(function (person) {
  // new scope, person is introduced
});
```

### Including templates with their scope as arguments

And lastly, let's make the template inclusion more descriptive to the reader:

```handlebars
<template name="person" args="name age city">
  <div>
    Everyone, meet {{name}}.
    {{name}} is {{age}} years old and is coming from {{city}}.
  </div>
</template>
```

Now the inclusion would look like this:

```handlebars
{{> person name=jack.name age=jack.age city=jack.bio.homeTown}}
```

The syntax is a lot more verbose now but what we have here is just a set of
named arguments. Included template gets its own scope set to the passed
arguments, similar to a function in JavaScript that gets its own scope set to
its positional arguments:

```javascript
function (name, age, city) {
  return "Everyone, meet " + name + ".\n" +
    name + " is " + age + " years old and is coming from " + city + ".";
}
```

This already works in Blaze without any changes. The trick is, the same syntax
is used to set a custom data context. And if this is the only place where we use
data context, it can as well treated as a template-local scope.

Arguments declared in the template open tag are optional but I think it makes it
very clear to anyone who is going to use this template in the future, what are
the expected arguments.


## Try it out!

We are done! Following this pattern, I believe, your templates can become
easier to follow, less confusing to read and more explicit. The data context is
a legacy from Handlebars and I wish it would remain there.

You can try using these features and this style as soon as my PR lands to a
release. You can also pull it from GitHub and play with it running Meteor from a
checkout.

[ember]: http://emberjs.com/guides/templates/handlebars-basics/
[ractive]: http://www.ractivejs.org/
[blaze]: https://www.meteor.com/blaze
[spark]: https://github.com/meteor/meteor/tree/b39033c3c304feed47eb0600cb64ff8730318afe/packages/spark
[spacebars]: https://github.com/meteor/meteor/tree/devel/packages/spacebars
[this]: http://javascriptissexy.com/understand-javascripts-this-with-clarity-and-master-it/
[with]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/with

