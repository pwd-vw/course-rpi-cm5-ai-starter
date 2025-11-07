"""Quick camera capture test for Raspberry Pi Camera Module 3."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/captures"),
        help="Directory to save the captured image.",
    )
    parser.add_argument(
        "--filename",
        type=str,
        default=None,
        help="Custom filename for the capture (default uses timestamp).",
    )
    parser.add_argument(
        "--resolution",
        type=str,
        default="1920x1080",
        help="Resolution in WIDTHxHEIGHT format (default: 1920x1080).",
    )
    return parser.parse_args()


def capture_image(output_dir: Path, filename: str, resolution: tuple[int, int]) -> Path:
    try:
        from picamera2 import Picamera2  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - hardware specific
        raise SystemExit(
            "picamera2 is required. Install it with 'sudo apt install python3-picamera2'."
        ) from exc

    picam2 = Picamera2()
    config = picam2.create_still_configuration(main={"size": resolution})
    picam2.configure(config)
    picam2.start()

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    picam2.capture_file(str(output_path))
    picam2.close()
    return output_path


def parse_resolution(value: str) -> tuple[int, int]:
    try:
        width, height = map(int, value.lower().split("x"))
        return width, height
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Resolution must be WIDTHxHEIGHT, e.g. 1920x1080") from exc


def main() -> None:
    args = parse_args()
    resolution = parse_resolution(args.resolution)
    filename = args.filename or f"capture_{datetime.now():%Y%m%d_%H%M%S}.jpg"
    path = capture_image(args.output, filename, resolution)
    print(f"[OK] Image saved to {path}")


if __name__ == "__main__":
    main()
