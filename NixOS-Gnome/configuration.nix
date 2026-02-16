# Edit this configuration file to define what should be installed on
# your system.  Help is available in the configuration.nix(5) man page
# and in the NixOS manual (accessible by running ‘nixos-help’).

{ config, pkgs, ... }:

{
	imports =
	[ # Include the results of the hardware scan.
		./hardware-configuration.nix
		# Include script for declarative flatpack managment
		./flatpak.nix
	];

	# Bootloader.
	boot.loader.systemd-boot.enable = true;
	boot.loader.efi.canTouchEfiVariables = true;

	#### Nvidia Setup ####
	# Enable OpenGL
	hardware.graphics = 
	{
		enable = true;
	};

	services.xserver.videoDrivers = ["nvidia"];
	hardware.nvidia = 
	{
		# Modesetting is required.
    	modesetting.enable = true;

		# Nvidia power management. Experimental, and can cause sleep/suspend to fail.
		# Enable this if you have graphical corruption issues or application crashes after waking
		# up from sleep. This fixes it by saving the entire VRAM memory to /tmp/ instead 
		# of just the bare essentials.
		powerManagement.enable = false;

		# Fine-grained power management. Turns off GPU when not in use.
		# Experimental and only works on modern Nvidia GPUs (Turing or newer).
		powerManagement.finegrained = false;

		# Use the NVidia open source kernel module (not to be confused with the
		# independent third-party "nouveau" open source driver).
		# Support is limited to the Turing and later architectures. Full list of 
		# supported GPUs is at: 
		# https://github.com/NVIDIA/open-gpu-kernel-modules#compatible-gpus 
		# Only available from driver 515.43.04+
		open = false;

		# Enable the Nvidia settings menu,
		# accessible via `nvidia-settings`.
		nvidiaSettings = true;

		# Optionally, you may need to select the appropriate driver version for your specific GPU.
		package = config.boot.kernelPackages.nvidiaPackages.stable;
	};

	hardware.nvidia.prime = 
	{
		offload = 
		{
			enable = true;
			enableOffloadCmd = true;
		};
		
		# Make sure to use the correct Bus ID values for your system!
		# Watch out for the formatting; convert them from hexadecimal to decimal, 
		# remove the padding (leading zeroes), replace the dot with a colon, then add them like this: 

		# intelBusId = "PCI:0:2:0";
		nvidiaBusId = "PCI:1:0:0";
		amdgpuBusId = "PCI:101:0:0";
	};

	networking.hostName = "asb-nixos"; # Define your hostname.
	# networking.wireless.enable = true;  # Enables wireless support via wpa_supplicant.

	# Configure network proxy if necessary
	# networking.proxy.default = "http://user:password@proxy:port/";
	# networking.proxy.noProxy = "127.0.0.1,localhost,internal.domain";

	# Enable networking
	networking.networkmanager.enable = true;

	# Set your time zone.
	time.timeZone = "America/Chicago";

	# Select internationalisation properties.
	i18n.defaultLocale = "en_US.UTF-8";

	i18n.extraLocaleSettings = 
	{
		LC_ADDRESS = "en_US.UTF-8";
		LC_IDENTIFICATION = "en_US.UTF-8";
		LC_MEASUREMENT = "en_US.UTF-8";
		LC_MONETARY = "en_US.UTF-8";
		LC_NAME = "en_US.UTF-8";
		LC_NUMERIC = "en_US.UTF-8";
		LC_PAPER = "en_US.UTF-8";
		LC_TELEPHONE = "en_US.UTF-8";
		LC_TIME = "en_US.UTF-8";
	};

	# Enable the X11 windowing system.
	services.xserver.enable = true;

	##### Enable the GNOME Desktop Environment. #####
	services.displayManager.gdm.enable = true;
	services.desktopManager.gnome.enable = true;

	# To disable installing GNOME's suite of applications
	# and only be left with GNOME shell.
	services.gnome.core-apps.enable = false;
	services.gnome.core-developer-tools.enable = false;
	services.gnome.games.enable = false;
	environment.gnome.excludePackages = with pkgs; [gnome-tour];

	# Enable Flatpaks
	services.flatpak.enable = true;

	# Configure keymap in X11
	services.xserver.xkb = 
	{
		layout = "us";
		variant = "";
	};

	# Enable CUPS to print documents.
	services.printing.enable = true;

	# Enable sound with pipewire.
	services.pulseaudio.enable = false;
	security.rtkit.enable = true;
	services.pipewire = 
	{
		enable = true;
		alsa.enable = true;
		alsa.support32Bit = true;
		pulse.enable = true;
		# If you want to use JACK applications, uncomment this
		#jack.enable = true;

		# use the example session manager (no others are packaged yet so this is enabled by default,
		# no need to redefine it in your config for now)
		#media-session.enable = true;
  	};

	# Enable touchpad support (enabled default in most desktopManager).
	# services.xserver.libinput.enable = true;

	# Install fish
	programs.fish.enable = true;

	# Define a user account. Don't forget to set a password with ‘passwd’.
	users.users.austinsbrown = 
	{
		isNormalUser = true;
		description = "austinsbrown";
		extraGroups = [ "networkmanager" "wheel" ];
		shell = pkgs.fish;
		packages = with pkgs; [];
	};

	# Allow unfree packages
	nixpkgs.config.allowUnfree = true;

	# List packages installed in system profile. To search, run:
	# $ nix search wget
	environment.systemPackages = with pkgs; 
	[
		vim
		gnome-terminal
		git
		lshw
		wget
		nautilus
		gnome-tweaks
		baobab
		gnome-software
		parted
		gparted
		vlc
		resources
		nerd-fonts.jetbrains-mono
		gnomeExtensions.just-perfection
		gnomeExtensions.blur-my-shell
		gnomeExtensions.caffeine
		gnomeExtensions.dash-to-dock
		gnomeExtensions.user-themes
		gnomeExtensions.appindicator
	];


	# Enable the OpenSSH daemon.
	# services.openssh.enable = true;s

	# This value determines the NixOS release from which the default
	# settings for stateful data, like file locations and database versions
	# on your system were taken. It‘s perfectly fine and recommended to leave
	# this value at the release version of the first install of this system.
	# Before changing this value read the documentation for this option
	# (e.g. man configuration.nix or on https://nixos.org/nixos/options.html).
	system.stateVersion = "25.11"; # Did you read the comment?
}
