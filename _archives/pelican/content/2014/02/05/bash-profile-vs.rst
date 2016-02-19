.bash_profile vs .bashrc
================================================

:date: 2005-07-25
:category: Translation
:tags: linux, unix, mac, bash, shell
:slug: bash-profile-vs
:author: Josh Staiger
:translator: r.4ntix Shawn
:summary: 对.bash_profile 和 .bashrc 的说明和建议

.. role:: bash(code)
   :language: bash
..

    原文：http://www.joshstaiger.org/archives/2005/07/bash_profile_vs.html

每当我工作在Linux、Unix 以及Mac OS X 下，想要为我的shell 设置PATH 和其他环境变量的时候，我总是忘记我究竟该编辑哪个bash 配置文件。应该编辑 ``.bash_profile`` 还是 ``.bashrc`` 呢？

实际上，你可以把你的bash 配置写到这两个配置文件中的任意一个，它们不存在的话则创建它。但是，为什么会存在两个不同的配置文件呢？他们的区别是什么呢？

根据bash 的 `man page <http://linux.die.net/man/1/bash>`_ 说明，``.bash_profile`` 是在使用 **登录式shell** 的时候执行的，而 ``.bashrc`` 则是在使用 **交互式非登录shell** 时执行。

什么是 **登录式shell** 和 **交互式非登录shell** ？
------------------------------------------------------------------------------------------

每当你直接坐在电脑前或者是远程使用ssh 通过console 使用账号和密码进行登录时：``.bash_profile`` 将在初始化命令提示符之前执行，完成shell 的配置。

但是，如果你已经登录你的电脑，在图形界面Gnome 或者KDE 下打开一个终端窗口(xterm)，这时 ``.bashrc`` 将在这个窗口命令提示符初始化之前执行，以完成shell 的配置。同时，当你在一个终端里执行 :bash:`/bin/bash` 时，``.bashrc`` 也将被执行。

为什么会存在两个不同的配置文件？
----------------------------------------------------

有时候，你想在你每次登录机器时，打印出机器的一些诊断信息(平均负载、内存使用率、当前用户等)，你可以通过配置 ``.bash_profile`` 来完成。但是，如果你使用 ``.bashrc`` 来配置的话，则会在每次打开终端窗口时都打印出这些信息来，而不仅仅只是在登录的时候。

Mac OS X —— 一个列外
--------------------------------------

Mac OS X 的Terminal.app 终端程序是个例外。它对每个新建的终端窗口，都默认以 **登录式shell** 方式打开，然后执行 ``.bash_profile`` 而不是 ``.bashrc`` 。虽然其他的GUI 终端模拟器也可以这样，但基本都不这么干。

建议
--------

大多数情况下没有人愿意同时维护两个不同的配置文件，来分别应对 **登录式shell** 和 **交互式非登录shell** ——这样的话，当你想设置PATH 时，你得同时在两个文件里都配置。其实，你可以通过在 ``.bash_profile`` 里引用 ``.bashrc``，然后在 ``.bashrc`` 里进行PATH 和其他配置。

将下面几行代码添加到你的 ``.bash_profile`` 文件里：

.. code-block:: bash

    if [ -f ~/.bashrc ]; then
        source ~/.bashrc
    fi

现在当你通过console 进行 **登录式shell** 时，``.bashrc`` 也将被执行了。
