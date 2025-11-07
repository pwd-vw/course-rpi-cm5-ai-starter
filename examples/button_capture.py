"""Use a button press to trigger a camera capture."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def main() -> None:
    try:
        from gpiozero import Button  # type: ignore
        from picamera2 import Picamera2  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - hardware specific
        raise SystemExit("Install gpiozero and picamera2 before running this example.") from exc

    button = Button(23, pull_up=True)
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration())
    picam2.start()

    captures_dir = Path("artifacts/captures")
    captures_dir.mkdir(parents=True, exist_ok=True)

    print("Press the physical button connected to BCM 23 to capture an image. Press Ctrl+C to exit.")

    try:
        while True:
            button.wait_for_press()
            filename = captures_dir / f"button_capture_{datetime.now():%Y%m%d_%H%M%S}.jpg"
            picam2.capture_file(str(filename))
            print(f"Captured image -> {filename}")
            button.wait_for_release()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        picam2.close()
        button.close()


if __name__ == "__main__":
    main()
