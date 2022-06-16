# perform updates
sudo pacman -Syu

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


# bspwm
sudo pacman -S bspwm sxhkd

cp -r bspwm ~/.config/
chmod +x ~/.config/bspwm/bspwmrc # make it executable

cp -r sxhkd ~/.config/
chmod +x ~/.config/sxhkd/sxhkdrc # make it executable


# copy fonts
sudo cp -r fonts/* /usr/share/fonts


#install nitrogen
sudo pacman -S nitrogen
sudo mkdir /usr/share/backgrounds
sudo cp -r backgrounds/* /usr/share/backgrounds
mkdir ~/.config/nitrogen
cp -r nitrogen/* ~/.config/nitrogen


#install kitty
sudo pacman -S kitty
cp -r kitty ~/.config

#install vbox stuff
sudo pacman -S virtualbox-guest-utils
sudo systemctl enable vboxservice.service

#install zsh and starship. copy my .zshrc over
sudo pacman -S zsh
curl -sS https://starship.rs/install.sh | sh
cp .zshrc ~/
chsh -s $(which zsh) # change default shell
