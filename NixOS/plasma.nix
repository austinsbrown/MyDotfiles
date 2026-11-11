{ config, pkgs, ... }:

{
    services = 
    {
        desktopManager.plasma6.enable = true;
        displayManager.plasma-login-manager.enable = true;
    };
    
    programs.partition-manager.enable = true;

    environment.systemPackages = with pkgs; 
	[
		konsave
    ];

    environment.plasma6.excludePackages = with pkgs.kdePackages; 
    [
        kate
        konsole
        plasma-systemmonitor
    ];
}
