rbenv/pyenv #1 eval "$(pyenv init -)" 做了什么
=================================================

:date: 2014-08-24
:category: Writings
:tags: rbenv, pyenv, bash, shell
:slug: rbenv-pyenv-init
:author: r.4ntix Shawn
:summary: rbenv/pyenv 系列文章#1: init 做了什么。

.. role:: bash(code)
   :language: bash
..


概述
------

`pyenv`_ 是我日常开发过程中常用来管理python 版本和virtualenv 的工具。甚至可以说，我几乎每天都在使用了 `pyenv`_ 的bash 环境下工作。

其实 `pyenv`_ 是从fork `rbenv`_ 而来，两者的核心代码完全一致。`rbenv`_ 是用来管理ruby environment 的，其作者是 `Basecamp <https://basecamp.com>`_ 的 `Sam Stephenson <https://github.com/sstephenson>`_ 。

有趣的是，rbenv/pyenv 是纯shell 脚本实现的，不依赖于ruby/python 本身。具体的实现过程也很精巧。现在基于Linux 的开发的工作，也基本上都绕不开python。就我所在的团队，包括测试的同学，也都开始使用 `pyenv`_ 来管理python 环境。

所以，是时候来更加的深入了解rbenv/pyenv 了。

在这里，我将以 `pyenv`_ 为例，分几篇文章来描述rbenv/pyenv 核心代码的具体实现，但是并不涉及ruby-build、pyenv-build 这样的plugin 实现。

.. _pyenv: https://github.com/yyuu/pyenv
.. _rbenv: https://github.com/sstephenson/rbenv

文件结构
--------------

如下图，pyenv 的文件结构是这样的：

.. image:: {attach}pyenv.png
   :class: th
   :width: 50%
   :alt: pyenv structure

1. shims 是pyenv 和用户交互的接口层。
    这里面存放了我们平时在pyenv shell 环境下所执行的python、pip 等命令文件。当然，这些名为python、pip 的命令文件「并不是真正的python、pip 执行文件」，而是负责命令中转调度的binstub files。

2. versions 是存放各个python 版本文件的地方。
    里面存放了我们installed 的「真正的python、pip 等文件」。

3. libexec 是pyenv 的核心代码目录。
    bin/pyenv 则直接软连接到了libexec/pyenv。我们平时所执行的 :bash:`pyenv *` 的命令，实际上最后都调用了libexec/pyenv-* 文件（除plugin/*/bin/pyenv-* 命令之外）。

    比如我们执行 :bash:`pyenv init -` 则实际调用为 :bash:`libexec/pyenv-init -` 。

4. plugin 是存放plugin 的目录。
    pyenv 安装时自带了一个叫做python-build 的plugin。它提供了我们安装和卸载python 时所用的 :bash:`pyenv install`、 :bash:`pyenv uninstall` 这两个命令。

    其他更多的插件，可看 `Plugins wiki page <https://github.com/yyuu/pyenv/wiki/Plugins>`_ ，这里面的 :bash:`pyenv-virtualenv` 插件可以用来管理virtualenv 环境。

5. hooks 并不存在叫做hooks 的目录。但是却是pyenv 很有用的一个功能。
    pyenv 提供了3个hook 点，分别为 :bash:`exec`、 :bash:`rehash`、 :bash:`which`。当在执行 :bash:`pyenv-exec`、 :bash:`pyenv-rehash`、 :bash:`pyenv-which` 时，则会调用hook files。

    这些hook files，可存放的目录为：

    .. code-block:: bash

        plugins/*/etc/pyenv.d:${PYENV_HOOK_PATH}:${PYENV_ROOT}/pyenv.d:/usr/local/etc/pyenv.d:/etc/pyenv.d:/usr/lib/pyenv/hooks

6. completions 是存放shell completion 的目录。
    目前支持的shell 为：bash、fish、zsh。

pyenv-init
----------

在安装完pyenv 之后，根据安装提示，我们需要在shell 的配置文件里，加入几行配置代码。以bash 为例：

.. code-block:: bash

    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"

其中前两行export 指令，设置了pyenv 的路径，并添加到我们的已有PATH 的最前面，以便我们执行pyenv 时，系统能自动从该路径下找到pyenv。

