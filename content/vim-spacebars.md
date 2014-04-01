Title: Spacebars in your Vim
Slug: vim-spacebars
Date: 2014-04-01

[Spacebars] is a templating language inspired by Handlebars (Mustache) and is a
default language used by [Blaze], [Meteor]'s live DOM-updating engine.

I am a heavy Vim user and it frustrates me when something doesn't work well in
my favorite text editor. For this time, my templates were not displayed
perfectly and Vim's auto-indenter was confused by the new syntax so it looked
pretty bad even with the [mustache/vim-mustache-handlebars] installed.

![Spacebars in Vim](/images/spacebars.png)

So, learning some VimScript from `:h syntax` and [VimScriptTheHardWay] book, I
managed to fork and fix some syntax highlighting issues, implement folds for
block-helpers, fix auto-indenter (by borrowing some code from
[othree/html5.vim]) so block-helpers tags are respected as well as other html
tags.

The result can be seen on [Slava/vim-spacebars].

P.S.: the theme is Tomorrow and you can get my fork of it for Vim on
[Slava/vim-colors-tomorrow].

[Spacebars]: https://github.com/meteor/meteor/tree/master/packages/spacebars
[Blaze]: https://www.meteor.com/blog/2014/03/27/meteor-080-introducing-blaze
[Meteor]: https://www.meteor.com
[mustache/vim-mustache-handlebars]: https://github.com/mustache/vim-mustache-handlebars
[VimScriptTheHardWay]: http://learnvimscriptthehardway.stevelosh.com/
[othree/html5.vim]: https://github.com/othree/html5.vim
[Slava/vim-spacebars]: https://github.com/Slava/vim-spacebars
[Slava/vim-colors-tomorrow]: https://github.com/Slava/vim-colors-tomorrow

