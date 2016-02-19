linux 下mp3 显示乱码
==================================

:date: 2008-09-28
:category: Writings
:tags: ubuntu, linux, mp3, id3tag
:slug: linux-remove-mp3-id3-tag
:author: r.4ntix Shawn
:summary: 写了个bash 脚本删除ID3 Tag


我的audacious，还有其他的一些音乐播放器对于一些mp3 的标题一直显示乱码，全是ID3 tag 惹的祸。一气之下，批量删除mp3 的ID3 tag 之。

.. code-block:: bash

    #!/bin/bash

    # 需要安装mid3v2 ， 执行sudo apt-get install python-mutagen

    help()
    {
        cat << HELP
            deltag -- can delete tag of mp3

            USAGE: deltag [-h] folder
            OPTIONS: -h help text
            EXAMPLE: deltag "/home/Xuange/Music/"

            ==>will delete all tag of mp3 from /home/Xuange/Music/  !
            (: 能自动遍历所有子目录中的mp3文件。:)

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

    if [ -d "$1" ]; then
        echo "deleting tag of mp3 ...."
        find "$1" -name "*.[Mm][Pp]3" -type f -print | sed 's/^/"/;s/$/"/' | xargs mid3v2 -D
    else
        error "error: no such dir $1. -h for help"
    fi

    exit 0
