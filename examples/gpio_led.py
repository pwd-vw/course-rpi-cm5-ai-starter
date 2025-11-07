"""Template for toggling an LED with gpiozero."""

from __future__ import annotations

import time


def blink_led(pin: int = 18, interval: float = 0.25) -> None:
    try:
        from gpiozero import LED  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - hardware specific
        raise SystemExit("gpiozero is required. Install it with 'sudo apt install python3-gpiozero'.") from exc

    led = LED(pin)
    print(f"Blinking LED on BCM {pin}. Press Ctrl+C to stop.")
    try:
        while True:
            led.on()
            time.sleep(interval)
            led.off()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stopping blink loop...")
    finally:
        led.close()


if __name__ == "__main__":
    blink_led()
