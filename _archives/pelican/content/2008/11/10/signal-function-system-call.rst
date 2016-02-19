signal(sig, function) 系统调用
======================================================

:date: 2008-11-10
:category: Writings
:tags: c, program
:slug: signal-function-system-call
:author: r.4ntix Shawn
:summary: 解析signal 系统调用

.. role:: c(code)
   :language: c
..


在这星期《操作系统实验指导》上看到了这样一个系统调用：:c:`signal(sig, function)`，呵呵，很好奇，因为每次这课的系统调用都说得很不清楚，连函数原型也没有。所以导致很多同学写的(也可能是抄的..)程序编译不成功，即使编译成功了程序也出错。

于是翻了翻书，书上说这个系统调用的函数原型是 :c:`void (*signal (int sig, void (*func) (int))) (int);`，更是一惊，这样的函数原型在学校这种SB 课本上是很少见的，可能有些同学看都看不懂，更别说，好好的调用了。当然 :c:`<signal.h>` 头文件(跟进去看看就知道了，老外还真细心)为代码用户解决了 :c:`conversion from ‘int (*)(int)’ to ’void (*)(int)’` 这样的问题，虽然能成功编译文件，但编译时照样会出现警告！

当然如果你认为“警告”无关紧要的话，你就去死吧。0 warning，0 error ，才是我的追求。

:c:`void (*signal (int sig, void (*func) (int))) (int);` 的原型其实是这样的 :c:`void (*p) (int);`，有点熟悉了吧？再深入一点 :c:`signal (int sig, void (*func) (int));`，会引出一个问题，如果 :c:`*func` 函数是 :c:`int (*func) (int)` 的怎么办？很多人一不小心就会写成这样。需要强制转换对吧？应该出现ERROR，但为什么，还能编译成功呢？进去 :c:`<signal.h>` 头文件看看，在75行：

.. code-block:: c

    /* Type of a signal handler.  */
    typedef void (*__sighandler_t) (int);
    extern __sighandler_t __sysv_signal (int __sig, __sighandler_t __handler)
      __THROW;

原来人家都把强制转换做好了的。
我们也可以这样，显示的强制转换：

.. code-block:: c

    signal (SIGINT, (void (*)(int))func);
    /* 或者可读性好一些的：*/
    typedef void (*func_t)(int);
    ...
    signal (SIGINT, (func_t)func);

好了，现在来对这个typedef 进行理解吧，直接看《THE C PROGRAMMING LANGUAGE》 Page.147

.. code-block:: c

    typedef int (*PFI) (char *, char *);
    /*
     * creates the type PFI, for ''pointer to function (of two char * arguments) returning int,'' which can be used in contexts like
     * PFI strcmp, numcmp;
     */

现在应该完全理解这个 :c:`signal(sig, function)` 系统调用了吧。
