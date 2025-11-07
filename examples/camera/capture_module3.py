"""Capture helper tailored for Raspberry Pi Camera Module 3."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exposure", type=float, default=0.0, help="Manual exposure time in seconds (0 for auto)")
    parser.add_argument("--awb", type=str, default="auto", help="Automatic white balance mode")
    parser.add_argument(
        "--hdr",
        action="store_true",
        help="Enable HDR mode (requires Pi Camera Module 3 and latest firmware)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/captures"),
        help="Directory to store captures",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        from picamera2 import Picamera2, Preview  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - hardware specific
        raise SystemExit(
            "Install picamera2 with 'sudo apt install python3-picamera2' before running this example."
        ) from exc

    picam2 = Picamera2()
    config = picam2.create_still_configuration(
        main={"size": (4608, 2592) if args.hdr else (2304, 1296)},
        controls={
            "ExposureTime": int(args.exposure * 1_000_000) if args.exposure > 0 else None,
            "AwbMode": args.awb,
            "HdrMode": 1 if args.hdr else 0,
        },
    )
    picam2.configure(config)
    picam2.start_preview(Preview.NULL)
    picam2.start()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    filename = args.output_dir / f"module3_{datetime.now():%Y%m%d_%H%M%S}.jpg"
    picam2.capture_file(str(filename))
    picam2.close()

    print(f"Capture saved to {filename}")


if __name__ == "__main__":
    main()

