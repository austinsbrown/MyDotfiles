{ config, pkgs, ... }:

{
	# Enable OpenGL
	hardware.graphics =
	{
		enable = true;
		enable32Bit = true;
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
		powerManagement.finegrained = true;

		# Use the NVidia open source kernel module (not to be confused with the
		# independent third-party "nouveau" open source driver).
		# Support is limited to the Turing and later architectures. Full list of
		# supported GPUs is at:
		# https://github.com/NVIDIA/open-gpu-kernel-modules#compatible-gpus
		# Only available from driver 515.43.04+
		# Must be true on Blackwell (RTX 50-series) and newer, which the proprietary module doesn't support.
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

		# Make sure to use the correct Bus ID values for your system! Find them with `lspci -D | grep -E "VGA|3D"`.
		# lspci prints hexadecimal: convert each part to decimal, remove the padding (leading zeroes)
		# and replace the dot with a colon. e.g. 0000:65:00.0 -> "PCI:101:0:0"

		# Use intelBusId instead of amdgpuBusId on machines with an Intel iGPU.
		# intelBusId = "PCI:0:2:0";
		nvidiaBusId = "PCI:1:0:0";
		amdgpuBusId = "PCI:101:0:0";
	};
}