而最后一行 :bash:`eval "$(pyenv init -)"` 正是魔法的开始，pyenv 的初始化隐藏其中。

让我们来具体看看libexec/pyenv-init 的代码。

1. 获取到当前的shell name。

.. code-block:: bash

    if [ -z "$shell" ]; then
      shell="$(ps c -p "$PPID" -o 'ucomm=' 2>/dev/null || true)"
      shell="${shell##-}"
      shell="${shell%% *}"
      shell="$(basename "${shell:-$SHELL}")"
    fi

2. 创建shims、versions 目录。

.. code-block:: bash

    mkdir -p "${PYENV_ROOT}/"{shims,versions}

3. 打印设置shims path 到我们的$PATH 最前面。

.. code-block:: bash

    if [[ ":${PATH}:" != *:"${PYENV_ROOT}/shims":* ]]; then
      case "$shell" in
      fish )
        echo "setenv PATH '${PYENV_ROOT}/shims' \$PATH"
      ;;
      * )
        echo 'export PATH="'${PYENV_ROOT}'/shims:${PATH}"'
      ;;
      esac
    fi

这样的话，当我们输入执行python、pip 等命令时，shell 就会首先到shims 目录去寻找了。

4. 设置PYENV_SHELL 环境变量。

.. code-block:: bash

    case "$shell" in
    fish )
      echo "setenv PYENV_SHELL $shell"
    ;;
    * )
      echo "export PYENV_SHELL=$shell"
    ;;
    esac

5. 打印shell completion。

.. code-block:: bash

    completion="${root}/completions/pyenv.${shell}"
    if [ -r "$completion" ]; then
      case "$shell" in
      fish ) echo ". '$completion'" ;;
      *    ) echo "source '$completion'" ;;
      esac
    fi

6. 根据参数判断打印是否rehash。

.. code-block:: bash

    if [ -z "$no_rehash" ]; then
      echo 'pyenv rehash 2>/dev/null'
    fi

:bash:`pyenv rehash` 是pyenv 代码实现中最为核心的部分，它的作用是在shims 目录下生成正确的binstub files。

7. 打印一个名叫 **pyenv** 的shell 函数。

.. code-block:: bash

    # example for bash

    commands=(`pyenv-commands --sh`)
    cat <<EOS
    pyenv() {
      local command
      command="\$1"
      if [ "\$#" -gt 0 ]; then
        shift
      fi

      case "\$command" in
      ${commands[*]})
        eval "\`pyenv "sh-\$command" "\$@"\`";;
      *)
        command pyenv "\$command" "\$@";;
      esac
    }
    EOS
..

8. eval "$(pyenv init -)" 执行 :bash:`pyenv init -` 打印出来的代码。
    这里非常关键，在我们执行 :bash:`eval "$(pyenv init -)"` 时，最终eval 的正是 :bash:`pyenv-init` echo 出来的各个语句。而在第七部步时 :bash:`pyenv-init` echo 了一个名为 **pyenv** 的shell 函数。最终被eval 解析执行。

到这里我们已经明白，原来每次我们在bash 输入执行的pyenv 实际上都是这个叫做 **pyenv** 的shell 函数！

名为pyenv 的shell 函数
----------------------

在这个名为 **pyenv** 的shell 函数里，实际上将我们执行的 :bash:`pyenv *` 命令分为了两类：

1. rehash|shell
    当我们执行 :bash:`pyenv rehash`、 :bash:`pyenv shell` 时，通过eval 解析执行 :bash:`libexec/pyenv-sh-rehash`、 :bash:`libexec/pyenv-sh-shell` 命令输出的内容。

2. others
    除 :bash:`rehash|shell` 之外的 :bash:`pyenv *` 命令，通过command 传递给实际的libexec/pyenv 调度相应的 :bash:`pyenv-*` 执行。

关于 :bash:`command` 这个命令，是忽略shell 函数的，所以能正确的传递给真实的libexec/pyenv 执行：
    Runs command with arguments ignoring any shell function named command. Only shell builtin commands or commands found by searching the PATH are executed.

所以，当我们挥动手指，敲打出 :bash:`pyenv *` 命令并按下回车键时，在shell 里的实际执行流程为：

1. pyenv shell function
2. bin/pyenv(libexec/pyenv)
3. libexec/pyenv-*

就像是魔法一样。
