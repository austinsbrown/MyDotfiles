#!/usr/bin/bash

# perform updates
sudo pacman -Syu

# install grub
sudo pacman -S grub os-prober
sudo grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
sudo os-prober
sudo grub-mkconfig -o /boot/grub/grub.cfg

# install yay
sudo pacman -S --needed git base-devel
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
cd ..

mkdir ~/.config

# install display stuff
sudo pacman -S sddm
sudo systemctl enable sddm.service
sudo pacman -S qt5-graphicaleffects qt5-quickcontrols2 qt5-svg
sudo cp sddm.conf /etc
sudo cp -r sddm/* /usr/share/sddm/themes/


# bspwm
sudo pacman -S bspwm sxhkd
cp -r bspwm ~/.config/
chmod +x ~/.config/bspwm/bspwmrc # make it executable
cp -r sxhkd ~/.config/
chmod +x ~/.config/sxhkd/sxhkdrc # make it executable


# copy fonts
sudo cp -r fonts/* /usr/share/fonts

# copy themes
sudo cp -r themes/ /usr/share/themes/


sudo pacman -S polybar
sudo pacman -S pacman-contrib
cp -r polybar ~/.config/

sudo pacman -S picom
cp -r picom ~/.config/

# install nitrogen
sudo pacman -S nitrogen
sudo mkdir /usr/share/backgrounds
sudo cp -r backgrounds/* /usr/share/backgrounds
mkdir ~/.config/nitrogen
cp -r nitrogen/* ~/.config/nitrogen

# neofetch
cp -r neofetch ~/.config

# install kitty
sudo pacman -S kitty
cp -r kitty ~/.config

# install rofi
sudo pacman -S rofi
cp -r rofi ~/.config/

# install vbox stuff
sudo pacman -S virtualbox-guest-utils
sudo systemctl enable vboxservice.service

# install zsh and starship. copy my .zshrc over
sudo pacman -S zsh
curl -sS https://starship.rs/install.sh | sh
cp .zshrc ~/
chsh -s $(which zsh) # change default shell

# install msc. apps
sudo pacman -S vim ranger firefox neofetch reflector rsync thunar lxappearance
yay -S visual-studio-code-bin