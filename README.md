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

### Use virt-manager to Create the VM
1. Open virt-manager.
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

## Method 1 for Camera Spoof

### Rationale
This method leverages OBS (Open Broadcast Software) and a custom MJPEG server to spoof a webcam feed. OBS allows live or prerecorded clips to be used as the webcam feed, which can then be passed to the VM.

---

### Step 1: Install OBS Studio and Video Loopback
Install the required software:
```bash
sudo apt install v4l2loopback-dkms
sudo apt install obs-studio
```

---

### Step 2: Setup OBS Studio
1. Launch OBS using `obs`.
2. Select "I will only be using the virtual camera."
3. Create a scene for the live camera feed:
   - Add a source of "Video Capture Device."
   - Create new and select your live camera.
4. Create a scene for prerecorded clips:
   - Add a media source and select the prerecorded clip file location.
5. Start the OBS virtual camera.

---

### Step 3: Setup MJPEG Server
Identify the OBS video stream by launching VLC:
- Go to Media -> Open Capture Device.
- Test each device under `/dev/video[number]`.

#### Modify the Python Server
Navigate to the MJPEG server directory and edit `main.py`:
1. Update the `cap = VideoCapture(...)` line with the correct `/dev/video[number]`.
2. Update the IP address bound to the VM in the last line with a shared subnet IP.

#### Run the Server
```bash
python main.py
```

---

### Final Step: Configure Windows VM
Install the IP Adapter file on the Windows VM (found in the `VM-Programs` directory). Enter the IP and port of the Python server. Ensure the chosen IP shares a subnet with the VM.

The VM "Camera" will now be the OBS virtual cam feed.

---

**Note:** This guide is for educational purposes only. Ensure compliance with your institution's policies.

## Method 2: Using a Raspberry Pi Zero with OTG and Gadget Mode
### Rationale

The Raspberry Pi Zero supports OTG, allowing it to emulate USB devices such as a webcam. By combining this with a lightweight MJPEG stream from a remote OBS server, the Raspberry Pi can act as a virtual webcam. This setup is ideal for streaming pre-recorded or live video content from an OBS instance to a connected host system (e.g., Windows VM or Lockdown Browser environment).

### Step 1: Set Up Your Raspberry Pi Zero for USB OTG
#### Enable OTG Mode

1. Flash the Raspberry Pi OS Lite to your microSD card using tools like Raspberry Pi Imager or balenaEtcher.
2. After flashing, mount the boot partition of the microSD card on your computer.
3. Edit the config.txt file and add the following line at the end to enable USB OTG:
   `dtoverlay=dwc2`
4. Edit the `cmdline.txt` file and add `modules-load=dwc2,g_ether` after `rootwait` (on the same line). It should look something like this:

   `root=/dev/mmcblk0p2 rootfstype=ext4 fsck.repair=yes rootwait modules-load=dwc2,g_ether`

5. Create an empty file named ssh (no extension) in the boot partition to enable `SSH`.

6. Insert the microSD card into the Raspberry Pi Zero and connect it to your computer via the micro-USB port (labeled “USB”). It should boot up as a USB Ethernet device.

#### Access the Raspberry Pi via SSH

1. Find the IP address of your Raspberry Pi (using tools like arp -a or check your DHCP client list).
2. SSH into the Raspberry Pi:
   `ssh pi@<raspberry-pi-ip>`

Default password is `raspberry`. Change the password after logging in using `passwd`.

### Step 2: Set Up USB Gadget Webcam on the Raspberry Pi

1. **Install Dependencies**: Update and install necessary packages:

   ```SH
   sudo apt update
   sudo apt install -y libv4l2loopback-utils v4l2loopback-dkms gstreamer1.0-tools
   ```

