# Camera Module 3 Guide

## Verify Camera Detection
- Run `libcamera-hello --list-cameras` to ensure the module appears with `IMX708` sensor ID.
- Execute `libcamera-hello -t 0` for a live preview; press `Ctrl+C` to exit.

## Capture Still Images
- Quick test: `python scripts/camera-test.py`
- HDR capture: `python examples/camera/capture_module3.py --hdr`
- Custom resolution: `python scripts/camera-test.py --resolution 4056x3040`

## Exposure and White Balance
- For static scenes, fix exposure: `python examples/camera/capture_module3.py --exposure 0.01`
- Available AWB modes include `auto`, `incandescent`, `fluorescent`, `daylight`, `cloudy`.
- Use `libcamera-still --list-controls` to discover additional control names.

## Video Capture
- Install `libcamera-apps` (handled by the setup script).
- Record 1080p video: `libcamera-vid -t 10000 -o test.h264 --codec h264`
- Convert to MP4 with `ffmpeg -framerate 30 -i test.h264 -c copy test.mp4`

## Troubleshooting Focus
- If autofocus hunts, switch to manual control with `--lens-position` using `libcamera-still`.
- Clean the lens with a microfiber cloth and ensure proper lighting for the scene.

