# course-rpi-cm5-ai-starter

Starter kit for Raspberry Pi 5 combining one-click provisioning, hardware compatibility checks, camera workflows, and GPIO control templates.

## Features
- Automated setup script that installs system packages, enables interfaces, and provisions a Python virtual environment.
- Hardware compatibility checker with JSON output for CI pipelines or remote diagnostics.
- Camera Module 3 capture examples (still, HDR, button-triggered workflows).
- GPIO templates for LED blinking, PWM dimming, and button event handling.
- Opinionated documentation covering hardware assembly, OS flashing, and troubleshooting.

## Quickstart
```bash
git clone https://github.com/pwd-vw/course-rpi-cm5-ai-starter.git
cd course-rpi-cm5-ai-starter
./scripts/initial-setup.sh
source .venv/bin/activate
python scripts/hardware_check.py
```

## Key Scripts
- `scripts/initial-setup.sh`: One-click installer for Raspberry Pi OS Bookworm on Pi 5.
- `scripts/hardware_check.py`: Summarises camera, GPIO, and interface status.
- `scripts/camera-test.py`: Captures a still image with configurable resolution.
- `scripts/gpio-test.py`: Blinks an LED to validate GPIO wiring.

## Example Workflows
- `examples/01-hello-camera/camera.py`: Hello world capture using Picamera2.
- `examples/camera/capture_module3.py`: HDR and manual exposure template for Camera Module 3.
- `examples/button_capture.py`: Trigger a capture with a physical button.
- `examples/gpio/pwm_led.py`: Fade an LED using PWM.

## Documentation Map
- `docs/hardware-setup.md`: Assemble Pi 5 and peripherals.
- `docs/os-installation.md`: Flash OS, perform first boot tasks, and run setup scripts.
- `docs/environment-setup.md`: Manage the Python environment and configuration files.
- `docs/camera-module3-guide.md`: Capture recipes and troubleshooting for Camera Module 3.
- `docs/gpio-guide.md`: Wiring and control tips for GPIO labs.
- `docs/troubleshooting.md`: Common issues and debug commands.

## Contributing
- Fork, branch, and open pull requests targeting `main`.
- Keep scripts executable (`chmod +x`) and include usage notes in docstrings.
- Prefer platform-agnostic Python where possible; gate hardware-specific imports behind try/except.
