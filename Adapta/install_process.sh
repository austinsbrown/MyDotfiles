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



#install nitrogen
sudo pacman -S nitrogen
sudo cp -r backgrounds/* /usr/share

sudo pacman -S alacritty


#install zsh and oh-my-zsh
sudo pacman -S zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"


