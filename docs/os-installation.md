# Operating System Installation

## 1. Flash Raspberry Pi OS Bookworm
- Download the latest Raspberry Pi Imager from <https://www.raspberrypi.com/software/>
- Select **Raspberry Pi 5** → **Raspberry Pi OS (64-bit) with desktop**.
- Use **Settings** to preconfigure Wi-Fi, locale, hostname, and SSH (enable password or key-based login).
- Flash the microSD card and safely eject it when the process completes.

## 2. First Boot Checklist
- Insert the microSD card and power on the Raspberry Pi 5.
- Complete the desktop onboarding wizard if prompted.
- Update the system: `sudo apt update && sudo apt full-upgrade -y`
- Enable interfaces via `sudo raspi-config` → **Interface Options** → enable **Camera**, **I2C**, **SPI**.
- Reboot to apply firmware updates: `sudo reboot`

## 3. Clone and Setup the Starter Kit
- Install Git if missing: `sudo apt install -y git`
- Clone the repository: `git clone https://github.com/pwd-vw/course-rpi-cm5-ai-starter.git`
- Run the one-click setup script from the repo root: `./scripts/initial-setup.sh`
- Activate the Python environment: `source .venv/bin/activate`

## 4. Verify Hardware Access
- Camera: `libcamera-hello --list-cameras`
- GPIO: `python scripts/gpio-test.py`
- Hardware checker: `python scripts/hardware_check.py`

## 5. Optional Desktop Integration
- Create a desktop shortcut invoking `lxterminal -e "bash -lc 'cd ~/course-rpi-cm5-ai-starter && source .venv/bin/activate'"`
- Install Visual Studio Code via `sudo apt install -y code` or use SSH remote on your workstation.
