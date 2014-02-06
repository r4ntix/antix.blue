C 指针两种不常用法
============================

:date: 2007-10-28
:category: Writings
:tags: c, program
:slug: c-pointers-two-skills
:author: r.4ntix Shawn
:summary: 学C 的笔记

.. role:: c(code)
   :language: c
..


C 语言中，两种不常用的指针用法，及其定义形式：

One
------

.. code-block:: c

    int Print (int (*p)[2]) // 此时，*p 指向一个具有2个元素的一维数组
    {   // *p 相当与*arry，代表arry 数组的0行0列的首地址
        // pass
    }

    int main()
    {
        int arry[3][2]={{1,2},{3,4},{5,6}}; // 定义一个arry 二维数组
        Print(arry);                        // 将arry数组的首地址，递交给Print() 函数
        return 0;
    }
..

注：用好了，就简化了对二维数组的调用了哦，仔细想想吧。

Two
------

.. code-block:: c

    int compare(int x,int y)
    {
        // pass
    }

    int (*p)(int x,int y) // 定义一个指向函数的指针，函数返回值为 int 型
    {
        // pass
    }

    int main()
    {
        int num1,num2;
        p=compare;          // 将compare()函数的 首地址，赋予指针*p
        compare(num1,num2);
        (*p)(num1,num2);    // 此时，(*p)(num1,num2) 与compare(num1,num2) 等价
        return 0;
    }
..

注：若把这种方法用在子函数的函数参数列表中，会有意想不到的好处。

:c:`void proccess(int x,int y,int (*p)(int,int))` 想到了什么没有？WoW，通用函数 :)