2. **Enable USB Webcam Gadget**: Create a USB gadget configuration for the virtual webcam:

   ```SH
   sudo mkdir /opt/usb-webcam
   cd /opt/usb-webcam
   sudo nano webcam-gadget.sh
   ```

   Add the following script to configure the gadget:

   ```bash
   #!/bin/bash
   modprobe libcomposite
   cd /sys/kernel/config/usb_gadget/
   mkdir -p webcam
   cd webcam
   
   echo 0x1d6b > idVendor  # Linux Foundation
   echo 0x0104 > idProduct # Multifunction Composite Gadget
   echo 0x0100 > bcdDevice # v1.0.0
   echo 0x0200 > bcdUSB    # USB2
   
   mkdir -p strings/0x409
   echo "0123456789" > strings/0x409/serialnumber
   echo "Raspberry Pi Zero" > strings/0x409/manufacturer
   echo "USB Webcam" > strings/0x409/product
   
   mkdir -p configs/c.1/strings/0x409
   echo "Config 1: Webcam" > configs/c.1/strings/0x409/configuration
   echo 120 > configs/c.1/MaxPower
   
   mkdir -p functions/uvc.usb0
   echo 3072 > functions/uvc.usb0/streaming_maxpacket
   mkdir -p functions/uvc.usb0/control/header/h
   ln -s functions/uvc.usb0/control/header/h functions/uvc.usb0/control/class/fs
   ln -s functions/uvc.usb0/control/header/h functions/uvc.usb0/control/class/hs
   
   mkdir -p functions/uvc.usb0/streaming/mjpeg/m
   echo 1 > functions/uvc.usb0/streaming/mjpeg/m/bmaControls
   echo 640 > functions/uvc.usb0/streaming/mjpeg/m/wWidth
   echo 480 > functions/uvc.usb0/streaming/mjpeg/m/wHeight
   echo 333333 > functions/uvc.usb0/streaming/mjpeg/m/dwDefaultFrameInterval
   echo 640000 > functions/uvc.usb0/streaming/mjpeg/m/dwMinBitRate
   echo 1280000 > functions/uvc.usb0/streaming/mjpeg/m/dwMaxBitRate
   echo 614400 > functions/uvc.usb0/streaming/mjpeg/m/dwMaxVideoFrameBufferSize
   ln -s functions/uvc.usb0 configs/c.1/
   
   ls /sys/class/udc > UDC
   ```
3. Make the script executable:

   `sudo chmod +x webcam-gadget.sh`
4. Run the script:

   `sudo ./webcam-gadget.sh`

The Raspberry Pi will now register as a USB webcam.

### Step 3: Stream Video from Remote OBS Server

1. Set Up MJPEG Stream on OBS:

   - In OBS Studio on the remote machine, go to Settings > Stream.
   - Select Custom Streaming Server and configure:
     - Server: http://<raspberry-pi-ip>:8080
     - Stream Key: Any string (e.g., live).
   - Install and run an MJPEG server plugin or use the built-in `obs-mjpeg-server` plugin if available.

2. Stream the Video to Raspberry Pi: On the Raspberry Pi, use ffmpeg or gstreamer to pull the MJPEG stream and redirect it to the USB webcam gadget.

Example using `ffmpeg`:

`ffmpeg -i http://<obs-server-ip>:8080/stream -f v4l2 /dev/video0`

Example using gstreamer:
`gst-launch-1.0 souphttpsrc location=http://<obs-server-ip>:8080/stream ! jpegdec ! v4l2sink device=/dev/video0`

### Step 4: Connect the Raspberry Pi to the Host System

1. Plug the Raspberry Pi Zero into the host system's USB port.
2. It should be recognized as a USB webcam.
3. Open the video application (e.g., Lockdown Browser) on the host system, and select the virtual webcam as the input source.

#### Notes

 Ensure the OBS server, Raspberry Pi, and host system are on the same network or have a direct route to each other.
 Use a stable power source for the Raspberry Pi to avoid interruptions.
 Test the setup with a video conferencing app before using it in a critical environment.

