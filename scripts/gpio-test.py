"""Basic GPIO sanity check for Raspberry Pi 5."""

from __future__ import annotations

import argparse
import time


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--led-pin", type=int, default=18, help="BCM pin number for the LED (default: 18)")
    parser.add_argument(
        "--blink-count", type=int, default=5, help="Number of times to blink the LED (default: 5)"
    )
    parser.add_argument("--interval", type=float, default=0.5, help="Blink interval in seconds (default: 0.5)")
    return parser.parse_args()


def blink_led(pin: int, blink_count: int, interval: float) -> None:
    try:
        from gpiozero import LED  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - hardware specific
        raise SystemExit("gpiozero is required. Install it with 'sudo apt install python3-gpiozero'.") from exc

    led = LED(pin)
    print(f"[INFO] Blinking LED on BCM pin {pin}")

    for i in range(1, blink_count + 1):
        print(f"  -> Blink {i}/{blink_count}")
        led.on()
        time.sleep(interval)
        led.off()
        time.sleep(interval)

    led.close()


def main() -> None:
    args = parse_args()
    blink_led(args.led_pin, args.blink_count, args.interval)
    print("[OK] GPIO test completed successfully.")


if __name__ == "__main__":
    main()
