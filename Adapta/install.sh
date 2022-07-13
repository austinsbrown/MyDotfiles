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

# make config folder in home directory
mkdir ~/.config

read -p "Is this a virtual machine? (y/n) " yn
case $yn in
    [yY] ) sudo pacman -S virtualbox-guest-utils;
         sudo systemctl enable vboxservice.service;;
    [nN] ) ;;
    * )  ;;
esac

# install everything else
sudo pacman -S  sddm bspwm sxhkd polybar picom nitrogen kitty rofi \
                zsh vim ranger firefox neofetch reflector rsync \
                thunar lxappearance pacman-contrib fish

yay -S visual-studio-code-bin

# fix dual boot time issue
sudo timedatectl set-local-rtc 1

# set up display stuff
sudo systemctl enable sddm.service
sudo pacman -S qt5-graphicaleffects qt5-quickcontrols2 qt5-svg
sudo cp sddm.conf /etc
sudo cp -r sddm/* /usr/share/sddm/themes/

# set up bspwm
cp -r bspwm ~/.config/
chmod +x ~/.config/bspwm/bspwmrc # make it executable
cp -r sxhkd ~/.config/
chmod +x ~/.config/sxhkd/sxhkdrc # make it executable

# copy fonts
sudo cp -r fonts/* /usr/share/fonts

# copy themes
mkdir /usr/share/themes
sudo cp -r themes/* /usr/share/themes/

# set up polybar
cp -r polybar ~/.config/

# set up picom
cp -r picom ~/.config/

# set up nitrogen
sudo mkdir /usr/share/backgrounds
sudo cp -r backgrounds/* /usr/share/backgrounds
mkdir ~/.config/nitrogen
cp -r nitrogen/* ~/.config/nitrogen

# neofetch
cp -r neofetch ~/.config

# install kitty
cp -r kitty ~/.config

# install rofi
cp -r rofi ~/.config/

# set up fish and starship
curl -sS https://starship.rs/install.sh | sh
mkdir ~/.config/fish
cp -r fish/* ~/.config/fish
chsh -s $(which fish) # change default shell
