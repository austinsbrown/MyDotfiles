{ config, pkgs, ... }:

{
	##### Enable the GNOME Desktop Environment. #####
	services.desktopManager.gnome.enable = true;

	# To disable installing GNOME's suite of applications
	# and only be left with GNOME shell.
	services.gnome.core-apps.enable = false;
	services.gnome.core-developer-tools.enable = false;
	services.gnome.games.enable = false;
	environment.gnome.excludePackages = with pkgs; [gnome-tour];

    environment.systemPackages = with pkgs; 
	[
		gnomeExtensions.appindicator
		gnomeExtensions.blur-my-shell
		gnomeExtensions.caffeine
		gnomeExtensions.dash-to-dock
        gnomeExtensions.desktop-icons-ng-ding
		gnomeExtensions.gamemode-shell-extension
        gnomeExtensions.just-perfection
		gnomeExtensions.user-themes
        gnome-software
        gnome-tweaks
        gnome-terminal
    ];
}

