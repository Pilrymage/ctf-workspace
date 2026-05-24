#!/bin/bash
cat << EOF >> /etc/nix/nix.conf
substituters = https://mirrors.tuna.tsinghua.edu.cn/nix-channels/store https://cache.nixos.org/

trusted-public-keys = cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY=
EOF

usermod -aG nix-users $(whoami)

systemctl restart nix-daemon