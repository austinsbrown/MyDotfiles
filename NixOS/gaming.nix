{ config, pkgs, ... }:

{
	programs.gamemode.enable = true;
	programs.gamescope =
	{
		enable = true;
		capSysNice = false; # true would give gamescope higher CPU scheduling priority, but breaks running it inside Steam

		# Enable HDR (also applies to the Steam gamescope session)
		args = [ "--hdr-enabled" ];

		# Enable gamescope's Vulkan WSI layer
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

	environment.systemPackages = with pkgs;
	[
		protonup-ng
		mangohud
	];

	environment.sessionVariables = 
	{
    	STEAM_EXTRA_COMPAT_TOOLS_PATHS = 
			"\${HOME}/.steam/root/compatibilitytools.d";
	};
}
