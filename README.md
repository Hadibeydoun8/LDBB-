# Lockdown Browser Bypass

## Method 1: Full Bypass

### Overview
This guide outlines the steps to create an undetectable virtual machine (VM) using QEMU, which can be recompiled to bypass Lockdown Browser detection. The process has been demonstrated on Ubuntu, but it can be adapted for Windows or macOS environments. All required files can be found in the associated repository.

---

## Setup QEMU

### Rationale
Using QEMU allows for creating a VM that is undetectable by Lockdown Browser due to its open-source nature, which enables custom patches and configurations.

---

### Step 1: Install QEMU Dependencies

#### Build Dependencies
```bash
sudo apt install git build-essential ninja-build python3-venv libglib2.0-0 flex
```

#### QEMU Dependencies
Install QEMU from the package manager to ensure all dependencies are available, even though the binaries will be replaced with recompiled versions.
```bash
sudo apt install qemu-system qemu-kvm virt-manager bridge-utils
```

---

### Step 2: Get and Patch QEMU Source Code

#### Download the QEMU Source Code
Retrieve the source code for QEMU version 8.2.2:
```bash
wget https://download.qemu.org/qemu-8.2.2.tar.xz # Get source code
tar xvJf qemu-8.2.2.tar.xz # Extract code
```

#### Apply the Patch
Ensure the repository containing the patch is cloned and place the patch file in the source code directory:
```bash
cd qemu-8.2.2 # Enter build directory
git apply ../qemu-patch/qemu-8.2.0.patch # Apply patch
```

---

### Step 3: Install Additional Build Dependencies
Install the following dependencies for specific build options. These provide various quality-of-life improvements for the VM:
```bash
sudo apt install libglib2.0-dev libjack-dev libpixman-1-dev libspice-server-dev libudev-dev libusbredirparser-dev libusb libusb-1.0-0-dev
```

---

### Step 4: Build and Install the Patched Version
Configure the build with the required flags:
```bash
./configure --enable-virtfs --enable-kvm --enable-libusb --enable-libudev --enable-spice --enable-usb-redir --enable-jack
```
Build and install:
```bash
sudo make install -j$(nproc)
```

---

## Create Windows VM

### Download Windows ISO
Download the Windows 10 ISO:

[Windows 10 ISO Download](https://www.microsoft.com/en-us/software-download/windows10iso)

### Use `virt-manager` to Create the VM
1. Open `virt-manager`.
2. Click the first icon to create a new VM.
3. Select the downloaded Windows ISO as the installation media.
4. Allocate resources (e.g., 8 GB RAM, 4 CPU cores).
5. Create a 25 GB disk image.
6. Name the VM and check the "Customize configuration" option.
7. Switch to XML view under the "View" menu.

### Apply XML Configuration
Use the following XML template for required changes. Replace `REPLACE YOUR UUID HERE!` with a unique UUID for your setup:

```xml
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

---

**Now that the VM is undetectable you can run and use the lockdown browser and exit it to use chrome and another application in the host system, simply pass your real webcam to the VM and your off to the races**

**Follow these next steps to also spoof your camera**

# Method 1 for Camera Spoof

### Rationale 
For this to work a few idea will be leveraged, first a control software will be used, for us, it will be OBS or Open Broadcast Software, this will be where you can set and manager you web cam inclduing having it live or a prereocrded clip, or multiple pre recorded clips
Next we will create our own python MJPEG server to give the Windows VM and way to receive the video
Finally we will compile our own windows driver to recive this footage and pass it to the lockdown browser 

### Install OBS Studio and Video Loop back 
```SH
sudo apt install v4l2loopback-dkms
sudo apt install obs-studio
```

### Setup OBS Studio
1. Launch OBS by `obs`
2. Select "I will only be using the virtual machine"
3. Create a scene for the live camera feed
   1. Add a source of video capture device
   2. Create new
   3. Select your live camera
4. Add a Scene for all pre-recorded clips
   1. Under source add a media source
   2. select you recorded clip file location
5. Start OBS virtual camera

### Setup MJPEG Server
First identify which video stream is OBS on, do this by lauching VLC, Media -> Open Capture Device
Under video device name test each one `/dev/video[number]`

#### Run python server
```SH
cd ../mjpeg-server
```
open the main.py file and change the line with the "cap = VideoCapture(CHANGE THIS NUMBER TO YOUR /dev/video[NUMBER]"
change the last line "0.0.0.0" IP to the IP bound to your VM you can figure this out with `ifconfig`

#### Run the server
```SH
python main.py
```

On the windows VM install the IP Adapter file found in VM-Programs and enter the IP and Port of the python server, make sure the IP chosen shares a subnet with the VM

The "Camera" on your VM will now be what is shared by the OBS virtual cam
**Note:** This guide is for educational purposes only. Ensure compliance with your institution's policies.
