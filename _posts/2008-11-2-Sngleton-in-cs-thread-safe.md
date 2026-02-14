---
hidden: true
title: Singleton in C# thread-safe
date: 2009-11-02 15:47:13
tags:
    - pattern
    - singleton
    - thread-safe
    - .net
    - csharp
categories:
    - programming
    - .net
permalink: /2009/11/02/except-with-linq
---

<a target="_blank" href="{{ site.url }}/assets/imgs/posts/7444.singleton_78195B3B.jpg">
<img src="{{ site.url }}/assets/imgs/posts/7444.singleton_78195B3B.jpg" alt="Singleton" border="0" title="singleton" style="display:inline;border-width:0;" /></a>


everyone knows the implementation of singleton pattern, nothing new under the sun:

* private instance
* private constructor
* public method that controls if the instance is null (in this case initialize it),and returns the instance

the code will be similar to this

{% highlight cs %}

public Singleton
{
    private Singleton instance = null;
    private Singleton() { }
    public Singleton GetIstance()
    {
           if (instance == null)
                  instance = new Singleton();
           return instance;
    }
}

{% endhighlight %}


Well I learned,with my regret, that this kind of approach is not thread-safe,ie: in multi-threaded environment, two threads simultaneously ask an instance, and the operating system runs the context-switch, just after the if, and so before you make a new, then I’ll have two instances, of which only one is valid (the second)

The first solution that everyone uses is:

{% highlight cs %}

public sealed class Singleton
{
   private static volatile Singleton _instance = null;
        private Singleton() { }

        public static Singleton GetIstance()
        {
            if (_instance == null)
            {
                lock(typeof(Singleton))
                {
                    if (_instance == null)
                    {
                        _instance = new Singleton();
                    }
                }
            }
            return _instance;
        }
    }
{% endhighlight %}

Essentially,in the worst case of context-switch before the new, (in this case possible only before the lock), we check by the second if that the first thread receives the instance created by the second thread.

Beautiful... but unwatchable!!! I have to check in two consecutive times, the same condition. Operation that will not be optimized at compile time, because of the little word "volatile" ( topic of other posts if it is the case) in declaration of the static instance .

Can appear that this is the right direction to follow, for the concept "I want something robust, so it will be increasingly difficult" ,but the easiest solution is this:

{% highlight cs %}

public sealed class Singleton
{
    public static readonly Singleton = new Singleton();
    private Singleton() { }
}
{% endhighlight %}

Because the initialization of static members are thread-safe in .Net Framework

See you soon

E.