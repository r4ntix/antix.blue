Ubuntu Upstart 基于事件的启动进程
============================================================

:date: 2009-01-08
:category: Writings
:tags: ubuntu, linux
:slug: ubuntu-upstart-event-based-init-daemon
:author: r.4ntix Shawn
:summary: Ubuntu 的下一代init 程序


昨晚上在看《开源世界的旅行手册》的时候，其「II.地理——第15章 基本系统——启动流程」中描述到：

1. 读取MBR 的信息，启动Boot Manager
2. 加载系统内核，启动init 进程
3. init 进程读取/etc/inittab 文件中的信息，并进入预设的运行级别，按顺序运行该运行级别对应文件夹下的脚本。脚本通常以start 选项启动，并指向一个系统中的程序。
4. 根据/etc/rcS.d/ 文件夹中对应的脚本启动Xwindow 服务器xorg
5. 启动登录管理器，等待用户登录

注意第3条，我在ubuntu 8.04 上并没有发现所谓的/etc/inittab 文件，在网上找了一些资料知道从ubuntu 6.10 开始，ubuntu 已经开始用Upstart 取代了传统的System V 的init daemon (Sysvinit)。于是随着这个好奇，找了一些资料了解到下一代init 程序，如：Upstart，initng 的发展，及其优势。主要看了Upstart 的资料，从官网上看，目前Upstart 的用户包括了：

* Ubuntu 6.10 and later
* Fedora 9 and later
* Debian experimental

总的来说，Upstart 这种基于事件的启动模式来说，优势是很明显的，很灵活。实质上，改变了linux 以往的runlevel 的模式。

资料：

1. http://upstart.ubuntu.com/
2. http://labs.chinamobile.com/community/my_blog/225/2804

`资料2 <http://labs.chinamobile.com/community/my_blog/225/2804>`_ 中有这么一句话：

    在/etc/event.d/rc? 文件中定义的rc? 工作会运行/etc/init.d/rc 脚本，这个脚本会运行链接到/etc/rc?.d 目录中的/etc/init.d 中的启动脚本，以模拟SysVinit 的行为。

实质上，/etc/rc?.d 目录中的文件，是到/etc/init.d 中启动脚本的一个符号链接(ln -s)，终归到底就是在/etc/init.d/ 目录的脚本执行。而这样做，却把/etc/init.d/ 中的脚本归类了，分为由不同的事件来驱动，并且排了个启动顺序。再次 见证linux 的文件管理方式的符号链接模式的便利，和灵活。赞一个～～

考试好无聊哦，咱想回家 ^_^
