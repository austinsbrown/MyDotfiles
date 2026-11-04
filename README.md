# MyDotfiles

My personal Linux configs, grouped by the environment they're for.

| Folder | What it is |
|--------|------------|
| [`NixOS/`](NixOS) | NixOS system config for my main machine: GNOME and KDE Plasma 6, Nvidia PRIME offload, Steam/gamemode and Podman |
| [`Common/`](Common) | Configs shared across setups: fish, kitty and wallpapers |
| [`Plasma-Everblush/`](Plasma-Everblush) | An Everblush theme set for KDE Plasma 6 |
| [`BSPWM/`](BSPWM) | Legacy Arch Linux setup with bspwm, sxhkd, polybar, rofi and picom |
| [`WSL/`](WSL) | zsh (oh-my-zsh) and alacritty configs for WSL |

## NixOS

`configuration.nix` is the entry point. It imports one module per concern:

- `gnome.nix`: GNOME without the core app suite, plus shell extensions
- `plasma.nix`: Plasma 6 and konsave
- `nvidia-hybrid.nix`: Nvidia driver with PRIME offload. Check the bus IDs for your hardware.
- `flatpak.nix`: declarative Flatpak management (disabled by default)

`hardware-configuration.nix` isn't in the repo. Use the one NixOS generates for your machine.

```bash
sudo cp NixOS/*.nix /etc/nixos/
sudo nixos-rebuild switch
```

## Common

- **fish** (`Common/fish/config.fish` → `~/.config/fish/`): sets up starship, eza aliases and a few git shortcuts.
- **kitty** (`Common/kitty/` → `~/.config/kitty/`): `kitty.conf` takes its colors from an included theme file. To switch themes, change `include everblush_theme.conf` to `catppuccin_mocha_theme.conf`.
- **Wallpapers** (`Common/Wallpapers/`): wallpaper collection.

## Plasma-Everblush

A Plasma 6 port of the Everblush XFCE rice. It includes a color scheme, a Plasma Style, an Aurorae window decoration, Konsole colors and an icon overlay on Tela.

```bash
Plasma-Everblush/install.sh           # install into ~/.local/share
Plasma-Everblush/install.sh --apply   # install and apply to the running session
```

See [`Plasma-Everblush/README.md`](Plasma-Everblush/README.md) for details and for how to regenerate the SVGs, and [`PALETTE.md`](Plasma-Everblush/PALETTE.md) for the colors.

## BSPWM (legacy)

`BSPWM/install.sh` installs packages with pacman/yay on Arch and copies the configs into `~/.config`. It hasn't been kept up to date since fish, kitty and the wallpapers moved to `Common/`, so check the paths before running it.
