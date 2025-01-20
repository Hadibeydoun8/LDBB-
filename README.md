# Lockdown Browser Bypass

# Method 1 Full Bypass

All files can be found in this repo, to follow along simply git clone and use the command found in the guild, when I wrote this I was using Ubuntu although the command can be translated to windows and more easily macOS

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
7. Use the XML file below as a template for the required changed
```XML
<domain type="kvm">
    <name>**YOUR VM NAME**</name>
    <uuid>YOUR UUID</uuid>
    <metadata>
        <libosinfo:libosinfo xmlns:libosinfo="http://libosinfo.org/xmlns/libvirt/domain/1.0">
            <libosinfo:os id="http://microsoft.com/win/10"/>
        </libosinfo:libosinfo>
    </metadata>
    <memory unit="KiB">8392704</memory>
    <currentMemory unit="KiB">8392704</currentMemory>
    <vcpu placement="static">4</vcpu>
    <os>
        <type arch="x86_64" machine="pc-q35-8.2">hvm</type>
        <boot dev="hd"/>
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
    <cpu mode="host-model" check="partial"/>
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
    <devices>
        <emulator>/usr/local/bin/qemu-system-x86_64</emulator>
        ****** REPLACE WITH YOUR DISK INFORMATION COPY AND PASTE FROM YOUR XML FILE ******
        <disk type="file" device="disk">
            <driver name="qemu" type="qcow2" discard="unmap"/>
            <source file="/var/lib/libvirt/images/win10.qcow2"/>
            <target dev="sda" bus="sata"/>
            <address type="drive" controller="0" bus="0" target="0" unit="0"/>
        </disk>
        
        <disk type="file" device="cdrom">
            <driver name="qemu" type="raw"/>
            <source file="/home/hbeydoun/Downloads/Win10_22H2_English_x64v1.iso"/>
            <target dev="sdb" bus="sata"/>
            <readonly/>
            <address type="drive" controller="0" bus="0" target="0" unit="1"/>
        </disk>
        ***********************************************************************************
        <controller type="usb" index="0" model="qemu-xhci" ports="15">
            <address type="pci" domain="0x0000" bus="0x02" slot="0x00" function="0x0"/>
        </controller>
        <controller type="pci" index="0" model="pcie-root"/>
        <controller type="pci" index="1" model="pcie-root-port">
            <model name="pcie-root-port"/>
            <target chassis="1" port="0x10"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x0" multifunction="on"/>
        </controller>
        <controller type="pci" index="2" model="pcie-root-port">
            <model name="pcie-root-port"/>
            <target chassis="2" port="0x11"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x1"/>
        </controller>
        <controller type="pci" index="3" model="pcie-root-port">
            <model name="pcie-root-port"/>
            <target chassis="3" port="0x12"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x2"/>
        </controller>
        <controller type="pci" index="4" model="pcie-root-port">
            <model name="pcie-root-port"/>
            <target chassis="4" port="0x13"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x3"/>
        </controller>
        <controller type="pci" index="5" model="pcie-root-port">
            <model name="pcie-root-port"/>
            <target chassis="5" port="0x14"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x4"/>
        </controller>
        <controller type="pci" index="6" model="pcie-root-port">
            <model name="pcie-root-port"/>
            <target chassis="6" port="0x15"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x5"/>
        </controller>
        <controller type="pci" index="7" model="pcie-root-port">
            <model name="pcie-root-port"/>
            <target chassis="7" port="0x16"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x6"/>
        </controller>
        <controller type="pci" index="8" model="pcie-root-port">
            <model name="pcie-root-port"/>
            <target chassis="8" port="0x17"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x7"/>
        </controller>
        <controller type="pci" index="9" model="pcie-root-port">
            <model name="pcie-root-port"/>
            <target chassis="9" port="0x18"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x03" function="0x0" multifunction="on"/>
        </controller>
        <controller type="pci" index="10" model="pcie-root-port">
            <model name="pcie-root-port"/>
            <target chassis="10" port="0x19"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x03" function="0x1"/>
        </controller>
        <controller type="pci" index="11" model="pcie-root-port">
            <model name="pcie-root-port"/>
            <target chassis="11" port="0x1a"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x03" function="0x2"/>
        </controller>
        <controller type="pci" index="12" model="pcie-root-port">
            <model name="pcie-root-port"/>
            <target chassis="12" port="0x1b"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x03" function="0x3"/>
        </controller>
        <controller type="pci" index="13" model="pcie-root-port">
            <model name="pcie-root-port"/>
            <target chassis="13" port="0x1c"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x03" function="0x4"/>
        </controller>
        <controller type="pci" index="14" model="pcie-root-port">
            <model name="pcie-root-port"/>
            <target chassis="14" port="0x1d"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x03" function="0x5"/>
        </controller>
        <controller type="sata" index="0">
            <address type="pci" domain="0x0000" bus="0x00" slot="0x1f" function="0x2"/>
        </controller>
        <interface type="network">
            <mac address="52:54:00:2f:64:1d"/>
            <source network="default"/>
            <model type="e1000e"/>
            <address type="pci" domain="0x0000" bus="0x01" slot="0x00" function="0x0"/>
        </interface>
        <serial type="pty">
            <target type="isa-serial" port="0">
                <model name="isa-serial"/>
            </target>
        </serial>
        <console type="pty">
            <target type="serial" port="0"/>
        </console>
        <input type="tablet" bus="usb">
            <address type="usb" bus="0" port="1"/>
        </input>
        <input type="mouse" bus="ps2"/>
        <input type="keyboard" bus="ps2"/>
        <graphics type="spice" autoport="yes">
            <listen type="address"/>
            <gl enable="no"/>
        </graphics>
        <audio id="1" type="none"/>
        <video>
            <model type="vga" vram="16384" heads="1" primary="yes"/>
            <address type="pci" domain="0x0000" bus="0x00" slot="0x01" function="0x0"/>
        </video>
        <hostdev mode="subsystem" type="usb" managed="yes">
            <source>
                <vendor id="0x04f2"/>
                <product id="0xb6b6"/>
            </source>
            <address type="usb" bus="0" port="2"/>
        </hostdev>
        <watchdog model="itco" action="reset"/>
        <memballoon model="virtio">
            <address type="pci" domain="0x0000" bus="0x03" slot="0x00" function="0x0"/>
        </memballoon>
    </devices>
</domain>

```

