Title: Meteor meets your text editor
Slug: meteor-plus-text-editor
Date: 2014-02-04


<iframe width="640" height="360" src="//www.youtube.com/embed/CcPZ56t8x4I" frameborder="0" allowfullscreen></iframe>

More than a month ago I started working on JavaScript IntelliSense for
[Meteor](https://www.meteor.com). Several days ago I presented it in my
lightning talk on [Meteor Devshop
11](https://www.youtube.com/watch?v=CcPZ56t8x4I). After getting lots of positive
responses on Twitter and the meteor-talk mailing list I continue on improving
it. [My work brings](https://github.com/Slava/tern-meteor) more intelligent
tooling to Sublime Text 2/3, Vim and Emacs when you work on a Meteor app in
JavaScript.


There is a simple problem with web development these days: the tooling is
lacking a lot of features people had for years: static analysis tools, runtime
dynamic analysers, code editors support and others.

Code editor support is especially important as we spend most of our time there:
writing and, more commonly, reading and exploring code. Modern IDEs like
WebStorm and Visual Studio have accomplished big results in bringing such
intelligent support to their costly products. For light-weight editors lovers
there is open-source project working on that - [TernJS](http://ternjs.net).

![Initial email](/images/tern-meteor-email.png)

One day I opened an [interesting email from Bondi
French](https://groups.google.com/forum/#!topic/meteor-talk/b_yGWIqXl7Y) to
meteor-talk. In his email Bondi asked if anyone tried to integrate TernJS,
code-analysis engine for JavaScript, with Meteor. It looked like a good idea to
me and I decided to give it a try.

Fortunately, I was on my vacation hanging out on sunny warm San Diego beaches
with my good friends, so I had a lot of time to "background process" these
thoughts.

Nothing made me so enthusiastic to work on such project like a good time spent
outdoors in a good company of friends. It probably was the first time in last 6
month when I got so much sun and spent less than 10 hours a day in front of a
computer.

![Photo credits to @armansu on Instagram](/images/sd-beach.jpg)

One day I refused to go to a movie theater with others and sat down for a solid
couple of hours implementing an MVP for Meteor + Tern integration: convert type
definitions of Meteor public API (using existing work of
[`meteor.ts.d`](https://github.com/borisyankov/DefinitelyTyped/blob/master/meteor/meteor.d.ts))
and teaching Tern basic scoping rules of Meteor.

After my vacation week I found another weekend to finish and test my work. After
testing it on a simple app with Sublime Text first, I [recorded a simple
screencast](https://www.youtube.com/watch?v=5cAHxpNEHTc) to show my work to
people. The next day I [recorded the
sequel](https://www.youtube.com/watch?v=TIE9ZOqlvFo) walking through the
installation process for Vim. The same day happy users reported this plugin to
work on Emacs as well. I was happy. The MVP worked for people. It worked for me.

![Type-based auto-completion with Meteor app](/images/tern-vim-completion.gif)

Smart types-based auto-completion, "jump to definition", "find references",
documentation look up in Meteor apps worked out of the box, thanks to Tern's
flexible plugin system.

To reach the wider audience I proposed my lightning talk and showed off to
everyone on the Internet.

I consider it to be pretty successful for a weekend for fun project:

- It works for my work
- Everyone on the mailing list thread was excited and supportive
- The [GitHub repo](https://github.com/Slava/tern-meteor) got more than 350
  unique views in over the first week

It also got covered by all Meteoric knowledge sources: [meteor-talk mailing
list](https://groups.google.com/forum/#!topic/meteor-talk/b_yGWIqXl7Y),
[Meteor's twitter](https://twitter.com/imslavko/status/429111204762509313),
[/r/Meteor](http://www.reddit.com/r/Meteor/comments/1wctij/meteor_autocompletion_plugin_for_sublime/),
[Meteorpedia](http://www.meteorpedia.com/read/TernJS), [Meteor Hacks
weekly](http://meteorhacks.com/meteor-weekly-ralph-chat-jade-for-meteor-ui.html),
[Meteor
Podcast](http://www.meteorpodcast.com/2014/01/24/episode-3-january-24th-2014/),
[Meteor Devshop SF](https://www.youtube.com/watch?v=CcPZ56t8x4I), Meteor's
Youtube channel. That's hard to miss :).

<blockquote class="twitter-tweet" data-cards="hidden" lang="en"><p><a href="https://twitter.com/search?q=%23MeteorDevshop&amp;src=hash">#MeteorDevshop</a>: Meteor autocompletion for Vim, Emacs and Sublime Text: <a href="https://t.co/Zkperjba9C">https://t.co/Zkperjba9C</a>; Slides: <a href="http://t.co/hTNJTDIaJb">http://t.co/hTNJTDIaJb</a></p>&mdash; Slava Kim (@imslavko) <a href="https://twitter.com/imslavko/statuses/429111204762509313">January 31, 2014</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

But it is not over yet! There is a big room for improvements in my plugin! I am
already in the process of bringing Meteor smart-packages analysis support,
documentation support and bringing the tooling for definitions generation for
newer Meteor versions and Atmosphere packages.

Hopefully, this little side project will make a lot more people happier working
with Meteor. Alright, folks, I going back to oplog work. Will work on this
during next weekend!

