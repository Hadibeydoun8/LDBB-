# Lockdown Browser Bypass

# Method 1 Full Bypass

All files can be found in this repo, to follow along simply git clone and use the command found in the guild, when I wrote this I was using Ubuntu although the command can be translated to windows and more easily macOS

## Setup QEMU

### Rational 
The first step to bypass detection is to create an undetectable VM, QEMU lends itself well to this idea as it's open source and can be recompiled to suit our needs. Although the source code can be compiled to windows, macOS, and linux I have opted to use Ubuntu due to the environment it offers

### QEMU Patch
Begin by retrieving the source code for qemu version 8.2.2 as thats what I patched with however any version is likley fine 
#### Dependencies
#### Build Dependencies 
```
sudo apt install sudo apt install git build-essential ninja-build python3-venv libglib2.0-0 flex bison
```
#### Install QEMU Dependencies 
_Although the QEMU build will replace the binary's with our recompiled and rebuilt ones, it is still important to install QEMU from a package manager to get all of its dependence_

```
sudo apt install qemu qemu-kvm virt-manager bridge-utils
```

#### Get QEMU source code 

```sh
wget https://download.qemu.org/qemu-8.2.2.tar.xz # Get source code
tar xvJf qemu-8.2.2.tar.xz # Extract Code
cd qemu-8.2.2 # Enter Directory
```

#### Patch Source 
