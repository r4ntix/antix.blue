error while loading shared libraries?
==========================================================================

:date: 2009-03-17
:category: Writings
:tags: linux, c, program, mysql
:slug: error-while-loading-shared-libraries
:author: r.4ntix Shawn
:summary: .so 动态库的加载问题


最近在看mysql 的api。用C 写和mysql 交互的代码，用的是xampp-linux-devel-1.7 包，全部的lib 和include 都放在了/opt 下面。编译时指定include 和lib 搜索位置都没问题。可在程序运行时./connect 时，出错：

.. code-block:: bash

    ./connect: error while loading shared libraries: libmysqlclient.so.15.0.0:cannot open shared object file: No such file or directory

查了一下，是ld(动态装载器)找不到libmysqlclient.so.15.0.0 的所在位置。解决办法：

.. code-block:: bash

    sudo touch /etc/ld.so.conf.d/mysql.conf
    sudo gedit /etc/ld.so.conf.d/mysql.conf

在里面写上libmysqlclient.so.15.0.0 所在的目录位置就可以，比如：/opt/lampp/lib/mysql 保存后，执行sudo ldconfig -v 就可以了。

.so 动态库的解决办法都一样 :)
