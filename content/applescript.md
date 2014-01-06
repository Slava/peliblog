Title: Applescript
Slug: applescript
Date: 2013-01-31

In Collections we used Applescript in our tech. stack for deep integration with OS X and there are my thoughts about it and its usage.

What is Applescript for me? Another technology I use to achieve certain result. But Applescript looks different from any other *script language (hate you, love you, JS).

If you look at it closer, Applescript was designed to be easy to get automation tool. Deep integration with OS X and very natural syntax. Long statements come up together to construct script, very readable script, script in plain English. It might look strange at first sight but such readability brings a lot of benefits, you have probably already felt it if got hands dirty with Objective-C.  Here I would admit, Apple did great job.

The Power of Applescript is in applications supporting it. Richer programming interface is, more opportunities you get. That is very important as you do not mess up with UI, programming mouse movements and virtually hitting keyboard for every simple action. Something, [AutoHotKey](http://www.autohotkey.com/) missed in Windows, right?

Bad thing: it is difficult to find good tool for developing. Built-in Applescript Editor does the job fairly well. Replies and Events on bottom pane make debugging much easier, but failure codes like "-1000201" on crashes will make you use modern search engines couple of times. I found it strange, but behavior of my scripts differed in XCode, Applescript Editor and `osascript` cli utility.

Applescript is good for fast and easy automation of GUI apps and I heard it works perfect with Automator. It can help, if you need some way to get information from other apps in your Cocoa app (as we did in Collections) calling it from Objective-C code. Also it is still good in scripting AHK way.

Applescript is still bad for real programming. One can write GUI applications on Applescript and be quite successful in it but I am not that crazy. Absence of good debug tools makes it even worse.

Some bonus. You always can find syntax descriptions and tutorials with comprehensive skill of using google, but there are some tips for you:

- Applescript is OO-language. And do not let reverse order in `the selection of the document of window number 2 of first application` confuse you.
- There are some natural things that help you. E.g.: `items` will be equal to `every item` which is really nice.
- Some scope confusing may stop you, but remember to use very powerful keyword `my` or statement `of me` referring to current object, `this` or `self` in other languages.
- Be careful with reserved words, sometimes they may appear from nowhere.
- Use built-in documentation (in Applescript editor `File->Open Dictionary...`) with docs for installed apps. If you do not find app you need, try manually open app bundle through `browse...`.
- You are bash-guru? Csh-ninja? Maybe zsh-rockstar? `do shell "..."` is your friend then. Bring power of command line tools to your hacky scripts.
- `quoted form of thePath` quotes strings, works best with filesystem paths.

Slava Kim, messed with Applescript for week in January 2013.
