{ config, pkgs, ... }:

{
	programs.gamemode.enable = true;
	programs.gamescope = 
    {
        enable = true;
        capSysNice = false; # Gives higher CPU scheduling priority

        # Enable HDR
        env = 
        {
            ENABLE_GAMESCOPE_WSI = "1";
        };
    };

    programs.steam = 
    {
  		enable = true;
		gamescopeSession.enable = true;
	};

    environment.systemPackages = with pkgs; [mangohud];
}

