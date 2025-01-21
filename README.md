# Lockdown Browser Bypass

# Method 1 Full Bypass

All files can be found in this repo, to follow along simply git clone and use the command found in this guide, when I wrote this I was using Ubuntu although the command can be translated to windows and more easily macOS

## Setup QEMU

### Rational 
The first step to bypass detection is to create an undetectable VM, QEMU lends itself well to this idea as it's open source and can be recompiled to suit our needs. Although the source code can be compiled to windows, macOS, and linux I have opted to use Ubuntu due to the environment it offers

### QEMU Patch
Begin by retrieving the source code for qemu version 8.2.2 as thats what I patched with however any version is likley fine 
### Dependencies
#### Build Dependencies 
```
sudo apt install git build-essential ninja-build python3-venv libglib2.0-0 flex
```
#### Install QEMU Dependencies 
_Although the QEMU build will replace the binary's with our recompiled and rebuilt ones, it is still important to install QEMU from a package manager to get all of its dependence_

```
sudo apt install qemu-system qemu-kvm virt-manager bridge-utils
```

#### Get QEMU source code 

```sh
wget https://download.qemu.org/qemu-8.2.2.tar.xz # Get source code
tar xvJf qemu-8.2.2.tar.xz # Extract Code
```

#### Patch Source 
To copy and paste commands make sure to have git cloned this repo and placed the source code there 
```SH
cd qemu-8.2.2 # Enter Build Directory
git apply ../qemu-patch/qemu-8.2.0.patch # Apply patch
```

#### Install dependencies for build options 
These dependencies are only required for the configuration options used in the next step, however the same goals can be accomplished with no build options they do however provide some 'quality of life' improvements
```SH
sudo apt install libglib2.0-dev libjack-dev libpixman-1-dev libspice-server-dev libudev-dev libusbredirparser-dev libusb libusb-1.0-0-dev
```


#### Build Patched Version
```SH
./configure --enable-virtfs --enable-kvm --enable-libusb --enable-libudev --enable-spice --enable-usb-redir --enable-jack # you can configure with any build flags you would like to use the former will work just fine for what we are doing 

sudo make install -j$(nproc) 
```

#### Create Windows VM
Download the Windows 10 iso from the link 

https://www.microsoft.com/en-us/software-download/windows10iso

run `virt-manager`
1. Create a new vm using the first icon in vert-manager 
2. Select your downloaded windows ISO for your installation media 
3. Set memory and CPU's, 8GB and 4 Cores is a good starting point
4. Create a disk image, 25GB is plenty
5. Name the VM on the last step and select the 'customize configuration' check box
6. Switch to the XML View next to under view
7. Use the XML file below as a template for the required changes, an entire example file can also be found in the git under EXAMPLE.XML
8. Under display, if built with the feature, use spice over VNC you will get better display performance  
```XML
<domain xmlns:qemu="http://libvirt.org/schemas/domain/qemu/1.0" type="kvm">
    <name>Entertainment</name>
    <uuid>REPLACE YOUR UUID HERE!</uuid>
    <metadata>
        <libosinfo:libosinfo xmlns:libosinfo="http://libosinfo.org/xmlns/libvirt/domain/1.0">
            <libosinfo:os id="http://microsoft.com/win/10"/>
        </libosinfo:libosinfo>
    </metadata>
    <memory unit="KiB">1548288</memory>
    <currentMemory unit="KiB">1548288</currentMemory>
    <memoryBacking>
        <source type="memfd"/>
        <access mode="shared"/>
    </memoryBacking>
    <vcpu placement="static">12</vcpu>
    <os firmware="efi">
        <type arch="x86_64" machine="pc-q35-7.0">hvm</type>
        <loader/>
        <smbios mode="host"/>
    </os>
    <features>
        <acpi/>
        <apic/>
        <hyperv mode="custom">
            <relaxed state="on"/>
            <vapic state="on"/>
            <spinlocks state="on" retries="8191"/>
            <vendor_id state="on" value="GenuineIntel"/>
        </hyperv>
        <kvm>
            <hidden state="on"/>
        </kvm>
        <vmport state="off"/>
        <smm state="on"/>
        <ioapic driver="kvm"/>
    </features>
    <cpu mode="host-passthrough" check="none" migratable="on">
        <feature policy="disable" name="hypervisor"/>
    </cpu>
    <clock offset="localtime">
        <timer name="rtc" tickpolicy="catchup"/>
        <timer name="pit" tickpolicy="delay"/>
        <timer name="hpet" present="no"/>
        <timer name="hypervclock" present="yes"/>
    </clock>
    <on_poweroff>destroy</on_poweroff>
    <on_reboot>restart</on_reboot>
    <on_crash>destroy</on_crash>
    <pm>
        <suspend-to-mem enabled="no"/>
        <suspend-to-disk enabled="no"/>
    </pm>
    <qemu:commandline>
        <qemu:arg value="-smbios"/>
        <qemu:arg value="type=0,version=UX305UA.201"/>
        <qemu:arg value="-smbios"/>
        <qemu:arg value="type=1,manufacturer=ASUS,product=UX305UA,version=2021.1"/>
        <qemu:arg value="-smbios"/>
        <qemu:arg value="type=2,manufacturer=Intel,version=2021.5,product=Intel i9-12900K"/>
        <qemu:arg value="-smbios"/>
        <qemu:arg value="type=3,manufacturer=XBZJ"/>
        <qemu:arg value="-smbios"/>
        <qemu:arg value="type=17,manufacturer=KINGSTON,loc_pfx=DDR5,speed=4800,serial=000000,part=0000"/>
        <qemu:arg value="-smbios"/>
        <qemu:arg value="type=4,manufacturer=Intel,max-speed=4800,current-speed=4800"/>
        <qemu:arg value="-cpu"/>
        <qemu:arg value="host,family=6,model=158,stepping=2,model_id=Intel(R) Core(TM) i9-12900K CPU @ 2.60GHz,vmware-cpuid-freq=false,enforce=false,host-phys-bits=true,hypervisor=off"/>
        <qemu:arg value="-machine"/>
        <qemu:arg value="q35,kernel_irqchip=on"/>
    </qemu:commandline>
</domain>
```
