# ctf_lib

这是一个个人用于解决 CTF 的环境。

在 Kali-linux WSL 里实作，因为 Crypto 的科学软件需要 Conda 以及 Linux 环境。
同理， `pwntools` 等等在 Linux 内核环境下能发挥更大作用。
本仓库所引用的安全工具的 Python 依赖来自于 [pwn.college](pwn.college) 的 Dojo 里自动为每位用户生成的环境。
具体参见： [这里](https://github.com/pwncollege/dojo/blob/master/workspace/additional/additional.nix)。
用它们来作为你的 CTF 的基础。

推荐使用 VSCode Remote Explorer 连接并做题。
比如，打开每道题目的 Jupyter Notebook，然后在本地 VSCode Jupyter 里读取 ipynb 文件。

同时，方便下载比赛题目，你可以文件浏览器里指定一个网络位置（Network Location）。
比如，`\\wsl$\Kali-linux\home\<YOUR_HOME>\ctf-workspace` 直接跳转到 Workspaces 中。
由于文件系统的转换速度慢，该路径只负责存放题目文件，而 Linux shell 用于交互。

## 下载

在你的 Linux 发行版里安装 Nix 包管理器，然后执行以下命令 ：

```shell
git clone https://github.com/Pilrymage/ctf-workspace && cd ctf-workspace && sudo ./setup.sh
nix-shell
```

它会按照 `shell.nix` 文件的内容复刻题目的环境。

如果在受限的环境中使用，只相当于单纯的引用头文件，你需要确保依赖的完整:

```shell
mkdir ctf_lib && cd ctf_lib && wget https://raw.githubusercontent.com/Pilrymage/ctf-workspace/refs/heads/main/ctf_lib/__init__.py
```

## 解题
1. 在包含 `shell.nix` 的目录打开 nix-shell，等待安装完毕。
   这两个环境应当相互独立；你需要分别安装工具。

2. `challenges.csv` 记录当前比赛的题目。
   执行 `python challenges.py`，将从该 csv 文件中生成解题目录，并为每一个题目目录放置 template 文件夹里的所有内容。
   这里使用 Jupiter Notebook。当你在 Nix Shell 内部启动 `jupyter-notebook` 时，你可以在本地的 VS Code 里连接其内核。
   
3. VSCode 可以指定 Python 解释器与环境，从而为开发环境提供辅助。

