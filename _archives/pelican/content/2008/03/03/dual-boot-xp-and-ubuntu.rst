Ubuntu & XP 双系统
================================

:date: 2008-03-03
:category: Writings
:tags: system, linux, xp, ubuntu
:slug: dual-boot-xp-and-ubuntu
:author: r.4ntix Shawn
:summary: 装双系统并且在XP 下做GRUB 引导

.. role:: bash(code)
   :language: bash
..


现在，我的Ubuntu 7.10 已经很舒服的在我手上运行了。以前用过Ubuntu 6.10，所以从Windows 到Ubuntu  没什么不适应的。这个版本还是变化挺大的，界面越做越好了，和朋友一样，不准备改变默认的主题了，真的很漂亮，很清爽。 由于是第一次装双系统并且在XP 下做GRUB 引导，所以记录下来。

1. 在XP 下做GRUB 引导
    我选择在XP 下做GRUB 引导的原因很简单：如果重装XP 的话，能很方便的再做一次引导，而用Linux 的GRUB 去写MBR 的话，重装XP 后要引导Linux 很麻烦，因为MBR 被XP 重新修改了。

    我参考了一些资料，决定用GRUB4DOS，下载后只用从压缩包里解压两个文件(grldr 和menu.lst)放在C 盘根目录就可以，然后修改boot.ini 在最后另起一行添加 :bash:`C:\grldr="Ubuntu 7.10"`。

2. 安装Ubuntu
    具体的步骤就不说了，保证网络顺畅连接就可以(安装过程中要从网络下载安全更新和语言包)，全傻瓜式安装。分区自己注意就可以。

    重点是，将Linux 的GRUB 安装到根挂载区。如果默认不变，那么前面的GRUB4DOS 就白做了。进行到GRUB 安装界面时，按Advanced，把里面的内容从hd0 改成Ubuntu 所在的分区。接下来就自动安装了，泡杯咖啡吧，嘿嘿。安装完后，重启就可进入Linux 了。

3. 安装显卡驱动，解决声卡无声
    要玩比VISTA 还酷的3D 特效，当然要装好显卡的驱动。我的显卡是GF 7300 GT，安装命令如下：

    .. code-block:: bash

        sudo cp /etc/X11/xorg.conf /etc/X11/xorg.conf.bak 备份
        sudo apt-get install nvidia-glx-new   安装驱动
        sudo nvidia-glx-config enable   开启驱动
        sudo nvidia-xconfig –add-argb-glx-visuals –composite   开启3D特效
    ..

    我一次性成功。

    有很多人安装Ubuntu 完毕后，系统没有声音，我的ALC 883 声卡就受影响。我查了很多资料后发现，其实只要：
    :bash:`sudo gedit /etc/modprobe.d/alsa-base` 编辑alsa-base 文件，在最后加上一行 :bash:`options snd-hda-intel model=laptop-automute` 重启就可以了。嘿嘿，Ubuntu 启动时的鼓声还是挺不错的哦。

4. 其他的一些完善设置
    其他的就一些，常用的设置了，像播放器呀，字体美化，QQ 等等。
