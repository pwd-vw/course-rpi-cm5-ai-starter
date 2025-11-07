# Hardware Setup Guide

## Required Components
- Raspberry Pi 5 (4 GB or 8 GB recommended)
- Official Raspberry Pi 27 W USB-C power supply
- Raspberry Pi Camera Module 3 (wide or standard)
- microSD card (32 GB or larger, UHS-I)
- USB keyboard and mouse
- Micro-HDMI to HDMI cable and monitor
- Breadboard, jumper wires, LEDs, resistors (220 Ω), momentary button

## Assembly Steps
- Disconnect power before wiring; static discharge can damage components.
- Install the camera ribbon cable using the CSI connector closest to the USB ports (CAM0). Ensure the blue tab faces the Ethernet port.
- Connect the micro-HDMI cable to HDMI0 for the primary display.
- Insert the prepared microSD card into the microSD slot.
- Attach GPIO peripherals:
  - LED anode → BCM 18 through 220 Ω resistor; cathode → ground
  - Button leg → BCM 23; other leg → 3.3 V; add a 10 kΩ pull-down to ground if not using internal pull-ups
- Connect USB keyboard and mouse.
- Apply power only after all components are seated.

## Camera Focus and Orientation
- Use `libcamera-still --list-controls` to confirm focus and zoom capabilities.
- Adjust the focus ring on the Camera Module 3 if images appear soft.
- Mount the camera securely to prevent rolling shutter artifacts during captures.

## Optional Accessories
- Heatsink or active cooler for sustained AI workloads.
- PoE HAT if powering via Ethernet.
- Dedicated CSI-to-HDMI breakout board for longer camera cable runs.
