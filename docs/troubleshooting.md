# Troubleshooting

## Camera Issues
- **`libcamera` reports no cameras**: Re-seat the ribbon cable, ensure `sudo raspi-config nonint do_camera 0` ran successfully, and reboot.
- **Pink tint or exposure problems**: Update firmware with `sudo rpi-update`, then reboot.
- **`picamera2` import fails**: Install via `sudo apt install python3-picamera2` and verify you are using the system Python or the project virtualenv with `apt`-provided site-packages.

## GPIO Issues
- **`gpiozero` cannot access hardware**: Ensure the user is in the `gpio` group (`sudo adduser $USER gpio`) and re-login.
- **Button constantly triggered**: Confirm pull-up/pull-down wiring. Use `pinout` command to visualise GPIO mapping.
- **Permission denied on `/dev/gpiomem`**: Run the one-click setup script which adds the correct udev rules, or temporarily run scripts with `sudo`.

## Performance and Stability
- **Thermal throttling**: Attach a heatsink/fan and enable the `performance` governor via `sudo apt install -y cpufrequtils` and `sudo cpufreq-set -g performance` for demanding workloads.
- **Low disk space**: Run `sudo apt autoremove`, clear `/var/log`, or expand filesystem with `sudo raspi-config --expand-rootfs`.
- **Power warnings**: Use the official 27 W supply; check for lightning bolt icon on HDMI output.

## Debug Commands
- Camera diagnostics: `libcamera-hello --info-text "Exposure ${ExposureTime} AWB ${AwbMode}"`
- Interface status: `vcgencmd get_camera` and `ls -l /dev/video*`
- GPIO mapping: `raspi-gpio get` for real-time pin states
