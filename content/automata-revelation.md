Title: Pushdown Automata Revelation
Slug: pda-revelation
Date: 2013-05-07

Today a revelation happened to me.

I remember approximately three years ago, back in the high school, I was solving algorithmic problems for fun. One of the problems was to parse and calculate and arithmetic expression. 

Allowed symbols/operators were: '+', '-', '*', '/', 'sin', 'cos', '(', ')' and numbers were decimals. It was so hard to code a solution for this problem, handling all the cases was easy compared to structuring your procedural program written in C. I remember writing 5 procedures calling each other parsing expression.

Today I have watched video on Coursera about push down automatas and it occurred to me: Did I build implicit automata 3 years ago?

Looks like I used these procedures as states and used recursion stack as automata stack :). It wasn't clear to me how to make up a 'final state' so I used global variable and set it to true when my code failed to parse the expression.

It is fun to see how I had written such stuff long time ago and made a 'full circle' in this sense. I like this feeling, I like programming :).

my 3 years old code: http://pastebin.com/JUeXLeea 
debug version of this code: http://pastebin.com/JYUaibem
online judge with unit tests: http://acmp.ru/index.asp?main=task&id_task=451 (in Russian)

