# OptimusUI

OptimusUI is a graphical user interface for prime-select.  
It allows a Laptop or Desktop system with an integrated GPU and a dedicated GPU to switch between these two. By either
running entirely on the dGPU, the iGPU or using nVidia's Offloading technology.

To learn more about prime-select take a look at:

- openSUSE: [SUSEPrime](https://github.com/openSUSE/SUSEPrime) (Supported)
- Ubuntu/Debian: [nvidia-prime](https://wiki.ubuntuusers.de/Hybrid-Grafikkarten/PRIME/) (Supported)

Currently not supported because the binary name is different from what OptimusUI expects

- Fedora: [FedoraPrime](https://github.com/bosim/FedoraPrime)
- Arch Linux: [nvidia-prime-select](https://github.com/wildtruc/nvidia-prime-select) (Note: There are two packages
  nvidia-prime and nvidia-prime-select (AUR) they are NOT the same!)

## Requirements

This application aims to be as simple as possible. this also includes it's dependencies.  
But there are still various things which can not be distributed by this application.
The following needs to be present on the target system:

- proprietary nvidia driver version >= 390
- suse-prime or nvidia-prime
- bbswitch (Recommended but not required)

# FAQ

## Do I need this?

- GPU based on Turing (GTX 16 / RTX 20 series) or Newer
    - nvidia driver 435 or newer: **NO**
    - nvidia driver older than 435: **YES**
        - But the GPU will probably not work because earlier drivers might not have support for it anyway
- GPU based on Pascal (GTX 10 series) or earlier: **YES**
    - This will require nVidia driver 390 or newer
    - bbswitch is recommended to actually turn off the GPU if not in use as these and older GPUs lack the required power
      management features (e.g. GSP coprocessor)
- Open source nvidia drivers: **NO**

OptimusUI will evaluate most of these requirements on its own and notify the user. However, it does not validate
the nvidia driver version as of now.

**NOTICE:** Depending on your distribution the package for prime-select might depend on further requirements not listed
here

## How does it work?

OptimusUI will do a brief system survey by this it checks the following things:

- If prime-select can be found in one of the following locations (escaping the sandbox using flatpak-spawn)
  following path:
    - `"/usr/bin/prime-select"`
    - `"/usr/sbin/prime-select"`
    - `"/bin/prime-select"`
    - `"/sbin/prime-select"`
- Once found it will continue and look up ALL pci devices on the host system (sandboxed) and look for
  devices with vendor id `0x10DE` (nvidia) and if it is a GPU by looking up their device class `30000` (dekstop) and `
  30200` (mobile)
- Then it will look up the GPU name using `lspci -d 10DE:DEVICE_ID` (sandboxed)
- Afterward it will run `lsmod | grep -i bbswtich` on the host (escaping the sandbox) to verify if the bbswitch kernel
  module is loaded

All of this in done entirely offline and locally. The results of this system survey is not stored or uploaded
anywhere

## There are already interfaces for prime-select why make a new one?

Because none of these are on flathub.
Which causes them not to be exactly distribution agnostic and will require the distribution in question to actually ship
these interfaces. Furthermore, they are not very immutable friendly either.

There are also GNOME extensions and Plasma Widget which aim at providing similar features but these are not desktop
agnostic. Hence, you can not use a KDE Plasmoid (are they still called like this?) on GNOME or a GNOME extension on KDE.
Let alone entirely different desktop environments based on a different software stack.

Also in case of Gnome extensions they often tend to break on new Gnome releases and often are no longer maintained which
renders them effectively unusable.

Therefore instead of porting an existing application to be a flatpak I just develop my own from scratch with flatpak
already in mind.