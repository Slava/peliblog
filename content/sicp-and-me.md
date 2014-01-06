Title: SICP and Me
Slug: sicp
Date: 2013-11-03

#I am a bit late but it is still great!

![A pic from 4Chan](https://d262ilb51hltx0.cloudfront.net/proxy/1*k5v65hJ2AxMM3gaZ8rxvEQ.jpeg)

As someone who didn't study Computer Science at top university [yet] I am continuously learning everything they would have taught me at school. Since my knowledge is quite eclectic, a lot of foundation is still missing.</p>

Two month ago “Structure and Interpretation of Computer Programs” has been selected as my next learning target and I don't regret. After reading “On Lisp” and “The Little Schemer” SICP looked like a reasonable extension but I was wrong. If books mentioned above were rather practical and were focusing on work with the specific languages (Common Lisp and Scheme), SICP was giving more theoretical and abstract knowledge about computer languages and programming expressed with Scheme. I believe it could be done with any other language capable of passing functions and making closures (and I have heard they use Python to teach this course nowadays).

Since I am a very lazy reader the video course was chosen over the book as a primary source. MIT OCW has a publicly available recording of the course directed by HP back in 1986 for HP employees. They have done a great job, AV quality is probably better than a dozen of JS Conf talks.

## The Course

Course is lectured by the book authors: Sussman and Abelson. There is no surprise the concepts are explained so clearly and authentically. Every lecture can become an eye-opening story of the particular idea. Eventually all lectures fall into coherent story with a very simple conclusion: “There is no magic”.

It starts with very easy concepts such as iteration, recursion or higher order functions. Despite simplicity of the subject, lectures are very interesting to watch as they are presented from unusual to me angle. Even though I am not a beginner in these things, the 25 years old video lecture surprised me. The surprise repeated later again when the professor proved the equality of data and functions — basic building blocks or primitives.

Remember the first time you have heard about method dispatch or the event loop and lazy evaluation of some hip platform? What about so long awaited generators, streams and functional primitives in your favorite language? SICP, a course from last century may explain them much better than someone on Stack Overflow. Not only that, they will explain how to implement those in terms of language primitives.
> “Any sufficiently complicated C or Fortran program contains an ad hoc, informally-specified, bug-ridden, slow implementation of half of Common Lisp.” — Greenspun’s tenth rule

Later, SICP reaches more advanced topics we don't usually see widely used in day to day engineering but they bring more insight on how things work. Y-Combinator to achieve recursion, metacircular evaluator, declarative and logical programming are only some examples.

Eventually to dispel the rest of the magic there are solid 4 hours dedicated to implementation of Lisp on a register machine with further compilation and optimizations steps for performance and simple memory management techniques for the runtime. Remember, those are still from 1986 and the answer “Let us just implement it on JVM” didn’t exist.

## SICP and Me

I certainly benefited from lectures. I improved my understanding of basic things and ensured my knowledge of more advanced concepts. In addition learnt about things I couldn't even describe, much less use in the real world out there.

My experience was spoiled a little bit in the end when the topic pivoted from the promotion of high level concepts to low-level implementation details. In my opinion, too much time was dedicated to implementation (many hours were spent just writing code on a chalkboard).

But it makes sense since the implementation was the way to dismiss magic and make things transparent, less abstract. And let’s not forget it is an introductory course after all (MIT 6.001 indicates its level).

Never forget: primitives, means of combination and means of abstraction.

