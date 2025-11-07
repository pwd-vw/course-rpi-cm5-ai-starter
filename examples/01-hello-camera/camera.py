"""Hello Camera example for Raspberry Pi Camera Module 3."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def main() -> None:
    try:
        from picamera2 import Picamera2, Preview  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - hardware specific
        raise SystemExit(
            "picamera2 is required. Install it with 'sudo apt install python3-picamera2'."
        ) from exc

    picam2 = Picamera2()
    picam2.start_preview(Preview.NULL)
    config = picam2.create_still_configuration(main={"size": (2304, 1296)})
    picam2.configure(config)
    picam2.start()

    output_dir = Path("../../artifacts/captures").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"hello_camera_{datetime.now():%Y%m%d_%H%M%S}.jpg"
    picam2.capture_file(str(output_path))

    picam2.stop()
    picam2.close()

    print(f"Saved capture to {output_path}")


if __name__ == "__main__":
    main()
