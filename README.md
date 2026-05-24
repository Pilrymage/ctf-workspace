# ctf_lib

在 Kali-linux WSL 里实作，因为 Crypto 的科学软件需要 Conda 以及 Linux 环境。
同理， `pwntools` 等等在 Linux 内核环境下能发挥更大作用。
本仓库所引用的安全工具的 Python 依赖来自于 [pwn.college](pwn.college) 的 Dojo 里自动为每位用户生成的环境。具体参见： [这里](https://github.com/pwncollege/dojo/blob/master/workspace/additional/additional.nix)。用它们来作为你的 CTF 的基础。

推荐使用 VSCode Remote Explorer 连接并做题。
同时，方便下载比赛题目，你可以文件浏览器里指定一个网络位置（Network Location）。
比如，`\\wsl$\Kali-linux\home\<YOUR_HOME>\ctf-workspace` 直接跳转到 Workspaces 中。
由于文件系统的转换速度慢，该路径只负责存放题目文件，而 Linux shell 用于交互。

## 下载

```shell
git clone https://github.com/Pilrymage/ctf-workspace
```

如果在受限的环境中使用，只相当于单纯的引用头文件:
```
mkdir ctf_lib && cd ctf_lib && wget https://raw.githubusercontent.com/Pilrymage/ctf-workspace/refs/heads/main/ctf_lib/__init__.py
```

## 安装

安装依赖（非Crypto）：
```shell
uv venv
source .venv/bin/activate
uv pip install -e .
```

Crypto 依赖（Sage等）：
```sh
cd ./Crypto
pixi install
```

## 解题
1. 下载完毕后，你可以使用 `uv run python solve.py` 以及 `pixi run python solve.py` 来运行环境。
   它们会自动找到父路径下的解释器。

   这两个环境应当相互独立；你需要分别安装工具。
2. `challenges.csv` 记录当前比赛的题目。
   执行 `uv run python setup.py`，将从该 csv 文件中生成解题目录。
   
3. VSCode 可以指定 Python 解释器与环境，从而为开发环境提供辅助。
   `uv` 环境位于 `/.venv/bin/python`，`pixi` 环境位于 `/Crypto/.pixi/envs/default/bin/python`。