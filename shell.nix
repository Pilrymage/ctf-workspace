# shell.nix
let
  # 使用清华镜像下载 nixpkgs 的特定版本（24.05，稳定分支）
  nixpkgs = builtins.fetchTarball {
    url = "https://mirrors.tuna.tsinghua.edu.cn/nix-channels/nixpkgs-24.05-darwin/nixexprs.tar.xz";
    sha256 = "04aghwf3q2a353znfwgfx81z6c0nv7zwlh7w8fpi5syxbch28npj";  # 下面会教你怎么获取正确的 hash
  };
  pkgs = import nixpkgs {};
in

let
  # 如果你有 bata24-gef.nix，可取消下面两行的注释，并删掉 gef 的直接引用
  # bata24-gef = import ./bata24-gef.nix { inherit pkgs; };
  
  pythonPackages = ps: with ps; [
    angr
    asteval
    flask
    ipython
    jupyter
    pillow
    psutil
    pwntools
    pycryptodome
    pyroute2
    r2pipe
    requests
    ropper
    scapy
    selenium
    tqdm
  ];

  pythonEnv = pkgs.python3.withPackages pythonPackages;

  tools = with pkgs; {
    build = [ (lib.hiPrio gcc) (lib.lowPrio clang) clang-tools cmake gnumake nasm qemu rustup ];

    cli-tools = [ atuin bat delta hexyl hyperfine navi sd zoxide ];

    compress = [ gnutar gzip unzip zip ];

    # 这里 gef 是 nixpkgs 中的版本；如果你用自定义 bata24-gef，可替换为 [ bata24-gef ... ]
    debug = [ gef gdb ltrace pwndbg strace ];

    documentation = [ man-pages man-pages-posix ];

    editor = [ emacs gedit nano neovim vim ];

    exploit = [ aflplusplus rappel ropgadget sage ];

    fetch = [ fastfetch neofetch ];

    finder = [ broot dust eza fd fzf ripgrep ripgrep-all ];

    lsp = [ ruff ];

    # 使用 nixpkgs 提供的版本；有自定义文件时可换为 [ burpsuite ... ]
    network = [ netcat-openbsd nmap tcpdump termshark tshark wireshark ];

    # 同理，用 nixpkgs 版本代替 ghidra / ida-free / binaryninja-free 可能不存在或需额外许可
    reverse = [ cutter file pkgs.ghidra radare2 ];

    shells = [ fish nushell oh-my-zsh starship zsh ];

    system = [ bottom firejail htop ncdu nftables openssh rsync ];

    terminal = [ kitty.terminfo screen tmux zellij ];

    web = [ firefox geckodriver ];
  };

in
pkgs.mkShell {
  name = "pwncollege-ctf-env";

  # 直接将所有软件包放入 buildInputs
  buildInputs =
    [ (pkgs.lib.hiPrio pythonEnv) ]
    ++ tools.build
    ++ tools.cli-tools
    ++ tools.compress
    ++ tools.debug
    ++ tools.documentation
    ++ tools.editor
    ++ tools.exploit
    ++ tools.fetch
    ++ tools.finder
    ++ tools.lsp
    ++ tools.network
    ++ tools.reverse
    ++ tools.shells
    ++ tools.system
    ++ tools.terminal
    ++ tools.web;

  shellHook = ''
    echo "🎯 pwn.college CTF 环境已加载"
  '';
}