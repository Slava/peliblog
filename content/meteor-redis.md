Title: Meteor + Redis = <3
Slug: meteor-redis
Date: 2014-08-08

In the period of time from June till mid-July 2014 we worked with [Justin Santa
Barbara][jsb] on the experimental [Redis][redis] support for [Meteor][meteor].

<iframe width="640" height="360" src="//www.youtube.com/embed/-Vnb8tjnE3k?rel=0" frameborder="0" allowfullscreen></iframe>

There is no doubt that Redis has become quite popular for a wide range of tasks.
Thanks to a big number of different data-structures and operators, everyone is
free to use Redis in any imaginable way: from message queue to distributed lock
and to main application data-store.

The last use-case, application data-store, was the most interesting to us as we
can easily synchronize data between clients and servers and give the same
semantics and commands as the original Redis in a JavaScript implementation for
the browser. That's exactly what we did: we have built an in-memory JS
implementation of Redis commands and called it [MiniRedis][miniredis] (the same
way we already have [MiniMongo][minimongo] for MongoDB). All the server-side
pub/sub logic is implemented in a separate package called
[Redis-Livedata][redis-livedata].

This allows us to give users of Meteor the same API on both client and server
with seamless data synchronization.

We did some work to make Redis-based structures work with other parts of Meteor
so right now you can easily publish data, subscribe to it (both client-server
and server-server), control access to data and write permissions, pass Redis
subset of data to Blaze Views to keep the DOM representation in sync with the
model.

After talking to users about their most common use-cases, we decided to focus on
Strings and Maps as those are usually the things you push to the clients as the
application data. For example, you would not push a huge Set to every client,
instead, you would just query on the server in an RPC or on demand.

After spending 1.5 month on this project, we are super happy with the results.
I [have given a talk about it][slava-talk] on Meteor Devshop July 2014 in SF and
the feedback so far has been positive. Justin and I are still thinking of
continuing to work on Redis integration if the community wants it.

Also checkout [another Devshop talk][jsb-talk] by Justin Santa Barbara on Meteor
Devshop May 2014 that presents a different approach to the integration.

Simply speaking, this work is nothing amazing but a good show-case that
the integration of other data-stores shouldn't have any problems with Meteor
specifically.

[miniredis]: https://github.com/meteor/miniredis
[minimongo]: https://github.com/meteor/meteor/tree/devel/packages/minimongo
[redis-livedata]: https://github.com/meteor/redis-livedata
[jsb]: https://twitter.com/justinsantab
[redis]: http://redis.io
[meteor]: https://www.meteor.com
[slava-talk]: https://www.youtube.com/watch?v=-Vnb8tjnE3k&list
[jsb-talk]: https://www.youtube.com/watch?v=T7-_Nc6zTH0

