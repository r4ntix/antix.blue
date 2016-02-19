Discuz! 6.x/7.x SODB-2008-13 Check
====================================================================

:date: 2008-11-17
:category: Writings
:tags: discuz, security, poc, bash
:slug: discuz-6.x-7.x-sodb-2008-13-bash-check
:author: r.4ntix Shawn
:summary: SODB-2008-13 bash scan poc


好吧，我承认上个周末，我并没有像往常一样玩一整天的PES2009。实际上在星期六，我用早上的时间看了正则，下午写下了Discuz! 6.x/7.x SODB-2008-13 Check，这个东东。在我写的前一天heige 发布了exp，不得不说这个是对我的一个诱惑。因为很久没看到DZ 出这么严重的洞洞了 :(

说明一下，这不是首发，写出来的那天就被一个朋友在他的blog 上发出来了。不过，发出来只是一个“bug”版本，比如说抓取的结果并不是很好，还有关于google 自动处理机的一些问题。主要的是，并没有整合那个exp，整合的当然不能乱发了。我还是把这个“bug”代码帖一下，记录一下。

.. code-block:: bash

    #!/bin/bash

    # Discuz! 6.x/7.x SODB-2008-13 Check
    # 文件中google_page_count 参数是 google 搜索结果的页数，大于0就可以，太大了，google 会认为是自动机而停止处理！
    # 如果修改了搜索的关键字，抓取链接需自行处理，本脚本只是简单测试
    #
    #                              date: 11.15.2008


    help()
    {
       cat < < HELP
    #===================================================#
    Discuz! 6.x/7.x SODB-2008-13 Check
    +---------------------------------------------------------+
    USAGE: dzcheck [-h] google_page_count
    OPTIONS: -h help text
    EXAMPLE: ./dzcheck 10
    +---------------------------------------------------------+
                                    date: 11.15.2008
    #===================================================#

    HELP
       exit 0
    }

    error()
    {
       # print an error and exit
       echo "$1"
       exit 1
    }

    # the main
    if [ "$#" -lt 1 ]; then
        help
    fi

    while [ -n "$1" ]; do
    case $1 in
       -h) help;shift;; # function help is called
       --) shift;break;; # end of options
       -*) error "error: no such option $1. -h for help";;
       *) break;;
    esac
    done

    countPage=0
    flag=0
    while [ "$flag" -lt "$1" ]; do
        wget --no-cookies --user-agent="Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)" --referer="http://www.google.cn"  "http://www.google.cn/search?hl=zh-CN&newwindow=1&q=inurl:bbs/wap/index.php+Powered+by+Discuz!&start=$countPage&sa=N"  -O /tmp/t_url -T 7 -t 4
        for url in $(sed 's_<p><a [^>]*href="[^"]\+\/index\.php\?_\n&\n_g' /tmp/t_url | grep "<p><a href=" | awk -F"\"" '{print $2}')
        do
            wget --no-cookies --user-agent="Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)" --referer="http://www.google.cn" --post-data='action=register' -O /tmp/check -T 7 -t 4 "$url"
            if [ "$(grep "email" /tmp/check | wc -l)" != "0" ]; then
                echo "OK! $url "
                echo "OK : $url" >> urllist
            else
                echo "NO! $url "
            fi
        done
        countPage=$(($countPage+10))
        flag=$(($flag+1))
    done
    rm -r /tmp/t_url /tmp/check
    echo "开启WAP注册的结果URL列表保存在当前目录下urllist"

    exit 0
