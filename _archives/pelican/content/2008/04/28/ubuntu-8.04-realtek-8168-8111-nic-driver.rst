Ubuntu 8.04 Realtek 8168/8111 网卡不能上网解决办法
============================================================================================

:date: 2008-04-28
:category: Writings
:tags: ubuntu, linux
:slug: ubuntu-8.04-realtek-8168-8111-nic-driver
:author: r.4ntix Shawn
:summary: 给官方驱动打Patch 解决


..

    2008年10月16日：官方已经修复了网卡驱动的问题。

一、确定你也遭受同样的问题
--------------------------------------------

确定你的网卡为Realtek 8168/8111网卡，可用lspci 查看。你的Ubuntu 内核为 2.6.24，似乎现在只有这个内核或者更高内核，出现死活不能上网的问题。包括在Win 下打开wake-on-lan after shutdown 为enable，也不能上网。看看你现在Ubuntu 的网卡驱动是不是r8169，这个驱动对Realtek 8168/8111 竟然不支持，有人在官方提交了BUG 报告了，但现在还没更新。

并且你试图自己下载8168的驱动，自己安装的时候，出现错误：

.. code-block:: bash

    xuange@R-desktop:/usr/src/r8168-8.005.00$ sudo make clean modules
    make -C src/ clean
    make[1]: Entering directory `/usr/src/r8168-8.005.00/src'
    rm -rf *.o *.ko *~ core* .dep* .*.d .*.cmd *.mod.c *.a *.s .*.flags .tmp_versions Module.symvers Modules.symvers rset
    make[1]: Leaving directory `/usr/src/r8168-8.005.00/src'
    make -C src/ modules
    make[1]: Entering directory `/usr/src/r8168-8.005.00/src'
    make -C /lib/modules/2.6.24-12-generic/build SUBDIRS=/src modules
    make[2]: Entering directory `/usr/src/linux-headers-2.6.24-12-generic'
    scripts/Makefile.build:41: /src/Makefile: No such file or directory
    make[3]: *** No rule to make target `/src/Makefile'. Stop.
    make[2]: *** [_module_/src] Error 2
    make[2]: Leaving directory `/usr/src/linux-headers-2.6.24-12-generic'
    make[1]: *** [modules] Error 2
    make[1]: Leaving directory `/usr/src/r8168-8.005.00/src'
    make: *** [modules] Error 2
    xuange@R-desktop:/usr/src/r8168-8.005.00$

现在，如果像我所说的一样，很不幸，你和我们一样，遇到了这个问题。 :(

二、解决办法
--------------------

你需要安装一个patch 软件包，可以叫别人下了后拷贝给你：`r8168-8.005.00版本驱动的Patch <http://forum.ubuntu.org.cn/download/file.php?id=32364&sid=2ada0f5b55bf226cab872bef441a6412>`_

下载Realtek 8168/8111网卡官方文件驱动，同样可以叫别人下了后拷贝给你，地址：
http://www.realtek.com.tw/downloads/downloadsView.aspx?Langid=1&PNid=13&PFid=5&Level=5&Conn=4&DownTypeID=3&GetDown=false

现在，我们可以动手了，自己编译驱动安装：

.. code-block:: bash

    tar xvjf r8168-8.005.00.tar.bz2

    # 解压r8168-8.005.00.tar.bz2后，将补丁文件r8168-8.005.00.hardy.diff.txt，放在./r8168-8.005.00/src 里。

    cd ./r8168-8.005.00/src
    patch < r8168-8.005.00.hardy.diff.txt
    cd ..
    make clean
    make modules
    sudo make install
    sudo depmod -a
    sudo insmod ./src/r8168.ko

OK！ 不用重启，看看，是不是能上网了？嘿嘿。 :)

最后，感谢energymomentum 发的补丁文件。期待官方升级驱动...

补丁来源：`《r8168 driver patch for 2.6.24 kernel and higher》 <http://ubuntuforums.org/showthread.php?p=4718501>`_
